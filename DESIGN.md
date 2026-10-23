---
name: Visor de Prendas
description: A garment stock wall that reads like the WhatsApp Business catalog the owner already sells from.
colors:
  ground: "#0b141a"
  panel: "#111b21"
  bar: "#202c33"
  raised: "#2a3942"
  line: "#26343c"
  text: "#e9edef"
  muted: "#8696a0"
  green: "#00a884"
  green-hover: "#06cf9c"
  green-deep: "#005c4b"
  green-chip: "#0a332c"
  danger: "#f7838f"
  plate: "#ffffff"
typography:
  headline:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, sans-serif"
    fontSize: "20px"
    fontWeight: 600
    lineHeight: 1.45
  title-drawer:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, sans-serif"
    fontSize: "19px"
    fontWeight: 600
    lineHeight: 1.45
  title:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 600
    lineHeight: 1.45
  label-section:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.45
  body:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.45
    fontFeature: "tnum"
  body-strong:
    fontFamily: "Segoe UI Variable Text, Segoe UI, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 600
    lineHeight: 1.45
    fontFeature: "tnum"
rounded:
  thumb: "5px"
  inner: "6px"
  tile: "8px"
  bubble: "10px"
  chip: "16px"
  pill: "18px"
  search: "19px"
spacing:
  hair: "4px"
  tight: "6px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
components:
  button-primary:
    backgroundColor: "{colors.green}"
    textColor: "{colors.panel}"
    rounded: "{rounded.pill}"
    padding: "0 12px"
    height: "36px"
  button-primary-hover:
    backgroundColor: "{colors.green-hover}"
  button-primary-disabled:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.muted}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.text}"
    rounded: "{rounded.pill}"
    padding: "0 12px"
    height: "36px"
  button-ghost-hover:
    backgroundColor: "{colors.raised}"
  button-icon:
    textColor: "{colors.muted}"
    rounded: "{rounded.pill}"
    size: "36px"
  chip:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.muted}"
    rounded: "{rounded.chip}"
    padding: "0 14px"
    height: "32px"
  chip-active:
    backgroundColor: "{colors.green-chip}"
    textColor: "{colors.green}"
  search:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.text}"
    rounded: "{rounded.search}"
    padding: "0 12px"
    height: "38px"
  tile:
    backgroundColor: "{colors.panel}"
    rounded: "{rounded.tile}"
    padding: "6px"
  tile-hover:
    backgroundColor: "{colors.bar}"
  size-pill:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.text}"
    typography: "{typography.body-strong}"
    rounded: "{rounded.thumb}"
    padding: "0 7px"
    height: "22px"
  size-stepper:
    backgroundColor: "{colors.ground}"
    rounded: "{rounded.tile}"
    padding: "6px 4px 4px"
  toast:
    backgroundColor: "{colors.bar}"
    textColor: "{colors.text}"
    rounded: "{rounded.bubble}"
    padding: "10px 10px 10px 16px"
  toast-saved:
    backgroundColor: "{colors.green-deep}"
    textColor: "{colors.text}"
---

# Design System: Visor de Prendas

## Overview

**Creative North Star: "The WhatsApp Catalog"**

The stock wall reads like the WhatsApp Business catalog the owner already sells from: dark WhatsApp chrome, photo tiles, one line of text under each, nothing else. It turns down the dark photo-manager look: no folder-tree sidebar, no metadata panels. The interface is a quiet frame around about 400 garment photos. Its density is set for scrolling and recognition, not for reading.

The chrome has no hue, so the only colour on screen comes from the garments. Green is the one exception and it means "done": you commit with it, the saved-rename bubble wears it, and active filters glow with it. Every rename leaves a before → after receipt with an undo, written like a sent chat message. Depth comes from four tonal steps of blue-black. Shadows are not used for depth.

Motion is short and eased with one exponential-out curve (`cubic-bezier(.16, 1, .3, 1)`). Hovers last 200ms. The post-save ring flash lasts 1.6s, the unsaved-changes nudge 1.4s, and the toast slides up 12px. Reduced motion turns all of it off.

**Key Characteristics:**
- WhatsApp dark grammar: ground, panel, bar and raised surfaces, separated by tone instead of lines.
- Hue-free chrome. Garment photos carry the colour.
- Green is reserved for confirmation and active state.
- One 14px size on tiles, with hierarchy set by weight and muted colour.
- 4:5 photo plates cropped with `object-fit: cover`, never letterboxed.
- Pills for controls, 8px rounding for content, a tailed bubble for the saved receipt.
- Inline SVG line icons (24 viewBox, 1.8 stroke, round caps).

## Colors

The palette is WhatsApp's dark blue-black family with one confirmation green and one soft error pink. The photos supply every other colour.

### Primary
- **Send Green** (`green`): WhatsApp's send-button green. Used on the commit button ("Renombrar carpeta"), active toggle dots and labels, active chip text, the 3px ring that flashes on a tile after a save, plus the native caret and the checkbox/range accent.
- **Send Green, Lit** (`green-hover`): hover state of the commit button only.
- **Sent-Bubble Green** (`green-deep`): background of the saved-rename toast, which mimics a sent message. Also the text-selection highlight.
- **Active-Chip Green** (`green-chip`): background of the selected zone chip.

