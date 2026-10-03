---
name: math2ggb
description: >-
  Turn a math problem (especially geometry) into GeoGebra .ggb files. For each
  figure it produces THREE deliverables from the SAME dependency-constrained
  construction: a 静态复刻图 (static faithful reproduction that exactly matches the
  printed figure), a 干净可交互图 (clean interactive figure — same print-identical
  look, no text/aids, fully draggable with every condition preserved), and a
  动态理解图 (dynamic teaching figure adding auxiliary lines, annotations, and live
  angle/length readouts on a toggle). All encode the problem's conditions as real
  constraints, so dragging a driver point keeps every condition satisfied. Use
  when the user wants a GeoGebra file or .ggb, asks to turn a geometry/math
  problem or figure into GeoGebra, wants an interactive GeoGebra applet / 动态几何
  / 几何画板, or mentions GeoGebra, ggb, or 动态几何. Drives the real GeoGebra
  engine in a browser and exports via getBase64.
---

# Math → GeoGebra (.ggb)

For **each figure** in the problem, produce **three** files, all built from the
SAME dependency-constrained construction. **In all three the base visible content
equals the printed figure — exactly the same points, segments, and angle marks:
no more, no less** (only the 动态理解图 adds aids, and only on a toggle that
defaults off).

1. **静态复刻图** (static faithful) — the printed figure reproduced exactly: only
   the original's points, segments, and its own angle ticks; no axes/grid, no
   extra labels or auxiliary lines. The clean, print-matching reference still.
2. **干净可交互图** (clean interactive) — **visually identical to the original**
   (same marks; no text, no annotations, no visible auxiliary / locus / hidden
   circle), but the full interactive construction: helper constraint objects (e.g.
   the circumcircle a point rides on) are **kept but hidden**, so dragging a driver
   point keeps every condition satisfied. For hands-on exploration of the original
   figure itself.
3. **动态理解图** (dynamic teaching) — the SAME construction PLUS teaching aids
   (the revealed hidden circle, the fold, medians, a locus, annotations, live
   `Angle`/`Distance` readouts) on a **single toggleable layer** (a `显示辅助`
   checkbox). Unchecking it returns the view to the exact original.

Relationship: 1 and 2 show the identical clean content (= the print) — 静态复刻图 is
the faithful still, 干净可交互图 is the same figure meant to be dragged; 3 = the
干净可交互图 plus the toggle-gated teaching layer. Suggested filenames per figure:
`<fig>_static.ggb`, `<fig>_clean.ggb`, `<fig>_dynamic.ggb`.

## Hard rules

1. **Never hand-write `geogebra.xml`.** Drive the real GeoGebra engine in a
   browser (its JS API) and export with `getBase64()` — the only way to guarantee
   a valid file. (Hand XML breaks on internal command names, path parameters,
   perspectives.)
2. **Encode the problem's conditions as real dependencies — in all three files.**
   A figure is NOT a pile of free points. Only the genuine degrees of freedom are
   draggable (**driver points**); every other point is **derived** by a
   construction that enforces a condition (concyclic, on-line, intersection,
   reflection/fold, midpoint, perpendicular, given angle/length, locus…). Dragging
   any driver point must move the whole figure while every condition stays
   satisfied. This includes the 静态复刻图 — it is a *clean render of the
   constrained construction*, not free dots.
3. **Match the original exactly by measuring it — never eyeball coordinates.**
   Point coordinates, segment lengths, and angle ratios must equal the printed
   figure. Crop + zoom each subfigure, read precise pixel coordinates of every
   labeled point, convert to a clean coordinate frame, and verify lengths/angles
   before AND after building. Driver points take the measured coordinates, so the
   constrained construction reproduces the drawing.
   *Exception:* when a figure is a 示意图 (explicitly not to scale) yet the problem
   gives exact metric values (e.g. `∠BAC=90°`, `BC=8`), honor the given values
   (they define the true figure) and use measurement for orientation/layout and
   for the positions of genuinely-free points.
4. **Final content = the original, no more no less — verify, then delete the
   scaffolding.** You MAY temporarily add measurement objects (extra `Angle`/
   `Distance`, ratio checks) to confirm coordinates, segment lengths, and angle
   ratios match the image; once confirmed you MUST `Delete(...)` every such
   **verification object before export** (delete, NOT hide — a hidden object still
   lives in the file). Keep three object categories straight:
   *original marks* → shown · *construction helpers* that enforce conditions →
   kept but hidden · *verification scaffolding* → deleted. Teaching aids exist
   only in the 动态理解图, gated behind the `显示辅助` toggle. See recipes §4c–§4d.

