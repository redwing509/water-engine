# Module 01 (01_energy_audit) VERIFICATION

Date: 2026-10-24 (Grok Bot, verification-queue item 6). Track A (shared infrastructure; also used by Track B).

Status: **executed + code-verified against independent analytic/limit references** (script `sims/verification/item6_checks.py`, output `results/verification/item6/checks.json`). This is verification only: **not validated** against experiment, and not a second-engine cross-check of the physics.

Result: 11/11 checks pass.

Reproduce: `python -m sims.verification.item6_checks` (about 10 s on 1 core, with the Module 04 step study).

## Method and findings

Faraday, NIST LHV, analytic Monte-Carlo moments and ideal-efficiency limit are independent of the module code path (hand formulas and published constants). No step/grid parameter exists (algebraic ledger), so GCI does not apply. The Monte-Carlo mean is checked against the analytic product of uniform means within 4 standard errors.

## Checks (tolerance fixed before evaluation)

| id | check | actual | reference | tol | pass |
|---|---|---|---|---|---|
| F1 | H2 mass flow 20 A, Faraday law, IUPAC M_H2 | 2.08944e-07 | 2.08931e-07 | 0.0001 (rel) | PASS |
| L-H2 | LHV H2 vs NIST-derived value | 1.19953e+08 | 1.1996e+08 | 0.01 (rel) | PASS |
| L-CH4 | LHV CH4 vs NIST-derived value | 5.00254e+07 | 5.003e+07 | 0.01 (rel) | PASS |
| L-CH3OH | LHV CH3OH vs NIST-derived value | 1.99307e+07 | 1.993e+07 | 0.01 (rel) | PASS |
| L-C2H5OH | LHV C2H5OH vs NIST-derived value | 2.68029e+07 | 2.681e+07 | 0.01 (rel) | PASS |
| L-H2O | water LHV is exactly 0 (limit) | 0 | 0 | 1 (abs) | PASS |
| MC1 | loop gain MC mean vs analytic product of means (tol = 4 standard errors) | 0.121826 | 0.121875 | 0.000349307 (abs) | PASS |
| MC2 | loop gain sample max <= analytic max 0.45*0.75*0.80 = 0.27 | True | True | 0 (bool) | PASS |
| K1 | ideal-efficiency kit: net shaft = H2 LHV power - electric (closed form) | -250.937 | -250.937 | 1e-09 (rel) | PASS |
| K2 | ideal-efficiency kit is still a net loss (no free energy) | True | True | 0 (bool) | PASS |
| K3 | LHV voltage of H2 = 1.25 V (textbook 1.253 V) | 1.25309 | 1.253 | 0.005 (rel) | PASS |
