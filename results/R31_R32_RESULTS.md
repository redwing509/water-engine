# R31+R32 rescore: every COST GAIN case

> **Model arithmetic only, not experimentally validated.** These numbers come from a 0-D engine-cycle cost rescore of the completed R31+R32 campaign (R32 finished 12:40 PM Pacific Time on 10 Nov 2026). They have not been validated against experiment and are not engine performance claims. The factory compression ratio is withheld and is not published here.

A row is listed when the best-cost wet case has **lower cost per mile than its own dry baseline** at **equal-or-better power** (verdict COST GAIN; cost change < -0.01 % and power change >= -0.01 %). Each wet case is compared only to a dry baseline from the same group: same fuel, climate regime, bore and stroke, rpm, and intake mode. Cost uses the project's existing cost model (dated retail fuel prices, water at $0.10/gal). "Hot" = high-performance regime (coolant 388 K, intake 400 K); "normal" = coolant 363 K, intake 320 K. `w` = water mass fraction of the liquid intake. Intake modes are `liquid`, `humid_evap`, and `humid_ambient`.

Source: complete R31+R32 rescore, 10 Nov 2026. R31 supplied 19,800 computed rows (792 groups, 25 points each). R32 added 15,840 computed midpoint rows (792 groups, 20 points each). All scored rows have status `computed`. There were no duplicate keys inside a stage. Machine-readable copy: [`r31_r32_cost_gain.csv`](r31_r32_cost_gain.csv).

## Headline result

Best modelled cost per mile after the complete rescore: **-9.728 %** (PRF91, normal, 86 x 107.5 mm, 1500 rpm, `humid_evap` and `liquid` tied; dry CR 8 -> wet CR 12, w 0.30, power +10.16 %).

| fuel | regime | bore x stroke | rpm | mode | dry -> wet CR (w) | cost/mile % | power % | cost/mile % before R32 midpoints |
|---|---|---|---|---|---|---|---|---|
| PRF91 | normal | 86x107.5 | 1500 | humid_evap | 8 -> 12 (0.3) | -9.728 | 10.16 | -9.728 |
| PRF91 | normal | 86x107.5 | 1500 | liquid | 8 -> 12 (0.3) | -9.728 | 10.16 | -9.728 |
| PRF91 | normal | 105x105 | 1500 | liquid | 8 -> 12 (0.3) | -9.717 | 10.15 | -9.717 |
| PRF91 | normal | 105x105 | 1500 | humid_evap | 8 -> 12 (0.3) | -9.717 | 10.15 | -9.717 |
| PRF87 | hot | 86x107.5 | 1500 | liquid | 6 -> 8 (0.3) | -9.715 | 13.03 | -13.572 |
| PRF87 | hot | 105x105 | 1500 | liquid | 6 -> 8 (0.3) | -9.709 | 13.02 | -13.590 |
| PRF87 | hot | 105x84 | 1500 | liquid | 6 -> 8 (0.3) | -9.691 | 13.00 | -13.343 |
| PRF87 | hot | 86x68.8 | 1500 | liquid | 6 -> 8 (0.3) | -9.642 | 12.94 | -13.037 |
| PRF87 | hot | 65x65 | 1500 | liquid | 6 -> 8 (0.3) | -9.626 | 12.92 | -12.886 |
| PRF91 | normal | 105x84 | 1500 | humid_evap | 8 -> 12 (0.3) | -9.558 | 9.95 | -9.558 |
| PRF91 | normal | 105x84 | 1500 | liquid | 8 -> 12 (0.3) | -9.558 | 9.95 | -9.558 |
| PRF91 | normal | 65x65 | 1500 | humid_evap | 8 -> 12 (0.3) | -9.340 | 9.69 | -9.340 |

## Baseline shift

An earlier partial R31+R32 figure of about 16.7 % was an artifact of missing compression-ratio-6 dry baseline rows. R32 added 108 eligible CR-6 dry rows, including one per intake mode for every PRF87 hot 1500 rpm geometry. Those dry rows have higher efficiency than the previous CR-5 dry baselines, so they became the comparison point and the apparent gain shrank.

For PRF87 hot, 86 x 107.5 mm, 1500 rpm, liquid: the result moved from **-13.572 %** (dry CR 5 -> 7, w 0.30) to **-9.715 %** (dry CR 6 -> 8, w 0.30). A reconstruction that removes the R32 CR-6 dry rows recovers **-16.652 %** for that group, which supports the mechanism. That -16.652 % figure is a reconstruction, not a re-opening of the original partial file. PRF91 normal baselines did not shift, because R31 already had CR-6 dry rows for those groups.

## Group counts

- R31 groups: 792; groups with R32 midpoint rows: 792
- Cost-gain before vs after adding R32 midpoints: kept 432, lost 7, new 1, none 352
- COST GAIN cases after the complete rescore: 433
- Of those 433, 23 use a dry baseline that was not marked eligible (the scorer falls back to the best available dry point when no eligible dry point exists). All 23 are E10 or E85, hot, 1500 rpm. They are included in the full list and flagged in the CSV; none is the headline best.
- 14 groups could not be scored (no usable dry/wet pair) and are omitted.

## Sanity check

An independent Hermes recompute of the top-12 table, the headline figures, and the group counts confirmed the official result (verdict: CONFIRMS). A controller recheck matched the scoring table to the thousandth. Both reviews agree the comparisons are like-for-like (same climate, fuel prices, and duty cycle within each group), that only computed rows were used, and that there was no double-counting. This remains model arithmetic, not experimental validation. The factory compression ratio stays withheld.

The earlier 1 Nov 2026 geometry-study screening (328 COST GAIN rows) is unchanged in [`SCREENING_RESULTS.md`](SCREENING_RESULTS.md). Its headline of -12.35 % (PRF87 hot, 1000 rpm, 105 x 131 mm, dry CR 5 -> 7) was not re-run in this campaign, which did not include 1000 rpm or that geometry, and still carries the weak dry-baseline caveat already noted there.

## PRF91 (72 rows)

