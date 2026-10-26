# water-engine-box-20261026-0040 - dryevap verdict robustness (R-WE-11, R-WE-13)
| cool frac | A CH3O n | A CH3O h | A C2H5 n | A C2H5 h | B PRF87 n | B PRF87 h | B CH3OH n | B CH3OH h | failed |
|---|---|---|---|---|---|---|---|---|---|
| 1.0 | -1.64/-1.67 | -1.23/-1.27 | -2.41/-2.43 | -1.59/-1.61 | fail | fail | fail | fail | 0 |
| 0.7 | missing | missing | missing | missing | fail | fail | fail | fail | 4 |
| 0.5 | missing | missing | missing | missing | fail | fail | fail | fail | 4 |
Step 1 verdict: Track A ordering (DEI dry beats water-majority w 0.55/0.6, best wet-minus-dry pp M03/CRN at klCR) UNDETERMINED (rows missing) at 70 % and 50 % cooling (Track B cells = best gain over w 0.05-0.20, l=liquid h=humid_evap).
| S_L case | PRF87 n stop w / gain pp M03/CRN | PRF91 n | PRF97 n | PRF87 h | PRF91 h | PRF97 h |
|---|---|---|---|---|---|---|
Step 2 verdict: NO measured WE-45 numbers (equations not machine-readable) -> +10/+20 % dilution-bias BRACKET only, not a measured bias; stop-w shift vs fit +0.000..+0.000 (0.01 grid estimate; humid_evap rows in CSV; * = grid points failed); sym chains complete.
Runtimes: step 1 ?, step 2 ? (box, 3 cores). Failed rows: cf 0.7: 4, cf 0.5: 4. Executed, cross-checked (Module 03 + M03-CRN), not validated. Track A + Track B; normal = 450 K wall, ~90 C coolant; hot = 520 K wall / 400 K intake.
STATUS: FAILED
