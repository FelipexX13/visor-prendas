# Visor de prendas

Visor local para un inventario de ropa guardado como carpetas de fotos (por ejemplo, en Google Drive
sincronizado al PC). Aplana el árbol de carpetas en un solo muro de fotos, para ver a ojo si una prenda ya está
registrada y sumarle tallas sin abrir carpeta por carpeta.

Solo usa la librería estándar de Python: un servidor HTTP local y una ventana de Edge (o Chrome) en modo app.

## Uso

Requisitos: Windows, Python 3.9 o superior y Edge o Chrome.

Doble clic en `app.pyw` y elige la carpeta raíz de las fotos. La recuerda para la próxima vez.

## Cómo lee las carpetas

- Una prenda es una carpeta con imágenes dentro.
- Su nombre es `<tallas> <color o notas>`, por ejemplo `S, 2.M, 3.2XL Azul ok`. `2.M` (o `M.2`) son dos
  unidades de M; una talla sola es una. Mujer va en talla francesa con `T` (`T36, 2.T38 Blanco`, para no
  confundirse con las carpetas de diseño `32`, `36`…) y niño por edad con su estatura (`2.14A 164cm Azul`),
  según la guía oficial de lacoste.com/fr/guidedestailles.
- Las carpetas que empiezan por `NO USAR` y las fotos de tela (`Tela.*`) se ocultan por defecto.

## Qué hace

- Agrupa las prendas por carpeta padre: la foto de frente grande, el resto en miniatura y vista a pantalla
  completa en calidad original.
- Editar tallas renombra la carpeta: ordena de XS a 9XL, quita las tallas en 0 y deja el resto del nombre igual.
  Nunca sobrescribe otra carpeta.
- Crear prenda: zona › fit › diseño, tallas, color y fotos de Descargas, que se mueven, no se copian. Deshacer
  las devuelve a Descargas y borra las carpetas que queden vacías.

La configuración se guarda en `%LOCALAPPDATA%\VisorPrendas`.