| regime | rpm | bore x stroke mm | mode | water w | CR dry -> wet | power % | cost/mile % | cost/mile % before | notes |
|---|---|---|---|---|---|---|---|---|---|
| normal | 1500 | 86x107.5 | humid_evap | 0.3 | 8 -> 12 | 10.16 | -9.728 | -9.728 | — |
| normal | 1500 | 86x107.5 | liquid | 0.3 | 8 -> 12 | 10.16 | -9.728 | -9.728 | — |
| normal | 1500 | 105x105 | liquid | 0.3 | 8 -> 12 | 10.15 | -9.717 | -9.717 | — |
| normal | 1500 | 105x105 | humid_evap | 0.3 | 8 -> 12 | 10.15 | -9.717 | -9.717 | — |
| normal | 1500 | 105x84 | humid_evap | 0.3 | 8 -> 12 | 9.95 | -9.558 | -9.558 | — |
| normal | 1500 | 105x84 | liquid | 0.3 | 8 -> 12 | 9.95 | -9.558 | -9.558 | — |
| normal | 1500 | 65x65 | humid_evap | 0.3 | 8 -> 12 | 9.69 | -9.340 | -9.340 | — |
| normal | 1500 | 65x65 | liquid | 0.3 | 8 -> 12 | 9.69 | -9.340 | -9.340 | — |
| hot | 1500 | 105x105 | liquid | 0.3 | 7 -> 9 | 11.87 | -7.643 | -10.301 | — |
| hot | 1500 | 86x107.5 | liquid | 0.3 | 7 -> 9 | 11.85 | -7.624 | -10.301 | — |
| hot | 1500 | 105x84 | liquid | 0.3 | 7 -> 9 | 11.79 | -7.577 | -10.138 | — |
| hot | 1500 | 86x68.8 | liquid | 0.3 | 7 -> 9 | 11.68 | -7.483 | -9.893 | — |
| normal | 1500 | 86x68.8 | humid_evap | 0.3 | 9 -> 12 | 9.19 | -7.478 | -9.379 | — |
| normal | 1500 | 86x68.8 | liquid | 0.3 | 9 -> 12 | 9.19 | -7.478 | -9.379 | — |
| hot | 1500 | 65x65 | liquid | 0.3 | 7 -> 9 | 11.64 | -7.452 | -9.786 | — |
| hot | 1500 | 65x52 | liquid | 0.3 | 7 -> 9 | 11.51 | -7.344 | -9.492 | — |
| normal | 2500 | 105x105 | liquid | 0.3 | 11 -> 14 | 9.52 | -6.870 | -7.816 | — |
| normal | 2500 | 105x105 | humid_evap | 0.3 | 11 -> 14 | 9.52 | -6.870 | -7.816 | — |
| normal | 2500 | 86x107.5 | humid_evap | 0.3 | 11 -> 14 | 9.49 | -6.848 | -7.813 | — |
| normal | 2500 | 86x107.5 | liquid | 0.3 | 11 -> 14 | 9.49 | -6.848 | -7.813 | — |
| normal | 1500 | 65x52 | humid_evap | 0.3 | 9 -> 12 | 8.44 | -6.838 | -9.071 | — |
| normal | 1500 | 65x52 | liquid | 0.3 | 9 -> 12 | 8.44 | -6.838 | -9.071 | — |
| normal | 2500 | 105x84 | humid_evap | 0.3 | 11 -> 14 | 9.25 | -6.639 | -7.650 | — |
| normal | 2500 | 105x84 | liquid | 0.3 | 11 -> 14 | 9.25 | -6.639 | -7.650 | — |
| normal | 2500 | 86x68.8 | humid_evap | 0.3 | 11 -> 14 | 8.88 | -6.328 | -7.442 | — |
| normal | 2500 | 86x68.8 | liquid | 0.3 | 11 -> 14 | 8.88 | -6.328 | -7.442 | — |
| normal | 2500 | 65x65 | liquid | 0.3 | 11 -> 14 | 8.69 | -6.164 | -7.355 | — |
| normal | 2500 | 65x65 | humid_evap | 0.3 | 11 -> 14 | 8.69 | -6.164 | -7.355 | — |
| hot | 2500 | 105x105 | liquid | 0.3 | 9 -> 11 | 11.61 | -6.128 | -6.758 | — |
| hot | 2500 | 86x107.5 | liquid | 0.3 | 9 -> 11 | 11.57 | -6.093 | -6.759 | — |
| hot | 2500 | 105x84 | liquid | 0.3 | 9 -> 11 | 11.52 | -6.048 | -6.706 | — |
| hot | 2500 | 86x68.8 | liquid | 0.3 | 9 -> 11 | 11.36 | -5.917 | -6.649 | — |
| hot | 2500 | 65x65 | liquid | 0.3 | 9 -> 11 | 11.27 | -5.837 | -6.646 | — |
| normal | 2500 | 65x52 | humid_evap | 0.3 | 11 -> 14 | 8.23 | -5.764 | -7.075 | — |
| normal | 2500 | 65x52 | liquid | 0.3 | 11 -> 14 | 8.23 | -5.764 | -7.075 | — |
| hot | 2500 | 65x52 | liquid | 0.3 | 9 -> 11 | 11.10 | -5.697 | -6.516 | — |
| hot | 4000 | 105x105 | liquid | 0.3 | 11 -> 14 | 11.08 | -5.564 | -6.455 | — |
| hot | 4000 | 105x84 | liquid | 0.3 | 11 -> 14 | 11.05 | -5.532 | -6.484 | — |
| hot | 4000 | 86x107.5 | liquid | 0.3 | 11 -> 14 | 11.04 | -5.530 | -6.445 | — |
| hot | 4000 | 86x68.8 | liquid | 0.3 | 11 -> 14 | 10.97 | -5.465 | -6.519 | — |
| hot | 1500 | 105x105 | humid_evap | 0.3 | 7 -> 8 | 18.71 | -5.444 | -10.020 | — |
| hot | 1500 | 86x107.5 | humid_evap | 0.3 | 7 -> 8 | 18.69 | -5.424 | -10.029 | — |
| hot | 4000 | 65x65 | liquid | 0.3 | 11 -> 14 | 10.91 | -5.414 | -6.549 | — |
| hot | 1500 | 105x84 | humid_evap | 0.3 | 7 -> 8 | 18.67 | -5.409 | -10.032 | — |
| hot | 4000 | 65x52 | liquid | 0.3 | 11 -> 14 | 10.84 | -5.356 | -6.602 | — |
| hot | 1500 | 86x68.8 | humid_evap | 0.3 | 7 -> 8 | 18.60 | -5.356 | -10.027 | — |
| hot | 1500 | 65x65 | humid_evap | 0.3 | 7 -> 8 | 18.59 | -5.349 | -10.042 | — |
| hot | 1500 | 65x52 | humid_evap | 0.3 | 7 -> 8 | 18.52 | -5.292 | -9.928 | — |
| hot | 2500 | 105x105 | humid_evap | 0.3 | 9 -> 10 | 18.48 | -4.481 | -6.240 | — |
| hot | 2500 | 86x107.5 | humid_evap | 0.3 | 9 -> 10 | 18.44 | -4.446 | -6.246 | — |
| hot | 2500 | 105x84 | humid_evap | 0.3 | 9 -> 10 | 18.44 | -4.445 | -6.316 | — |
| hot | 2500 | 86x68.8 | humid_evap | 0.3 | 9 -> 10 | 18.34 | -4.368 | -6.429 | — |
| hot | 4000 | 105x84 | humid_evap | 0.3 | 11 -> 13 | 17.98 | -4.342 | -4.784 | — |
| hot | 4000 | 86x68.8 | humid_evap | 0.3 | 11 -> 13 | 17.96 | -4.329 | -4.817 | — |
| hot | 4000 | 105x105 | humid_evap | 0.3 | 11 -> 13 | 17.96 | -4.329 | -4.756 | — |
| hot | 4000 | 65x52 | humid_evap | 0.3 | 11 -> 13 | 17.95 | -4.324 | -4.898 | — |
| hot | 2500 | 65x65 | humid_evap | 0.3 | 9 -> 10 | 18.28 | -4.318 | -6.525 | — |
| hot | 4000 | 65x65 | humid_evap | 0.3 | 11 -> 13 | 17.93 | -4.307 | -4.846 | — |
| hot | 4000 | 86x107.5 | humid_evap | 0.3 | 11 -> 13 | 17.91 | -4.291 | -4.744 | — |
| hot | 2500 | 65x52 | humid_evap | 0.3 | 9 -> 10 | 18.20 | -4.250 | -6.619 | — |
| normal | 4000 | 105x105 | liquid | 0.3 | 13 -> 14 | 7.76 | -3.896 | -4.590 | — |
| normal | 4000 | 105x105 | humid_evap | 0.3 | 13 -> 14 | 7.76 | -3.896 | -4.590 | — |
| normal | 4000 | 86x107.5 | humid_evap | 0.3 | 13 -> 14 | 7.74 | -3.880 | -4.587 | — |
| normal | 4000 | 86x107.5 | liquid | 0.3 | 13 -> 14 | 7.74 | -3.880 | -4.587 | — |
| normal | 4000 | 105x84 | humid_evap | 0.3 | 13 -> 14 | 7.42 | -3.587 | -4.328 | — |
| normal | 4000 | 105x84 | liquid | 0.3 | 13 -> 14 | 7.42 | -3.587 | -4.328 | — |
| normal | 4000 | 86x68.8 | liquid | 0.26 | 13 -> 14 | 6.89 | -3.233 | -4.046 | — |
| normal | 4000 | 86x68.8 | humid_evap | 0.26 | 13 -> 14 | 6.89 | -3.233 | -4.046 | — |
| normal | 4000 | 65x65 | liquid | 0.3 | 13 -> 14 | 6.84 | -3.065 | -3.931 | — |
| normal | 4000 | 65x65 | humid_evap | 0.3 | 13 -> 14 | 6.84 | -3.065 | -3.931 | — |
| normal | 4000 | 65x52 | humid_evap | 0.3 | 13 -> 14 | 6.46 | -2.720 | -3.669 | — |
| normal | 4000 | 65x52 | liquid | 0.3 | 13 -> 14 | 6.46 | -2.720 | -3.669 | — |

## PRF87 (74 rows)

