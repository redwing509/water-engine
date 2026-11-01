# Screening results: every COST GAIN case

> **Screening results: executed, not validated.** 0-D simulation screening (Module 03 engine cycle + independent M03-CRN Cantera cross-check, M03 knock model only). Not validated against experiment and not peer-reviewed. Not engine performance claims.

A row is listed when the best-cost wet case has **lower cost per mile than its own dry baseline** (DEI dry, spark optimised) at **equal-or-better power** in both engines (verdict COST GAIN). Water $0.10/gal, dated retail fuel prices. Normal regime: coolant 363 K, intake 320 K; hot: coolant 388 K, intake 400 K. `w` = water mass fraction of liquid intake. Edge flags mean the best point sits on the edge of the tested grid, so the true optimum may lie beyond it.

Source: geometry study combined tables `RESULT_AALL.md` (Track A, 120 groups, 84 COST GAIN) and `RESULT_BALL.md` (Track B, 244 groups, 244 COST GAIN), generated 2026-11-01 13:21-13:23 PST including Muse-merged chunks. Machine-readable copy: [`screening_results_cost_gain.csv`](screening_results_cost_gain.csv).

## Track A - C2H5OH (24 rows)

| regime | rpm | bore x stroke mm | water w | CR dry -> wet | d eta pp M03/CRN | power % | cost/mile % | edge flags | source |
|---|---|---|---|---|---|---|---|---|---|
| hot | 1000 | 105x131 | 0.28 | 22 -> 30 | +2.04/+2.14 | +5.3 | -2.86 | - | RESULT_AALL.md |
| hot | 1500 | 105x131 | 0.1 | 24 -> 30 | +1.23/+1.21 | +4.4 | -2.12 | - | RESULT_AALL.md |
| hot | 1500 | 65x81 | 0.28 | 24 -> 30 | +1.61/+1.64 | +4.8 | -1.99 | - | RESULT_AALL.md |
| hot | 1000 | 65x81 | 0.3 | 16 -> 18 | +1.50/+1.49 | +5.0 | -1.92 | w top of grid | RESULT_AALL.md |
| hot | 1500 | 86x86 | 0.28 | 24 -> 30 | +1.58/+1.61 | +4.7 | -1.86 | - | RESULT_AALL.md |
| hot | 2000 | 65x52 | 0.3 | 22 -> 26 | +1.52/+1.66 | +4.8 | -1.70 | w top of grid | RESULT_AALL.md |
| hot | 2000 | 65x65 | 0.3 | 26 -> 31 | +1.49/+1.58 | +4.7 | -1.51 | w top of grid | RESULT_AALL.md |
| hot | 2000 | 65x81 | 0.3 | 26 -> 31 | +1.50/+1.56 | +4.7 | -1.49 | w top of grid | RESULT_AALL.md |
| hot | 2000 | 86x69 | 0.3 | 26 -> 31 | +1.43/+1.45 | +4.5 | -1.33 | w top of grid | RESULT_AALL.md |
| hot | 2000 | 86x108 | 0.3 | 26 -> 31 | +1.48/+1.39 | +4.5 | -1.33 | w top of grid | RESULT_AALL.md |
| hot | 2000 | 86x86 | 0.3 | 26 -> 31 | +1.44/+1.41 | +4.5 | -1.29 | w top of grid | RESULT_AALL.md |
| hot | 2000 | 105x131 | 0.1 | 26 -> 30 | +0.85/+0.81 | +3.8 | -1.29 | - | RESULT_AALL.md |
| hot | 2000 | 105x84 | 0.27 | 26 -> 31 | +1.28/+1.22 | +4.1 | -1.18 | - | RESULT_AALL.md |
| hot | 2000 | 105x105 | 0.27 | 26 -> 31 | +1.29/+1.19 | +4.1 | -1.18 | - | RESULT_AALL.md |
| normal | 1000 | 65x81 | 0.3 | 16 -> 18 | +1.05/+1.05 | +0.5 | -0.92 | w top of grid | RESULT_AALL.md |
| hot | 2500 | 65x81 | 0.08 | 28 -> 30 | +0.53/+0.53 | +3.4 | -0.77 | - | RESULT_AALL.md |
| hot | 2500 | 105x131 | 0.04 | 28 -> 30 | +0.41/+0.38 | +1.8 | -0.66 | - | RESULT_AALL.md |
| hot | 2500 | 86x86 | 0.08 | 29 -> 30 | +0.46/+0.45 | +3.4 | -0.59 | - | RESULT_AALL.md |
| hot | 3000 | 65x81 | 0.1 | 29 -> 30 | +0.33/+0.42 | +3.2 | -0.24 | - | RESULT_AALL.md |
| hot | 3000 | 86x86 | 0.1 | 29 -> 30 | +0.26/+0.36 | +3.0 | -0.08 | - | RESULT_AALL.md |
| hot | 5000 | 65x81 | 0.01 | 29 -> 30 | +0.04/+0.11 | +0.2 | -0.04 | - | RESULT_AALL.md |
| hot | 4000 | 65x81 | 0.08 | 30 -> 30 | +0.19/+0.31 | +2.9 | -0.03 | - | RESULT_AALL.md |
| hot | 5000 | 86x86 | 0.01 | 29 -> 30 | +0.03/+0.09 | +0.2 | -0.02 | - | RESULT_AALL.md |
| hot | 6000 | 65x81 | 0.01 | 29 -> 30 | +0.03/+0.11 | +0.2 | -0.02 | - | RESULT_AALL.md |

## Track A - CH3OH (60 rows)

