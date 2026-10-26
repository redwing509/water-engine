# X5 / module 03 step-convergence study: results

Verification status: **not yet peer-review verified. The pre-registered criteria A1, A1-pmax, A2 and A5 FAILED.**

- Criteria: `ACCEPTANCE_CRITERIA.md`, commit 5335606. It was pushed 2026-10-24 13:44 PDT, before any run.
- Driver: `gci_study.py`. Three driver-only fixes were made after the criteria were pushed: sys.path for unpickling worker exceptions, passing per-fuel Module 02 fits to module 03, and JSON encoding of numpy scalars. No criterion, tolerance, design point or step was changed.
- Run: mail, 2026-10-24 13:51–13:53 PDT, 66 s wall time, 4 processes. Python 3.12.3, Cantera 3.2.0, CoolProp 8.0.0. Ran under the ai-job lock as `grokbot` on resource `water-engine`.
- Raw data: `results/raw.json` and `results/report.json`.
- This is code verification only. Nothing here is validation against experiment.

## Verdict per criterion (no criterion was tuned after the run)

| Criterion | Result | Notes |
|---|---|---|
| A1: GCI_fine ≤ 0.1% and \|f(0.5°) − f_ext\| ≤ 0.5% (eff, IMEP, T_EVO) | **FAIL** | 15 of 36 cases. In most of them the GCI is undefined because the three finest steps converge non-monotonically or with p ≤ 0. One is defined and exceeds the limit: M03 C2H5OH/water_majority T_EVO, GCI = 0.18%. |
| A1-pmax: GCI ≤ 1% | **FAIL** | One case: M03 C2H5OH/best_dry, oscillatory (p < 0). |
| A2: observed order p in [1.5, 2.5], monotone | **FAIL** | All 36 eff/IMEP/T_EVO cases. Observed p is between −0.8 and 1.0. The scheme does not show its formal second order. |
| A3: \|energy closure\| ≤ 1e-3 at 0.25° | PASS | Maximum \|closure\| at 0.25° is 2.1e-5. |
| A4: ideal-Otto error ≤ 1e-3 at 0.5°, not growing under refinement | PASS | Error at 0.5° is −3.5e-5 (CR 16) and −4.6e-5 (CR 24). It decreases monotonically under refinement and levels off near −3e-5, which is consistent with the finite 1° burn rather than with discretisation. |
| A5: extrapolated X5 − M03 ≤ 1% | **FAIL (undefined)** | f_ext does not exist where A1/A2 fail. The raw gap at each step is +0.72% to +0.76% on eff and IMEP. That gap is step-independent, so it comes from a modelling difference, not from discretisation. |

## What the data does show (descriptive, not a pass)

- **Step sensitivity is small.** Across all points, engines and quantities, the largest \|f(0.5°) − f(0.25°)\| / f is 9.2e-5. From 2° to 0.25° the change is at most 6.8e-4 (T_EVO, CH3OH/water_majority).
- **Convergence is not asymptotic.** Low or negative observed order at this size of change suggests a non-smooth or first-order element, or an iteration noise floor of about 1e-5 relative. Candidates are event handling not aligned to the step (Wiebe start/end, EVO, evaporation completion), the sub-step knock integral, and inner equilibrium or property solve tolerances. Not yet diagnosed.
- **The two engines share an algorithm.** The ideal-Otto results of X5 and M03 are bit-identical, which confirms that X5 is not method-independent. X5 does not count as a second engine under the 2-engine rule.
- **The X5 − M03 gap of about 0.74% is constant across steps.** It comes from a difference in model content (thermo, fuel or wall-heat bookkeeping), not from numerics. Its cause has not been found.

## What is needed to reach "verified"

1. Find the cause of the sub-second-order convergence. Check event alignment, iteration tolerances and the knock-integral sub-stepping. Then rerun this study unchanged.
2. Alternatively, pre-register a revised criterion set with a justification written before any rerun, for example a noise-floor-aware criterion. It must not be fitted to these results.
3. Explain the 0.74% X5 − M03 bias.
4. Build a method-independent second engine, for example an implicit/adaptive ODE solver or a different thermo path. This is required before any 2-engine claim.