| regime | rpm | bore x stroke mm | mode | water w | CR dry -> wet | power % | cost/mile % | cost/mile % before | notes |
|---|---|---|---|---|---|---|---|---|---|
| hot | 1500 | 86x107.5 | liquid | 0.3 | 6 -> 8 | 13.03 | -9.715 | -13.572 | — |
| hot | 1500 | 105x105 | liquid | 0.3 | 6 -> 8 | 13.02 | -9.709 | -13.590 | — |
| hot | 1500 | 105x84 | liquid | 0.3 | 6 -> 8 | 13.00 | -9.691 | -13.343 | — |
| hot | 1500 | 86x68.8 | liquid | 0.3 | 6 -> 8 | 12.94 | -9.642 | -13.037 | — |
| hot | 1500 | 65x65 | liquid | 0.3 | 6 -> 8 | 12.92 | -9.626 | -12.886 | — |
| hot | 1500 | 65x65 | humid_evap | 0.3 | 6 -> 8 | 20.36 | -9.326 | -13.329 | — |
| hot | 1500 | 86x68.8 | humid_evap | 0.3 | 6 -> 8 | 20.23 | -9.228 | -13.453 | — |
| hot | 1500 | 105x84 | humid_evap | 0.3 | 6 -> 8 | 20.05 | -9.090 | -13.708 | — |
| hot | 1500 | 105x105 | humid_evap | 0.3 | 6 -> 8 | 19.89 | -8.968 | -13.881 | — |
| normal | 1500 | 105x105 | humid_evap | 0.3 | 8 -> 11 | 10.06 | -8.913 | -11.736 | — |
| normal | 1500 | 105x105 | liquid | 0.3 | 8 -> 11 | 10.06 | -8.913 | -11.736 | — |
| normal | 1500 | 86x107.5 | humid_evap | 0.3 | 8 -> 11 | 10.05 | -8.900 | -11.759 | — |
| normal | 1500 | 86x107.5 | liquid | 0.3 | 8 -> 11 | 10.05 | -8.900 | -11.759 | — |
| normal | 1500 | 105x84 | humid_evap | 0.3 | 8 -> 11 | 9.77 | -8.674 | -11.635 | — |
| normal | 1500 | 105x84 | liquid | 0.3 | 8 -> 11 | 9.77 | -8.674 | -11.635 | — |
| normal | 1500 | 86x68.8 | liquid | 0.3 | 8 -> 11 | 9.40 | -8.364 | -11.486 | — |
| normal | 1500 | 86x68.8 | humid_evap | 0.3 | 8 -> 11 | 9.40 | -8.364 | -11.486 | — |
| normal | 1500 | 65x65 | humid_evap | 0.3 | 8 -> 11 | 9.23 | -8.221 | -11.432 | — |
| normal | 1500 | 65x65 | liquid | 0.3 | 8 -> 11 | 9.23 | -8.221 | -11.432 | — |
| normal | 1500 | 65x52 | liquid | 0.3 | 8 -> 11 | 8.75 | -7.815 | -11.086 | — |
| normal | 1500 | 65x52 | humid_evap | 0.3 | 8 -> 11 | 8.75 | -7.815 | -11.086 | — |
| normal | 2500 | 105x105 | liquid | 0.3 | 10 -> 13 | 9.65 | -7.380 | -8.769 | — |
| normal | 2500 | 105x105 | humid_evap | 0.3 | 10 -> 13 | 9.65 | -7.380 | -8.769 | — |
| normal | 2500 | 86x107.5 | humid_evap | 0.3 | 10 -> 13 | 9.63 | -7.362 | -8.773 | — |
| normal | 2500 | 86x107.5 | liquid | 0.3 | 10 -> 13 | 9.63 | -7.362 | -8.773 | — |
| normal | 2500 | 105x84 | liquid | 0.3 | 10 -> 13 | 9.40 | -7.169 | -8.637 | — |
| normal | 2500 | 105x84 | humid_evap | 0.3 | 10 -> 13 | 9.40 | -7.169 | -8.637 | — |
| normal | 2500 | 86x68.8 | liquid | 0.3 | 10 -> 13 | 9.07 | -6.888 | -8.479 | — |
| normal | 2500 | 86x68.8 | humid_evap | 0.3 | 10 -> 13 | 9.07 | -6.888 | -8.479 | — |
| normal | 2500 | 65x65 | liquid | 0.3 | 10 -> 13 | 8.90 | -6.743 | -8.428 | — |
| normal | 2500 | 65x65 | humid_evap | 0.3 | 10 -> 13 | 8.90 | -6.743 | -8.428 | — |
| hot | 2500 | 105x105 | liquid | 0.3 | 8 -> 10 | 11.71 | -6.740 | -8.522 | — |
| hot | 2500 | 86x107.5 | liquid | 0.3 | 8 -> 10 | 11.68 | -6.718 | -8.523 | — |
| hot | 1500 | 86x107.5 | humid_evap | 0.3 | 6 -> 7 | 19.41 | -6.700 | -13.868 | — |
| hot | 2500 | 105x84 | liquid | 0.3 | 8 -> 10 | 11.63 | -6.679 | -8.419 | — |
| hot | 2500 | 86x68.8 | liquid | 0.3 | 8 -> 10 | 11.52 | -6.586 | -8.265 | — |
| hot | 2500 | 65x65 | liquid | 0.3 | 8 -> 10 | 11.46 | -6.537 | -8.193 | — |
| hot | 2500 | 65x52 | liquid | 0.3 | 8 -> 10 | 11.34 | -6.432 | -7.982 | — |
| normal | 2500 | 65x52 | liquid | 0.3 | 10 -> 13 | 8.47 | -6.379 | -8.209 | — |
| normal | 2500 | 65x52 | humid_evap | 0.3 | 10 -> 13 | 8.47 | -6.379 | -8.209 | — |
| hot | 2500 | 65x52 | humid_evap | 0.3 | 8 -> 10 | 18.59 | -6.055 | -8.291 | — |
| hot | 4000 | 105x105 | liquid | 0.3 | 10 -> 13 | 11.19 | -6.036 | -7.507 | — |
| hot | 4000 | 105x84 | liquid | 0.3 | 10 -> 13 | 11.16 | -6.016 | -7.565 | — |
| hot | 4000 | 86x107.5 | liquid | 0.3 | 10 -> 13 | 11.15 | -6.008 | -7.506 | — |
| hot | 2500 | 65x65 | humid_evap | 0.3 | 8 -> 10 | 18.50 | -5.979 | -8.323 | — |
| hot | 4000 | 86x68.8 | liquid | 0.3 | 10 -> 13 | 11.10 | -5.968 | -7.645 | — |
| hot | 2500 | 86x68.8 | humid_evap | 0.3 | 8 -> 10 | 18.46 | -5.950 | -8.296 | — |
| hot | 4000 | 65x65 | liquid | 0.3 | 10 -> 13 | 11.06 | -5.932 | -7.710 | — |
| hot | 2500 | 105x84 | humid_evap | 0.3 | 8 -> 10 | 18.41 | -5.908 | -8.270 | — |
| hot | 4000 | 65x52 | liquid | 0.3 | 10 -> 13 | 11.02 | -5.894 | -7.807 | — |
| hot | 2500 | 105x105 | humid_evap | 0.3 | 8 -> 10 | 18.35 | -5.863 | -8.236 | — |
| hot | 1500 | 65x52 | liquid | 0.3 | 7 -> 8 | 11.12 | -5.538 | -1.900 | — |
| hot | 1500 | 65x52 | humid_evap | 0.3 | 7 -> 8 | 18.76 | -5.478 | -2.425 | — |
| hot | 2500 | 86x107.5 | humid_evap | 0.3 | 8 -> 9 | 18.42 | -4.739 | -8.239 | — |
| hot | 4000 | 65x52 | humid_evap | 0.3 | 10 -> 12 | 18.09 | -4.727 | -5.772 | — |
| hot | 4000 | 105x84 | humid_evap | 0.3 | 10 -> 12 | 18.07 | -4.711 | -5.561 | — |
| hot | 4000 | 86x68.8 | humid_evap | 0.3 | 10 -> 12 | 18.07 | -4.710 | -5.631 | — |
| hot | 4000 | 65x65 | humid_evap | 0.3 | 10 -> 12 | 18.06 | -4.698 | -5.688 | — |
| hot | 4000 | 105x105 | humid_evap | 0.3 | 10 -> 12 | 18.05 | -4.692 | -5.511 | — |
| hot | 4000 | 86x107.5 | humid_evap | 0.3 | 10 -> 12 | 18.01 | -4.659 | -5.510 | — |
| normal | 4000 | 105x105 | humid_evap | 0.3 | 12 -> 13 | 7.73 | -3.988 | -4.904 | — |
| normal | 4000 | 105x105 | liquid | 0.3 | 12 -> 13 | 7.73 | -3.988 | -4.904 | — |
| normal | 4000 | 86x107.5 | liquid | 0.3 | 12 -> 13 | 7.72 | -3.976 | -4.907 | — |
| normal | 4000 | 86x107.5 | humid_evap | 0.3 | 12 -> 13 | 7.72 | -3.976 | -4.907 | — |
| hot | 1500 | 65x65 | humid_ambient | 0.1 | 6 -> 7 | 0.18 | -3.924 | -10.855 | — |
| hot | 1500 | 86x68.8 | humid_ambient | 0.1 | 6 -> 7 | 0.02 | -3.763 | -10.833 | — |
| normal | 4000 | 105x84 | humid_evap | 0.3 | 12 -> 13 | 7.41 | -3.703 | -4.672 | — |
| normal | 4000 | 105x84 | liquid | 0.3 | 12 -> 13 | 7.41 | -3.703 | -4.672 | — |
| normal | 4000 | 86x68.8 | humid_evap | 0.26 | 12 -> 13 | 6.93 | -3.385 | -4.432 | — |
| normal | 4000 | 86x68.8 | liquid | 0.26 | 12 -> 13 | 6.93 | -3.385 | -4.432 | — |
| normal | 4000 | 65x65 | liquid | 0.3 | 12 -> 13 | 6.88 | -3.224 | -4.328 | — |
| normal | 4000 | 65x65 | humid_evap | 0.3 | 12 -> 13 | 6.88 | -3.224 | -4.328 | — |
| normal | 4000 | 65x52 | liquid | 0.3 | 13 -> 13 | 6.57 | -2.263 | -2.263 | — |
| normal | 4000 | 65x52 | humid_evap | 0.3 | 13 -> 13 | 6.57 | -2.263 | -2.263 | — |