| regime | rpm | bore x stroke mm | water w | CR dry -> wet | d eta pp M03/CRN | power % | cost/mile % | edge flags | source |
|---|---|---|---|---|---|---|---|---|---|
| hot | 1000 | 105x131 | 0.3 | 16 -> 32 | +4.29/+4.39 | +5.5 | -8.29 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 1500 | 105x131 | 0.3 | 18 -> 32 | +3.90/+3.55 | +5.0 | -7.18 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 2000 | 105x131 | 0.3 | 18 -> 32 | +3.78/+3.31 | +4.6 | -6.80 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 2000 | 86x108 | 0.3 | 18 -> 32 | +3.71/+3.47 | +4.6 | -6.76 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 2000 | 65x81 | 0.3 | 18 -> 32 | +3.55/+3.66 | +4.5 | -6.67 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 1500 | 65x81 | 0.3 | 18 -> 32 | +3.42/+3.77 | +4.4 | -6.61 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 2000 | 105x105 | 0.3 | 18 -> 32 | +3.63/+3.35 | +4.4 | -6.57 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 1500 | 86x86 | 0.3 | 18 -> 32 | +3.46/+3.67 | +4.3 | -6.54 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 2000 | 86x86 | 0.3 | 18 -> 32 | +3.54/+3.51 | +4.3 | -6.51 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 2000 | 65x65 | 0.3 | 18 -> 32 | +3.37/+3.69 | +4.2 | -6.40 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 1000 | 105x131 | 0.3 | 18 -> 32 | +3.27/+3.35 | +4.1 | -6.38 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 2000 | 105x84 | 0.3 | 18 -> 32 | +3.49/+3.39 | +4.1 | -6.36 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 2000 | 86x69 | 0.3 | 18 -> 32 | +3.38/+3.55 | +4.0 | -6.30 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 1500 | 105x131 | 0.3 | 20 -> 32 | +3.05/+2.70 | +3.9 | -5.63 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 2500 | 65x81 | 0.3 | 20 -> 32 | +3.11/+3.13 | +3.9 | -5.62 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 2500 | 105x131 | 0.3 | 22 -> 32 | +3.05/+2.49 | +4.0 | -5.27 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 1500 | 86x86 | 0.3 | 20 -> 32 | +2.62/+2.80 | +3.2 | -4.97 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 1000 | 86x86 | 0.3 | 16 -> 22 | +2.51/+2.61 | +3.3 | -4.96 | w top of grid | RESULT_AALL.md |
| hot | 2500 | 86x86 | 0.3 | 22 -> 32 | +2.81/+2.66 | +3.6 | -4.92 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 2000 | 65x52 | 0.3 | 18 -> 26 | +2.57/+2.98 | +3.3 | -4.88 | w top of grid | RESULT_AALL.md |
| normal | 2000 | 105x131 | 0.285 | 22 -> 32 | +2.69/+2.23 | +3.5 | -4.83 | CR edge of grid | RESULT_AALL.md |
| hot | 3000 | 65x81 | 0.3 | 22 -> 32 | +2.75/+2.72 | +3.5 | -4.80 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 3000 | 105x131 | 0.3 | 22 -> 32 | +2.83/+2.30 | +3.5 | -4.78 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 2000 | 86x108 | 0.3 | 22 -> 32 | +2.60/+2.36 | +3.4 | -4.68 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 1500 | 65x81 | 0.28 | 20 -> 30 | +2.39/+2.62 | +3.0 | -4.66 | - | RESULT_AALL.md |
| hot | 3000 | 86x86 | 0.3 | 22 -> 32 | +2.67/+2.52 | +3.3 | -4.58 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 2000 | 105x105 | 0.285 | 22 -> 32 | +2.53/+2.25 | +3.2 | -4.55 | CR edge of grid | RESULT_AALL.md |
| normal | 2000 | 65x81 | 0.3 | 22 -> 32 | +2.40/+2.53 | +3.1 | -4.42 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 2500 | 105x131 | 0.28 | 22 -> 32 | +2.50/+2.05 | +3.0 | -4.40 | CR edge of grid | RESULT_AALL.md |
| normal | 2000 | 86x86 | 0.285 | 22 -> 32 | +2.39/+2.36 | +3.0 | -4.37 | CR edge of grid | RESULT_AALL.md |
| normal | 2000 | 105x84 | 0.285 | 22 -> 32 | +2.36/+2.27 | +2.9 | -4.27 | CR edge of grid | RESULT_AALL.md |
| normal | 2000 | 65x65 | 0.3 | 22 -> 32 | +2.21/+2.51 | +2.7 | -4.09 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 2000 | 86x69 | 0.285 | 22 -> 32 | +2.20/+2.38 | +2.6 | -4.05 | CR edge of grid | RESULT_AALL.md |
| normal | 2500 | 65x81 | 0.3 | 24 -> 32 | +2.20/+2.21 | +2.9 | -3.89 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 4000 | 65x81 | 0.3 | 24 -> 32 | +2.33/+2.33 | +2.9 | -3.86 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 2500 | 86x86 | 0.28 | 24 -> 32 | +2.16/+2.02 | +2.8 | -3.80 | CR edge of grid | RESULT_AALL.md |
| normal | 3000 | 105x131 | 0.28 | 24 -> 32 | +2.18/+1.72 | +2.7 | -3.70 | CR edge of grid | RESULT_AALL.md |
| hot | 4000 | 105x131 | 0.3 | 24 -> 32 | +2.30/+1.85 | +2.7 | -3.70 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 3000 | 65x81 | 0.3 | 24 -> 32 | +2.11/+2.12 | +2.7 | -3.63 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 4000 | 86x86 | 0.3 | 24 -> 32 | +2.22/+2.11 | +2.6 | -3.60 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 3000 | 86x86 | 0.28 | 24 -> 32 | +2.04/+1.91 | +2.4 | -3.50 | CR edge of grid | RESULT_AALL.md |
| normal | 1000 | 86x86 | 0.3 | 18 -> 22 | +1.75/+1.69 | +2.4 | -3.35 | w top of grid | RESULT_AALL.md |
| hot | 1000 | 65x81 | 0.3 | 16 -> 18 | +1.65/+1.65 | +2.5 | -3.16 | w top of grid | RESULT_AALL.md |
| hot | 5000 | 65x81 | 0.3 | 26 -> 32 | +1.97/+2.04 | +2.5 | -3.11 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 5000 | 105x131 | 0.3 | 26 -> 32 | +1.90/+1.52 | +2.2 | -2.89 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 1000 | 65x81 | 0.3 | 16 -> 18 | +1.48/+1.50 | +2.2 | -2.87 | w top of grid | RESULT_AALL.md |
| normal | 4000 | 65x81 | 0.3 | 26 -> 32 | +1.76/+1.83 | +2.2 | -2.84 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 5000 | 86x86 | 0.3 | 26 -> 32 | +1.84/+1.80 | +2.2 | -2.83 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 4000 | 105x131 | 0.28 | 26 -> 32 | +1.75/+1.36 | +2.0 | -2.79 | CR edge of grid | RESULT_AALL.md |
| normal | 2000 | 65x52 | 0.3 | 22 -> 26 | +1.54/+1.83 | +2.1 | -2.74 | w top of grid | RESULT_AALL.md |
| normal | 4000 | 86x86 | 0.28 | 26 -> 32 | +1.67/+1.59 | +1.9 | -2.69 | CR edge of grid | RESULT_AALL.md |
| hot | 6000 | 65x81 | 0.3 | 26 -> 32 | +1.68/+1.95 | +1.8 | -2.51 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 6000 | 86x86 | 0.3 | 26 -> 32 | +1.54/+1.69 | +1.5 | -2.22 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 5000 | 65x81 | 0.3 | 28 -> 32 | +1.47/+1.61 | +1.8 | -2.21 | w top of grid; CR edge of grid | RESULT_AALL.md |
| hot | 6000 | 105x131 | 0.3 | 26 -> 32 | +1.55/+1.36 | +1.5 | -2.20 | w top of grid; CR edge of grid | RESULT_AALL.md |
| normal | 5000 | 105x131 | 0.28 | 26 -> 32 | +1.40/+1.20 | +1.3 | -2.07 | CR edge of grid | RESULT_AALL.md |
| normal | 5000 | 86x86 | 0.28 | 28 -> 32 | +1.37/+1.35 | +1.6 | -2.05 | CR edge of grid | RESULT_AALL.md |
| normal | 6000 | 65x81 | 0.28 | 28 -> 32 | +1.17/+1.48 | +1.1 | -1.64 | CR edge of grid | RESULT_AALL.md |
| normal | 6000 | 86x86 | 0.28 | 28 -> 32 | +1.08/+1.26 | +0.9 | -1.46 | CR edge of grid | RESULT_AALL.md |
| normal | 6000 | 105x131 | 0.28 | 28 -> 32 | +1.09/+0.96 | +0.9 | -1.44 | CR edge of grid | RESULT_AALL.md |

