# Track A cool_frac step 3: knock engine 2 on hot cf0.5/cf0.7 rows (box)

Engine 1 = M03 LW (knock_integral_at_xb90, knock if >=1 per model). Engine 2 = CRECK-tau LW and full CRECK end-gas on the M03-CRN trace (knock_diag.endgas, ranking-validated, absolute +2-2.5 CR offset vs M03 on PRF). D-E LW uses RON 108.7/108.6 (PRF-fit correlation, indicative only for alcohols). Highest CR with each LW < 1 = knock-limited CR. EXECUTED, not validated.

| cf | fuel | w | klCR M03 | klCR CRECK-tau | klCR D-E | full end-gas knock-free up to | rows ok/failed |
|---|---|---|---|---|---|---|---|
| 05 | C2H5OH | 0.0 | 20 | <12 | <12 | none | 9/0 |
| 05 | C2H5OH | 0.55 | 25 | 25 | 25 | 24 | 8/0 |
| 05 | C2H5OH | 0.6 | 25 | 25 | 25 | 24 | 8/0 |
| 05 | CH3OH | 0.0 | 20 | 20 | <12 | 17 | 9/0 |
| 05 | CH3OH | 0.55 | 25 | 25 | 25 | 24 | 8/0 |
| 05 | CH3OH | 0.6 | 25 | 25 | 25 | 24 | 8/0 |
| 07 | C2H5OH | 0.0 | 20 | 13 | <12 | 13 | 9/0 |
| 07 | C2H5OH | 0.55 | 25 | 25 | 25 | 24 | 8/0 |
| 07 | C2H5OH | 0.6 | 25 | 25 | 25 | 24 | 8/0 |
| 07 | CH3OH | 0.0 | 20 | 20 | <12 | 17 | 9/0 |
| 07 | CH3OH | 0.55 | 25 | 25 | 25 | 24 | 8/0 |
| 07 | CH3OH | 0.6 | 25 | 25 | 25 | 24 | 8/0 |
