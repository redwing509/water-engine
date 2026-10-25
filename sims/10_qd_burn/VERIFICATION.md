# Module 10 (10_qd_burn) VERIFICATION

Date: 2026-10-24 (Grok Bot, verification-queue item 6). Track A (shared infrastructure; also used by Track B).

Status: **executed + code-verified against independent analytic/limit references** (script `sims/verification/item6_checks.py`, output `results/verification/item6/checks.json`). This is verification only: **not validated** against experiment, and not a second-engine cross-check of the physics.

Result: 7/8 checks pass; FAILED: Q7.

Reproduce: `python -m sims.verification.item6_checks` (about 10 s on 1 core, with the Module 04 step study).

## Method and findings

Calibration point, hand re-evaluation of the Tabaczynski chain at an untested state (CR 16), and exact scaling laws (duration ~ 1/S_L, CAD ~ rpm^0.5) are checked.

**DEFECT FOUND (Q7, latent):** Module 03's QD burn path (`_qd_timescales`/`_qd_burn`/`_qd_burn_angle`, opt-in `--burn-model qd`) mixes units: `duration` and `ca50` are radians but `cad_per_tau_e = tau_e*rpm/60*360` is in degrees, so the ramp is 57.3x too wide (CA90-CA10 = 25.0 'rad' instead of 0.436 rad for a 25 deg duration). Every published Module 03 result uses the default `wiebe` model (checked: all summary.json files say `burn_model: wiebe`), so no published number is affected. Proposed one-line fix (not applied here, Module 03 is owned by the PR 6 integrator work): `cad_per_tau_e = tau_e * omega` (radians), or convert with math.radians. Q8 passes only because x(CA50)=0.5 is symmetric in the ramp width.

**Observation:** Module 10 gives duration ~ S_L^-1 at fixed turbulence while Module 03's production burn law is duration ~ S_L^-0.5 (SPEC). They agree only at the calibration point; this is a modelling difference to resolve before Module 10 replaces Module 03's burn law.

## Checks (tolerance fixed before evaluation)

| id | check | actual | reference | tol | pass |
|---|---|---|---|---|---|
| Q1 | calibration point: CH3OH CR10 w0 S_L 0.72099 -> 25.0 CAD (Module 03 CA10-90) | 25 | 25 | 1e-06 (rel) | PASS |
| Q2 | hand evaluation of the Tabaczynski chain at CR 16, S_L 0.5 | 34.8638 | 34.8638 | 1e-09 (rel) | PASS |
| Q3 | scaling: duration proportional to 1/S_L (m_fuel = 0) | 2 | 2 | 1e-12 (rel) | PASS |
| Q4 | scaling: duration_CAD proportional to rpm^0.5 (u' ~ rpm, lambda ~ rpm^-0.5) | 1.41421 | 1.41421 | 1e-12 (rel) | PASS |
| Q5 | flame area pi B^2 xb^(2/3) (docstring) == code 4 A_bore xb^(2/3) | 0.0146373 | 0.0146373 | 1e-12 (rel) | PASS |
| Q6 | S_L -> 0 limit: burn-up time infinite | True | True | 0 (bool) | PASS |
| Q7 | Module 03 QD ramp: CA90 - CA10 = duration | 25 | 0.436332 | 1e-12 (rel) | **FAIL** |
| Q8 | Module 03 QD ramp: x(CA50) = 0.5 | 0.5 | 0.5 | 1e-12 (rel) | PASS |