## Track B - E10 (32 rows)

| regime | rpm | bore x stroke mm | water w | CR dry -> wet | d eta pp M03/CRN | power % | cost/mile % | edge flags | source |
|---|---|---|---|---|---|---|---|---|---|
| normal | 2000 | 65x81 | 0.3 | 9 -> 16 | +4.99/+5.05 | +10.2 | -11.05 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 105x131 | 0.3 | 9 -> 16 | +5.15/+5.01 | +10.2 | -11.01 | w top of grid | RESULT_BALL.md |
| hot | 1500 | 105x131 | 0.3 | 7 -> 9 | +3.37/+3.38 | +13.0 | -8.17 | w top of grid | RESULT_BALL.md |
| hot | 1500 | 65x81 | 0.3 | 7 -> 9 | +3.19/+3.40 | +12.8 | -8.04 | w top of grid | RESULT_BALL.md |
| normal | 1500 | 105x131 | 0.3 | 9 -> 12 | +3.58/+3.50 | +8.9 | -7.93 | w top of grid | RESULT_BALL.md |
| normal | 1000 | 105x131 | 0.26 | 7 -> 9 | +3.16/+3.31 | +8.0 | -7.79 | - | RESULT_BALL.md |
| normal | 3000 | 105x131 | 0.3 | 12 -> 18 | +3.89/+3.48 | +8.8 | -7.74 | w top of grid | RESULT_BALL.md |
| normal | 2500 | 105x131 | 0.3 | 12 -> 17 | +3.75/+3.37 | +9.0 | -7.61 | w top of grid | RESULT_BALL.md |
| hot | 3000 | 65x81 | 0.3 | 9 -> 12 | +3.39/+3.38 | +12.9 | -7.56 | w top of grid | RESULT_BALL.md |
| hot | 3000 | 105x131 | 0.3 | 9 -> 12 | +3.47/+3.44 | +12.8 | -7.54 | w top of grid | RESULT_BALL.md |
| normal | 3000 | 65x81 | 0.3 | 12 -> 18 | +3.63/+3.43 | +8.4 | -7.42 | w top of grid | RESULT_BALL.md |
| normal | 1000 | 65x81 | 0.3 | 7 -> 9 | +2.87/+3.29 | +7.6 | -7.33 | w top of grid | RESULT_BALL.md |
| normal | 2500 | 65x81 | 0.3 | 12 -> 17 | +3.42/+3.30 | +8.4 | -7.12 | w top of grid | RESULT_BALL.md |
| normal | 1500 | 65x81 | 0.3 | 9 -> 12 | +3.08/+3.39 | +7.9 | -7.07 | w top of grid | RESULT_BALL.md |
| hot | 2500 | 105x131 | 0.3 | 9 -> 12 | +3.20/+3.15 | +12.2 | -7.02 | w top of grid | RESULT_BALL.md |
| hot | 2500 | 65x81 | 0.3 | 9 -> 12 | +3.10/+3.14 | +12.2 | -7.00 | w top of grid | RESULT_BALL.md |
| normal | 4000 | 105x131 | 0.3 | 15 -> 22 | +3.54/+3.00 | +8.4 | -6.75 | w top of grid | RESULT_BALL.md |
| normal | 5000 | 105x131 | 0.3 | 15 -> 24 | +3.58/+3.11 | +7.9 | -6.67 | w top of grid | RESULT_BALL.md |
| normal | 5000 | 65x81 | 0.3 | 15 -> 24 | +3.44/+3.10 | +7.7 | -6.52 | w top of grid | RESULT_BALL.md |
| normal | 4000 | 65x81 | 0.3 | 15 -> 22 | +3.31/+2.94 | +8.1 | -6.43 | w top of grid | RESULT_BALL.md |
| hot | 1000 | 105x131 | 0.3 | 6 -> 7 | +2.43/+2.53 | +11.7 | -6.37 | w top of grid | RESULT_BALL.md |
| hot | 1000 | 65x81 | 0.3 | 6 -> 7 | +2.24/+2.52 | +11.4 | -6.14 | w top of grid | RESULT_BALL.md |
| normal | 6000 | 105x131 | 0.3 | 17 -> 24 | +3.34/+2.57 | +8.1 | -6.05 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 65x81 | 0.3 | 12 -> 17 | +2.93/+2.99 | +11.3 | -5.89 | w top of grid | RESULT_BALL.md |
| normal | 6000 | 65x81 | 0.3 | 17 -> 26 | +3.17/+2.71 | +7.5 | -5.85 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 105x131 | 0.3 | 12 -> 17 | +2.96/+2.97 | +11.3 | -5.82 | w top of grid | RESULT_BALL.md |
| hot | 4000 | 105x131 | 0.3 | 12 -> 15 | +2.71/+2.50 | +11.8 | -5.45 | w top of grid | RESULT_BALL.md |
| hot | 4000 | 65x81 | 0.3 | 12 -> 15 | +2.58/+2.41 | +11.5 | -5.27 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 105x131 | 0.3 | 15 -> 19 | +2.54/+2.27 | +11.3 | -4.79 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 65x81 | 0.3 | 15 -> 19 | +2.43/+2.18 | +11.2 | -4.65 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 105x131 | 0.3 | 9 -> 9 | +1.33/+1.17 | +10.6 | -2.73 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 65x81 | 0.3 | 9 -> 9 | +1.02/+1.07 | +9.8 | -2.04 | w top of grid | RESULT_BALL.md |

## Track B - E85 (60 rows)

