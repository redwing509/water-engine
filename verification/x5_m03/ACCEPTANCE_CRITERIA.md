# Step-convergence and energy-closure verification: module 03 and X5 (pre-registered)

These criteria were committed and pushed **before** any run of `gci_study.py`. The base is `xcheck/cycle` @ 0d47bc7.

**Verification status: not yet peer-review verified.** This study is the step that would move module 03 and X5 from "partial" toward "code-verified".

## What is being tested

| Engine | Source | Integrator |
|---|---|---|
| module 03 | `sims/03_engine_cycle/run.py`, `integrate_cycle` | crank-angle RK2 (explicit midpoint), production step 0.5° CA |
| X5 | `scripts_run/xcheck.py`, `integrate` | independent re-implementation of the same SPEC §6 algorithm, same scheme and step |

Both are run on the six design points of `results/xcheck/cycle.md`:

- CH3OH: best_dry, best_overall, water_majority
- C2H5OH: best_dry, best_overall, water_majority

Both are also run on the ideal-Otto case at CR = 16 and CR = 24.

## Method

CA50 and the 10–90 % burn duration are found once per engine at the production step, using that engine's own retard search. They are then **frozen**, and the cycle is re-integrated at steps of 2, 1, 0.5 and 0.25° CA (refinement ratio r = 2). The GCI follows Celik et al., J. Fluids Eng. 130 (2008) 078001, with Fs = 1.25 and the three finest steps.

## Quantities

- Gross indicated efficiency (`eff`)
- IMEP
- T at EVO (`T_EVO`)
- Peak pressure (`pmax`)
- Energy-closure fraction (`closure`)

## Criteria (stated before running)

- **A1 (discretisation error):** for every engine, point and quantity among eff, IMEP and T_EVO, both of these hold:
  - GCI_fine at 0.25° ≤ 0.1 %;
  - |f(0.5°) − f_ext| / |f_ext| ≤ 0.5 %, i.e. the production step is converged to engineering accuracy.
- **A1-pmax:** GCI_fine for pmax ≤ 1 %. This is looser because pmax is sampled at nodes.
- **A2 (order):** the observed order p, from 1, 0.5 and 0.25°, lies in [1.5, 2.5] for eff, IMEP and T_EVO. The scheme is nominally 2nd order. If the convergence is monotone but the order is anomalous, the result is reported as such and counts as FAIL.
- **A3 (first law):** |closure| ≤ 1e-3 of fuel energy at 0.25°, for every point and both engines.
- **A4 (analytic benchmark, ideal Otto, γ = 1.4):** |eff − (1 − CR^(1−γ))| ≤ 1e-3 at 0.5°, and the error does not grow under refinement.
- **A5 (code cross-check):** the Richardson-extrapolated relative difference between X5 and module 03 is ≤ 1 % for eff, IMEP, T_EVO and pmax, at every point.
  - **Disclosure:** the 1 % tolerance was chosen *after* the X5 table (2026-10-24 02:00 PDT) was public, so A5 is not blind.
  - The test also reports whether the X5 − module 03 gap is step-invariant. A step-invariant gap means the difference is in the model, not the discretisation.

## What a PASS does and does not mean

- **A1–A4 all PASS:** the engine is *code-verified* for these outputs. It is still **not validated**, because there is no engine-experiment comparison.
- **A5 PASS:** the shared algorithm is implemented consistently twice. X5 uses the *same model and scheme*, so it is **not an independent second engine** under the 2-engine rule, whatever A5 shows. The 2-engine rule needs a method-independent engine; the cfd branch is a candidate, but it is not verified.
- **Any FAIL:** the engine stays "partial", and the failure is reported as-is. Nothing is tuned.
