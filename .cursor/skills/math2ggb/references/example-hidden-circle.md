# Worked Example — "Hidden Circle" geometry problem

A complete, verified template. **Two figures × three renders = 6 files.** All three
renders of a figure share ONE dependency graph; all show ONLY the original's marks
(the 动态理解图 hides its aids behind a `显示辅助` checkbox that defaults off). No
render is a pile of free points — dragging a driver keeps every condition. Any
temporary measurement objects are **deleted** before export.

The three renders (per figure):
- **静态复刻图** — faithful print-match still (constrained; you MAY `SetFixed` the
  drivers so it stays put).
- **干净可交互图** — the SAME clean look, drivers left draggable (conditions hold),
  no text/aids/visible helper circles.
- **动态理解图** — same construction + teaching aids on the `显示辅助` toggle.

Suggested names: `fig1_static.ggb` / `fig1_clean.ggb` / `fig1_dynamic.ggb` (same for
fig2). (In the mathVideoMaker run these were `fig*_original` /
`fig*_interactive_clean` / `fig*_interactive`.)

**Verify → delete (do this in every block before export).** Add throwaway checks,
read them against the measured image, then delete them:
```js
g.evalCommand('vBC=Distance(B,C)'); g.evalCommand('vADB=Angle(A,D,B)'); g.evalCommand('vACB=Angle(A,C,B)');
// read & compare, e.g. g.getValue('vADB') ≈ g.getValue('vACB'); g.getValue('vBC') matches the drawing
['vBC','vADB','vACB'].forEach(n=>g.evalCommand('Delete('+n+')'));   // MUST delete (not hide) before saving
```

**Condition list (from Stage A):** `∠ADB=∠ACB ⇒ A,B,C,D concyclic`; `E = AD ∩ BC`;
`fold ⇒ F = reflection of D over BC`; part-1① marks the two equal angles `∠EAC` (at A)
and `∠EBF` (at B); `H = midpoint AC`; `∠KEB=∠HEA & ∠KBE=∠HAE ⇒ △BEK∼△AEH`; part 2:
`∠BAC=90°, ∠ACB=30°, BC=8` ⇒ `AK_min = 2√3−2`, `BK = 2√2`. Driver coords below are
the **measured** positions (Stage A/B); D/E/F/H/K are derived.
(题图2 is a 示意图 that prints no angle ticks, so its 静态复刻图 / 干净可交互图 carry none.)

Each block is the `expression` you evaluate in the browser (wrapped in
`(function(){var g=window.ggbApplet; … })()`). After each: screenshot, then POST-save.

---

## Fig 1 — 静态复刻图 (faithful still; constrained, print-identical)
Circle + helper lines are built (to enforce the conditions) then **hidden**. The
original's own angle ticks are ∠EAC (at A) and ∠EBF (at B). Drivers are fixed so the
still stays put.
```js
g.reset(); g.setAxesVisible(false,false); g.setGridVisible(false);
['A=(1.76,3.76)','B=(0,0)','C=(4.6,0)',        // drivers @ MEASURED coords
 'c=Circle(A,B,C)',                             // encodes ∠ADB=∠ACB (D concyclic) — hidden
 'D=Point(c)','gg=Line(B,C)','lAD=Line(A,D)',   // helper lines — hidden
 'E=Intersect(lAD,gg)',                         // E = AD ∩ BC
 'F=Reflect(D,gg)',                             // fold: F = reflection of D over BC
 'sAB=Segment(A,B)','sBC=Segment(B,C)','sCA=Segment(C,A)','sAD=Segment(A,D)',
 'sBD=Segment(B,D)','sBF=Segment(B,F)','sFE=Segment(F,E)','sFC=Segment(F,C)',
 'aEAC=Angle(E,A,C)','aEBF=Angle(E,B,F)'].forEach(c=>g.evalCommand(c));  // ORIGINAL ticks (equal angles)
g.evalCommand('SetCoords(D,2.21,-1.38)');       // measured D (already lies on c)
['A','B','C','D','E','F'].forEach(p=>{g.setColor(p,0,0,0);g.setPointSize(p,4);});
['sAB','sBC','sCA','sAD','sBD','sBF','sFE','sFC'].forEach(s=>{g.setColor(s,0,0,0);g.setLineThickness(s,2);g.setLabelVisible(s,false);});
['aEAC','aEBF'].forEach(a=>{g.setColor(a,0,0,0);g.setLabelVisible(a,false);g.evalCommand('SetFilling('+a+',0)');}); // arcs, no fill/label
// verification scaffolding: confirm concyclic angles equal, then DELETE
g.evalCommand('vADB=Angle(A,D,B)'); g.evalCommand('vACB=Angle(A,C,B)');   // read: g.getValue('vADB') ≈ g.getValue('vACB')
['vADB','vACB'].forEach(n=>g.evalCommand('Delete('+n+')'));
['c','gg','lAD'].forEach(o=>g.setVisible(o,false));   // hide helpers -> clean, print-like (kept for dependencies)
['A','B','C','D'].forEach(p=>g.evalCommand('SetFixed('+p+',true)'));   // static still (omit this line for the 干净可交互图)
g.setCoordSystem(-2.1,6.7,-2.1,4.5);
```

