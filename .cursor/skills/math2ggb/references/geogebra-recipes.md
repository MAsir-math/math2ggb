# GeoGebra Recipes & Gotchas

Everything here is driven through the **live GeoGebra JS API** (`ggbApplet`) in a
browser — you type GeoGebra *input-bar* syntax via `evalCommand`, style via API
methods, then `getBase64()`. This sidesteps the many traps of hand-writing
`geogebra.xml` (internal command names, path parameters, etc.).

---

## 1. Driving the applet from the browser

After `scripts/ggb_server.py` is running and the browser is at
`http://localhost:PORT/generator.html`, use your browser tool's
"evaluate JavaScript" (CDP `Runtime.evaluate`) to run these.

**Wait until ready:**
```js
new Promise(r=>{let n=0;const t=setInterval(()=>{
  if(window.__ready&&window.ggbApplet&&window.ggbApplet.evalCommand){clearInterval(t);r('READY')}
  else if(++n>40){clearInterval(t);r('TIMEOUT')}},500)})
```
(evaluate with awaitPromise=true)

**Build a figure** (reset first, run commands, style, frame, then export):
```js
(function(){
  var g = window.ggbApplet;
  g.reset();
  g.setAxesVisible(false,false); g.setGridVisible(false);
  ['A=(0,0)','B=(4,0)','C=(1,3)','p=Polygon(A,B,C)'].forEach(c=>g.evalCommand(c));
  g.setColor('p',20,90,220);
  g.setCoordSystem(-2,7,-2,5);        // xmin,xmax,ymin,ymax
  return 'objs='+g.getAllObjectNames().length;
})()
```

**Export & save** (POST base64 to the server — never return base64 to the agent):
```js
fetch('/save?name=fig1.ggb',{method:'POST',body:window.ggbApplet.getBase64()}).then(r=>r.text())
```
(evaluate with awaitPromise=true; expect `OK <bytes> -> fig1.ggb`)

**Verify visually:** take a browser screenshot after building.

**Round-trip check** (prove the saved file re-opens; loads from the server):
```js
fetch('/fig1.ggb').then(r=>r.arrayBuffer()).then(buf=>{
  var b=new Uint8Array(buf),s='';for(var i=0;i<b.length;i++)s+=String.fromCharCode(b[i]);
  window.ggbApplet.setBase64(btoa(s));
  return new Promise(res=>setTimeout(()=>res('objs='+window.ggbApplet.getAllObjectNames().length),800));
})
```

---

## 2. Construction commands (input-bar syntax for `evalCommand`)

Assign a name so you can style it later: `name=Command(...)`.

| Need | Command |
|------|---------|
| Point (free) | `A=(1,2)` |
| Point on a path (draggable along it) | `D=Point(c)` then `SetCoords(D,x,y)` to place it |
| Segment / line / ray | `Segment(A,B)`, `Line(A,B)`, `Ray(A,B)` |
| Polygon | `Polygon(A,B,C)` |
| Circle through 3 pts / center+radius / center+pt | `Circle(A,B,C)`, `Circle(A,r)`, `Circle(A,B)` |
| Intersection | `Intersect(obj1,obj2)` ; nth: `Intersect(c,line,1)` |
| Midpoint | `Midpoint(A,C)` |
| Reflection over line | `Reflect(D,line)`  (works via input syntax; do NOT worry that XML calls it "Mirror") |
| Rotation / dilation | `Rotate(obj,angle,center)`, `Dilate(obj,factor,center)` |
| Perpendicular / parallel | `PerpendicularLine(P,line)`, `Line(P,line)` |
| Angle (value + arc) | `Angle(A,B,C)` (vertex B) ; of a vector: `Angle(Vector(E,B))` |
| Distance / length | `Distance(A,B)` |
| **Locus** (trace of dependent pt as a path-point moves) | `Locus(K,D)` (D must be a Point on a path) |
| Text (static) | `Text("hello",(x,y))` |
| Text (dynamic value) | `Text("AK = "+akv,(x,y))` (akv a number object) |

### Spiral similarity (map A→B centered at E, apply to H → K)
Robust, orientation-safe formula (used for "△BEK ∼ △AEH" type constructions):
```
K=Rotate(Dilate(H, Distance(E,B)/Distance(E,A), E), Angle(Vector(E,B))-Angle(Vector(E,A)), E)
```
Then `Locus(K,D)` traces K's path as D moves on its circle — a common "hidden
locus is a circle" reveal.

> Angle orientation: prefer `Angle(Vector(E,B))-Angle(Vector(E,A))` for a signed
> rotation. `Angle(A,E,B)` returns a 0–360° value whose orientation is easy to get
> backwards.

---

## 3. Styling & view (JS API methods)