### Neutral
- **Night Ground** (`ground`): the wall background behind tiles. Sticky section headers use it too, so they cover the tiles as they scroll under. Size steppers and the rename preview are recessed into it.
- **Chat Panel** (`panel`): tile cards, the garment drawer, and button text on green.
- **Header Bar** (`bar`): the top bar, the drawer head, hovered and selected tiles, the default toast, and the viewer's nav buttons.
- **Raised Field** (`raised`): the pill search, chips, size pills, thumbnail placeholders, ghost-button hover, the inset outline of line buttons, and the disabled commit button.
- **Hairline** (`line`): the only drawn borders. These are the drawer's left edge and the top edge of its sticky footer.
- **Message Text** (`text`): primary text. Also the colour of focus outlines, the selected-tile ring and the unsaved-preview nudge ring.
- **Meta Grey** (`muted`): counts, secondary labels, placeholders, inactive icons, unpressed toggle rings, and the old name in a before → after.
- **Viewer Plate** (`plate`): paper-white backing behind the original image in the full-screen viewer only.

### Semantic
- **Soft Error Pink** (`danger`): error toast inset ring and the "carpeta quedaría sin nombre" warning. Never decorative.

### Named Rules
**The Photos Carry Color Rule.** Chrome surfaces, text and icons stay on the blue-black and grey neutrals. The only hues allowed in chrome are the green family (confirmation and active state) and the error pink. If a new element needs colour to be noticed, it should use weight or tone instead.

**The Green Means Done Rule.** Green marks something committed or switched on: the commit button, the saved bubble, active chips and toggles, the post-save flash. It also appears on the native caret and selection, as in WhatsApp itself. Green is never used on hover or focus for neutral controls, and never as decoration.

## Typography

**Body Font:** Segoe UI Variable Text (with Segoe UI, system-ui, sans-serif)

**Character:** The app uses the same platform face the owner sees in WhatsApp Desktop on Windows. One family carries every role. Tabular numerals are on globally so counts line up.

### Hierarchy
- **Headline** (600, 20px): empty-state titles only.
- **Title, drawer** (600, 19px): the garment's colour/notes name at the head of the drawer.
- **Title** (600, 16px): the open folder's name in the top bar. Drawer and viewer headers use 16px at 400.
- **Label, section** (400, 15px, muted): sticky group headers. The path is muted and the last segment (zone › **fit**) is set in 600 text colour.
- **Body** (400, 14px, line-height 1.45): everything else. That covers tiles, chips, buttons, counts, the toast and the drawer copy. Body measure is capped at 46ch in empty states.
- **Body strong** (600, 14px): size codes in pills and steppers, chip zone names, the new name in a rename preview.

### Named Rules
**The One Size Tile Rule.** Every text element on a tile is 14px. Size pills are 600, the colour/notes name is 400, and the design label is muted 400 after a middle dot. Rank comes from weight and colour, never from a second size.

## Layout

The app is a full-height two-row grid: the top bar above a scrolling main area. The top bar has a 56px minimum height, 16px side padding and a 12px gap, and wraps when narrow. It contains the folder name and count, the pill search (flex 1 1 320px, max 560px), and right-aligned tools. A horizontally scrolling zone chip rail sits under it with a 8px gap and no scrollbar.

The wall has 16px side padding and 64px bottom padding. It is a run of sections, each with a sticky header (22px above, 10px below) over an auto-fill grid. The grid uses `minmax(var(--tile), 1fr)` with 12px gaps. The tile width defaults to 220px and the user can set it from 160 to 380px with a range slider, which gives 4 to 6 tiles across at 1500px. Inside a tile, the 4:5 plate sits above a 4-column thumbnail row (square thumbs, 4px gap) and a caption block.

The garment drawer is a 400px right column with a sticky 56px head and a sticky footer that appears only when there are unsaved changes. At 900px and below it becomes a full-screen overlay and the zoom slider is hidden. The full-screen viewer is a 56px head, the image stage and a thumbnail strip, with 48px round previous/next buttons fixed at mid-height.

The spacing rhythm is 4, 6, 8, 12 and 16px, with 24px reserved for the toast's distance from the bottom edge.

## Elevation & Depth

The system is flat and tonal. Depth is a four-step lightness ladder (ground → panel → bar → raised): each element nested inside another, or hovered, moves one step lighter. Rings drawn as inset or spread `box-shadow` mark state without changing layout. The only true drop shadow belongs to the floating toast.

### Shadow Vocabulary
- **Toast float** (`box-shadow: 0 6px 24px rgba(0, 0, 0, .45)`): the only floating element, the status/receipt bubble.
- **Selection ring** (`box-shadow: 0 0 0 2px <text>`): the tile whose drawer is open.
- **Saved flash** (`0 0 0 3px <green>`, fading over 1.6s): the tile that was just renamed.
- **Changed outline** (`inset 0 0 0 1px <muted>`): a size stepper whose count differs from disk.
- **Line button** (`inset 0 0 0 1px <raised>`): secondary buttons such as "Cambiar carpeta" and "Descartar".

