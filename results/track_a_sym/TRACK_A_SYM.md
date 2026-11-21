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
| CH3OH | normal | w 0.55 @ klCR | 24 | 360 | 290.9 | 0.4362 | 0.4358 | -1.64 / -1.67 | -4.95 | +6.06 / +3.75 | +6.14 | agree | power loss / power loss |
| CH3OH | normal | w 0.55 @ best eta | 24 | 360 | 290.9 | 0.4362 | 0.4358 | -1.64 / -1.67 | -4.95 | +6.06 / +3.75 | +6.14 | agree | power loss / power loss |
| CH3OH | normal | w 0.6 @ klCR | 24 | 360 | 290.9 | 0.4231 | 0.4228 | -2.95 / -2.98 | -7.80 | +9.89 / +6.96 | +9.97 | agree | power loss / power loss |
| CH3OH | normal | w 0.6 @ best eta | 24 | 360 | 290.9 | 0.4231 | 0.4228 | -2.95 / -2.98 | -7.80 | +9.89 / +6.96 | +9.97 | agree | power loss / power loss |
| CH3OH | normal | w 0.7 @ klCR | 24 | 360 | 290.9 | 0.3794 | - | -7.32 / - | -17.34 | +24.38 / +19.30 | - | CRN failed (wet) | power loss (1 engine) / power loss (1 engine) |
| CH3OH | normal | w 0.7 @ best eta | 24 | 360 | 290.9 | 0.3794 | - | -7.32 / - | -17.34 | +24.38 / +19.30 | - | CRN failed (wet) | power loss (1 engine) / power loss (1 engine) |
| C2H5OH | normal | DEI dry baseline | 28 | 360 | 294.0 | 0.4664 | 0.4661 | - / - | - | - / - | - | - | - / - |
| C2H5OH | normal | w 0.55 @ klCR | 23 | 360 | 293.8 | 0.4423 | 0.4418 | -2.41 / -2.43 | -5.72 | +10.68 / +5.45 | +10.74 | agree | power loss / power loss |
| C2H5OH | normal | w 0.55 @ best eta | 23 | 360 | 293.8 | 0.4423 | 0.4418 | -2.41 / -2.43 | -5.72 | +10.68 / +5.45 | +10.74 | agree | power loss / power loss |
| C2H5OH | normal | w 0.6 @ klCR | 23 | 360 | 293.8 | 0.4316 | 0.4311 | -3.48 / -3.50 | -8.00 | +14.63 / +8.06 | +14.69 | agree | power loss / power loss |
| C2H5OH | normal | w 0.6 @ best eta | 23 | 360 | 293.8 | 0.4316 | 0.4311 | -3.48 / -3.50 | -8.00 | +14.63 / +8.06 | +14.69 | agree | power loss / power loss |
| C2H5OH | normal | w 0.7 @ klCR | 23 | 360 | 293.8 | 0.3959 | 0.3955 | -7.05 / -7.06 | -15.61 | +28.95 / +17.80 | +28.99 | agree | power loss / power loss |
| C2H5OH | normal | w 0.7 @ best eta | 23 | 360 | 293.8 | 0.3959 | 0.3955 | -7.05 / -7.06 | -15.61 | +28.95 / +17.80 | +28.99 | agree | power loss / power loss |
| CH3OH | hot | DEI dry baseline | 20 | 400 | 291.1 | 0.4574 | 0.4574 | - / - | - | - / - | - | - | - / - |
| CH3OH | hot | w 0.55 @ klCR | 23 | 400 | 290.9 | 0.4451 | 0.4447 | -1.23 / -1.27 | -4.09 | +5.05 / +2.76 | +5.14 | agree | power loss / power loss |
| CH3OH | hot | w 0.55 @ best eta | 23 | 400 | 290.9 | 0.4451 | 0.4447 | -1.23 / -1.27 | -4.09 | +5.05 / +2.76 | +5.14 | agree | power loss / power loss |
| CH3OH | hot | w 0.6 @ klCR | 23 | 400 | 290.9 | 0.4323 | 0.4319 | -2.51 / -2.55 | -6.86 | +8.71 / +5.82 | +8.80 | agree | power loss / power loss |
| CH3OH | hot | w 0.6 @ best eta | 23 | 400 | 290.9 | 0.4323 | 0.4319 | -2.51 / -2.55 | -6.86 | +8.71 / +5.82 | +8.80 | agree | power loss / power loss |
| CH3OH | hot | w 0.7 @ klCR | 23 | 400 | 290.9 | 0.3892 | - | -6.82 / - | -16.14 | +22.53 / +17.52 | - | CRN failed (wet) | power loss (1 engine) / power loss (1 engine) |
| CH3OH | hot | w 0.7 @ best eta | 23 | 400 | 290.9 | 0.3892 | - | -6.82 / - | -16.14 | +22.53 / +17.52 | - | CRN failed (wet) | power loss (1 engine) / power loss (1 engine) |
| C2H5OH | hot | DEI dry baseline | 26 | 400 | 304.1 | 0.4680 | 0.4678 | - / - | - | - / - | - | - | - / - |
| C2H5OH | hot | w 0.55 @ klCR | 23 | 400 | 293.8 | 0.4521 | 0.4516 | -1.59 / -1.61 | -0.94 | +8.64 / +3.51 | +8.70 | agree | power loss / power loss |
| C2H5OH | hot | w 0.55 @ best eta | 23 | 400 | 293.8 | 0.4521 | 0.4516 | -1.59 / -1.61 | -0.94 | +8.64 / +3.51 | +8.70 | agree | power loss / power loss |
| C2H5OH | hot | w 0.6 @ klCR | 23 | 400 | 293.8 | 0.4415 | 0.4410 | -2.65 / -2.67 | -3.26 | +12.44 / +5.99 | +12.51 | agree | power loss / power loss |
| C2H5OH | hot | w 0.6 @ best eta | 23 | 400 | 293.8 | 0.4415 | 0.4410 | -2.65 / -2.67 | -3.26 | +12.44 / +5.99 | +12.51 | agree | power loss / power loss |
| C2H5OH | hot | w 0.7 @ klCR | 23 | 400 | 293.8 | 0.4059 | 0.4055 | -6.21 / -6.23 | -11.07 | +26.21 / +15.30 | +26.27 | agree | power loss / power loss |
| C2H5OH | hot | w 0.7 @ best eta | 23 | 400 | 293.8 | 0.4059 | 0.4055 | -6.21 / -6.23 | -11.07 | +26.21 / +15.30 | +26.27 | agree | power loss / power loss |