## Requirements
- A **browser tool**: navigate, evaluate JavaScript (CDP `Runtime.evaluate`), screenshot.
- **Internet** (generator page loads GeoGebra from geogebra.org's CDN).
- `python3` (helper server + measuring the image).

## Stage checklist
```
- [ ] A. Understand + measure: solve; write the CONDITION LIST; MEASURE the image (crop+zoom, read pixel coords of every labeled point); convert to clean coords; verify lengths/angles.
- [ ] B. Model as a constraint graph: split driver (free) vs derived points; map each condition to a construction; plan the three renders (静态复刻=faithful still, 干净可交互=clean+draggable, 动态理解=+toggle aids). Only true DOF draggable.
- [ ] C. Generate via the GeoGebra engine (server + browser); export all three .ggb per figure.
- [ ] D. Validate: compare coords/lengths/angles vs the image; DRAG-TEST every condition holds; confirm no leftover aids/verification marks; round-trip re-open.
- [ ] E. Deliver: list files (three per figure) + the sandbox-safe way to open them.
```

---

## A. Understand & measure the original

1. **Solve** the geometry (exact positions, invariants, answer). Verify with a
   quick `python3` script when there is real computation (loci, minima, lengths).
2. **Write the condition list** — every relationship the problem states or
   implies. Example: `∠ADB=∠ACB ⇒ A,B,C,D concyclic`; `E = AD ∩ BC`;
   `fold ⇒ F = reflection of D over BC`; `H = midpoint AC`; `△BEK∼△AEH`;
   `∠BAC=90°, ∠ACB=30°, BC=8`. This list drives Stage B.
3. **Measure the image (mandatory — no eyeballing).** For each subfigure: crop it
   and upscale ≥4×; read the pixel coordinates of every labeled point; convert to
   a clean frame (flip y, anchor one point at the origin, choose a scale so a key
   length is round); record all coordinates. Then verify the measured coords
   reproduce the drawn shape (segment-length ratios, angles) and fit the condition
   list. See recipes §4a.

## B. Model as a constraint graph (per figure)

1. **Classify points** using the condition list:
   - **Driver (free) points** — the minimal set with genuine freedom (often the
     triangle's vertices, plus one point constrained to a circle/line, e.g.
     `D=Point(c)`). Place drivers at the **measured** coordinates.
   - **Derived points** — everything a condition determines (`Intersect`,
     `Reflect`, `Midpoint`, spiral similarity, `Locus`…). Lock them to the
     conditions; never leave them free.
   - Map each condition → a construction (recipes §4b table).
2. **Three renders from the SAME graph:**
   - **静态复刻图**: hide helper-only objects (a circle used only to constrain a
     point, helper lines used only for `Intersect`); show ONLY the original's
     points + segments + its own angle ticks; axes/grid off; no annotations. The
     faithful print-matching still.
   - **干净可交互图**: the same clean content as the 静态复刻图 (helpers hidden;
     only the original's marks; no text, no aids, no visible auxiliary/locus/hidden
     circle), delivered as the full interactive construction — dragging a driver
     keeps all conditions. In practice: the 动态理解图 with its teaching layer
     removed (no `显示辅助` checkbox, all aids hidden), or the 静态复刻图 explicitly
     presented for dragging.
   - **动态理解图**: build the teaching aids (revealed hidden circle, fold,
     medians, locus, descriptive `Text`, live `Angle`/`Distance`) and gate them all
     on one `显示辅助` checkbox (`SetConditionToShowObject` — recipes §4d), so the
     view collapses to the exact original when unchecked. Color by role.
   - For all three, **delete all verification scaffolding before export** (rule 4, recipes §4c).
3. Only true degrees of freedom are movable; derived points must not be free.
   Pick a clean view (axes off; ~1.34 aspect — recipes §3).

## C. Generate the .ggb (reliable, verified path)

1. **Start the server** (serves the generator page, receives exports):
   ```bash
   python3 scripts/ggb_server.py <OUTPUT_DIR> 8777
   ```
   Run it in the background; it prints the URL and save location.
2. **Open** `http://localhost:8777/generator.html`; evaluate the "wait until
   ready" snippet (recipes §1).
3. **Build → verify → clean → frame → export**, once per render (three per figure).
   Evaluate a `(function(){var g=window.ggbApplet; … })()` that resets, runs the
   `evalCommand` list, and styles. Then:
   - **Verify (scaffolding):** optionally add temp `Angle`/`Distance` objects and
     read them (`getValue`) to confirm lengths/angles match the measured image.
   - **Clean per render:** `Delete(...)` every verification object (recipes §4c).
     · 静态复刻图 & 干净可交互图 → hide all helper/auxiliary objects
     (`setVisible(false)`), show only the original's marks, add NO text/aids/toggle.
     · 动态理解图 → gate teaching aids on the `显示辅助` checkbox (recipes §4d).
   - `setAxesVisible(false,false)`, `setGridVisible(false)`, `setCoordSystem(...)`,
     return a status. **Screenshot** — it must show only the original's marks (for
     the 动态理解图, also screenshot with hints OFF to confirm it equals the
     original). Then **save**:
   ```js
   fetch('/save?name=<figure>_<static|clean|dynamic>.ggb',{method:'POST',body:window.ggbApplet.getBase64()}).then(r=>r.text())
   ```
   `references/example-hidden-circle.md` has complete, verified build blocks
   (静态复刻图 + 干净可交互图 + 动态理解图, with verify→delete and the toggle) to adapt.