| regime | rpm | bore x stroke mm | water w | CR dry -> wet | d eta pp M03/CRN | power % | cost/mile % | edge flags | source |
|---|---|---|---|---|---|---|---|---|---|
| hot | 1000 | 105x131 | 0.3 | 9 -> 14 | +4.96/+5.11 | +15.0 | -10.81 | w top of grid | RESULT_BALL.md |
| hot | 1500 | 105x131 | 0.3 | 10 -> 16 | +5.00/+4.84 | +14.6 | -10.25 | w top of grid | RESULT_BALL.md |
| hot | 1000 | 86x86 | 0.3 | 9 -> 14 | +4.48/+5.13 | +14.0 | -10.03 | w top of grid | RESULT_BALL.md |
| hot | 1000 | 65x81 | 0.3 | 9 -> 14 | +4.33/+5.09 | +13.9 | -9.92 | w top of grid | RESULT_BALL.md |
| hot | 1500 | 65x81 | 0.3 | 10 -> 16 | +4.51/+4.82 | +13.9 | -9.65 | w top of grid | RESULT_BALL.md |
| hot | 2500 | 86x86 | 0.3 | 12 -> 22 | +4.87/+4.75 | +13.6 | -9.46 | w top of grid | RESULT_BALL.md |
| hot | 2500 | 105x131 | 0.3 | 12 -> 20 | +4.91/+4.49 | +14.1 | -9.37 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 105x84 | 0.3 | 12 -> 20 | +4.59/+4.54 | +13.7 | -9.06 | - | RESULT_BALL.md |
| hot | 2000 | 105x131 | 0.3 | 12 -> 18 | +4.62/+4.24 | +14.3 | -9.03 | - | RESULT_BALL.md |
| hot | 2500 | 65x81 | 0.3 | 12 -> 20 | +4.58/+4.47 | +13.7 | -9.03 | w top of grid | RESULT_BALL.md |
| normal | 1000 | 105x131 | 0.3 | 10 -> 16 | +4.15/+4.29 | +5.3 | -8.90 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 86x69 | 0.3 | 12 -> 20 | +4.40/+4.54 | +13.4 | -8.81 | - | RESULT_BALL.md |
| hot | 2000 | 86x108 | 0.3 | 12 -> 18 | +4.44/+4.23 | +14.0 | -8.78 | - | RESULT_BALL.md |
| hot | 2000 | 105x105 | 0.3 | 12 -> 18 | +4.47/+4.24 | +14.0 | -8.77 | - | RESULT_BALL.md |
| hot | 1500 | 86x86 | 0.3 | 11 -> 16 | +4.17/+4.43 | +13.8 | -8.67 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 86x86 | 0.3 | 12 -> 18 | +4.25/+4.22 | +13.6 | -8.45 | - | RESULT_BALL.md |
| normal | 2000 | 105x131 | 0.3 | 12 -> 22 | +4.33/+3.99 | +4.7 | -8.42 | - | RESULT_BALL.md |
| hot | 2000 | 65x52 | 0.3 | 12 -> 20 | +4.08/+4.49 | +12.9 | -8.39 | - | RESULT_BALL.md |
| hot | 3000 | 105x131 | 0.3 | 14 -> 22 | +4.53/+3.94 | +13.8 | -8.38 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 65x81 | 0.3 | 12 -> 18 | +4.13/+4.18 | +13.5 | -8.34 | - | RESULT_BALL.md |
| normal | 2000 | 86x108 | 0.3 | 12 -> 22 | +4.22/+4.03 | +4.6 | -8.31 | - | RESULT_BALL.md |
| normal | 2000 | 105x105 | 0.3 | 12 -> 22 | +4.23/+4.03 | +4.6 | -8.28 | - | RESULT_BALL.md |
| normal | 2000 | 65x81 | 0.3 | 12 -> 22 | +4.03/+4.06 | +4.4 | -8.14 | - | RESULT_BALL.md |
| normal | 2000 | 86x86 | 0.3 | 12 -> 22 | +4.10/+4.06 | +4.4 | -8.14 | - | RESULT_BALL.md |
| normal | 2000 | 105x84 | 0.3 | 12 -> 22 | +4.11/+4.06 | +4.4 | -8.10 | - | RESULT_BALL.md |
| hot | 3000 | 86x86 | 0.3 | 14 -> 22 | +4.27/+3.93 | +13.3 | -8.01 | w top of grid | RESULT_BALL.md |
| normal | 1000 | 86x86 | 0.3 | 10 -> 16 | +3.64/+4.31 | +4.2 | -8.00 | w top of grid | RESULT_BALL.md |
| hot | 3000 | 65x81 | 0.3 | 14 -> 22 | +4.18/+3.89 | +13.2 | -7.93 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 65x65 | 0.3 | 12 -> 18 | +3.89/+4.14 | +12.9 | -7.90 | - | RESULT_BALL.md |
| normal | 1000 | 65x81 | 0.3 | 10 -> 16 | +3.49/+4.29 | +4.0 | -7.84 | w top of grid | RESULT_BALL.md |
| hot | 4000 | 105x131 | 0.3 | 16 -> 26 | +4.33/+3.67 | +13.2 | -7.70 | w top of grid | RESULT_BALL.md |
| normal | 1500 | 105x131 | 0.3 | 12 -> 18 | +3.82/+3.62 | +5.0 | -7.64 | w top of grid | RESULT_BALL.md |
| hot | 4000 | 86x86 | 0.3 | 16 -> 26 | +4.14/+3.67 | +12.9 | -7.45 | w top of grid | RESULT_BALL.md |
| hot | 4000 | 65x81 | 0.3 | 16 -> 26 | +4.06/+3.65 | +12.8 | -7.38 | w top of grid | RESULT_BALL.md |
| normal | 2500 | 105x131 | 0.3 | 14 -> 24 | +3.87/+3.38 | +4.3 | -7.22 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 105x131 | 0.3 | 18 -> 28 | +4.15/+3.31 | +13.1 | -7.17 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 86x86 | 0.3 | 18 -> 28 | +3.96/+3.29 | +12.7 | -6.91 | w top of grid | RESULT_BALL.md |
| normal | 2500 | 86x86 | 0.3 | 14 -> 24 | +3.62/+3.42 | +3.9 | -6.85 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 65x81 | 0.3 | 18 -> 28 | +3.88/+3.26 | +12.6 | -6.83 | w top of grid | RESULT_BALL.md |
| normal | 2500 | 65x81 | 0.3 | 14 -> 24 | +3.54/+3.41 | +3.8 | -6.79 | w top of grid | RESULT_BALL.md |
| normal | 1500 | 86x86 | 0.3 | 12 -> 18 | +3.33/+3.60 | +4.0 | -6.78 | w top of grid | RESULT_BALL.md |
| normal | 1500 | 65x81 | 0.3 | 12 -> 18 | +3.19/+3.57 | +3.8 | -6.59 | w top of grid | RESULT_BALL.md |
| normal | 3000 | 105x131 | 0.3 | 16 -> 26 | +3.59/+2.97 | +4.2 | -6.50 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 86x69 | 0.3 | 14 -> 22 | +3.22/+3.38 | +3.7 | -6.27 | - | RESULT_BALL.md |
| normal | 2000 | 65x65 | 0.3 | 14 -> 22 | +3.09/+3.35 | +3.5 | -6.10 | - | RESULT_BALL.md |
| normal | 3000 | 86x86 | 0.3 | 16 -> 26 | +3.34/+2.98 | +3.7 | -6.10 | w top of grid | RESULT_BALL.md |
| normal | 3000 | 65x81 | 0.3 | 16 -> 26 | +3.25/+2.96 | +3.6 | -6.01 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 105x131 | 0.3 | 20 -> 30 | +3.56/+2.88 | +12.0 | -5.97 | w top of grid | RESULT_BALL.md |
| normal | 4000 | 105x131 | 0.3 | 18 -> 28 | +3.40/+2.56 | +4.0 | -5.91 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 65x81 | 0.3 | 20 -> 30 | +3.43/+2.92 | +11.8 | -5.85 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 86x86 | 0.3 | 20 -> 30 | +3.43/+2.90 | +11.8 | -5.78 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 65x52 | 0.3 | 14 -> 22 | +2.79/+3.32 | +2.9 | -5.55 | - | RESULT_BALL.md |
| normal | 4000 | 86x86 | 0.3 | 18 -> 28 | +3.15/+2.54 | +3.5 | -5.51 | w top of grid | RESULT_BALL.md |
| normal | 4000 | 65x81 | 0.3 | 18 -> 30 | +3.08/+2.67 | +3.2 | -5.44 | w top of grid | RESULT_BALL.md |
| normal | 5000 | 105x131 | 0.3 | 20 -> 30 | +2.81/+2.09 | +2.9 | -4.65 | w top of grid | RESULT_BALL.md |
| normal | 5000 | 65x81 | 0.3 | 20 -> 30 | +2.62/+2.13 | +2.7 | -4.40 | w top of grid | RESULT_BALL.md |
| normal | 5000 | 86x86 | 0.3 | 20 -> 30 | +2.64/+2.12 | +2.7 | -4.38 | w top of grid | RESULT_BALL.md |
| normal | 6000 | 105x131 | 0.3 | 22 -> 30 | +2.16/+1.57 | +2.0 | -3.33 | w top of grid | RESULT_BALL.md |
| normal | 6000 | 65x81 | 0.3 | 22 -> 30 | +2.05/+1.69 | +1.9 | -3.19 | w top of grid | RESULT_BALL.md |
| normal | 6000 | 86x86 | 0.3 | 22 -> 30 | +2.05/+1.64 | +1.8 | -3.15 | w top of grid | RESULT_BALL.md |