## Fig 1 — 干净可交互图 (identical look, drivers draggable)
**Exactly the 静态复刻图 block above, minus the `SetFixed` line** — leave A,B,C,D
draggable (D rides the hidden circle `c`, so it stays concyclic; F stays the
reflection). No text, no aids, only the original's marks. Save as `fig1_clean.ggb`.

## Fig 1 — 动态理解图 (same graph + hidden circle shown + live angles + notes on toggle)
```js
g.reset(); g.setAxesVisible(false,false); g.setGridVisible(false);
['A=(1.76,3.76)','B=(0,0)','C=(4.6,0)','c=Circle(A,B,C)','D=Point(c)',
 'gg=Line(B,C)','lAD=Line(A,D)','E=Intersect(lAD,gg)','F=Reflect(D,gg)',
 'sAB=Segment(A,B)','sBC=Segment(B,C)','sCA=Segment(C,A)','sAD=Segment(A,D)','sBD=Segment(B,D)',
 'sBF=Segment(B,F)','sFE=Segment(F,E)','sFC=Segment(F,C)',
 'aEAC=Angle(E,A,C)','aEBF=Angle(E,B,F)',                        // ORIGINAL ticks -> base (always shown)
 'adb=Angle(A,D,B)','acb=Angle(A,C,B)','bfc=Angle(B,F,C)','bac=Angle(B,A,C)'].forEach(c=>g.evalCommand(c));
g.evalCommand('SetCoords(D,2.21,-1.38)');
['A','B','C'].forEach(p=>{g.setColor(p,20,90,220);g.setPointSize(p,5);});
g.setColor('D',220,30,30); g.setPointSize('D',6);      // D = draggable driver
['E','F'].forEach(p=>{g.setColor(p,20,20,20);g.setPointSize(p,4);});
['sAB','sBC','sCA','sAD','sBD','sBF','sFE','sFC'].forEach(s=>{g.setColor(s,30,30,30);g.setLineThickness(s,2);g.setLabelVisible(s,false);});
['aEAC','aEBF'].forEach(a=>{g.setColor(a,0,0,0);g.setLabelVisible(a,false);g.evalCommand('SetFilling('+a+',0)');});
// --- teaching aids (styled, then gated on the 显示辅助 checkbox) ---
g.setColor('c',230,150,0); g.setLineStyle('c',1); g.setLineThickness('c',2); g.setLabelVisible('c',false); // hidden circle REVEALED
['adb','acb'].forEach(a=>{g.setColor(a,0,150,0);g.setLabelStyle(a,2);});     // equal ∠ADB, ∠ACB (values)
g.setColor('bfc',150,80,220); g.setLabelStyle('bfc',2);
g.setColor('bac',20,90,220); g.setLabelStyle('bac',2);
g.evalCommand('t1=Text("\u2220ADB=\u2220ACB \u21d2 A,B,C,D concyclic",(-2.0,4.45))');
g.evalCommand('t2=Text("fold: F=Reflect(D,BC), \u2220BFC=180\u00b0-\u2220BAC",(-2.0,-1.7))');
g.setColor('t1',0,120,0); g.setColor('t2',150,80,220);
// (verify with temp Distance/Angle as in the top snippet, then Delete before saving)
g.evalCommand('showAids=true'); g.evalCommand('SetCaption(showAids,"\u663e\u793a\u8f85\u52a9")');
['c','adb','acb','bfc','bac','t1','t2'].forEach(o=>g.evalCommand('SetConditionToShowObject('+o+',showAids)'));
g.setVisible('lAD',false); g.setVisible('gg',false);
g.setCoordSystem(-2.4,7.0,-2.25,4.75);
```
> Screenshot twice: `显示辅助` on (teaching view) and off (must equal the 静态复刻图 / 干净可交互图).

