# Module 11 (11_spray_flame) VERIFICATION

Date: 2026-10-24 (Grok Bot, verification-queue item 6). Track A (shared infrastructure; also used by Track B).

Status: **executed + code-verified against independent analytic/limit references** (script `sims/verification/item6_checks.py`, output `results/verification/item6/checks.json`). This is verification only: **not validated** against experiment, and not a second-engine cross-check of the physics.

Result: 8/8 checks pass.

Reproduce: `python -m sims.verification.item6_checks` (about 10 s on 1 core, with the Module 04 step study).

## Method and findings

No-liquid limits, the Zeldovich heat-sink factor, the Metghalchi-Keck identity and a closed-form inverse of the MIE criterion (max SMD for 50 mJ) compared with the module's bisection (an independent solution path; agreement 1e-9). No discretisation parameter: GCI does not apply (bisection tolerance is the only numerical parameter and is covered by S7).

## Checks (tolerance fixed before evaluation)

| id | check | actual | reference | tol | pass |
|---|---|---|---|---|---|
| S1 | no liquid: S_BL = S_L exactly (tau_e = 0) | 1.2 | 1.2 | 1e-12 (rel) | PASS |
| S2 | no liquid: MIE = cp rho dT_ad pi/6 (C_Q alpha/S_L)^3 | 2.33656e-07 | 2.33656e-07 | 1e-12 (rel) | PASS |
| S3 | heat-sink factor = 1 at zero sink | 1 | 1 | 0 (abs) | PASS |
| S4 | Zeldovich factor exp(-E/2R (1/T2 - 1/Tad)) at 100 K sink | 0.872687 | 0.872687 | 1e-12 (rel) | PASS |
| S5 | Metghalchi-Keck ratio = 1 at phi = 1 and floored at 0 when non-flammable | True | True | 0 (bool) | PASS |
| S6 | S_L(T0,p0) = S_L0 (power-law identity) | 0.5 | 0.5 | 1e-15 (rel) | PASS |
| S7 | max SMD for MIE = 50 mJ: bisection vs closed-form inverse | 0.000325253 | 0.000325253 | 1e-09 (rel) | PASS |
| S8 | MIE monotone increasing in SMD | True | True | 0 (bool) | PASS |
