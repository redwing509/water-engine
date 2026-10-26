# Track A - symmetric DEI water-majority sweep (box, Oct 25 2026)

Status: **EXECUTED, numerically cross-checked (Module 03 + M03-CRN, same toolchain), NOT validated.**
All rows DEI (fuel evaporated in the intake, dew-point capped) for dry AND wet; humid_evap bound (i); normal = 450 K wall / 363 K port wall / T_in 360 K (~90 C coolant); hot = 520 K / 388 K / 400 K. CR grid 9-30 (wet), 6-30 (dry). Cost vs the fuel's DEI dry baseline from this sweep (sims/cost prices 2026-10-25; $0.10/gal water headline, $0 secondary). 'COST GAIN' only if power >= baseline AND cost lower in both engines.

## DEI dry baseline check vs results/dryevap/baselines.csv

* CH3OH normal: sweep DEI rule CR 21 T_in 360.0 eta 0.45259 vs baselines.csv CR 21 T_in 360.0 eta 0.45259 (diff +0.00e+00)
* C2H5OH normal: sweep DEI rule CR 28 T_in 360.0 eta 0.46637 vs baselines.csv CR 20 T_in 360.0 eta 0.45116 (diff +1.52e-02)
* CH3OH hot: sweep DEI rule CR 20 T_in 400.0 eta 0.45741 vs baselines.csv CR 20 T_in 400.0 eta 0.45741 (diff +0.00e+00)
* C2H5OH hot: sweep DEI rule CR 26 T_in 400.0 eta 0.46797 vs baselines.csv CR 24 T_in 400.0 eta 0.46438 (diff +3.59e-03)

## Rows

| fuel | regime | row | CR | T_in K | T_IVC K | eta M03 | eta CRN | gain pp M03 / CRN | power % | cost/mile % $0.10 / $0 (M03) | CRN cost/mile % | engines | verdict ($0.10 / $0) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CH3OH | normal | DEI dry baseline | 21 | 360 | 291.1 | 0.4526 | 0.4525 | - / - | - | - / - | - | - | - / - |
| CH3OH | normal | w 0.51 @ klCR | 24 | 360 | 290.9 | 0.4445 | 0.4441 | -0.81 / -0.84 | -3.14 | +3.75 / +1.81 | +3.83 | agree | power loss / power loss |
| CH3OH | normal | w 0.51 @ best eta | 24 | 360 | 290.9 | 0.4445 | 0.4441 | -0.81 / -0.84 | -3.14 | +3.75 / +1.81 | +3.83 | agree | power loss / power loss |
| CH3OH | normal | w 0.52 @ klCR | 24 | 360 | 290.9 | 0.4426 | 0.4422 | -1.00 / -1.03 | -3.56 | +4.28 / +2.26 | +4.36 | agree | power loss / power loss |
| CH3OH | normal | w 0.52 @ best eta | 24 | 360 | 290.9 | 0.4426 | 0.4422 | -1.00 / -1.03 | -3.56 | +4.28 / +2.26 | +4.36 | agree | power loss / power loss |
| C2H5OH | normal | DEI dry baseline | 28 | 360 | 294.0 | 0.4664 | 0.4661 | - / - | - | - / - | - | - | - / - |
| C2H5OH | normal | w 0.51 @ klCR | 23 | 360 | 293.8 | 0.4490 | 0.4485 | -1.74 / -1.76 | -4.29 | +8.25 / +3.87 | +8.31 | agree | power loss / power loss |
| C2H5OH | normal | w 0.51 @ best eta | 23 | 360 | 293.8 | 0.4490 | 0.4485 | -1.74 / -1.76 | -4.29 | +8.25 / +3.87 | +8.31 | agree | power loss / power loss |
| C2H5OH | normal | w 0.52 @ klCR | 23 | 360 | 293.8 | 0.4474 | 0.4470 | -1.89 / -1.92 | -4.62 | +8.81 / +4.23 | +8.87 | agree | power loss / power loss |
| C2H5OH | normal | w 0.52 @ best eta | 23 | 360 | 293.8 | 0.4474 | 0.4470 | -1.89 / -1.92 | -4.62 | +8.81 / +4.23 | +8.87 | agree | power loss / power loss |
| CH3OH | hot | DEI dry baseline | 20 | 400 | 291.1 | 0.4574 | 0.4574 | - / - | - | - / - | - | - | - / - |
| CH3OH | hot | w 0.51 @ klCR | 23 | 400 | 290.9 | 0.4533 | 0.4528 | -0.42 / -0.45 | -2.34 | +2.83 / +0.92 | +2.92 | agree | power loss / power loss |
| CH3OH | hot | w 0.51 @ best eta | 23 | 400 | 290.9 | 0.4533 | 0.4528 | -0.42 / -0.45 | -2.34 | +2.83 / +0.92 | +2.92 | agree | power loss / power loss |
| CH3OH | hot | w 0.52 @ klCR | 23 | 400 | 290.9 | 0.4514 | 0.4509 | -0.60 / -0.64 | -2.75 | +3.34 / +1.34 | +3.43 | agree | power loss / power loss |
| CH3OH | hot | w 0.52 @ best eta | 23 | 400 | 290.9 | 0.4514 | 0.4509 | -0.60 / -0.64 | -2.75 | +3.34 / +1.34 | +3.43 | agree | power loss / power loss |
| C2H5OH | hot | DEI dry baseline | 26 | 400 | 304.1 | 0.4680 | 0.4678 | - / - | - | - / - | - | - | - / - |
| C2H5OH | hot | w 0.51 @ klCR | 23 | 400 | 293.8 | 0.4588 | 0.4583 | -0.92 / -0.94 | +0.53 | +6.30 / +2.00 | +6.36 | agree | no cost gain / no cost gain |
| C2H5OH | hot | w 0.51 @ best eta | 23 | 400 | 293.8 | 0.4588 | 0.4583 | -0.92 / -0.94 | +0.53 | +6.30 / +2.00 | +6.36 | agree | no cost gain / no cost gain |
| C2H5OH | hot | w 0.52 @ klCR | 23 | 400 | 293.8 | 0.4573 | 0.4568 | -1.07 / -1.10 | +0.19 | +6.84 / +2.34 | +6.90 | agree | no cost gain / no cost gain |
| C2H5OH | hot | w 0.52 @ best eta | 23 | 400 | 293.8 | 0.4573 | 0.4568 | -1.07 / -1.10 | +0.19 | +6.84 / +2.34 | +6.90 | agree | no cost gain / no cost gain |
