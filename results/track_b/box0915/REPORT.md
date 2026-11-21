# Track B box0915: B2 knock criteria, B4 CR re-optimisation (EXECUTED; CRN = verification; NOT validated)

| chain | crit | w | dry CR/klCR | dry eta | wet CR/klCR | wet CA50 | wet eta | gain pp M03/CRN | engines | power % | cost/mile % ($0.10 / $0) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C2H5OH_hot_humid_evap | LW | 0.288 | 12.0/12.0 | 0.3897 | 16.0/16.0 | 9.4 | 0.4290 | 3.934/3.923 | agree | 29.7 | -7.68 / -9.17 | COST GAIN |
| C2H5OH_hot_humid_evap | DE | 0.288 | 10.5/10.5 | 0.3804 | 13.0/13.0 | 14.3 | 0.4088 | 2.840/2.850 | agree | 26.9 | -5.42 / -6.95 | COST GAIN |
| CH3OH_hot_humid_evap | LW | 0.235 | 8.0/8.0 | 0.3502 | 16.0/16.0 | 10.9 | 0.4275 | 7.731/7.708 | agree | 37.4 | -17.63 / -18.09 | COST GAIN |
| CH3OH_hot_humid_evap | DE | 0.235 | 10.5/10.5 | 0.3779 | 13.0/13.0 | 14.2 | 0.4077 | 2.973/2.965 | agree | 27.5 | -6.77 / -7.29 | COST GAIN |
| CH3OH_normal_liquid | LW | 0.132 | 17.0/17.0 | 0.4238 | 17.0/17.0 | 9.6 | 0.4344 | 1.065/1.050 | agree | 8.4 | -2.18 / -2.45 | COST GAIN |
| CH3OH_normal_liquid | DE | 0.132 | 12.5/12.5 | 0.4024 | 15.5/15.5 | 14.5 | 0.4235 | 2.114/2.101 | agree | 9.5 | -4.73 / -4.99 | COST GAIN |
| PRF87_normal_liquid | LW | 0.1 | 9.0/9.0 | 0.3710 | 9.5/9.5 | 14.2 | 0.3789 | 0.794/0.798 | agree | 3.4 | -1.92 / -2.09 | COST GAIN |
| PRF87_normal_liquid | DE | 0.1 | 9.0/9.0 | 0.3710 | 9.5/9.5 | 14.2 | 0.3789 | 0.794/0.798 | agree | 3.4 | -1.92 / -2.09 | COST GAIN |

**How to read this (labels added 2026-10-25 PM, no number changed):**
* B4 gain = best wet point at its OWN knock-limited CR minus best dry point at the dry knock-limited CR, same knock criterion. Most of the gain comes from RAISING CR (knock relief by the water), not from water at fixed CR (fixed-CR chain gains: see `chain_gain_pp` in b4_cr_reopt.csv, +0.8 to +1.8 pp).
* power % = IMEP change; in humid_evap it also includes evaporative charge cooling (T_IVC ~400 -> ~312 K hot, ~+18-20 % trapped mass at fixed p_IVC; no gas-exchange model). Indicated upper bounds, not brake power.
* CR grid 9-16 (job spec): wet klCR = 16 means grid-capped, the true klCR may be higher (C2H5OH_hot_humid_evap, CH3OH_hot_humid_evap, CH3OH_normal_liquid).
* CH3OH_hot_humid_evap LW: the dry knock-limited CR under Livengood-Wu is 8 (vs 10.5 under Douaud-Eyzat), so its +7.7 pp is mostly CR 8 -> 16; the DE row (+3.0 pp) is the conservative number.
* Status: EXECUTED in Module 03 and cross-checked by M03-CRN (two in-repo engines, same toolchain; M03-CRN has no knock model, knock limit is Module 03 only). NOT validated against experiment.
