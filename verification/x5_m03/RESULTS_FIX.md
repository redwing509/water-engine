# Item 1 re-run: step-convergence study after the pre-registered fix (FIX_PREREG.md)

Code: c0385a7 (`verify/x5-m03-step-convergence-20261024`). Script: `gci_study.py` unchanged. Output: `results_fix/`. Run 2026-10-24 14:17 PDT, box, 4 processes, 26 s wall time.
Criteria: `ACCEPTANCE_CRITERIA.md`, unchanged.

## Verdict
| criterion | baseline (a229803) | after fix |
|---|---|---|
| A1 GCI_fine ≤ 0.1 %, production-step error ≤ 0.5 % (eff, IMEP, T_EVO) | FAIL | **PASS** (max GCI 1.4e-5 relative) |
| A1-pmax GCI ≤ 1 % | FAIL | **FAIL**: M03 CH3OH/water_majority, oscillatory pmax, so no GCI is defined |
| A2 observed order in [1.5, 2.5] | FAIL (p −0.8…1.0) | **FAIL, 1 of 6 points**: CH3OH/water_majority (M03 eff/IMEP p = 1.39, T_EVO 3.63; X5 eff/IMEP 1.17). The other 5 points give p = 1.58–2.36 for both engines |
| A3 closure ≤ 1e-3 | PASS | PASS |
| A4 ideal Otto | PASS | PASS (error −3.0e-5 at CR16 and −4.0e-5 at CR24, at 0.25°) |
| A5 X5−M03 ≤ 1 % (extrapolated) | FAIL (no extrapolation possible) | **FAIL only where pmax has no extrapolated value** (water_majority). Every defined gap is ≤ 0.76 % and **step-invariant** (eff +0.725…+0.758 %, T_EVO +0.58…+0.63 %, pmax +0.40…+0.50 %) |

Module 03 and X5 are now **code-verified for eff, IMEP and T_EVO at 5 of 6 design points**. This is not validated against experiment.
CH3OH/water_majority stays "partial", as predicted in FIX_PREREG.md: the absolute changes there are < 3e-5 in eff, but the order is irregular, most likely because the saturation cap switches on and off inside a step.
The production step (0.5°) was already accurate. The fix moves production efficiencies by −0.007 % to +0.007 % relative, so no published module 03 conclusion changes.

## Detail
| engine | point | p eff old→new | p T_EVO old→new | GCI eff new | GCI pmax new | eff(0.5°) old→new (shift) |
|---|---|---|---|---|---|---|
| M03 | CH3OH/best_dry | 0.84→2.01 | 0.05→2.00 | 1.4e-06 | 7.7e-07 | 0.42067→0.42069 (+0.0032 %) |
| X5 | CH3OH/best_dry | 0.84→2.01 | 0.06→2.00 | 1.4e-06 | 8.1e-07 | 0.42381→0.42382 (+0.0032 %) |
| M03 | CH3OH/best_overall | -0.80→2.12 | -0.06→2.04 | 2.0e-06 | 1.5e-07 | 0.45427→0.45430 (+0.0055 %) |
| X5 | CH3OH/best_overall | -0.53→1.74 | 0.20→1.86 | 5.0e-06 | 5.4e-07 | 0.45761→0.45763 (+0.0056 %) |
| M03 | CH3OH/water_majority | 0.30→1.39 | 1.01→3.63 | 4.7e-06 | — | 0.44610→0.44607 (-0.0068 %) |
| X5 | CH3OH/water_majority | -0.23→1.17 | 0.99→1.53 | 1.4e-05 | 2.1e-05 | 0.44947→0.44944 (-0.0064 %) |
| M03 | C2H5OH/best_dry | 0.73→2.01 | -0.15→2.00 | 1.5e-06 | 1.2e-05 | 0.44545→0.44547 (+0.0046 %) |
| X5 | C2H5OH/best_dry | 0.73→2.01 | -0.13→2.00 | 1.5e-06 | 1.5e-05 | 0.44874→0.44876 (+0.0047 %) |
| M03 | C2H5OH/best_overall | -0.65→2.35 | 0.15→2.12 | 1.4e-06 | 1.2e-06 | 0.45290→0.45293 (+0.0072 %) |
| X5 | C2H5OH/best_overall | -0.32→1.75 | 0.55→1.86 | 5.6e-06 | 3.6e-06 | 0.45618→0.45621 (+0.0073 %) |
| M03 | C2H5OH/water_majority | 0.91→2.36 | 0.03→2.10 | 1.2e-06 | 1.3e-06 | 0.44893→0.44896 (+0.0054 %) |
| X5 | C2H5OH/water_majority | 0.93→1.58 | -0.23→1.77 | 8.1e-06 | 4.3e-06 | 0.45221→0.45223 (+0.0055 %) |

| point | X5−M03 eff old→new | T_EVO old→new | pmax old→new |
|---|---|---|---|
| CH3OH/best_dry | +0.745 %→+0.745 % | +0.595 %→+0.603 % | +0.479 %→+0.479 % |
| CH3OH/best_overall | —→+0.734 % | —→+0.603 % | +0.476 %→+0.476 % |
| CH3OH/water_majority | —→+0.758 % | +0.631 %→+0.631 % | +0.496 %→— |
| C2H5OH/best_dry | +0.739 %→+0.739 % | —→+0.584 % | —→+0.402 % |
| C2H5OH/best_overall | —→+0.725 % | +0.583 %→+0.603 % | +0.483 %→+0.482 % |
| C2H5OH/water_majority | +0.732 %→+0.731 % | —→+0.608 % | +0.474 %→+0.474 % |

"—" means not defined (non-monotone triple, so no Richardson extrapolation).
The diagnostic variant runs are in `diag/diag_results_run1.json` (8 variants) and `diag/diag_results.json` (base, evapfix, anchor+evapfix).
The X5−M03 bias does not depend on step size, so it comes from a model or property difference, not from the integrator. See item 2.