## E85 (72 rows)

| regime | rpm | bore x stroke mm | mode | water w | CR dry -> wet | power % | cost/mile % | cost/mile % before | notes |
|---|---|---|---|---|---|---|---|---|---|
| hot | 1500 | 86x107.5 | liquid | 0.3 | 12 -> 17 | 14.95 | -9.212 | -8.766 | dry baseline not marked eligible |
| hot | 1500 | 86x107.5 | humid_evap | 0.3 | 12 -> 17 | 14.95 | -9.212 | -8.766 | dry baseline not marked eligible |
| hot | 1500 | 105x105 | humid_evap | 0.3 | 12 -> 17 | 14.94 | -9.208 | -8.754 | dry baseline not marked eligible |
| hot | 1500 | 105x105 | liquid | 0.3 | 12 -> 17 | 14.94 | -9.208 | -8.754 | dry baseline not marked eligible |
| hot | 1500 | 105x84 | liquid | 0.3 | 12 -> 17 | 14.40 | -8.778 | -8.241 | dry baseline not marked eligible |
| hot | 1500 | 105x84 | humid_evap | 0.3 | 12 -> 17 | 14.40 | -8.778 | -8.241 | dry baseline not marked eligible |
| hot | 2500 | 86x107.5 | liquid | 0.3 | 13 -> 20 | 13.78 | -8.500 | -9.243 | — |
| hot | 2500 | 86x107.5 | humid_evap | 0.3 | 13 -> 20 | 13.78 | -8.500 | -9.243 | — |
| hot | 2500 | 105x105 | liquid | 0.3 | 13 -> 20 | 13.78 | -8.497 | -9.235 | — |
| hot | 2500 | 105x105 | humid_evap | 0.3 | 13 -> 20 | 13.78 | -8.497 | -9.235 | — |
| hot | 2500 | 105x84 | humid_evap | 0.3 | 13 -> 20 | 13.46 | -8.238 | -9.057 | — |
| hot | 2500 | 105x84 | liquid | 0.3 | 13 -> 20 | 13.46 | -8.238 | -9.057 | — |
| hot | 1500 | 86x68.8 | liquid | 0.3 | 13 -> 17 | 14.48 | -8.202 | -7.611 | dry baseline not marked eligible |
| hot | 1500 | 86x68.8 | humid_evap | 0.3 | 13 -> 17 | 14.48 | -8.202 | -7.611 | dry baseline not marked eligible |
| hot | 1500 | 65x65 | humid_evap | 0.3 | 13 -> 17 | 14.15 | -7.937 | -7.357 | dry baseline not marked eligible |
| hot | 1500 | 65x65 | liquid | 0.3 | 13 -> 17 | 14.15 | -7.937 | -7.357 | dry baseline not marked eligible |
| hot | 2500 | 86x68.8 | humid_evap | 0.3 | 13 -> 20 | 13.07 | -7.926 | -8.857 | — |
| hot | 2500 | 86x68.8 | liquid | 0.3 | 13 -> 20 | 13.07 | -7.926 | -8.857 | — |
| hot | 2500 | 65x65 | humid_evap | 0.3 | 13 -> 20 | 12.94 | -7.814 | -8.811 | — |
| hot | 2500 | 65x65 | liquid | 0.3 | 13 -> 20 | 12.94 | -7.814 | -8.811 | — |
| normal | 1500 | 86x107.5 | humid_evap | 0.3 | 12 -> 19 | 4.64 | -7.644 | -7.266 | — |
| normal | 1500 | 86x107.5 | liquid | 0.3 | 12 -> 19 | 4.64 | -7.644 | -7.266 | — |
| normal | 1500 | 105x105 | liquid | 0.3 | 12 -> 19 | 4.62 | -7.629 | -7.255 | — |
| normal | 1500 | 105x105 | humid_evap | 0.3 | 12 -> 19 | 4.62 | -7.629 | -7.255 | — |
| normal | 1500 | 105x84 | humid_evap | 0.3 | 12 -> 19 | 4.17 | -7.225 | -6.776 | — |
| normal | 1500 | 105x84 | liquid | 0.3 | 12 -> 19 | 4.17 | -7.225 | -6.776 | — |
| hot | 1500 | 65x52 | humid_evap | 0.3 | 13 -> 17 | 13.13 | -7.108 | -6.628 | dry baseline not marked eligible |
| hot | 1500 | 65x52 | liquid | 0.3 | 13 -> 17 | 13.13 | -7.108 | -6.628 | dry baseline not marked eligible |
| hot | 2500 | 65x52 | liquid | 0.3 | 14 -> 20 | 12.34 | -6.768 | -6.768 | — |
| hot | 2500 | 65x52 | humid_evap | 0.3 | 14 -> 20 | 12.34 | -6.768 | -6.768 | — |
| normal | 1500 | 86x68.8 | liquid | 0.3 | 12 -> 19 | 3.62 | -6.738 | -6.189 | — |
| normal | 1500 | 86x68.8 | humid_evap | 0.3 | 12 -> 19 | 3.62 | -6.738 | -6.189 | — |
| normal | 1500 | 65x65 | humid_evap | 0.3 | 12 -> 19 | 3.42 | -6.552 | -5.995 | — |
| normal | 1500 | 65x65 | liquid | 0.3 | 12 -> 19 | 3.42 | -6.552 | -5.995 | — |
| hot | 4000 | 86x107.5 | humid_evap | 0.3 | 17 -> 20 | 12.86 | -5.942 | -6.049 | — |
| hot | 4000 | 86x107.5 | liquid | 0.3 | 17 -> 20 | 12.86 | -5.942 | -6.049 | — |
| hot | 4000 | 105x105 | humid_evap | 0.3 | 17 -> 20 | 12.82 | -5.911 | -6.020 | — |
| hot | 4000 | 105x105 | liquid | 0.3 | 17 -> 20 | 12.82 | -5.911 | -6.020 | — |
| normal | 2500 | 105x105 | liquid | 0.3 | 15 -> 20 | 3.99 | -5.642 | -6.043 | — |
| normal | 2500 | 105x105 | humid_evap | 0.3 | 15 -> 20 | 3.99 | -5.642 | -6.043 | — |
| normal | 2500 | 86x107.5 | liquid | 0.3 | 15 -> 20 | 3.99 | -5.641 | -6.053 | — |
| normal | 2500 | 86x107.5 | humid_evap | 0.3 | 15 -> 20 | 3.99 | -5.641 | -6.053 | — |
| normal | 1500 | 65x52 | liquid | 0.3 | 12 -> 18 | 2.58 | -5.499 | -5.499 | — |
| normal | 1500 | 65x52 | humid_evap | 0.3 | 12 -> 18 | 2.58 | -5.499 | -5.499 | — |
| hot | 4000 | 105x84 | liquid | 0.3 | 17 -> 20 | 12.29 | -5.464 | -5.615 | — |
| hot | 4000 | 105x84 | humid_evap | 0.3 | 17 -> 20 | 12.29 | -5.464 | -5.615 | — |
| normal | 2500 | 105x84 | liquid | 0.3 | 15 -> 20 | 3.46 | -5.155 | -5.616 | — |
| normal | 2500 | 105x84 | humid_evap | 0.3 | 15 -> 20 | 3.46 | -5.155 | -5.616 | — |
| hot | 4000 | 86x68.8 | humid_evap | 0.3 | 17 -> 20 | 11.73 | -4.991 | -5.199 | — |
| hot | 4000 | 86x68.8 | liquid | 0.3 | 17 -> 20 | 11.73 | -4.991 | -5.199 | — |
| hot | 4000 | 65x65 | humid_evap | 0.3 | 17 -> 20 | 11.54 | -4.825 | -5.062 | — |
| hot | 4000 | 65x65 | liquid | 0.3 | 17 -> 20 | 11.54 | -4.825 | -5.062 | — |
| normal | 2500 | 86x68.8 | humid_evap | 0.3 | 15 -> 20 | 2.82 | -4.565 | -5.115 | — |
| normal | 2500 | 86x68.8 | liquid | 0.3 | 15 -> 20 | 2.82 | -4.565 | -5.115 | — |
| normal | 2500 | 65x65 | humid_evap | 0.3 | 15 -> 20 | 2.58 | -4.344 | -4.953 | — |
| normal | 2500 | 65x65 | liquid | 0.3 | 15 -> 20 | 2.58 | -4.344 | -4.953 | — |
| hot | 4000 | 65x52 | humid_evap | 0.3 | 17 -> 20 | 10.96 | -4.332 | -4.644 | — |
| hot | 4000 | 65x52 | liquid | 0.3 | 17 -> 20 | 10.96 | -4.332 | -4.644 | — |
| normal | 2500 | 65x52 | liquid | 0.3 | 15 -> 20 | 2.03 | -3.827 | -4.544 | — |
| normal | 2500 | 65x52 | humid_evap | 0.3 | 15 -> 20 | 2.03 | -3.827 | -4.544 | — |
| normal | 4000 | 105x105 | humid_evap | 0.26 | 19 -> 20 | 2.47 | -2.969 | -3.016 | — |
| normal | 4000 | 105x105 | liquid | 0.26 | 19 -> 20 | 2.47 | -2.969 | -3.016 | — |
| normal | 4000 | 86x107.5 | liquid | 0.26 | 19 -> 20 | 2.45 | -2.953 | -3.004 | — |
| normal | 4000 | 86x107.5 | humid_evap | 0.26 | 19 -> 20 | 2.45 | -2.953 | -3.004 | — |
| normal | 4000 | 105x84 | liquid | 0.26 | 19 -> 20 | 2.00 | -2.526 | -2.611 | — |
| normal | 4000 | 105x84 | humid_evap | 0.26 | 19 -> 20 | 2.00 | -2.526 | -2.611 | — |
| normal | 4000 | 86x68.8 | liquid | 0.26 | 19 -> 20 | 1.48 | -2.025 | -2.162 | — |
| normal | 4000 | 86x68.8 | humid_evap | 0.26 | 19 -> 20 | 1.48 | -2.025 | -2.162 | — |
| normal | 4000 | 65x65 | humid_evap | 0.26 | 19 -> 20 | 1.25 | -1.805 | -1.974 | — |
| normal | 4000 | 65x65 | liquid | 0.26 | 19 -> 20 | 1.25 | -1.805 | -1.974 | — |
| normal | 4000 | 65x52 | humid_evap | 0.26 | 19 -> 20 | 0.78 | -1.340 | -1.576 | — |
| normal | 4000 | 65x52 | liquid | 0.26 | 19 -> 20 | 0.78 | -1.340 | -1.576 | — |

