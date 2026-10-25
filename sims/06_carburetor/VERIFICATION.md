# Module 06 (06_carburetor) VERIFICATION

Date: 2026-10-24 (Grok Bot, verification-queue item 6). Track A (shared infrastructure; also used by Track B).

Status: **executed + code-verified against independent analytic/limit references** (script `sims/verification/item6_checks.py`, output `results/verification/item6/checks.json`). This is verification only: **not validated** against experiment, and not a second-engine cross-check of the physics.

Result: 10/10 checks pass.

Reproduce: `python -m sims.verification.item6_checks` (about 10 s on 1 core, with the Module 04 step study).

## Method and findings

Choked flux, venturi mass and stagnation-enthalpy round trips, the two analytic jet limits (Bernoulli mu->0, Hagen-Poiseuille large mu), the quadratic residual and the d^2-law lifetime are all closed form. The jet sizing rounds to 0.01 mm drill sizes, hence the 3 % tolerance on J5. Algebraic/closed-form model: GCI does not apply.

## Checks (tolerance fixed before evaluation)

| id | check | actual | reference | tol | pass |
|---|---|---|---|---|---|
| N1 | choked flux = Cd rho* a* (independent isentropic-relation form) | 224.606 | 224.606 | 1e-10 (rel) | PASS |
| N2 | venturi mass conservation: Cd A rho V = mdot | 0.035281 | 0.035281 | 1e-06 (rel) | PASS |
| N3 | venturi stagnation enthalpy: T + V^2/(2cp) = T0 | 300 | 300 | 1e-09 (rel) | PASS |
| J1 | jet mu->0 limit = Bernoulli Cd A sqrt(2 rho dp) | 0.0010438 | 0.0010438 | 1e-06 (rel) | PASS |
| J2 | jet viscous limit = Hagen-Poiseuille pi rho d^4 dp/(128 mu L) | 7.70672e-07 | 7.70672e-07 | 0.001 (rel) | PASS |
| J3 | jet residual: a mdot^2 + b mdot = dp | 2000 | 2000 | 1e-10 (rel) | PASS |
| J4 | float head >= signal -> zero flow (limit) | 0 | 0 | 0 (abs) | PASS |
| J5 | sized jet (0.01 mm drill rounding) delivers requested flow within rounding | 9.93918e-05 | 0.0001 | 0.03 (rel) | PASS |
| E1 | d2-law lifetime = D0^2/K, K = 8k ln(1+B)/(rho_l cp) | 0.286488 | 0.286488 | 1e-12 (rel) | PASS |
| V1 | WFR valve: fully open at 15 kPa, closed at 25 kPa, linear midpoint 0.5 | True | True | 0 (bool) | PASS |
