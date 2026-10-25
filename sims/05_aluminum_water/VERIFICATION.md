# Module 05 (05_aluminum_water) VERIFICATION

Date: 2026-10-24 (Grok Bot, verification-queue item 6). Track A (shared infrastructure; also used by Track B).

Status: **executed + code-verified against independent analytic/limit references** (script `sims/verification/item6_checks.py`, output `results/verification/item6/checks.json`). This is verification only: **not validated** against experiment, and not a second-engine cross-check of the physics.

Result: 12/12 checks pass.

Reproduce: `python -m sims.verification.item6_checks` (about 10 s on 1 core, with the Module 04 step study).

## Method and findings

Hand Hess sums use NIST-JANAF formation enthalpies (H2O(l) -285.83, Al(OH)3 gibbsite -1293.18, AlOOH boehmite -996.10, Al2O3 corundum -1675.69 kJ/mol); the module reads its own thermo table, so agreement to 1e-6 checks the stoichiometry and unit chain, not the source data. Literature band 15-16.5 MJ/kg Al heat (Shkolnikov et al., Renew. Sust. Energy Rev. 15 (2011) 4611) is an external sanity range. Algebraic model: GCI does not apply.

## Checks (tolerance fixed before evaluation)

| id | check | actual | reference | tol | pass |
|---|---|---|---|---|---|
| H-gibbsite | heat released gibbsite, hand Hess sum [J/kg Al] | 1.61477e+07 | 1.61477e+07 | 1e-06 (rel) | PASS |
| H-boehmite | heat released boehmite, hand Hess sum [J/kg Al] | 1.57308e+07 | 1.57308e+07 | 1e-06 (rel) | PASS |
| H-corundum | heat released corundum, hand Hess sum [J/kg Al] | 1.51622e+07 | 1.51622e+07 | 1e-06 (rel) | PASS |
| Y1 | H2 yield 1.5 mol/mol Al = 0.11207 kg/kg Al | 0.112077 | 0.11207 | 0.0001 (rel) | PASS |
| Lit-gibbsite | gibbsite heat inside literature band 15.0-16.5 MJ/kg Al | True | True | 0 (bool) | PASS |
| Lit-boehmite | boehmite heat inside literature band 15.0-16.5 MJ/kg Al | True | True | 0 (bool) | PASS |
| Lit-corundum | corundum heat inside literature band 15.0-16.5 MJ/kg Al | True | True | 0 (bool) | PASS |
| Z1 | zero aluminium -> zero energy (limit) | 0 | 0 | 0 (abs) | PASS |
| Z2 | excess water: energy = 1 kg Al x total ledger (Al-limited) | 2.95916e+07 | 2.95916e+07 | 1e-12 (rel) | PASS |
| C-gibbsite | Hess closure gibbsite (module identity) | 0 | 0 | 1e-06 (abs) | PASS |
| C-boehmite | Hess closure boehmite (module identity) | 0 | 0 | 1e-06 (abs) | PASS |
| C-corundum | Hess closure corundum (module identity) | 1.30227e-16 | 0 | 1e-06 (abs) | PASS |