## Track B - PRF87 (60 rows)

| regime | rpm | bore x stroke mm | water w | CR dry -> wet | d eta pp M03/CRN | power % | cost/mile % | edge flags | source |
|---|---|---|---|---|---|---|---|---|---|
| hot | 1000 | 105x131 | 0.3 | 5 -> 7 | +4.41/+4.49 | +14.1 | -12.35 | w top of grid | RESULT_BALL.md |
| hot | 1000 | 86x86 | 0.3 | 5 -> 7 | +4.30/+4.60 | +14.0 | -12.28 | w top of grid | RESULT_BALL.md |
| hot | 1000 | 65x81 | 0.3 | 5 -> 7 | +4.21/+4.58 | +14.0 | -12.26 | w top of grid | RESULT_BALL.md |
| hot | 1500 | 65x81 | 0.3 | 6 -> 8 | +3.65/+3.83 | +13.0 | -9.71 | w top of grid | RESULT_BALL.md |
| hot | 1500 | 86x86 | 0.3 | 6 -> 8 | +3.71/+3.85 | +13.0 | -9.70 | w top of grid | RESULT_BALL.md |
| hot | 1500 | 105x131 | 0.3 | 6 -> 8 | +3.77/+3.77 | +13.0 | -9.70 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 105x131 | 0.3 | 9 -> 12 | +3.71/+3.50 | +10.0 | -8.20 | - | RESULT_BALL.md |
| normal | 2500 | 105x131 | 0.3 | 10 -> 14 | +3.83/+3.53 | +9.9 | -8.16 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 105x105 | 0.3 | 9 -> 12 | +3.62/+3.50 | +9.8 | -8.02 | - | RESULT_BALL.md |
| normal | 3000 | 105x131 | 0.3 | 10 -> 14 | +3.83/+3.48 | +9.7 | -8.01 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 86x108 | 0.3 | 9 -> 12 | +3.59/+3.48 | +9.8 | -8.00 | - | RESULT_BALL.md |
| normal | 2500 | 86x86 | 0.3 | 10 -> 14 | +3.65/+3.52 | +9.6 | -7.87 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 105x84 | 0.3 | 9 -> 12 | +3.50/+3.49 | +9.5 | -7.80 | - | RESULT_BALL.md |
| normal | 2000 | 86x86 | 0.3 | 9 -> 12 | +3.47/+3.47 | +9.5 | -7.78 | - | RESULT_BALL.md |
| normal | 2500 | 65x81 | 0.3 | 10 -> 14 | +3.56/+3.48 | +9.5 | -7.78 | w top of grid | RESULT_BALL.md |
| normal | 1500 | 105x131 | 0.3 | 8 -> 10 | +3.35/+3.29 | +9.8 | -7.77 | w top of grid | RESULT_BALL.md |
| normal | 3000 | 86x86 | 0.3 | 10 -> 14 | +3.66/+3.46 | +9.4 | -7.75 | w top of grid | RESULT_BALL.md |
| normal | 3000 | 65x81 | 0.3 | 10 -> 14 | +3.59/+3.42 | +9.4 | -7.69 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 65x81 | 0.3 | 9 -> 12 | +3.37/+3.43 | +9.4 | -7.66 | - | RESULT_BALL.md |
| normal | 2000 | 86x69 | 0.3 | 9 -> 12 | +3.33/+3.46 | +9.2 | -7.50 | - | RESULT_BALL.md |
| normal | 4000 | 105x131 | 0.3 | 12 -> 18 | +3.75/+3.35 | +9.3 | -7.47 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 65x65 | 0.3 | 9 -> 12 | +3.22/+3.41 | +9.0 | -7.36 | - | RESULT_BALL.md |
| normal | 4000 | 86x86 | 0.3 | 12 -> 18 | +3.64/+3.35 | +9.1 | -7.32 | w top of grid | RESULT_BALL.md |
| normal | 4000 | 65x81 | 0.3 | 12 -> 18 | +3.58/+3.31 | +9.0 | -7.27 | w top of grid | RESULT_BALL.md |
| normal | 1500 | 86x86 | 0.3 | 8 -> 10 | +3.02/+3.24 | +9.0 | -7.11 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 65x52 | 0.3 | 9 -> 12 | +3.03/+3.38 | +8.6 | -6.97 | - | RESULT_BALL.md |
| normal | 1500 | 65x81 | 0.3 | 8 -> 10 | +2.89/+3.20 | +8.8 | -6.92 | w top of grid | RESULT_BALL.md |
| hot | 3000 | 105x131 | 0.3 | 8 -> 10 | +3.03/+2.93 | +11.9 | -6.86 | w top of grid | RESULT_BALL.md |
| hot | 3000 | 65x81 | 0.3 | 8 -> 10 | +2.93/+2.95 | +11.8 | -6.80 | w top of grid | RESULT_BALL.md |
| hot | 3000 | 86x86 | 0.3 | 8 -> 10 | +2.97/+2.97 | +11.8 | -6.80 | w top of grid | RESULT_BALL.md |
| hot | 2500 | 105x131 | 0.3 | 8 -> 10 | +2.95/+2.86 | +11.8 | -6.78 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 65x81 | 0.3 | 10 -> 14 | +3.16/+3.26 | +11.3 | -6.71 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 86x86 | 0.3 | 10 -> 14 | +3.18/+3.27 | +11.3 | -6.69 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 105x131 | 0.3 | 7.5 -> 9 | +2.81/+2.74 | +12.0 | -6.68 | - | RESULT_BALL.md |
| hot | 2500 | 86x86 | 0.3 | 8 -> 10 | +2.87/+2.86 | +11.6 | -6.66 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 105x131 | 0.3 | 10 -> 14 | +3.18/+3.21 | +11.2 | -6.62 | w top of grid | RESULT_BALL.md |
| hot | 2500 | 65x81 | 0.3 | 8 -> 10 | +2.81/+2.83 | +11.6 | -6.61 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 105x105 | 0.3 | 7.5 -> 9 | +2.77/+2.74 | +11.9 | -6.60 | - | RESULT_BALL.md |
| normal | 6000 | 105x131 | 0.3 | 14 -> 20 | +3.47/+2.91 | +9.0 | -6.57 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 86x108 | 0.3 | 7.5 -> 9 | +2.73/+2.72 | +11.8 | -6.56 | - | RESULT_BALL.md |
| normal | 5000 | 86x86 | 0.3 | 14 -> 20 | +3.37/+2.94 | +8.9 | -6.55 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 105x84 | 0.3 | 7.5 -> 9 | +2.71/+2.74 | +11.7 | -6.49 | - | RESULT_BALL.md |
| hot | 2000 | 86x86 | 0.3 | 7.5 -> 9 | +2.68/+2.72 | +11.7 | -6.46 | - | RESULT_BALL.md |
| normal | 5000 | 105x131 | 0.3 | 14 -> 18 | +3.35/+2.68 | +9.5 | -6.45 | w top of grid | RESULT_BALL.md |
| normal | 6000 | 86x86 | 0.3 | 14 -> 20 | +3.37/+2.88 | +8.8 | -6.43 | w top of grid | RESULT_BALL.md |
| normal | 6000 | 65x81 | 0.3 | 14 -> 20 | +3.31/+2.83 | +8.7 | -6.38 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 65x81 | 0.3 | 7.5 -> 9 | +2.61/+2.68 | +11.6 | -6.37 | - | RESULT_BALL.md |
| normal | 1000 | 105x131 | 0.3 | 7 -> 8 | +2.55/+2.76 | +8.9 | -6.32 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 86x69 | 0.3 | 7.5 -> 9 | +2.61/+2.72 | +11.5 | -6.32 | - | RESULT_BALL.md |
| hot | 2000 | 65x65 | 0.3 | 7.5 -> 9 | +2.54/+2.68 | +11.4 | -6.23 | - | RESULT_BALL.md |
| normal | 5000 | 65x81 | 0.3 | 14 -> 18 | +3.12/+2.55 | +9.1 | -6.10 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 65x52 | 0.3 | 7.5 -> 9 | +2.45/+2.67 | +11.2 | -6.03 | - | RESULT_BALL.md |
| hot | 4000 | 105x131 | 0.3 | 10 -> 12 | +2.65/+2.43 | +11.4 | -5.59 | w top of grid | RESULT_BALL.md |
| hot | 4000 | 86x86 | 0.3 | 10 -> 12 | +2.56/+2.39 | +11.3 | -5.45 | w top of grid | RESULT_BALL.md |
| normal | 1000 | 86x86 | 0.3 | 7 -> 8 | +2.16/+2.61 | +7.9 | -5.42 | w top of grid | RESULT_BALL.md |
| hot | 4000 | 65x81 | 0.3 | 10 -> 12 | +2.51/+2.35 | +11.2 | -5.39 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 86x86 | 0.3 | 12 -> 16 | +2.62/+2.53 | +10.6 | -5.24 | w top of grid | RESULT_BALL.md |
| normal | 1000 | 65x81 | 0.3 | 7 -> 8 | +2.04/+2.55 | +7.6 | -5.22 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 105x131 | 0.3 | 12 -> 14 | +2.45/+2.10 | +11.2 | -4.85 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 65x81 | 0.3 | 12 -> 14 | +2.32/+1.98 | +10.9 | -4.65 | w top of grid | RESULT_BALL.md |