## D. Validate

- **Compare to the image**: screenshot each figure and check point arrangement,
  segment lengths/ratios, and angle marks against the original crop. Fix until it matches.
- **Marks = original, no more no less**: every final file must show exactly the
  original's points/segments/angle ticks — **no leftover verification objects, no
  visible auxiliary/locus/hidden circle, no stray marks**. The 静态复刻图 and the
  干净可交互图 show only the original's marks; for the 动态理解图, toggling `显示辅助`
  OFF must reproduce the original exactly.
- **Drag-test the conditions** (esp. the 干净可交互图 and 动态理解图): move each
  driver point and confirm the whole figure follows and every condition still holds
  (e.g. `∠ADB` stays `=∠ACB`, `F` stays the reflection, `K` stays on its locus). If
  moving a "point" leaves the rest still, it was wrongly left free — turn it into a
  derived object.
- **Round-trip** the most complex file (recipes §1); `unzip -l file.ggb` shows `geogebra.xml`.

## E. Deliver
- List each figure's three `.ggb`: 静态复刻图 / 干净可交互图 / 动态理解图, and what's draggable.
- **How to open (macOS):** the App Store GeoGebra Classic 6 is sandboxed and shows
  a **blank** window if a file is double-clicked or passed on the command line
  ("Cannot open file"). Open via **☰ menu → Open (打开) → From this device → pick
  the file**, or **drag the .ggb onto the GeoGebra window**. The web app
  (geogebra.org/classic) and non-sandboxed desktop builds open files normally.
  (Details: recipes §5.6.)

---

## Key gotchas (full list in `references/geogebra-recipes.md` §5)
- Use the **'AG'** applet, never graphics-only 'G' — 'G' exports a broken perspective that opens **blank** on desktop.
- **Export via the POST server**; don't return base64 to yourself.
- `Reflect`, `Rotate`, `Dilate`, `Locus`, `Point(circle)`, `Intersect`, `Midpoint` all work via `evalCommand` input syntax.
- Spiral similarity: `K=Rotate(Dilate(H,Distance(E,B)/Distance(E,A),E), Angle(Vector(E,B))-Angle(Vector(E,A)), E)`, then `Locus(K,D)`.
- **Hidden ≠ removed**: helper/auxiliary objects a construction depends on (the path circle, `Locus`) must be **hidden** (`setVisible false`) in the 静态复刻图 / 干净可交互图, never deleted; only verification scaffolding is deleted.
- Set **axes off before export** so a fresh open stays clean.

## Resources
- `references/geogebra-recipes.md` — commands, JS API, image-measuring recipe, condition→constraint table, gotchas.
- `references/example-hidden-circle.md` — a complete verified example (静态复刻图 + 干净可交互图 + 动态理解图, for 2 figures).
- `scripts/ggb_server.py` — serve generator + receive exported `.ggb`.
- `templates/generator.html` — loads the real GeoGebra engine (AG layout).