---

## Fig 2 — 静态复刻图 (part-2 givens; clean; the printed figure has NO angle ticks)
图2 is a 示意图, so honor the exact givens (∠BAC=90°, ∠ACB=30°, BC=8). D concyclic, E
intersection, H midpoint, K spiral similarity — all derived. Only the original's
points/segments show; no circles, no locus, no angle ticks.
```js
g.reset(); g.setAxesVisible(false,false); g.setGridVisible(false);
['A=(2,2*sqrt(3))','B=(0,0)','C=(8,0)',              // realizes ∠BAC=90°, ∠ACB=30°, BC=8
 'c=Circle(A,B,C)','D=Point(c)','gg=Line(B,C)','lAD=Line(A,D)',
 'E=Intersect(lAD,gg)','H=Midpoint(A,C)',            // H on AC (midpoint) — a real dependency
 'rr=Distance(E,B)/Distance(E,A)','th=Angle(Vector(E,B))-Angle(Vector(E,A))',
 'Hd=Dilate(H,rr,E)','K=Rotate(Hd,th,E)',            // △BEK∼△AEH
 'sAB=Segment(A,B)','sBC=Segment(B,C)','sCA=Segment(C,A)','sAD=Segment(A,D)','sBD=Segment(B,D)',
 'sAK=Segment(A,K)','sBK=Segment(B,K)','sEK=Segment(E,K)','sEH=Segment(E,H)'].forEach(c=>g.evalCommand(c));
g.evalCommand('SetCoords(D,4,-4)');                   // D on the arc, matching the drawing's D
['A','B','C','D','E','H','K'].forEach(p=>{g.setColor(p,0,0,0);g.setPointSize(p,4);});
['sAB','sBC','sCA','sAD','sBD','sAK','sBK','sEK','sEH'].forEach(s=>{g.setColor(s,0,0,0);g.setLineThickness(s,2);g.setLabelVisible(s,false);});
// verification scaffolding: confirm givens + answer, then DELETE (read: vBC≈8, vA≈90°, vAK≈1.464, vBK≈2.828)
g.evalCommand('vBC=Distance(B,C)'); g.evalCommand('vA=Angle(B,A,C)'); g.evalCommand('vAK=Distance(A,K)'); g.evalCommand('vBK=Distance(B,K)');
['vBC','vA','vAK','vBK'].forEach(n=>g.evalCommand('Delete('+n+')'));
['c','gg','lAD','rr','th','Hd'].forEach(o=>g.setVisible(o,false));   // hide ALL helpers (no visible circle) -> clean
['A','B','C','D'].forEach(p=>g.evalCommand('SetFixed('+p+',true)'));   // static still (omit for 干净可交互图)
g.setCoordSystem(-1.5,10.5,-5.0,4.0);
```

## Fig 2 — 干净可交互图 (identical look, draggable; no circles/locus/text)
**The 静态复刻图 block above, minus the `SetFixed` line** — leave A,B,C,D draggable.
`c` stays hidden (D still rides it); do NOT build/show the locus. Dragging D moves K
(via the spiral similarity) while ∠BAC=90° etc. hold. Save as `fig2_clean.ggb`.