```js
g.setColor(name, r, g_, b);        // 0–255
g.setPointSize(name, 5);
g.setLineThickness(name, 3);
g.setLineStyle(name, 1);           // 0 solid, 1 dashed-long, 2 dashed-short, 3 dotted
g.setLabelVisible(name, true|false);
g.setLabelStyle(name, 2);          // 0 name, 1 name+value, 2 value, 3 caption  (angles: 2 shows "53°")
g.setVisible(name, false);         // hide helper objects (lines used only for Intersect, etc.)
g.setFilling(name, 0);             // angle sector fill opacity; 0 = arc outline only (textbook look)
g.setAxesVisible(false,false); g.setGridVisible(false);
g.setCoordSystem(xmin,xmax,ymin,ymax);
```
`SetFilling` can also be run as a command: `g.evalCommand('SetFilling(angA,0)')`.

**Keep 1:1 scale (no distortion):** make the view's aspect ratio match the
applet's (width/height ≈ 1100/820 ≈ 1.34). i.e. `(xmax-xmin)/(ymax-ymin) ≈ 1.34`.

**Color-by-role palette** (suggested): structure/triangle blue `20,90,220`;
draggable driver point red `220,30,30`; equal/derived green `0,150,0`; the
"reveal" circle gold `230,150,0` (dashed); a second locus purple `150,60,220`.

---

## 4. Three renders per figure, all constraint-based

Every figure yields **three** files, all built from the **SAME dependency graph**:

- **静态复刻图** (static faithful): a clean render that shows ONLY the original's
  marks — its points + segments + its own angle ticks; axes/grid off; helper-only
  objects **hidden** (a circle used only to constrain a point, helper lines used
  only for `Intersect`); no annotations; **no verification objects** (§4c). The
  faithful print-matching still.
- **干净可交互图** (clean interactive): the **same clean content** as the 静态复刻图
  (only the original's marks; all auxiliary/locus/hidden circles and helper lines
  **hidden but kept** so dependencies survive; no text, no aids, no toggle),
  delivered as the full interactive construction — dragging a driver keeps every
  condition. It is the 动态理解图 with the teaching layer stripped. Use it to
  hands-on explore the original figure itself.
- **动态理解图** (dynamic teaching): the same construction; the meaningful teaching
  aids (revealed hidden circle, fold, medians, locus, `Text`, live `Angle`/`Distance`)
  are gated on one `显示辅助` checkbox (§4d) so the view collapses to the **exact
  original** when unchecked. Also no verification objects.

**None is a pile of free points.** Encode every condition as a real dependency so
dragging a driver point keeps all conditions satisfied — in all three renders. The
静态复刻图 and 干净可交互图 show identical content (= the print); the difference is
intent (faithful still vs. figure-to-drag).

**Three object categories (keep them straight):** *original marks* → shown ·
*construction helpers* (enforce conditions) → kept but hidden with `setVisible(false)` ·
*verification scaffolding* → `Delete`d before export (§4c). Teaching aids (动态 only)
sit on the `显示辅助` toggle (§4d). **Final content of BOTH files = the original, no
more no less.**

**Driver vs derived points:**
- *Driver (free):* the minimal set with genuine freedom — usually the triangle's
  vertices, plus one point constrained to a circle/line (e.g. `D=Point(c)`). Place
  drivers at the **measured** coordinates so the figure reproduces the print.
- *Derived:* everything a condition fixes (`Intersect`, `Reflect`, `Midpoint`,
  spiral similarity, `Locus`…). Never leave these free. (Test: dragging a derived
  point should be impossible / snap back; dragging a driver moves the whole figure.)

### 4a. Measuring the original image (mandatory — no eyeballing)
```python
# crop + upscale each subfigure so you can read exact point pixels
from PIL import Image
im = Image.open("problem.jpg")
sub = im.crop((L, T, R, B))                       # box around one subfigure
sub = sub.resize((sub.width*5, sub.height*5), Image.LANCZOS)
sub.save("fig1_zoom.png")                          # read it; note each labeled point's pixel (px,py)
```
Convert pixels → math coords (image y points down):
```
x = (px - px_B) / s        # s = pixels per unit; pick s so a key length is round
y = (py_B - py) / s        # anchor B at origin; flip y
```
Choose `s` from a known/handy length (e.g. make BC = 8). Record every point, then
check segment-length ratios and key angles against the drawing before building —
and re-check after building (Stage D).

> 示意图 caveat: if the figure is explicitly not to scale but the problem gives
> exact values (`∠BAC=90°`, `BC=8`…), honor the given values; use measurement only
> for orientation/layout and for genuinely-free point positions (e.g. where D sits
> on its arc).