## Track B - PRF91 (60 rows)

| regime | rpm | bore x stroke mm | water w | CR dry -> wet | d eta pp M03/CRN | power % | cost/mile % | edge flags | source |
|---|---|---|---|---|---|---|---|---|---|
| normal | 1000 | 105x131 | 0.3 | 7 -> 10 | +4.15/+4.28 | +10.4 | -10.12 | w top of grid | RESULT_BALL.md |
| normal | 1500 | 105x131 | 0.3 | 8 -> 12 | +4.31/+4.24 | +10.3 | -9.84 | w top of grid | RESULT_BALL.md |
| normal | 1000 | 86x86 | 0.3 | 7 -> 10 | +3.85/+4.31 | +9.8 | -9.64 | w top of grid | RESULT_BALL.md |
| normal | 1500 | 86x86 | 0.3 | 8 -> 12 | +4.11/+4.28 | +10.0 | -9.57 | w top of grid | RESULT_BALL.md |
| normal | 1000 | 65x81 | 0.3 | 7 -> 10 | +3.73/+4.27 | +9.7 | -9.56 | w top of grid | RESULT_BALL.md |
| normal | 1500 | 65x81 | 0.3 | 8 -> 12 | +4.03/+4.24 | +9.9 | -9.54 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 105x131 | 0.3 | 10 -> 14 | +3.78/+3.56 | +9.9 | -8.15 | - | RESULT_BALL.md |
| normal | 2000 | 105x105 | 0.3 | 10 -> 14 | +3.70/+3.57 | +9.8 | -8.01 | - | RESULT_BALL.md |
| normal | 2000 | 86x108 | 0.3 | 10 -> 14 | +3.67/+3.55 | +9.7 | -7.99 | - | RESULT_BALL.md |
| normal | 2500 | 105x131 | 0.3 | 10 -> 14 | +3.77/+3.48 | +9.7 | -7.95 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 105x84 | 0.3 | 10 -> 14 | +3.60/+3.58 | +9.5 | -7.82 | - | RESULT_BALL.md |
| normal | 2000 | 86x86 | 0.3 | 10 -> 14 | +3.57/+3.55 | +9.5 | -7.80 | - | RESULT_BALL.md |
| normal | 2000 | 65x81 | 0.3 | 10 -> 14 | +3.47/+3.51 | +9.4 | -7.70 | - | RESULT_BALL.md |
| normal | 2500 | 86x86 | 0.3 | 10 -> 14 | +3.58/+3.46 | +9.3 | -7.65 | w top of grid | RESULT_BALL.md |
| normal | 2500 | 65x81 | 0.3 | 10 -> 14 | +3.50/+3.42 | +9.3 | -7.58 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 86x69 | 0.3 | 10 -> 14 | +3.44/+3.55 | +9.2 | -7.57 | - | RESULT_BALL.md |
| normal | 2000 | 65x65 | 0.3 | 10 -> 14 | +3.34/+3.50 | +9.1 | -7.45 | - | RESULT_BALL.md |
| normal | 4000 | 105x131 | 0.3 | 12 -> 18 | +3.77/+3.39 | +9.3 | -7.45 | w top of grid | RESULT_BALL.md |
| normal | 4000 | 86x86 | 0.3 | 12 -> 18 | +3.66/+3.39 | +9.1 | -7.31 | w top of grid | RESULT_BALL.md |
| normal | 4000 | 65x81 | 0.3 | 12 -> 18 | +3.61/+3.35 | +9.1 | -7.28 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 65x52 | 0.3 | 10 -> 14 | +3.16/+3.49 | +8.7 | -7.13 | - | RESULT_BALL.md |
| normal | 3000 | 105x131 | 0.3 | 12 -> 16 | +3.50/+3.08 | +9.7 | -7.11 | w top of grid | RESULT_BALL.md |
| hot | 1000 | 105x131 | 0.3 | 6 -> 7 | +2.61/+2.76 | +12.0 | -6.96 | w top of grid | RESULT_BALL.md |
| hot | 2500 | 105x131 | 0.3 | 8 -> 10 | +2.98/+2.91 | +11.8 | -6.80 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 105x131 | 0.3 | 8 -> 10 | +2.91/+2.86 | +11.8 | -6.79 | - | RESULT_BALL.md |
| normal | 3000 | 86x86 | 0.3 | 12 -> 16 | +3.31/+3.04 | +9.3 | -6.79 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 105x105 | 0.3 | 8 -> 10 | +2.88/+2.87 | +11.7 | -6.73 | - | RESULT_BALL.md |
| hot | 2000 | 86x108 | 0.3 | 8 -> 10 | +2.85/+2.85 | +11.7 | -6.71 | - | RESULT_BALL.md |
| hot | 2500 | 65x81 | 0.3 | 8 -> 10 | +2.87/+2.91 | +11.7 | -6.71 | w top of grid | RESULT_BALL.md |
| hot | 2500 | 86x86 | 0.3 | 8 -> 10 | +2.91/+2.94 | +11.7 | -6.71 | w top of grid | RESULT_BALL.md |
| normal | 3000 | 65x81 | 0.3 | 12 -> 16 | +3.22/+2.99 | +9.2 | -6.68 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 105x84 | 0.3 | 8 -> 10 | +2.84/+2.88 | +11.6 | -6.66 | - | RESULT_BALL.md |
| hot | 2000 | 86x86 | 0.3 | 8 -> 10 | +2.81/+2.86 | +11.6 | -6.64 | - | RESULT_BALL.md |
| hot | 2000 | 65x81 | 0.3 | 8 -> 10 | +2.75/+2.82 | +11.5 | -6.58 | - | RESULT_BALL.md |
| hot | 2000 | 86x69 | 0.3 | 8 -> 10 | +2.76/+2.86 | +11.5 | -6.54 | - | RESULT_BALL.md |
| normal | 5000 | 105x131 | 0.3 | 14 -> 20 | +3.43/+2.91 | +9.0 | -6.54 | w top of grid | RESULT_BALL.md |
| hot | 1000 | 86x86 | 0.3 | 6 -> 7 | +2.40/+2.74 | +11.4 | -6.50 | w top of grid | RESULT_BALL.md |
| hot | 4000 | 65x81 | 0.3 | 10 -> 14 | +3.03/+3.09 | +11.1 | -6.50 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 65x65 | 0.3 | 8 -> 10 | +2.70/+2.83 | +11.4 | -6.48 | - | RESULT_BALL.md |
| hot | 4000 | 86x86 | 0.3 | 10 -> 14 | +3.05/+3.11 | +11.1 | -6.48 | w top of grid | RESULT_BALL.md |
| hot | 4000 | 105x131 | 0.3 | 10 -> 14 | +3.06/+3.06 | +11.0 | -6.42 | w top of grid | RESULT_BALL.md |
| normal | 5000 | 86x86 | 0.3 | 14 -> 20 | +3.32/+2.88 | +8.8 | -6.37 | w top of grid | RESULT_BALL.md |
| hot | 1000 | 65x81 | 0.3 | 6 -> 7 | +2.30/+2.70 | +11.2 | -6.35 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 65x52 | 0.3 | 8 -> 10 | +2.62/+2.83 | +11.2 | -6.35 | - | RESULT_BALL.md |
| normal | 5000 | 65x81 | 0.3 | 14 -> 20 | +3.26/+2.84 | +8.7 | -6.31 | w top of grid | RESULT_BALL.md |
| normal | 6000 | 105x131 | 0.3 | 16 -> 22 | +3.25/+2.61 | +8.9 | -6.03 | w top of grid | RESULT_BALL.md |
| hot | 1500 | 105x131 | 0.3 | 7 -> 8 | +2.41/+2.42 | +11.6 | -5.91 | w top of grid | RESULT_BALL.md |
| normal | 6000 | 86x86 | 0.3 | 16 -> 22 | +3.13/+2.56 | +8.7 | -5.84 | w top of grid | RESULT_BALL.md |
| hot | 3000 | 105x131 | 0.3 | 10 -> 12 | +2.69/+2.52 | +11.7 | -5.80 | w top of grid | RESULT_BALL.md |
| normal | 6000 | 65x81 | 0.3 | 16 -> 22 | +3.07/+2.51 | +8.6 | -5.78 | w top of grid | RESULT_BALL.md |
| hot | 3000 | 86x86 | 0.3 | 10 -> 12 | +2.59/+2.48 | +11.5 | -5.63 | w top of grid | RESULT_BALL.md |
| hot | 3000 | 65x81 | 0.3 | 10 -> 12 | +2.52/+2.43 | +11.4 | -5.54 | w top of grid | RESULT_BALL.md |
| hot | 1500 | 86x86 | 0.3 | 7 -> 8 | +2.22/+2.38 | +11.1 | -5.49 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 86x86 | 0.3 | 12 -> 16 | +2.72/+2.68 | +10.7 | -5.39 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 65x81 | 0.3 | 12 -> 16 | +2.69/+2.66 | +10.7 | -5.38 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 105x131 | 0.3 | 12 -> 16 | +2.74/+2.67 | +10.7 | -5.38 | w top of grid | RESULT_BALL.md |
| hot | 1500 | 65x81 | 0.3 | 7 -> 8 | +2.13/+2.34 | +10.9 | -5.35 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 105x131 | 0.3 | 12 -> 14 | +2.45/+2.13 | +11.2 | -4.87 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 86x86 | 0.3 | 12 -> 14 | +2.36/+2.06 | +11.0 | -4.72 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 65x81 | 0.3 | 12 -> 14 | +2.30/+2.01 | +10.9 | -4.64 | w top of grid | RESULT_BALL.md |

