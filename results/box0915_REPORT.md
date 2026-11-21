# box0915 (Claude job water-engine-box-20261025-0915) - Track A + Track B - STATUS: DONE (EXECUTED + M03-CRN cross-check; NOT validated)
**Reconcile (Track A, results/track_a_reconcile on PR 9):** the earlier +1-2 pp water-majority gains were UNCOUPLED (dual-temp rerun ran Module 03 without the retained-liquid/film coupling). Coupled (PR #8, CR 24, w 0.6): every water-majority case loses to best dry or is not SPEC-eligible, normal and hot, both bounds, both engines (normal -0.7 to -8.4 pp; hot -1.7 to -9.8 pp, M03). The hot +2.05 pp also compared 400 K wet vs 320 K dry. This job adds wet rows at their OWN knock-limited CR (below).
**Step 1 (Track B, rig1):** CH3OH hot humid_evap chain from 200 to a 400 cap: stopped at step 235, best w 0.235, +1.618 pp M03 at CR 8; stop = M03-CRN gain not positive. Not capped, so the 500-step continuation was not needed.
**Step 2-3 (Track B, results/track_b/box0915):** gain = wet at own klCR (grid 9-16) vs dry at dry klCR; both engines agree in all 8 rows; all COST GAIN at $0.10/gal.
| chain | LW gain pp (CR dry->wet) | DE gain pp (CR dry->wet) | power % LW/DE | cost/mile % $0.10 LW/DE ($0 LW/DE) |
|---|---|---|---|---|
| C2H5OH hot humid_evap w0.288 | +3.93 (12->16*) | +2.84 (10.5->13) | +29.7/+26.9 | -7.7/-5.4 (-9.2/-7.0) |
| CH3OH hot humid_evap w0.235 | +7.73 (8->16*) | +2.97 (10.5->13) | +37.4/+27.5 | -17.6/-6.8 (-18.1/-7.3) |
| CH3OH normal liquid w0.132 | +1.07 (17->17*) | +2.11 (12.5->15.5) | +8.4/+9.5 | -2.2/-4.7 (-2.5/-5.0) |
| PRF87 normal liquid w0.10 | +0.79 (9->9.5) | +0.79 (9->9.5) | +3.4/+3.4 | -1.9/-1.9 (-2.1/-2.1) |
Gain survives under both knock criteria. *= top of tested CR grid (true klCR may be higher). Gains are mostly from RAISING CR (knock relief by water), and power includes humid_evap charge cooling (T_IVC 400->312 K): indicated upper bounds. The DE row is the conservative number for CH3OH hot (LW dry klCR is only 8).
**Step 4 (Track A, results/track_a_box, best rows, both engines agree unless noted):**
| fuel regime | best row (intake, w, bound, CR) | dpp vs best dry M03/CRN | power % | cost/mile % $0.10 / $0 | verdict |
|---|---|---|---|---|---|
| C2H5OH hot (dry CR 11, 0.3837) | humid_evap 0.5 i CR24 / dryair 0.6 i CR22 | +6.98/+6.93 ; +4.63/+4.61 | +35.1 ; +1.3 | -12.0/-15.4 ; -5.3/-10.8 | COST GAIN |
| CH3OH hot (dry CR 8, 0.3495) | humid_evap 0.6 i CR24 / dryair 0.5 i CR14 | +7.85/+7.80 ; +5.45/+5.41 | +34.8 ; +0.9 | -16.1/-18.4 ; -11.9/-13.5 | COST GAIN |
| C2H5OH normal (dry CR 24, 0.4455) | humid_evap 0.5 i CR24 | +0.35/+0.32 | +1.6 | +3.25 / -0.77 | water cost eats it; stay dry at $0.10 |
| CH3OH normal (dry CR 16, 0.4207) | humid_evap 0.5 i CR24 (1 engine: CRN failed) | +2.15/- | +3.7 | -3.1/-4.9 | 1 engine only; no 2-engine power-ok row -> stay dry |
Normal-regime dryair rows: all power loss, misfire flag Y (port wall 363 K). Hot-regime w 0.7 and 24/60 best rows: M03-CRN Cantera integrator failed (recorded, not re-run) -> 1 engine. Cost-optimal w at equal-or-better power: C2H5OH hot w0.5, CH3OH hot w0.6 (humid_evap, bound i); normal: w 0.
**Step 5 (Track A port wall, w 0.5 bound i dryair):** Module 11 misfire flag flips OFF at 369-374 K (CH3OH) and 374-378 K (C2H5OH), depending on SMD 200-500 um (1 K scan, misfire_flip.csv): ON at 363 K, OFF at 388 K for every fuel and regime; at 375 K C2H5OH is still ON for SMD 350/500.
**Runtimes (CPU-h):** Track B B2/B4 1.35, rig1 chain extension ~1.0 (3573 s); Track A sims 1.20 (+18 dry low-CR points added in the report pass, 10 s) + M03-CRN 1.85.
