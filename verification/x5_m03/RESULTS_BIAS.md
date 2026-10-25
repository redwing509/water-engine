# Item 2 result: the +0.74 % X5 - M03 bias (verification queue 2026-10-24)

Status: **EXECUTED + VERIFIED (agreement criterion met)**. Not VALIDATED against experiment.
Criterion pre-registered in BIAS_ITEM2.md (commit 378b63c) before this run.

## Root cause (X5 bugs, not M03)
1. `h_ref` was read from `standard_enthalpies_RT` with the gas at WATER_T but multiplied by R*T_REF: +9.79 J (0.67 % of Q_avail).
2. The enthalpy reference `h_ref` was used as the internal-energy reference: dn*R*T_ref = +2.89 J (0.20 %).
Together 12.68 J = 0.87 % of Q_avail, which gives the observed ~0.74 % in eff/IMEP after the cycle. Fix: `h_ref = P.h(T_REF)`, `u_ref0 = P.u(T_REF)`, and use u_ref in u_lat, U_ivc and evaluate.

## Rerun (gci_study.py unchanged, results_bias/)
| Check | Pre-registered | Result |
|---|---|---|
| max abs(X5-M03)/M03 at 0.5 deg, eff/IMEP/T_EVO/pmax, 6 points | <= 1e-4 | **3.9e-11** (C2H5OH/best_overall T_EVO) PASS |
| Otto limit eff X5 vs M03 | <= 1e-4 | 0.0 PASS |
| A1 / A3 / A4 | unchanged from RESULTS_FIX | PASS / PASS / PASS |
| A2, A1-pmax, A5 | unchanged | FAIL only at CH3OH/water_majority (same p = 1.394 in both codes) |

## Interpretation (frank)
- The bias is gone: X5 and M03 now agree to round-off. That also shows X5 is a line-for-line re-implementation of the M03 scheme. It is a useful code-level check, but it is **not an independent second engine** for the 2-engine rule. A method-independent engine (queue item 3) is still needed.
- Published X5 numbers in results/xcheck/cycle.md are about 0.7 % high and should be regenerated when this branch merges.
- Open SPEC question (not changed here): the model releases 0.98*LHV (an enthalpy, liquid basis) into sensible U, which is about 0.2 % inconsistent with dU_c. This needs a decision from Claude/James.
