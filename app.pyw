"""Visor de prendas: servidor local + ventana de Edge en modo app.

Doble clic para abrir. Solo usa la librería estándar de Python.
"""
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import threading
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = Path(os.environ.get("LOCALAPPDATA", HERE)) / "VisorPrendas"
CONFIG = DATA / "config.json"

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".avif"}
# Guía oficial de Lacoste (lacoste.com/fr/guidedestailles): mujer en talla francesa T32–T48,
# niño por edad con su estatura en cm.
KID_CM = {"1A": 80, "2A": 92, "3A": 98, "4A": 104, "5A": 110, "6A": 116, "8A": 128,
          "10A": 140, "12A": 152, "14A": 164, "16A": 176}
SIZES = (["XS", "S", "M", "L", "XL"] + [f"{n}XL" for n in range(2, 10)]
         + [f"T{n}" for n in range(32, 50, 2)] + list(KID_CM))
# "S", "2.S" (dos S) o "S.2" (también dos S); igual "T36" o "2.14A"
SIZE_RE = re.compile(r"^(?:(\d+)\.)?(XS|S|M|L|XL|[2-9]XL|T(?:3[2468]|4[02468])|(?:1[0246]|[1-68])A)(?:\.(\d+))?$", re.I)
TOKEN_RE = re.compile(r"([^\s,]+)[\s,]*")
CM_RE = re.compile(r"\d+cm(?:[\s,]+|$)", re.I)  # "14A 164cm": la estatura va pegada a la talla de niño
TELA_RE = re.compile(r"\btela\b", re.I)
BAD_CHARS = set('<>:"/\\|?*')

# Orden de las fotos dentro de una prenda: la de frente primero, la tela al final.
IMAGE_RANK = [
    (re.compile(r"delante|frente|front", re.I), 0),
    (re.compile(r"atr[aá]s|espalda|back", re.I), 3),
    (re.compile(r"cuello", re.I), 4),
    (TELA_RE, 5),
    (re.compile(r"model", re.I), 2),
    (re.compile(r"dise[ñn]o", re.I), 1),
]


def natural(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def image_rank(name):
    rank = next((r for rx, r in IMAGE_RANK if rx.search(name)), 2.5)
    p = Path(name)
    return (rank, natural(p.stem), p.suffix.lower())  # "foto.jpg" antes que "foto (1).jpg"


def parse_name(name):
    """'S, 2.M, XL Azul ok' -> ({'S': 1, 'M': 2, 'XL': 1}, 'Azul ok')"""
    sizes, rest = {}, name.strip()
    while m := TOKEN_RE.match(rest):
        s = SIZE_RE.match(m.group(1))
        if not s:
            break
        size = s.group(2).upper()
        sizes[size] = sizes.get(size, 0) + int(s.group(1) or s.group(3) or 1)
        rest = rest[m.end():]
        if size in KID_CM and (cm := CM_RE.match(rest)):
            rest = rest[cm.end():]
    return sizes, rest.strip()


def format_name(sizes, rest):
    label = lambda s: f"{s} {KID_CM[s]}cm" if s in KID_CM else s
    parts = [f"{n}.{label(s)}" if n > 1 else label(s) for s in SIZES if (n := sizes.get(s, 0)) > 0]
    return " ".join(p for p in (", ".join(parts), rest) if p)


def load_config():
    try:
        return json.loads(CONFIG.read_text("utf-8-sig"))
    except (OSError, ValueError):
        return {}


def save_config(**changes):
    DATA.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(load_config() | changes, ensure_ascii=False), "utf-8")


def image_list(files, prefix=""):
    images = sorted((f for f in files if Path(f).suffix.lower() in IMG_EXT), key=image_rank)
    return [{"file": f"{prefix}/{f}" if prefix else f, "tela": bool(TELA_RE.search(f))} for f in images]


def garment(root, folder, files):
    """Una prenda = una carpeta con imágenes adentro."""
    images = image_list(files)
    if not images:
        return None
    rel = Path(folder).relative_to(root)
    sizes, rest = parse_name(rel.name) if rel.parts else ({}, "")
    return {
        "path": rel.as_posix() if rel.parts else "",
        "group": list(rel.parts[:-1]),
        "name": rel.name,
        "sizes": sizes,
        "rest": rest,
        "images": images,
        "noUsar": any(p.lower().startswith("no usar") for p in rel.parts),
    }


