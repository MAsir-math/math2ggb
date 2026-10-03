# math2ggb

馬Sir教室｜用 [Math2GGB](https://github.com/GordenSun/Math2GGB) 做的圓周角示範。三份 `.ggb` 都是瀏覽器裡的真 GeoGebra applet 呼叫 `getBase64()` 匯出，不是手寫 `geogebra.xml` 再壓成 zip。

## 題目

圖中，AB 是圓 O 的直徑，C 在圓周上，且 ∠BAC = 35°。(a) 求 ∠ACB。(b) 若把 C 沿圓周移動（AB 仍為直徑），∠ACB 有何不變？

這是自擬題，不是舊卷。沒有印刷原圖可描點，所以圖按給定條件建成：AB 為直徑、C 在圓周上、起始時 ∠BAC = 35°。

(a) ∠ACB = 90°（直徑所對的圓周角是直角）。(b) C 沿圓周移動、且不與 A、B 重合時，∠ACB 仍是 90°。

## 三份檔

| 檔案 | 作用 |
| --- | --- |
| `examples/diameter_angle_static.ggb` | 靜態復刻。圓 O、直徑 AB、圓周點 C、∠BAC = 35°。A、B、C 都固定。 |
| `examples/diameter_angle_clean.ggb` | 可拖動。畫面與靜態復刻相同。C 是圓上的點，只能沿圓周移動；A、B 固定，O 是 AB 中點，所以 AB 仍是直徑。 |
| `examples/diameter_angle_dynamic.ggb` | 動態理解。同一作圖，另加「顯示輔助」核取方塊，**預設關閉**。打開才顯示直角 ∠ACB，以及「直徑所對的圓周角是直角」的說明。關掉之後回到原來的圖。 |

三份都用同一組約束：`O = Midpoint(A,B)`，`c = Circle(O,A)`，`C = Point(c)`。C 的起始位置是過 A、與 AB 成 35° 的射線和圓的另一個交點。

GeoGebra 的 `Angle` 是有向角，C 拖到另一側時可能量到 270° 而不是三角形內的 90°。檔案只顯示不大於 180° 的那一個角標，所以上下半圓看到的都是內角。

## 怎樣用真 applet 產出

Skill 整份放在 `.cursor/skills/math2ggb/`（上游 `GordenSun/Math2GGB`，commit `bf86d3895a662dcd135a137149a9b0975f8ae419`），沒有改上游 repo。

1. `python3 .cursor/skills/math2ggb/scripts/ggb_server.py examples 8777`
2. 瀏覽器打開 `http://localhost:8777/generator.html`。頁面載入 `https://www.geogebra.org/apps/deployggb.js`（perspective `AG`）。
3. 用 applet 的 `evalCommand` 作圖，再 `POST /save?name=….ggb`，body 是 `ggbApplet.getBase64()`。

伺服器把 base64 解碼寫成 `examples/*.ggb`。每個檔都是 zip，內有引擎寫出的 `geogebra.xml`（GeoGebra Classic 5.4）。曾把動態檔 `setBase64` 載回同一個 applet：`C` 仍是 `Point on c`，∠BAC = 35°，「顯示輔助」為關閉，直角與說明文字隱藏。

## 開啟

在 GeoGebra Classic 或 [geogebra.org/classic](https://www.geogebra.org/classic) 開啟。macOS App Store 版若雙擊出現空白，請用選單「打開 → 從這部裝置」選檔，或把檔案拖進 GeoGebra 視窗。

## 限制

真 applet 的 `getBase64()` 有成功，所以沒有用手寫 XML 充數。沒有印刷原圖，因此這是按 35° 和直徑條件畫的示意圖，不是對舊卷掃圖描點。
