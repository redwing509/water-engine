# Module dual_temp (dual_temp) VERIFICATION

Date: 2026-10-24 (Grok Bot, verification-queue item 6). Track A (shared infrastructure; also used by Track B).

Status: **executed + code-verified against independent analytic/limit references** (script `sims/verification/item6_checks.py`, output `results/verification/item6/checks.json`). This is verification only: **not validated** against experiment, and not a second-engine cross-check of the physics.

Result: 11/11 checks pass.

Reproduce: `python -m sims.verification.item6_checks` (about 10 s on 1 core, with the Module 04 step study).

## Method and findings

Regime values vs their cited bands; the `run_m03` monkey-patch is shown to reach every Module 03 function whose default argument is `DEFAULTS` (so the hot regime really changes wall T everywhere); and the `port_film_wall_T` Raoult bubble point / h_fg chain reproduces NIST normal boiling points (Clausius-Clapeyron shifted from 1 atm to the module's 1.0 bar) and IAPWS-95 h_fg. Not a discretised model: GCI does not apply.

## Checks (tolerance fixed before evaluation)

| id | check | actual | reference | tol | pass |
|---|---|---|---|---|---|
| R1 | normal coolant 90 C = 363.15 K (MAHLE/VW SSP 222 85-95 C band) | 363.15 | 363.15 | 0 (abs) | PASS |
| R2 | hot coolant 115 C = 388.15 K (inside 95-110 C mapped + pressurised margin; SAE 960271) | 388.15 | 388.15 | 0 (abs) | PASS |
| R3 | port wall = coolant in both regimes (stated assumption) | True | True | 0 (bool) | PASS |
| R4 | hot >= normal for coolant, chamber wall, port wall, max intake | True | True | 0 (bool) | PASS |
| R5 | chamber wall in Heywood ch.12 gas-side band 400-600 K | True | True | 0 (bool) | PASS |
| P0 | normal regime chamber wall equals unpatched Module 03 default (normal = baseline) | 450 | 450 | 0 (abs) | PASS |
| P1 | run_m03 wall_T patch seen by all 19 Module 03 functions defaulting to DEFAULTS | True | True | 0 (bool) | PASS |
| B-CH3OH | pure CH3OH bubble point at 1.0 bar vs NIST Tb(1 atm) shifted by Clausius-Clapeyron | 337.298 | 337.336 | 0.2 (abs) | PASS |
| B-C2H5OH | pure C2H5OH bubble point at 1.0 bar vs NIST Tb(1 atm) shifted by Clausius-Clapeyron | 351.237 | 351.095 | 0.2 (abs) | PASS |
| B-H2O | pure water bubble point at 1.0 bar = 372.76 K (IAPWS) | 372.756 | 372.76 | 0.1 (abs) | PASS |
| H-H2O | water h_fg at 373.124 K = 2256.4 kJ/kg (IAPWS-95) | 2.25647e+06 | 2.2564e+06 | 0.001 (rel) | PASS |