def scan(root, start=None, folders=None):
    """Prendas bajo `start` (o `root`). Si se pasa `folders`, le agrega las carpetas que no son prendas."""
    out, owners = [], {}
    for dirpath, dirnames, filenames in os.walk(start or root):
        dirnames.sort(key=natural)
        owner = owners.get(os.path.dirname(dirpath))
        if owner and not parse_name(os.path.basename(dirpath))[0]:
            # Subcarpeta sin tallas dentro de una prenda con tallas (p. ej. PJs/Helio): sus fotos son de esa prenda.
            folder, g = owner
            g["images"] += image_list(filenames, Path(dirpath).relative_to(folder).as_posix())
            owners[dirpath] = owner
        elif g := garment(root, dirpath, filenames):
            out.append(g)
            if g["sizes"]:  # una zona o la raíz con fotos sueltas no se traga lo de abajo
                owners[dirpath] = (dirpath, g)
        elif folders is not None and dirpath != str(root):
            folders.append(Path(dirpath).relative_to(root).as_posix())
    return out


def bad_name(name):
    return not name or name in (".", "..") or name.endswith((".", " ")) or bool(BAD_CHARS & set(name))


def downloads_dir():
    """Carpeta de Descargas de Windows (puede estar movida a otro disco)."""
    if custom := load_config().get("downloads"):
        return Path(custom)
    try:
        import winreg
        key = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as k:
            return Path(os.path.expandvars(winreg.QueryValueEx(k, "{374DE290-123F-4565-9164-39C4925E467B}")[0]))
    except OSError:
        return Path.home() / "Downloads"


def inside(root, rel):
    """Ruta absoluta de `rel` dentro de `root`, o None si se sale."""
    root = Path(root).resolve()
    p = (root / rel).resolve()
    return p if p == root or root in p.parents else None