## E10 (71 rows)

| regime | rpm | bore x stroke mm | mode | water w | CR dry -> wet | power % | cost/mile % | cost/mile % before | notes |
|---|---|---|---|---|---|---|---|---|---|
| normal | 1500 | 86x107.5 | humid_evap | 0.3 | 9 -> 13.5 | 9.23 | -9.119 | -7.615 | — |
| normal | 1500 | 86x107.5 | liquid | 0.3 | 9 -> 13.5 | 9.23 | -9.119 | -7.615 | — |
| normal | 1500 | 105x105 | liquid | 0.3 | 9 -> 13.5 | 9.22 | -9.110 | -7.616 | — |
| normal | 1500 | 105x105 | humid_evap | 0.3 | 9 -> 13.5 | 9.22 | -9.110 | -7.616 | — |
| normal | 1500 | 105x84 | humid_evap | 0.3 | 9 -> 13.5 | 8.94 | -8.872 | -7.229 | — |
| normal | 1500 | 105x84 | liquid | 0.3 | 9 -> 13.5 | 8.94 | -8.872 | -7.229 | — |
| normal | 1500 | 86x68.8 | humid_evap | 0.3 | 9 -> 13.5 | 8.60 | -8.590 | -6.798 | — |
| normal | 1500 | 86x68.8 | liquid | 0.3 | 9 -> 13.5 | 8.60 | -8.590 | -6.798 | — |
| normal | 1500 | 65x65 | humid_evap | 0.3 | 9 -> 13.5 | 8.49 | -8.498 | -6.673 | — |
| normal | 1500 | 65x65 | liquid | 0.3 | 9 -> 13.5 | 8.49 | -8.498 | -6.673 | — |
| normal | 1500 | 65x52 | humid_evap | 0.3 | 9 -> 13.5 | 8.04 | -8.116 | -6.361 | — |
| normal | 1500 | 65x52 | liquid | 0.3 | 9 -> 13.5 | 8.04 | -8.116 | -6.361 | — |
| normal | 2500 | 105x84 | humid_evap | 0.3 | 12 -> 18 | 8.54 | -7.533 | -7.533 | — |
| normal | 2500 | 105x84 | liquid | 0.3 | 12 -> 18 | 8.54 | -7.533 | -7.533 | — |
| normal | 2500 | 105x105 | liquid | 0.3 | 12 -> 17 | 8.82 | -7.448 | -7.031 | — |
| normal | 2500 | 105x105 | humid_evap | 0.3 | 12 -> 17 | 8.82 | -7.448 | -7.031 | — |
| normal | 2500 | 86x107.5 | liquid | 0.3 | 12 -> 17 | 8.81 | -7.437 | -7.019 | — |
| normal | 2500 | 86x107.5 | humid_evap | 0.3 | 12 -> 17 | 8.81 | -7.437 | -7.019 | — |
| normal | 2500 | 86x68.8 | liquid | 0.3 | 12 -> 18 | 8.29 | -7.319 | -7.319 | — |
| normal | 2500 | 86x68.8 | humid_evap | 0.3 | 12 -> 18 | 8.29 | -7.319 | -7.319 | — |
| normal | 2500 | 65x65 | liquid | 0.3 | 12 -> 18 | 8.18 | -7.225 | -7.225 | — |
| normal | 2500 | 65x65 | humid_evap | 0.3 | 12 -> 18 | 8.18 | -7.225 | -7.225 | — |
| hot | 2500 | 105x105 | liquid | 0.3 | 9 -> 12 | 12.19 | -7.010 | -7.010 | — |
| hot | 2500 | 86x107.5 | liquid | 0.3 | 9 -> 12 | 12.18 | -7.005 | -7.005 | — |
| hot | 2500 | 105x84 | liquid | 0.3 | 9 -> 12 | 12.16 | -6.989 | -6.989 | — |
| hot | 2500 | 65x65 | liquid | 0.3 | 9 -> 12 | 12.15 | -6.982 | -6.982 | — |
| hot | 2500 | 86x68.8 | liquid | 0.3 | 9 -> 12 | 12.14 | -6.966 | -6.966 | — |
| hot | 2500 | 65x52 | liquid | 0.3 | 9 -> 12 | 12.12 | -6.954 | -6.954 | — |
| normal | 2500 | 65x52 | humid_evap | 0.3 | 12 -> 18 | 7.86 | -6.950 | -6.950 | — |
| normal | 2500 | 65x52 | liquid | 0.3 | 12 -> 18 | 7.86 | -6.950 | -6.950 | — |
| normal | 4000 | 105x105 | liquid | 0.3 | 15 -> 18 | 8.36 | -5.695 | -5.695 | — |
| normal | 4000 | 105x105 | humid_evap | 0.3 | 15 -> 18 | 8.36 | -5.695 | -5.695 | — |
| normal | 4000 | 86x107.5 | humid_evap | 0.3 | 15 -> 18 | 8.34 | -5.680 | -5.680 | — |
| normal | 4000 | 86x107.5 | liquid | 0.3 | 15 -> 18 | 8.34 | -5.680 | -5.680 | — |
| hot | 4000 | 105x84 | liquid | 0.3 | 12 -> 16 | 11.36 | -5.536 | -5.536 | — |
| hot | 4000 | 105x105 | liquid | 0.3 | 12 -> 15.5 | 11.57 | -5.512 | -5.411 | — |
| hot | 4000 | 86x68.8 | liquid | 0.3 | 12 -> 16 | 11.30 | -5.489 | -5.489 | — |
| hot | 4000 | 86x107.5 | liquid | 0.3 | 12 -> 15.5 | 11.54 | -5.482 | -5.383 | — |
| normal | 4000 | 105x84 | liquid | 0.3 | 15 -> 18 | 8.06 | -5.429 | -5.429 | — |
| normal | 4000 | 105x84 | humid_evap | 0.3 | 15 -> 18 | 8.06 | -5.429 | -5.429 | — |
| hot | 4000 | 65x52 | liquid | 0.3 | 12 -> 16 | 11.23 | -5.424 | -5.424 | — |
| hot | 4000 | 65x65 | liquid | 0.3 | 12 -> 15.5 | 11.39 | -5.359 | -5.199 | — |
| normal | 4000 | 86x68.8 | liquid | 0.3 | 15 -> 18 | 7.66 | -5.080 | -5.080 | — |
| normal | 4000 | 86x68.8 | humid_evap | 0.3 | 15 -> 18 | 7.66 | -5.080 | -5.080 | — |
| hot | 2500 | 65x52 | humid_evap | 0.3 | 9 -> 10.5 | 19.57 | -5.035 | -1.458 | — |
| hot | 2500 | 65x65 | humid_evap | 0.3 | 9 -> 10.5 | 19.57 | -5.032 | -1.417 | — |
| hot | 2500 | 86x68.8 | humid_evap | 0.3 | 9 -> 10.5 | 19.53 | -4.999 | -1.376 | — |
| hot | 2500 | 105x105 | humid_evap | 0.3 | 9 -> 10.5 | 19.53 | -4.998 | -1.479 | — |
| hot | 2500 | 86x107.5 | humid_evap | 0.3 | 9 -> 10.5 | 19.52 | -4.995 | -1.494 | — |
| hot | 2500 | 105x84 | humid_evap | 0.3 | 9 -> 10.5 | 19.52 | -4.995 | -1.406 | — |
| normal | 4000 | 65x65 | humid_evap | 0.3 | 15 -> 18 | 7.45 | -4.896 | -4.896 | — |
| normal | 4000 | 65x65 | liquid | 0.3 | 15 -> 18 | 7.45 | -4.896 | -4.896 | — |
| normal | 4000 | 65x52 | humid_evap | 0.3 | 15 -> 18 | 6.93 | -4.436 | -4.436 | — |
| normal | 4000 | 65x52 | liquid | 0.3 | 15 -> 18 | 6.93 | -4.436 | -4.436 | — |
| hot | 4000 | 105x105 | humid_evap | 0.3 | 12 -> 13.5 | 19.23 | -4.033 | -2.731 | — |
| hot | 4000 | 105x84 | humid_evap | 0.3 | 12 -> 13.5 | 19.21 | -4.013 | -2.615 | — |
| hot | 4000 | 86x107.5 | humid_evap | 0.3 | 12 -> 13.5 | 19.20 | -4.004 | -2.707 | — |
| hot | 4000 | 86x68.8 | humid_evap | 0.3 | 12 -> 13.5 | 19.14 | -3.961 | -2.444 | — |
| hot | 4000 | 65x65 | humid_evap | 0.3 | 12 -> 13.5 | 19.10 | -3.925 | -2.348 | — |
| hot | 4000 | 65x52 | humid_evap | 0.3 | 12 -> 13.5 | 19.05 | -3.886 | -2.143 | — |
| hot | 1500 | 105x105 | liquid | 0.3 | 18 -> 9 | 16.30 | -1.711 | -1.711 | dry baseline not marked eligible |
| hot | 1500 | 86x107.5 | liquid | 0.3 | 18 -> 9 | 16.06 | -1.510 | -1.510 | dry baseline not marked eligible |
| hot | 1500 | 105x84 | liquid | 0.3 | 18 -> 9 | 15.97 | -1.430 | -1.430 | dry baseline not marked eligible |
| hot | 1500 | 105x105 | humid_evap | 0.3 | 18 -> 9 | 24.43 | -1.306 | -1.306 | dry baseline not marked eligible |
| hot | 1500 | 105x84 | humid_evap | 0.3 | 18 -> 9 | 24.33 | -1.229 | -1.229 | dry baseline not marked eligible |
| hot | 1500 | 86x107.5 | humid_evap | 0.3 | 18 -> 9 | 24.19 | -1.115 | -1.115 | dry baseline not marked eligible |
| hot | 1500 | 86x68.8 | humid_evap | 0.3 | 18 -> 9 | 23.97 | -0.936 | -0.936 | dry baseline not marked eligible |
| hot | 1500 | 86x68.8 | liquid | 0.3 | 18 -> 9 | 15.30 | -0.859 | -0.859 | dry baseline not marked eligible |
| hot | 1500 | 65x65 | humid_evap | 0.3 | 18 -> 9 | 23.57 | -0.618 | -0.618 | dry baseline not marked eligible |
| hot | 1500 | 65x52 | humid_evap | 0.3 | 18 -> 9 | 23.28 | -0.383 | -0.383 | dry baseline not marked eligible |
| hot | 1500 | 65x65 | liquid | 0.3 | 18 -> 9 | 14.74 | -0.380 | -0.380 | dry baseline not marked eligible |