## Fig 2 — 动态理解图 (circumcircle + K's locus + live AK/BK + notes on toggle)
```js
g.reset(); g.setAxesVisible(false,false); g.setGridVisible(false);
['A=(2,2*sqrt(3))','B=(0,0)','C=(8,0)','c=Circle(A,B,C)','D=Point(c)',
 'gg=Line(B,C)','lAD=Line(A,D)','E=Intersect(lAD,gg)','H=Midpoint(A,C)',
 'rr=Distance(E,B)/Distance(E,A)','th=Angle(Vector(E,B))-Angle(Vector(E,A))',
 'Hd=Dilate(H,rr,E)','K=Rotate(Hd,th,E)','loc=Locus(K,D)',       // second hidden circle (teaching aid)
 'sAB=Segment(A,B)','sBC=Segment(B,C)','sCA=Segment(C,A)','sAD=Segment(A,D)','sBD=Segment(B,D)',
 'sEH=Segment(E,H)','sEK=Segment(E,K)','sAK=Segment(A,K)','sBK=Segment(B,K)',
 'akv=Distance(A,K)','bkv=Distance(B,K)'].forEach(c=>g.evalCommand(c));
g.evalCommand('SetCoords(D,4,-4)');                    // bottom of circumcircle -> K=(2,2)
['A','B','C'].forEach(p=>{g.setColor(p,20,90,220);g.setPointSize(p,5);});
g.setColor('D',220,30,30); g.setPointSize('D',6);
g.setColor('E',20,20,20); g.setColor('H',0,150,0); g.setPointSize('H',5);
g.setColor('K',150,60,220); g.setPointSize('K',6);
['sAB','sBC','sCA','sAD','sBD','sEH','sEK','sAK','sBK'].forEach(s=>{g.setColor(s,60,60,60);g.setLineThickness(s,2);g.setLabelVisible(s,false);}); // original segments (base)
// --- teaching aids: circumcircle, K's locus, live AK/BK readout ---
g.setColor('c',230,150,0); g.setLineStyle('c',1); g.setLineThickness('c',2); g.setLabelVisible('c',false);
g.setColor('loc',150,60,220); g.setLineThickness('loc',3); g.setLabelVisible('loc',false);
g.evalCommand('t1=Text("AK = "+akv+"    BK = "+bkv,(-2.15,4.55))'); g.setColor('t1',20,20,20);
// verify then delete scaffolding: read vBC≈8, vAK≈1.464, vBK≈2.828, then remove
g.evalCommand('vBC=Distance(B,C)'); g.evalCommand('vAK=Distance(A,K)'); g.evalCommand('vBK=Distance(B,K)');
['vBC','vAK','vBK'].forEach(n=>g.evalCommand('Delete('+n+')'));
g.evalCommand('showAids=true'); g.evalCommand('SetCaption(showAids,"\u663e\u793a\u8f85\u52a9")');
['c','loc','t1'].forEach(o=>g.evalCommand('SetConditionToShowObject('+o+',showAids)'));
['rr','th','Hd','akv','bkv','lAD','gg'].forEach(o=>g.setVisible(o,false));
g.setCoordSystem(-2.3,10.3,-4.7,4.7);
```

Verified values: K=(2,2), AK=1.464 (=2√3−2), BK=2.828 (=2√2). The purple `loc` is
the circle (x−2)²+y²=4 — the "second hidden circle" (a teaching aid, on the toggle).

**Drag-test (Stage D):** in the Fig-1 干净可交互图 / 动态理解图, drag D around `c` →
`∠ADB` stays equal to `∠ACB` and `F` stays the reflection; drag A/B/C → whole figure
follows. In Fig 2, drag D → K travels along `loc`. (The 静态复刻图 has drivers fixed,
so it holds still.) If any labelled point does not participate, it was left free by
mistake — rebuild it as a derived object.

**Content check (Stage D):** every `v…` verification object was `Delete`d (none
remain). The 静态复刻图 and 干净可交互图 show only the original's marks — **no visible
circle/locus, no text**. For each 动态理解图, unchecking `显示辅助` must leave exactly
that (same marks, no more no less).