### 4b. Problem condition → GeoGebra constraint
| Condition in the problem | GeoGebra encoding |
|---|---|
| Concyclic (e.g. `∠ADB=∠ACB`) | `c=Circle(A,B,C)`; `D=Point(c)` then `SetCoords(D,…)` to the measured D |
| Point lies on a line/segment | `Point(Line(A,B))` or `Point(Segment(A,B))` |
| Intersection of two objects | `Intersect(o1,o2)` (nth: `Intersect(c,line,1)`) |
| Reflection / fold across a line | `Reflect(P, line)` |
| Midpoint | `Midpoint(A,C)` |
| Perpendicular / parallel | `PerpendicularLine(P,line)` / `Line(P,line)` |
| Given length `L` from `A` toward `B` | `A + L*UnitVector(Vector(A,B))`, or `Point(Circle(A,L))` |
| Given angle at a vertex | `Rotate(B, angle, A)` to make a ray, then a point on / intersection with it |
| Equal-angle pair ⇒ spiral similarity | `K=Rotate(Dilate(H,Distance(E,B)/Distance(E,A),E), Angle(Vector(E,B))-Angle(Vector(E,A)), E)` |
| Moving point traces a curve | `Locus(K, D)` (D a Point on a path) |
| Median / angle bisector | `Segment(A, Midpoint(B,C))` / `AngleBisector(A,B,C)` |

Reuse the SAME graph for all three renders. The 静态复刻图 and 干净可交互图 hide
helper-only objects and show just the original's marks (identical content; the
干净可交互图 is simply presented for dragging); the 动态理解图 adds teaching aids
gated on a toggle (§4d). Verification objects (§4c) are deleted from all three.

### 4c. Verification scaffolding (add → check → DELETE before export)
Precision is confirmed by measuring, not by eye. While building you MAY add
throwaway measurement objects, read them, then delete them:
```js
g.evalCommand('vBC=Distance(B,C)');                       // temp checks
g.evalCommand('vADB=Angle(A,D,B)'); g.evalCommand('vACB=Angle(A,C,B)');
// read + compare to the image measurements:
[['BC',g.getValue('vBC')],['ADB',g.getValue('vADB')],['ACB',g.getValue('vACB')]]
```
Then remove EVERY verification object before export — **delete, not hide** (a
hidden object still lives in the saved file):
```js
['vBC','vADB','vACB'].forEach(n=>g.evalCommand('Delete('+n+')'));
```
`Delete(obj)` also removes whatever depends on `obj`, so only ever delete the
throwaway checks — never a construction object other objects rely on.

### 4d. Teaching aids on a toggle (动态理解图 only)
Keep the base identical to the original; put every teaching aid behind one checkbox
so the view can collapse to the exact original.
```js
g.evalCommand('showAids=true');                            // boolean -> shows as a checkbox
g.evalCommand('SetCaption(showAids,"显示辅助")');
// gate each aid (revealed circle, locus, notes, live angles, helper segments):
['c','loc','t1','adb','acb'].forEach(o=>g.evalCommand('SetConditionToShowObject('+o+',showAids)'));
```
Unchecking `showAids` hides all aids → only the original's marks remain. (Or use
`Checkbox("显示辅助",{c,loc,t1,adb,acb})` to create the checkbox and its list at once.)
Do NOT gate the original's own marks — those stay visible always.

---

## 5. Gotchas (hard-won)

1. **Use 'AG' (algebra+graphics) perspective, never 'G'.** The graphics-only
   export writes a pane `divider="0.99"` that squishes the graphics view to ~1%
   → the file opens **blank** in desktop GeoGebra. `generator.html` already uses 'AG'.
2. **Never hand-write geogebra.xml.** Internal command names differ from input
   names (reflection is `Mirror` internally), point-on-path needs `pathParameter`,
   etc. Let the engine build it; `getBase64()` is always valid.
3. **Get the file out via the POST server**, not by returning base64 to the agent
   (it's large and opaque). `fetch('/save?name=...',{method:'POST',body:getBase64()})`.
4. **Axes off is saved in the perspective** when you call `setAxesVisible(false,false)`
   before export, so a fresh open respects it. (If you strip the whole `<gui>` block
   from the xml, axes-off is lost — don't do that; just regenerate with 'AG'.)
5. **Spiral-similarity / rotation orientation**: use `Angle(Vector(..))-Angle(Vector(..))`.
6. **macOS App Store GeoGebra is SANDBOXED** (`org.geogebra6.mac`,
   `com.apple.security.files.user-selected.read-write`). It can only read files the
   user **selects in the Open dialog** (or drags onto the window). Double-clicking or
   passing a path via command line fails with "Cannot open file" → looks blank. This
   is NOT a file problem. Tell users: open via **☰ menu → Open → From this device →
   pick the file**, or **drag the .ggb onto the GeoGebra window**. Non-sandboxed
   (geogebra.org download) builds and the web app open files normally.
7. **Validate a .ggb structurally** (optional): it's a zip containing `geogebra.xml`.
   `unzip -l file.ggb` should list `geogebra.xml`.
8. **Hidden ≠ removed.** `setVisible(false)` objects still exist in the saved file.
   Use `Delete(obj)` for verification scaffolding so the final content is exactly
   the original — no more, no less. Keep (hidden) only the helpers that constraints
   actually depend on.
