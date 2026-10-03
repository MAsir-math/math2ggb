# Math2GGB

A Cursor Agent Skill that turns a **math problem (especially geometry) into
GeoGebra `.ggb` files**. For each figure it produces **three** files built from the
SAME dependency-constrained construction:
- a **静态复刻图** (static faithful) — the printed figure reproduced exactly (only its points, segments, and angle marks, no more no less);
- a **干净可交互图** (clean interactive) — the same print-identical look with no text/aids/visible helper circles, but fully draggable with every condition preserved;
- a **动态理解图** (dynamic teaching) — the same base plus auxiliary lines, annotations, and live angle/length readouts on a **`显示辅助` toggle** — unchecking it returns to the exact original.

All three encode the problem's conditions as real constraints (concyclic, intersection,
reflection, midpoint, spiral similarity, locus…), so dragging a driver point keeps
every condition satisfied. Precise reproduction is enforced by **measuring the
original image** (never eyeballing) and by adding temporary measurement objects to
verify coordinates/lengths/angles, which are **deleted before export** so the final
file matches the original exactly.

It works by driving the **real GeoGebra engine** in a browser (GeoGebra's own JS
API) and exporting with `getBase64()`, so the produced files always open in
GeoGebra — no fragile hand-written XML.

## Install

Copy this folder into your Cursor skills directory:

```bash
# Personal (all projects):
cp -R Math2GGB ~/.cursor/skills/math2ggb

# or Project (this repo only):
cp -R Math2GGB <your-project>/.cursor/skills/math2ggb
```

Then just ask the agent, e.g. "把这道几何题做成 GeoGebra 文件" / "make an
interactive GeoGebra of this problem".

## Layout
```
Math2GGB/
├── SKILL.md                          # main orchestration (stages A–E)
├── references/
│   ├── geogebra-recipes.md           # commands, JS API, image-measuring, condition→constraint table, gotchas
│   └── example-hidden-circle.md      # verified example (静态复刻图 + 干净可交互图 + 动态理解图)
├── scripts/
│   └── ggb_server.py                 # serves generator + receives exported .ggb
└── templates/
    └── generator.html                # loads the real GeoGebra engine (AG layout)
```

## Requirements
- A browser tool (navigate, evaluate JS, screenshot).
- Internet (the generator page loads GeoGebra from geogebra.org's CDN).
- `python3`.

## Opening the output on macOS
The **App Store** GeoGebra Classic 6 is sandboxed: double-clicking a `.ggb` (or
passing it on the command line) shows a **blank** window. Open via
**☰ menu → Open → From this device → pick the file**, or **drag the file onto the
GeoGebra window**. The web app (geogebra.org/classic) opens files normally.
