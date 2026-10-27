# Track A cool_frac step 3c: two knock engines + two efficiency engines, hot cf0.5/cf0.7 (box)

klCR M03 = highest CR before the first M03 LW >= 1; klCR E2 = highest CR before the first full CRECK end-gas knock (rows not run are skipped); used CR = min (both knock engines must agree it is knock-free). Best row = highest M03 eta with CR <= used CR. Cost at 0.10 USD/gal water (0 USD/gal in brackets), both efficiency engines (M03 / M03-CRN, DEI latent credit). EXECUTED, not validated. CAVEAT: knock engine 2 is ranking-validated only (absolute +2-2.5 CR offset vs M03 on PRF), so a dry klCR lowered by engine 2 alone makes the dry baseline conservative; do not headline until the offset is resolved. C1 = |d_eta| <= 1.5 pp and |p_max ratio - 1| <= 5 %.

| cf | fuel | case | klCR M03 | klCR E2 | used CR | eta M03 / CRN | C1 | d_eta vs dry pp M03 / CRN | power % M03 / CRN | cost/mile % M03 / CRN ($0) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 05 | C2H5OH | humid_evap w 0.55 bound i | 26 | 26 | 26 | 0.4648 / 0.4652 (CR 26) | FAIL | +5.86 / +5.97 | +15.8 / +16.1 | -8.28 / -8.51 (-12.61 / -12.83) | COST GAIN - NOT 2-engine (C1 fail) |
| 05 | C2H5OH | humid_evap w 0.55 bound ii | 26 | 26 | 26 | 0.4507 / 0.4664 (CR 26) | FAIL | +4.45 / +6.09 | +12.3 / +16.4 | -5.41 / -8.75 (-9.88 / -13.05) | COST GAIN - NOT 2-engine (C1 fail) |
| 05 | C2H5OH | humid_evap w 0.6 bound i | 26 | 24 | 24 | 0.4610 / 0.4570 (CR 24) | FAIL | +5.49 / +5.15 | +15.2 / +14.4 | -6.54 / -5.88 (-11.90 / -11.27) | COST GAIN - NOT 2-engine (C1 fail) |
| 05 | C2H5OH | humid_evap w 0.6 bound ii | 26 | 24 | 24 | 0.4434 / 0.4559 (CR 23) | FAIL | +3.72 / +5.04 | +11.0 / +14.4 | -2.81 / -5.64 (-8.39 / -11.05) | COST GAIN - NOT 2-engine (C1 fail) |
| 05 | C2H5OH | dry DEI | 20 | 11 | 11 | 0.4062 / 0.4055 (CR 11) | pass | baseline | | | |
| 05 | CH3OH | humid_evap w 0.55 bound i | 26 | 26 | 26 | 0.4792 / 0.4705 (CR 26) | FAIL | +3.96 / +3.08 | +11.4 / +9.4 | -6.22 / -4.46 (-8.27 / -6.54) | COST GAIN - NOT 2-engine (C1 fail) |
| 05 | CH3OH | humid_evap w 0.55 bound ii | 26 | 26 | 26 | 0.4430 / 0.4469 (CR 21) | FAIL | +0.35 / +0.72 | +4.0 / +4.9 | +1.43 / +0.58 (-0.79 / -1.61) | fuel saved, but water cost eats it - NOT 2-engine (C1 fail) |
| 05 | CH3OH | humid_evap w 0.6 bound i | 26 | 24 | 24 | 0.4700 / 0.4584 (CR 24) | FAIL | +3.05 / +1.87 | +9.6 / +6.9 | -3.92 / -1.44 (-6.48 / -4.07) | COST GAIN - NOT 2-engine (C1 fail) |
| 05 | CH3OH | humid_evap w 0.6 bound ii | 25 | 24 | 24 | 0.4372 / 0.4348 (CR 19) | FAIL | -0.24 / -0.50 | +3.2 / +2.5 | +3.30 / +3.92 (+0.55 / +1.15) | no cost gain - NOT 2-engine (C1 fail) |
| 05 | CH3OH | dry DEI | 20 | 20 | 20 | 0.4396 / 0.4397 (CR 19) | pass | baseline | | | |
| 07 | C2H5OH | humid_evap w 0.55 bound i | 26 | 26 | 26 | 0.4675 / 0.4647 (CR 26) | pass | +4.42 / +4.19 | +13.3 / +12.7 | -4.96 / -4.50 (-9.44 / -9.01) | COST GAIN |
| 07 | C2H5OH | humid_evap w 0.55 bound ii | 26 | 26 | 26 | 0.4449 / 0.4651 (CR 25) | FAIL | +2.16 / +4.23 | +8.0 / +13.0 | -0.13 / -4.60 (-4.85 / -9.10) | COST GAIN - NOT 2-engine (C1 fail) |
| 07 | C2H5OH | humid_evap w 0.6 bound i | 26 | 24 | 24 | 0.4571 / 0.4554 (CR 24) | FAIL | +3.37 / +3.26 | +11.1 / +10.8 | -1.74 / -1.50 (-7.37 / -7.15) | COST GAIN - NOT 2-engine (C1 fail) |
| 07 | C2H5OH | humid_evap w 0.6 bound ii | 26 | 24 | 24 | 0.4366 / 0.4554 (CR 24) | FAIL | +1.32 / +3.25 | +6.1 / +10.8 | +2.87 / -1.50 (-3.03 / -7.14) | fuel saved, but water cost eats it - NOT 2-engine (C1 fail) |
| 07 | C2H5OH | dry DEI | 20 | 13 | 13 | 0.4234 / 0.4228 (CR 13) | pass | baseline | | | |
| 07 | CH3OH | humid_evap w 0.55 bound i | 26 | 26 | 26 | 0.4696 / 0.4672 (CR 26) | FAIL | +0.89 / +0.65 | -0.3 / -0.9 | +0.30 / +0.81 (-1.89 / -1.39) | power loss - NOT 2-engine (C1 fail) |
| 07 | CH3OH | humid_evap w 0.55 bound ii | 26 | 26 | 26 | 0.4365 / 0.4485 (CR 20) | FAIL | -2.43 / -1.22 | -6.3 / -3.7 | +7.91 / +5.00 (+5.56 / +2.71) | power loss - NOT 2-engine (C1 fail) |
| 07 | CH3OH | humid_evap w 0.6 bound i | 26 | 24 | 24 | 0.4578 / 0.4544 (CR 24) | FAIL | -0.29 / -0.63 | -2.5 / -3.2 | +3.39 / +4.15 (+0.64 / +1.38) | power loss - NOT 2-engine (C1 fail) |
| 07 | CH3OH | humid_evap w 0.6 bound ii | 26 | 24 | 24 | 0.4290 / 0.4367 (CR 23) | FAIL | -3.17 / -2.40 | -8.5 / -6.8 | +10.34 / +8.39 (+7.40 / +5.50) | power loss - NOT 2-engine (C1 fail) |
| 07 | CH3OH | dry DEI | 20 | 20 | 20 | 0.4607 / 0.4607 (CR 19) | pass | baseline | | | |
