# Module 04 (04_six_stroke) VERIFICATION

Date: 2026-10-24 (Grok Bot, verification-queue item 6). Track A (shared infrastructure; also used by Track B).

Status: **executed + code-verified against independent analytic/limit references** (script `sims/verification/item6_checks.py`, output `results/verification/item6/checks.json`). This is verification only: **not validated** against experiment, and not a second-engine cross-check of the physics.

Result: 7/7 checks pass.

Reproduce: `python -m sims.verification.item6_checks` (about 10 s on 1 core, with the Module 04 step study).

## Method and findings

Pump work is checked against the incompressible v*dp estimate; zero-water and geometry limits are closed-form. Step convergence: the crank-angle RK2 integrator was run at 2, 1 and 0.5 deg for two cases and the Roache GCI computed on net extra work (refinement ratio 2). Observed order p = 2.02 (adiabatic, close to the formal 2) and 4.19 (Woschni, super-convergent, error already at round-off level); GCI_fine = 8.2e-06 and 3.3e-07, i.e. the quick/production step sizes are converged far below 1 %.

## Checks (tolerance fixed before evaluation)

| id | check | actual | reference | tol | pass |
|---|---|---|---|---|---|
| P1 | isentropic pump work ~ v dp (incompressible estimate, 0.5 %) | 9911.22 | 9932.87 | 0.005 (rel) | PASS |
| P2 | shaft work = w_s/eta_pump | 16518.7 | 16518.7 | 1e-12 (rel) | PASS |
| G1 | geometry V(BDC)/V(TDC) = CR | 14 | 14 | 1e-12 (rel) | PASS |
| GCI-EVC220_10mg_adiabatic | RK2 crank-step GCI (fine 0.5 deg) on net extra work, EVC220_10mg_adiabatic: GCI_fine <= 1 % | 8.24058e-06 | 0 | 0.01 (abs) | PASS |
| GCI-EVC260_10mg_woschni | RK2 crank-step GCI (fine 0.5 deg) on net extra work, EVC260_10mg_woschni: GCI_fine <= 1 % | 3.29999e-07 | 0 | 0.01 (abs) | PASS |
| Z1 | zero water, adiabatic: |net extra work| <= 0.2 % of trapped enthalpy (reversible gas spring) | 4.47123e-07 | 0 | 0.002 (abs) | PASS |
| Z2 | zero water: EVO5 at mirror angle 720 - EVC (+-8 deg) | 500 | 500 | 8 (abs) | PASS |

## Step study (GCI, Roache 1998, Fs = 1.25)

| case | 2 deg | 1 deg | 0.5 deg | p | GCI_fine | extrapolated |
|---|---|---|---|---|---|---|
| EVC220_10mg_adiabatic | -9.265806 J | -9.265043 J | -9.264855 J | 2.02 | 8.24e-06 | -9.264794 J |
| EVC260_10mg_woschni | -15.887282 J | -15.885953 J | -15.885880 J | 4.19 | 3.30e-07 | -15.885876 J |