## Track B - PRF97 (32 rows)

| regime | rpm | bore x stroke mm | water w | CR dry -> wet | d eta pp M03/CRN | power % | cost/mile % | edge flags | source |
|---|---|---|---|---|---|---|---|---|---|
| normal | 2000 | 65x81 | 0.3 | 9 -> 15 | +4.63/+4.69 | +10.7 | -10.45 | w top of grid | RESULT_BALL.md |
| normal | 2000 | 105x131 | 0.3 | 9 -> 15 | +4.79/+4.68 | +10.7 | -10.42 | w top of grid | RESULT_BALL.md |
| hot | 1500 | 105x131 | 0.3 | 7 -> 9 | +3.30/+3.31 | +12.3 | -8.14 | w top of grid | RESULT_BALL.md |
| hot | 1500 | 65x81 | 0.3 | 7 -> 9 | +3.14/+3.35 | +12.2 | -8.05 | w top of grid | RESULT_BALL.md |
| normal | 1000 | 105x131 | 0.3 | 7 -> 9 | +3.21/+3.34 | +9.0 | -7.94 | w top of grid | RESULT_BALL.md |
| normal | 1500 | 105x131 | 0.3 | 9 -> 12 | +3.49/+3.43 | +9.5 | -7.86 | w top of grid | RESULT_BALL.md |
| hot | 3000 | 65x81 | 0.3 | 9 -> 12 | +3.33/+3.33 | +12.3 | -7.56 | w top of grid | RESULT_BALL.md |
| hot | 3000 | 105x131 | 0.3 | 9 -> 12 | +3.40/+3.38 | +12.2 | -7.52 | w top of grid | RESULT_BALL.md |
| normal | 1000 | 65x81 | 0.3 | 7 -> 9 | +2.87/+3.29 | +8.5 | -7.48 | w top of grid | RESULT_BALL.md |
| normal | 3000 | 105x131 | 0.3 | 12 -> 18 | +3.68/+3.36 | +9.2 | -7.47 | w top of grid | RESULT_BALL.md |
| normal | 2500 | 105x131 | 0.3 | 12 -> 17 | +3.54/+3.23 | +9.4 | -7.32 | w top of grid | RESULT_BALL.md |
| normal | 3000 | 65x81 | 0.3 | 12 -> 18 | +3.48/+3.33 | +8.9 | -7.25 | w top of grid | RESULT_BALL.md |
| normal | 1500 | 65x81 | 0.3 | 9 -> 12 | +3.07/+3.35 | +8.7 | -7.18 | w top of grid | RESULT_BALL.md |
| normal | 2500 | 65x81 | 0.3 | 12 -> 17 | +3.27/+3.17 | +8.9 | -6.94 | w top of grid | RESULT_BALL.md |
| hot | 2500 | 65x81 | 0.3 | 9 -> 12 | +3.01/+3.06 | +11.5 | -6.92 | w top of grid | RESULT_BALL.md |
| hot | 2500 | 105x131 | 0.3 | 9 -> 12 | +3.08/+3.05 | +11.4 | -6.88 | w top of grid | RESULT_BALL.md |
| hot | 1000 | 105x131 | 0.3 | 6 -> 7 | +2.40/+2.49 | +11.2 | -6.42 | w top of grid | RESULT_BALL.md |
| normal | 4000 | 105x131 | 0.3 | 15 -> 21 | +3.28/+2.79 | +9.0 | -6.38 | w top of grid | RESULT_BALL.md |
| normal | 5000 | 105x131 | 0.3 | 15 -> 22 | +3.32/+2.83 | +8.6 | -6.30 | w top of grid | RESULT_BALL.md |
| hot | 1000 | 65x81 | 0.3 | 6 -> 7 | +2.20/+2.49 | +10.9 | -6.18 | w top of grid | RESULT_BALL.md |
| normal | 4000 | 65x81 | 0.3 | 15 -> 21 | +3.07/+2.71 | +8.6 | -6.07 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 65x81 | 0.3 | 12 -> 17 | +2.81/+2.92 | +10.6 | -5.76 | w top of grid | RESULT_BALL.md |
| normal | 6000 | 105x131 | 0.3 | 17 -> 24 | +3.11/+2.50 | +8.5 | -5.75 | w top of grid | RESULT_BALL.md |
| hot | 5000 | 105x131 | 0.3 | 12 -> 17 | +2.81/+2.88 | +10.5 | -5.65 | w top of grid | RESULT_BALL.md |
| normal | 5000 | 65x81 | 0.3 | 17 -> 22 | +2.90/+2.30 | +8.7 | -5.57 | w top of grid | RESULT_BALL.md |
| normal | 6000 | 65x81 | 0.3 | 17 -> 24 | +2.94/+2.42 | +8.2 | -5.53 | w top of grid | RESULT_BALL.md |
| hot | 4000 | 105x131 | 0.3 | 12 -> 15 | +2.56/+2.39 | +10.9 | -5.26 | w top of grid | RESULT_BALL.md |
| hot | 4000 | 65x81 | 0.3 | 12 -> 15 | +2.45/+2.32 | +10.8 | -5.12 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 105x131 | 0.3 | 15 -> 19 | +2.36/+2.15 | +10.5 | -4.56 | w top of grid | RESULT_BALL.md |
| hot | 6000 | 65x81 | 0.3 | 15 -> 19 | +2.27/+2.08 | +10.3 | -4.44 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 105x131 | 0.3 | 9 -> 9 | +1.25/+1.10 | +10.0 | -2.68 | w top of grid | RESULT_BALL.md |
| hot | 2000 | 65x81 | 0.3 | 9 -> 9 | +0.96/+1.01 | +9.2 | -2.00 | w top of grid | RESULT_BALL.md |