def pick_folder(initial):
    code = (
        "import sys, tkinter as tk\n"
        "from tkinter import filedialog\n"
        "r = tk.Tk(); r.withdraw(); r.attributes('-topmost', True)\n"
        "p = filedialog.askdirectory(parent=r, initialdir=sys.argv[1] or None, title='Elige la carpeta de fotos')\n"
        "sys.stdout.write(p or '')\n"
    )
    python = Path(sys.executable).with_name("python.exe")
    if not python.exists():
        python = Path(sys.executable)
    res = subprocess.run(
        [str(python), "-c", code, initial or ""],
        capture_output=True, env=os.environ | {"PYTHONIOENCODING": "utf-8"},
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    picked = res.stdout.decode("utf-8").strip()
    return str(Path(picked)) if picked else None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, code, body=b"", ctype="application/json; charset=utf-8", headers=()):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in headers:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def fail(self, code, msg):
        self.send(code, {"error": msg})

    def send_file(self, p, cache="max-age=86400"):
        if not p or not p.is_file():
            return self.fail(404, "No existe")
        try:
            f = open(p, "rb")
        except OSError as e:
            return self.fail(500, str(e))
        with f:
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(p.name)[0] or "application/octet-stream")
            self.send_header("Content-Length", str(os.fstat(f.fileno()).st_size))
            self.send_header("Cache-Control", cache)
            self.end_headers()
            try:
                shutil.copyfileobj(f, self.wfile)
            except OSError:
                pass

    def do_GET(self):
        url = urllib.parse.urlsplit(self.path)
        root = load_config().get("root")
        if url.path == "/":
            self.send(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8",
                      [("Cache-Control", "no-store")])
        elif url.path == "/api/ping":
            self.send(200, {"ok": True})
        elif url.path == "/api/state":
            if not root or not Path(root).is_dir():
                return self.send(200, {"root": root, "missing": bool(root), "garments": [], "folders": []})
            folders = []
            garments = scan(root, folders=folders)
            self.send(200, {"root": root, "garments": garments, "folders": folders})
        elif url.path == "/api/downloads":
            dl = downloads_dir()
            try:
                entries = [e for e in os.scandir(dl) if e.is_file() and Path(e.name).suffix.lower() in IMG_EXT]
            except OSError:
                return self.fail(404, f"No encuentro la carpeta de Descargas ({dl})")
            entries.sort(key=lambda e: e.stat().st_mtime, reverse=True)
            self.send(200, {"dir": str(dl), "files": [e.name for e in entries[:60]]})
        elif url.path.startswith("/dl/"):
            name = urllib.parse.unquote(url.path[4:])
            self.send_file(downloads_dir() / name if name == Path(name).name else None, "no-cache")
        elif url.path.startswith("/img/") and root:
            self.send_file(inside(root, urllib.parse.unquote(url.path[5:])))
        else:
            self.fail(404, "No existe")

    def do_POST(self):
        # Header propio: otra página web no puede mandarlo sin permiso (CORS).
        if self.headers.get("X-Visor") != "1":
            return self.fail(403, "Prohibido")
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        root = load_config().get("root")
        path = urllib.parse.urlsplit(self.path).path

        if path == "/api/pick":
            picked = pick_folder(root)
            if picked:
                save_config(root=picked)
            return self.send(200, {"root": picked})

        if not root:
            return self.fail(400, "No hay carpeta abierta")

        if path == "/api/create":
            return self.create(Path(root).resolve(), body)

        folder = inside(root, body.get("path", ""))
        if not folder or not folder.is_dir():
            return self.fail(404, "La carpeta ya no existe. Recarga.")

        if path == "/api/reveal":
            os.startfile(folder)
            return self.send(200, {"ok": True})

        if path == "/api/rename":
            if folder == Path(root).resolve():
                return self.fail(400, "No se puede renombrar la carpeta raíz")
            old = folder.name
            if "name" in body:
                new = str(body["name"]).strip()
            else:
                _, rest = parse_name(old)
                sizes = {k.upper(): int(v) for k, v in body.get("sizes", {}).items() if int(v) > 0}
                new = format_name(sizes, rest)
            if bad_name(new):
                return self.fail(400, f"Nombre no válido: «{new}»")
            target = folder.with_name(new)
            if new != old:
                if target.exists() and new.lower() != old.lower():
                    return self.fail(409, f"Ya existe una carpeta «{new}» junto a esta")
                try:
                    folder.rename(target)
                except OSError as e:
                    return self.fail(500, f"No se pudo renombrar: {e.strerror or e}")
            return self.send(200, {"old": old, "garment": scan(Path(root).resolve(), target)[0]})

        if path == "/api/uncreate":
            # Deshacer una prenda recién creada: las fotos vuelven a Descargas y se quitan las carpetas que queden vacías.
            rootp = Path(root).resolve()
            if folder == rootp:
                return self.fail(400, "No se puede deshacer en la carpeta raíz")
            dl = downloads_dir()
            try:
                for f in body.get("files", []):
                    src = folder / Path(f).name
                    if src.is_file() and not (dl / src.name).exists():
                        shutil.move(src, dl / src.name)
                p = folder
                while p != rootp and not any(p.iterdir()):
                    p.rmdir()
                    p = p.parent
            except OSError as e:
                return self.fail(500, f"No se pudo deshacer del todo: {e.strerror or e}")
            return self.send(200, {"ok": True})

        self.fail(404, "No existe")

    def create(self, root, body):
        parts = [p.strip() for p in str(body.get("parent", "")).split("/") if p.strip()]
        if not parts or any(bad_name(p) for p in parts):
            return self.fail(400, "Elige zona y fit con nombres válidos")
        sizes = {k.upper(): int(v) for k, v in body.get("sizes", {}).items() if int(v) > 0}
        name = format_name(sizes, str(body.get("color", "")).strip())
        if bad_name(name):
            return self.fail(400, f"Nombre no válido: «{name}»")
        dl = downloads_dir()
        files = [dl / f for f in body.get("files", []) if f == Path(f).name and Path(f).suffix.lower() in IMG_EXT]
        if not files or not all(f.is_file() for f in files):
            return self.fail(400, "Elige al menos una foto de Descargas (o alguna ya no está ahí)")
        parent = inside(root, "/".join(parts))
        if not parent or parent == root:
            return self.fail(400, "Destino no válido")
        target = parent / name
        if target.exists():
            return self.fail(409, f"Ya existe «{name}» en {' › '.join(parts)}. Ábrela y súmale tallas.")
        moved = []
        try:
            target.mkdir(parents=True)
            for f in files:
                shutil.move(f, target / f.name)
                moved.append(f.name)
        except OSError as e:
            return self.fail(500, f"Se movieron {len(moved)} de {len(files)} fotos y luego falló: {e.strerror or e}")
        return self.send(200, {"garment": scan(root, target)[0], "files": moved})


def find_browser():
    for base in (os.environ.get("ProgramFiles(x86)"), os.environ.get("ProgramFiles"), os.environ.get("LOCALAPPDATA")):
        for rel in (r"Microsoft\Edge\Application\msedge.exe", r"Google\Chrome\Application\chrome.exe"):
            if base and (p := Path(base) / rel).exists():
                return str(p)
    return None


def open_window(port):
    url = f"http://127.0.0.1:{port}/"
    browser = find_browser()
    if not browser:
        import webbrowser
        webbrowser.open(url)
        return None
    return subprocess.Popen([
        browser, f"--app={url}", f"--user-data-dir={DATA / 'ventana'}",
        "--no-first-run", "--no-default-browser-check", "--window-size=1500,950",
    ])


def main():
    # Si ya hay una ventana abierta, abrir otra apuntando al mismo servidor.
    port = load_config().get("port")
    if port:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/api/ping", timeout=1)
            open_window(port)
            return
        except OSError:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    save_config(port=port)
    window = open_window(port)
    if window is None:
        server.serve_forever()
        return
    threading.Thread(target=server.serve_forever, daemon=True).start()
    window.wait()
    save_config(port=None)


if __name__ == "__main__":
    main()