### Named Rules
**The Tonal Step Rule.** Surfaces never cast shadows. To lift something, move it one step up the ground → panel → bar → raised ladder. Only the toast floats.

**The White Ring Rule.** Attention rings (focus outline at 2px with a 2px offset, the selected tile, the unsaved-preview nudge) use the text colour. Green rings appear only after something has been saved.

## Shapes

Controls are pills: their radius is half their height (chips 16px, buttons 18px, search 19px, and circles for the clear button, toggle dots and viewer nav). Content containers have soft corners: tiles, steppers, the preview and the drawer photo use 8px, and photo plates inside tiles use 6px. Small pieces use 5px (size pills, thumbnails, the "+N" counter). The saved toast is a 10px chat bubble whose bottom-right corner tightens to 2px and grows a clipped triangular tail, the sent-message silhouette. Borders are almost absent: the only drawn strokes are the drawer's 1px hairlines.

## Components

### Buttons
Quiet pills that come forward on hover. The commit button is the only one that is ever green.
- **Shape:** pill, 36px tall, 18px radius, 8px icon gap.
- **Primary (solid):** Send Green with Chat Panel text at 600. On hover it brightens to Send Green, Lit. Disabled, it falls back to Raised Field with muted text.
- **Ghost (default):** transparent with text colour, and a Raised Field fill on hover. Background and colour transition over 200ms.
- **Line:** ghost plus a 1px inset Raised Field outline. Used for secondary actions ("Cambiar carpeta", "Descartar", "Elegir otra").
- **Icon:** a 36px muted circle that turns text colour on hover.
- **Toggle:** a ghost button with a 16px ring dot. When pressed, the dot fills green and shows a check, and the label and count turn green.

### Chips
- **Style:** 32px pill, Raised Field background, muted count, zone name in 600 text colour.
- **State:** hover lightens the fill. When active the background becomes Active-Chip Green and both name and count turn Send Green. They are single-select filters with `aria-pressed`.

### Cards / Containers (Garment Tile)
- **Corner Style:** 8px outer, 6px plate, 5px thumbs.
- **Background:** Chat Panel at rest. Hover and selected both move to Header Bar, and selected adds the 2px text-colour ring.
- **Shadow Strategy:** none at rest (see Elevation & Depth).
- **Internal Padding:** 6px, with a 6px stack gap and a caption inset of 2px 4px 4px.
- **Content:** a 4:5 photo with cover crop, up to 3–4 square thumbnails at 55% opacity (the active one at 100%) plus a "+N" counter, size pills (`M`, `2XL ×2` with the count muted), and one name line that ends with an ellipsis.

### Inputs / Fields
- **Search:** a 38px pill on Raised Field with a muted magnifier and placeholder. When focused, the icon turns text colour. There is no focus border; the green caret marks it. A 26px round clear button appears when there is a query.
- **Size stepper:** a cell recessed into Night Ground with an 8px radius in a 4-column grid. The size label is 600 (muted when the count is zero), and the count sits between 26×28 minus/plus buttons. Disabled minus drops to 30% opacity. A changed count gets a 1px inset muted outline.

### Navigation
- **Top bar:** Header Bar fill, a 56px row, and the chip rail beneath. There are no tabs and no sidebar. The zone chips are the navigation.
- **Section headers:** sticky on Night Ground. The path is muted with a 16px chevron separator, the last segment is in strong text, and the counts are right-aligned and muted.

### Rename Receipt (signature)
Every rename is shown as before → after. In the drawer's sticky footer, the preview is recessed into Night Ground: the old name is muted with a strikethrough and the new name is in 600. After a save, the toast becomes a sent bubble in Sent-Bubble Green with a double-check icon, `old → new`, and a "Deshacer" button on a 20% black wash. Errors use the default bar bubble with an inset pink ring.

## Do's and Don'ts

### Do:
- **Do** take every surface colour from the ground → panel → bar → raised ladder, and lift by one step for hover and nesting.
- **Do** keep tile text at 14px and rank it by weight (600/400) and the muted grey.
- **Do** crop photos into 4:5 plates with `object-fit: cover` and a Raised Field placeholder underneath.
- **Do** use green only for a commit, a saved state or an active filter/toggle.
- **Do** show any destructive or renaming change as before (muted, struck through) → after (600), with an undo in the toast.
- **Do** make controls pills (radius = half the height) and content 8px-rounded.
- **Do** draw icons as inline SVG symbols: 24 viewBox, 1.8 stroke, round caps and joins, 20px by default.

### Don't:
- **Don't** put any hue in chrome other than the green family and the error pink. Colour belongs to the garments.
- **Don't** letterbox tile photos on white or any other fill. The 4:5 plate is cropped to fill.
- **Don't** use green for the hover, focus or decoration of neutral controls. Focus and selection rings are text-colour white.
- **Don't** add drop shadows to tiles, panels or bars. Only the floating toast has a shadow.
- **Don't** add a second type size inside a tile.
- **Don't** introduce folder-tree sidebars or metadata panels. The zone chips and sticky headers are the whole navigation.