## CH3OH (120 rows)

| regime | rpm | bore x stroke mm | mode | water w | CR dry -> wet | power % | cost/mile % | cost/mile % before | notes |
|---|---|---|---|---|---|---|---|---|---|
| hot | 1500 | 86x107.5 | liquid | 0.3 | 18 -> 32 | 4.82 | -6.981 | -6.981 | — |
| hot | 1500 | 86x107.5 | humid_evap | 0.3 | 18 -> 32 | 4.82 | -6.981 | -6.981 | — |
| hot | 1500 | 105x105 | liquid | 0.3 | 18 -> 32 | 4.60 | -6.788 | -6.788 | — |
| hot | 1500 | 105x105 | humid_evap | 0.3 | 18 -> 32 | 4.60 | -6.788 | -6.788 | — |
| hot | 1500 | 105x84 | humid_evap | 0.3 | 18 -> 32 | 4.16 | -6.399 | -6.399 | — |
| hot | 1500 | 105x84 | liquid | 0.3 | 18 -> 32 | 4.16 | -6.399 | -6.399 | — |
| hot | 2500 | 86x107.5 | humid_evap | 0.3 | 20 -> 32 | 3.95 | -5.651 | -6.478 | — |
| hot | 2500 | 86x107.5 | liquid | 0.3 | 20 -> 32 | 3.95 | -5.651 | -6.478 | — |
| hot | 1500 | 86x68.8 | liquid | 0.3 | 18 -> 29 | 3.63 | -5.605 | -5.605 | — |
| hot | 1500 | 86x68.8 | humid_evap | 0.3 | 18 -> 29 | 3.63 | -5.605 | -5.605 | — |
| normal | 1500 | 86x107.5 | humid_evap | 0.3 | 20 -> 32 | 3.66 | -5.389 | -6.284 | — |
| normal | 1500 | 86x107.5 | liquid | 0.3 | 20 -> 32 | 3.66 | -5.389 | -6.284 | — |
| normal | 1500 | 105x105 | liquid | 0.3 | 20 -> 32 | 3.51 | -5.258 | -6.144 | — |
| normal | 1500 | 105x105 | humid_evap | 0.3 | 20 -> 32 | 3.51 | -5.258 | -6.144 | — |
| hot | 2500 | 105x105 | liquid | 0.3 | 22 -> 32 | 3.72 | -4.997 | -4.997 | — |
| hot | 2500 | 105x105 | humid_evap | 0.3 | 22 -> 32 | 3.72 | -4.997 | -4.997 | — |
| normal | 1500 | 105x84 | humid_evap | 0.3 | 20 -> 32 | 3.09 | -4.865 | -5.861 | — |
| normal | 1500 | 105x84 | liquid | 0.3 | 20 -> 32 | 3.09 | -4.865 | -5.861 | — |
| hot | 2500 | 65x65 | liquid | 0.3 | 22 -> 32 | 3.46 | -4.754 | -4.754 | — |
| hot | 2500 | 65x65 | humid_evap | 0.3 | 22 -> 32 | 3.46 | -4.754 | -4.754 | — |
| hot | 2500 | 105x84 | liquid | 0.3 | 22 -> 32 | 3.45 | -4.741 | -4.741 | — |
| hot | 2500 | 105x84 | humid_evap | 0.3 | 22 -> 32 | 3.45 | -4.741 | -4.741 | — |
| hot | 2500 | 86x68.8 | humid_evap | 0.3 | 22 -> 32 | 3.33 | -4.637 | -4.637 | — |
| hot | 2500 | 86x68.8 | liquid | 0.3 | 22 -> 32 | 3.33 | -4.637 | -4.637 | — |
| hot | 2500 | 65x52 | liquid | 0.3 | 22 -> 32 | 3.11 | -4.428 | -4.428 | — |
| hot | 2500 | 65x52 | humid_evap | 0.3 | 22 -> 32 | 3.11 | -4.428 | -4.428 | — |
| hot | 1500 | 65x65 | liquid | 0.3 | 18 -> 24 | 3.10 | -4.404 | -3.640 | — |
| hot | 1500 | 65x65 | humid_evap | 0.3 | 18 -> 24 | 3.10 | -4.404 | -3.640 | — |
| normal | 2500 | 86x107.5 | humid_evap | 0.3 | 22 -> 32 | 3.03 | -4.356 | -4.356 | — |
| normal | 2500 | 86x107.5 | liquid | 0.3 | 22 -> 32 | 3.03 | -4.356 | -4.356 | — |
| normal | 2500 | 105x105 | humid_evap | 0.3 | 24 -> 32 | 2.97 | -3.924 | -4.212 | — |
| normal | 2500 | 105x105 | liquid | 0.3 | 24 -> 32 | 2.97 | -3.924 | -4.212 | — |
| normal | 1500 | 86x68.8 | humid_evap | 0.3 | 20 -> 27.5 | 2.55 | -3.858 | -4.496 | — |
| normal | 1500 | 86x68.8 | liquid | 0.3 | 20 -> 27.5 | 2.55 | -3.858 | -4.496 | — |
| hot | 4000 | 86x107.5 | liquid | 0.3 | 24 -> 32 | 2.81 | -3.774 | -4.047 | — |
| hot | 4000 | 86x107.5 | humid_evap | 0.3 | 24 -> 32 | 2.81 | -3.774 | -4.047 | — |
| normal | 2500 | 105x84 | humid_evap | 0.3 | 24 -> 32 | 2.72 | -3.691 | -4.045 | — |
| normal | 2500 | 105x84 | liquid | 0.3 | 24 -> 32 | 2.72 | -3.691 | -4.045 | — |
| hot | 4000 | 65x65 | humid_evap | 0.3 | 24 -> 32 | 2.71 | -3.679 | -4.088 | — |
| hot | 4000 | 65x65 | liquid | 0.3 | 24 -> 32 | 2.71 | -3.679 | -4.088 | — |
| normal | 2500 | 65x65 | humid_evap | 0.3 | 24 -> 32 | 2.61 | -3.585 | -4.081 | — |
| normal | 2500 | 65x65 | liquid | 0.3 | 24 -> 32 | 2.61 | -3.585 | -4.081 | — |
| normal | 2500 | 86x68.8 | liquid | 0.3 | 24 -> 32 | 2.56 | -3.541 | -3.985 | — |
| normal | 2500 | 86x68.8 | humid_evap | 0.3 | 24 -> 32 | 2.56 | -3.541 | -3.985 | — |
| hot | 4000 | 105x105 | humid_evap | 0.3 | 24 -> 32 | 2.56 | -3.540 | -3.830 | — |
| hot | 4000 | 105x105 | liquid | 0.3 | 24 -> 32 | 2.56 | -3.540 | -3.830 | — |
| hot | 4000 | 65x52 | liquid | 0.3 | 24 -> 32 | 2.56 | -3.540 | -4.036 | — |
| hot | 4000 | 65x52 | humid_evap | 0.3 | 24 -> 32 | 2.56 | -3.540 | -4.036 | — |
| hot | 4000 | 86x68.8 | liquid | 0.3 | 24 -> 32 | 2.48 | -3.466 | -3.863 | — |
| hot | 4000 | 86x68.8 | humid_evap | 0.3 | 24 -> 32 | 2.48 | -3.466 | -3.863 | — |
| hot | 4000 | 105x84 | liquid | 0.3 | 24 -> 32 | 2.43 | -3.411 | -3.755 | — |
| hot | 4000 | 105x84 | humid_evap | 0.3 | 24 -> 32 | 2.43 | -3.411 | -3.755 | — |
| normal | 2500 | 65x52 | humid_evap | 0.3 | 24 -> 32 | 2.33 | -3.319 | -3.929 | — |
| normal | 2500 | 65x52 | liquid | 0.3 | 24 -> 32 | 2.33 | -3.319 | -3.929 | — |
| normal | 1500 | 65x65 | liquid | 0.3 | 20 -> 24 | 2.29 | -3.080 | -3.338 | — |
| normal | 1500 | 65x65 | humid_evap | 0.3 | 20 -> 24 | 2.29 | -3.080 | -3.338 | — |
| hot | 5000 | 86x107.5 | humid_evap | 0.3 | 26 -> 32 | 2.31 | -2.983 | -2.983 | — |
| hot | 5000 | 86x107.5 | liquid | 0.3 | 26 -> 32 | 2.31 | -2.983 | -2.983 | — |
| hot | 5000 | 65x65 | humid_evap | 0.3 | 26 -> 32 | 2.28 | -2.945 | -2.945 | — |
| hot | 5000 | 65x65 | liquid | 0.3 | 26 -> 32 | 2.28 | -2.945 | -2.945 | — |
| hot | 5000 | 65x52 | liquid | 0.3 | 26 -> 32 | 2.15 | -2.827 | -2.827 | — |
| hot | 5000 | 65x52 | humid_evap | 0.3 | 26 -> 32 | 2.15 | -2.827 | -2.827 | — |
| normal | 4000 | 86x107.5 | liquid | 0.3 | 26 -> 32 | 2.13 | -2.809 | -2.809 | — |
| normal | 4000 | 86x107.5 | humid_evap | 0.3 | 26 -> 32 | 2.13 | -2.809 | -2.809 | — |
| hot | 1500 | 65x52 | liquid | 0.3 | 18 -> 20 | 2.28 | -2.790 | -1.663 | — |
| hot | 1500 | 65x52 | humid_evap | 0.3 | 18 -> 20 | 2.28 | -2.790 | -1.663 | — |
| hot | 5000 | 105x105 | liquid | 0.3 | 26 -> 32 | 2.06 | -2.741 | -2.741 | — |
| hot | 5000 | 105x105 | humid_evap | 0.3 | 26 -> 32 | 2.06 | -2.741 | -2.741 | — |
| normal | 4000 | 65x65 | liquid | 0.3 | 26 -> 32 | 2.03 | -2.716 | -2.716 | — |
| normal | 4000 | 65x65 | humid_evap | 0.3 | 26 -> 32 | 2.03 | -2.716 | -2.716 | — |
| hot | 5000 | 86x68.8 | humid_evap | 0.3 | 26 -> 32 | 2.03 | -2.709 | -2.709 | — |
| hot | 5000 | 86x68.8 | liquid | 0.3 | 26 -> 32 | 2.03 | -2.709 | -2.709 | — |
| normal | 4000 | 105x105 | liquid | 0.3 | 26 -> 32 | 1.98 | -2.660 | -2.660 | — |
| normal | 4000 | 105x105 | humid_evap | 0.3 | 26 -> 32 | 1.98 | -2.660 | -2.660 | — |
| hot | 5000 | 105x84 | liquid | 0.3 | 26 -> 32 | 1.94 | -2.626 | -2.626 | — |
| hot | 5000 | 105x84 | humid_evap | 0.3 | 26 -> 32 | 1.94 | -2.626 | -2.626 | — |
| normal | 4000 | 65x52 | humid_evap | 0.3 | 26 -> 32 | 1.93 | -2.619 | -2.619 | — |
| normal | 4000 | 65x52 | liquid | 0.3 | 26 -> 32 | 1.93 | -2.619 | -2.619 | — |
| normal | 4000 | 86x68.8 | humid_evap | 0.3 | 26 -> 32 | 1.89 | -2.578 | -2.578 | — |
| normal | 4000 | 86x68.8 | liquid | 0.3 | 26 -> 32 | 1.89 | -2.578 | -2.578 | — |
| normal | 4000 | 105x84 | humid_evap | 0.3 | 26 -> 32 | 1.87 | -2.560 | -2.560 | — |
| normal | 4000 | 105x84 | liquid | 0.3 | 26 -> 32 | 1.87 | -2.560 | -2.560 | — |
| hot | 6000 | 65x65 | liquid | 0.3 | 27.5 -> 32 | 1.90 | -2.374 | -2.408 | — |
| hot | 6000 | 65x65 | humid_evap | 0.3 | 27.5 -> 32 | 1.90 | -2.374 | -2.408 | — |
| hot | 6000 | 86x107.5 | humid_evap | 0.3 | 26 -> 32 | 1.63 | -2.326 | -2.326 | — |
| hot | 6000 | 86x107.5 | liquid | 0.3 | 26 -> 32 | 1.63 | -2.326 | -2.326 | — |
| hot | 6000 | 65x52 | liquid | 0.3 | 27.5 -> 32 | 1.79 | -2.271 | -2.356 | — |
| hot | 6000 | 65x52 | humid_evap | 0.3 | 27.5 -> 32 | 1.79 | -2.271 | -2.356 | — |
| hot | 6000 | 86x68.8 | humid_evap | 0.3 | 27.5 -> 32 | 1.63 | -2.119 | -2.151 | — |
| hot | 6000 | 86x68.8 | liquid | 0.3 | 27.5 -> 32 | 1.63 | -2.119 | -2.151 | — |
| normal | 5000 | 86x107.5 | liquid | 0.3 | 27.5 -> 32 | 1.63 | -2.118 | -2.133 | — |
| normal | 5000 | 86x107.5 | humid_evap | 0.3 | 27.5 -> 32 | 1.63 | -2.118 | -2.133 | — |
| normal | 5000 | 65x65 | liquid | 0.3 | 27.5 -> 32 | 1.62 | -2.109 | -2.219 | — |
| normal | 5000 | 65x65 | humid_evap | 0.3 | 27.5 -> 32 | 1.62 | -2.109 | -2.219 | — |
| hot | 6000 | 105x105 | humid_evap | 0.3 | 26 -> 32 | 1.38 | -2.093 | -2.093 | — |
| hot | 6000 | 105x105 | liquid | 0.3 | 26 -> 32 | 1.38 | -2.093 | -2.093 | — |
| normal | 5000 | 65x52 | liquid | 0.3 | 27.5 -> 32 | 1.57 | -2.053 | -2.218 | — |
| normal | 5000 | 65x52 | humid_evap | 0.3 | 27.5 -> 32 | 1.57 | -2.053 | -2.218 | — |
| hot | 6000 | 105x84 | liquid | 0.3 | 27.5 -> 32 | 1.53 | -2.017 | -2.022 | — |
| hot | 6000 | 105x84 | humid_evap | 0.3 | 27.5 -> 32 | 1.53 | -2.017 | -2.022 | — |
| normal | 5000 | 105x105 | liquid | 0.3 | 27.5 -> 32 | 1.48 | -1.969 | -1.985 | — |
| normal | 5000 | 105x105 | humid_evap | 0.3 | 27.5 -> 32 | 1.48 | -1.969 | -1.985 | — |
| normal | 5000 | 86x68.8 | liquid | 0.3 | 27.5 -> 32 | 1.46 | -1.954 | -2.043 | — |
| normal | 5000 | 86x68.8 | humid_evap | 0.3 | 27.5 -> 32 | 1.46 | -1.954 | -2.043 | — |
| normal | 5000 | 105x84 | humid_evap | 0.3 | 27.5 -> 32 | 1.40 | -1.896 | -1.945 | — |
| normal | 5000 | 105x84 | liquid | 0.3 | 27.5 -> 32 | 1.40 | -1.896 | -1.945 | — |
| normal | 6000 | 65x65 | liquid | 0.3 | 29 -> 32 | 1.28 | -1.589 | -1.589 | — |
| normal | 6000 | 65x65 | humid_evap | 0.3 | 29 -> 32 | 1.28 | -1.589 | -1.589 | — |
| normal | 6000 | 65x52 | humid_evap | 0.3 | 29 -> 32 | 1.24 | -1.551 | -1.551 | — |
| normal | 6000 | 65x52 | liquid | 0.3 | 29 -> 32 | 1.24 | -1.551 | -1.551 | — |
| normal | 6000 | 86x107.5 | liquid | 0.3 | 27.5 -> 32 | 1.00 | -1.500 | -1.561 | — |
| normal | 6000 | 86x107.5 | humid_evap | 0.3 | 27.5 -> 32 | 1.00 | -1.500 | -1.561 | — |
| normal | 1500 | 65x52 | liquid | 0.26 | 18 -> 18 | 1.33 | -1.448 | -1.448 | — |
| normal | 1500 | 65x52 | humid_evap | 0.26 | 18 -> 18 | 1.33 | -1.448 | -1.448 | — |
| normal | 6000 | 86x68.8 | liquid | 0.3 | 29 -> 32 | 1.11 | -1.423 | -1.423 | — |
| normal | 6000 | 86x68.8 | humid_evap | 0.3 | 29 -> 32 | 1.11 | -1.423 | -1.423 | — |
| normal | 6000 | 105x105 | liquid | 0.3 | 27.5 -> 32 | 0.84 | -1.351 | -1.410 | — |
| normal | 6000 | 105x105 | humid_evap | 0.3 | 27.5 -> 32 | 0.84 | -1.351 | -1.410 | — |
| normal | 6000 | 105x84 | liquid | 0.3 | 27.5 -> 32 | 0.81 | -1.321 | -1.351 | — |
| normal | 6000 | 105x84 | humid_evap | 0.3 | 27.5 -> 32 | 0.81 | -1.321 | -1.351 | — |

