# Module 08 water chemical effect: normal vs hot regime (J2, module 08 part)

Grok Bot, 2026-10-24 (Claude job reply-verification-20261024-1430). **Status: EXECUTED, single engine. Not verified, not validated.**

- **Code base:** `publish/pc-wme1-spray-20261024` @ 52193f2. It contains Hermes's `a6da0e8` stoich_o2 fix, `f55d15d` Q_dry/Q_wet enthalpy-basis fix and `3fa95c1` tests. `origin/wme1-spray` itself is still at 35166ff, so the fix is on GitHub only on the publish branch.
- **Driver:** `sims/08_water_chem/dual_temp.py` uses the unchanged module 08 functions and the San Diego mechanism. It covers CH3OH and C2H5OH at phi 1 and w = 0 / 0.3 / 0.6.
- **Regimes:** normal T_u = 360 K, hot T_u = 400 K, both at 1 atm, for T_ad and S_L.
- **Ignition:** tau_ig is computed at J2's TDC states (CR 16 and 24) from `j2_tdc_states_sandiego.json`, copied from xcheck/chem `j2_m02_dualT/tad_ign_sandiego.json`.
- **FH2O mechanisms:** `mechanisms/08_water_chem/*_fh2o{a,b}.yaml` are regenerated with `build_mechanisms` and not committed.
- **Output:** `dual_temp.json`. Run time 89 s on the box with 4 processes.

## Consistency check (stated before the run)
Module 08's "real" case must reproduce J2's San Diego values within 0.1 % for T_ad and 2 % for tau_ig.

**Result: PASS.** The largest differences are 0 for T_ad and 1.1e-7 for tau_ig, over 36 comparisons.

This only shows that the two drivers are consistent. They use the same mechanism and the same Cantera solvers, so this is **not** a 2-engine check.

## Chemical effect of H2O (definitions in module 08)
| quantity | formula |
|---|---|
| chem | (real − FH2O-b) / FH2O-b |
| third-body part | (FH2O-a − FH2O-b) / FH2O-b |
| direct-reaction part | (real − FH2O-a) / FH2O-a |

| fuel | w | regime | S_L real [m/s] | S_L chem | S_L 3rd-body | S_L direct | tau CR16 chem | tau CR24 chem |
|---|---|---|---|---|---|---|---|---|
| CH3OH | 0.3 | normal | 0.489 | +12.2 % | +9.3 % | +2.7 % | −9.5 % | −8.9 % |
| CH3OH | 0.3 | hot | 0.584 | +13.1 % | +10.0 % | +2.9 % | −10.3 % | −9.5 % |
| CH3OH | 0.6 | normal | 0.261 | +2.4 % | +8.2 % | −5.3 % | −19.2 % | −18.0 % |
| CH3OH | 0.6 | hot | 0.321 | +3.1 % | +8.3 % | −4.8 % | −20.5 % | −18.9 % |
| C2H5OH | 0.3 | normal | 0.497 | −11.4 % | −2.8 % | −8.8 % | −7.7 % | −7.1 % |
| C2H5OH | 0.3 | hot | 0.598 | −10.3 % | −2.3 % | −8.2 % | −8.1 % | −6.9 % |
| C2H5OH | 0.6 | normal | 0.271 | −25.4 % | −15.4 % | −11.9 % | −16.6 % | −15.3 % |
| C2H5OH | 0.6 | hot | 0.334 | −24.3 % | −14.4 % | −11.6 % | −17.4 % | −15.0 % |

At w = 0 there is no water and all effects are 0.

### Dry reference
| fuel | regime | S_L | tau CR16 | tau CR24 |
|---|---|---|---|---|
| CH3OH | normal | 0.612 m/s | 5.9 ms | 0.44 ms |
| CH3OH | hot | 0.723 m/s | 1.14 ms | 0.115 ms |
| C2H5OH | normal | 0.627 m/s | 27.5 ms | 2.2 ms |
| C2H5OH | hot | 0.748 m/s | 5.3 ms | 0.54 ms |

## Reading (single engine, not verified)
- **Hot vs normal.** The chemical effect of water hardly depends on regime: the change is ≤ 1.3 pp in S_L and ≤ 1.4 pp in tau.
  - Hot gives an S_L 19–23 % higher (absolute).
  - Hot also gives an ignition delay 4–5.5× shorter, which means earlier knock.
  - Hotter is therefore **not** better for knock margin. It is better only for burn rate.
- **Ignition.** Water chemistry shortens tau_ig by 7–20 %, almost entirely through the third-body effect; the direct-reaction part is ≤ 0.4 %. This works against the knock benefit of water's dilution and cooling.
- **Open question (needs scrutiny before anyone relies on it).** At w = 0.3 the sign of the S_L chemical effect is opposite for the two fuels:
  - CH3OH: +12 %
  - C2H5OH: −11 %

  The flames have not had a grid-independence check yet (verification-queue item 7 is still waiting for cpu-heavy). Treat the S_L chemical-effect numbers as unverified.