## C2H5OH (24 rows)

| regime | rpm | bore x stroke mm | mode | water w | CR dry -> wet | power % | cost/mile % | cost/mile % before | notes |
|---|---|---|---|---|---|---|---|---|---|
| hot | 1500 | 86x107.5 | humid_evap | 0.3 | 24 -> 30.5 | 5.03 | -2.103 | -2.430 | — |
| hot | 1500 | 86x107.5 | liquid | 0.3 | 24 -> 30.5 | 5.03 | -2.103 | -2.483 | — |
| hot | 1500 | 105x105 | liquid | 0.3 | 24 -> 30.5 | 4.88 | -1.963 | -2.428 | — |
| hot | 1500 | 105x105 | humid_evap | 0.3 | 24 -> 30.5 | 4.88 | -1.963 | -2.324 | — |
| hot | 1500 | 105x84 | liquid | 0.1 | 24 -> 30.5 | 4.07 | -1.889 | -2.357 | — |
| hot | 1500 | 105x84 | humid_evap | 0.3 | 24 -> 30.5 | 4.78 | -1.871 | -2.275 | — |
| hot | 1500 | 86x68.8 | humid_evap | 0.3 | 24 -> 27.5 | 4.63 | -1.363 | -1.647 | — |
| hot | 1500 | 86x68.8 | liquid | 0.3 | 24 -> 27.5 | 4.63 | -1.363 | -1.647 | — |
| hot | 2500 | 65x52 | liquid | 0.3 | 29 -> 30.5 | 4.30 | -0.680 | -0.372 | — |
| hot | 2500 | 65x52 | humid_evap | 0.3 | 29 -> 30.5 | 4.30 | -0.680 | -0.372 | — |
| hot | 2500 | 65x65 | liquid | 0.3 | 29 -> 30.5 | 4.25 | -0.633 | -0.414 | — |
| hot | 2500 | 65x65 | humid_evap | 0.3 | 29 -> 30.5 | 4.25 | -0.633 | -0.345 | — |
| hot | 2500 | 86x107.5 | liquid | 0.1 | 27.5 -> 29 | 3.46 | -0.595 | -0.761 | — |
| hot | 2500 | 86x107.5 | humid_evap | 0.3 | 27.5 -> 30.5 | 4.00 | -0.588 | -0.625 | — |
| hot | 1500 | 65x65 | liquid | 0.3 | 22 -> 22 | 4.31 | -0.516 | -0.516 | — |
| hot | 1500 | 65x65 | humid_evap | 0.3 | 22 -> 22 | 4.31 | -0.516 | -0.516 | — |
| hot | 2500 | 86x68.8 | humid_evap | 0.3 | 29 -> 30.5 | 4.07 | -0.454 | -0.231 | — |
| hot | 2500 | 86x68.8 | liquid | 0.3 | 29 -> 30.5 | 4.07 | -0.454 | -0.358 | — |
| hot | 2500 | 105x105 | liquid | 0.1 | 29 -> 29 | 3.50 | -0.432 | -0.432 | — |
| hot | 2500 | 105x105 | humid_evap | 0.26 | 29 -> 30.5 | 3.67 | -0.383 | -0.263 | — |
| hot | 2500 | 105x84 | liquid | 0.1 | 29 -> 29 | 3.41 | -0.346 | -0.346 | — |
| hot | 2500 | 105x84 | humid_evap | 0.26 | 29 -> 30.5 | 3.63 | -0.342 | -0.181 | — |
| hot | 4000 | 65x52 | liquid | 0.26 | 30.5 -> 30.5 | 3.48 | -0.024 | -0.121 | — |
| hot | 4000 | 65x52 | humid_evap | 0.26 | 30.5 -> 30.5 | 3.48 | -0.024 | 0.013 | — |
