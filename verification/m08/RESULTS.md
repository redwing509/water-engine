# Module 08 equilibrium benchmark: results (queue item 5, 2026-10-24)

Status: **EXECUTED + VERIFIED (equilibrium and reactor numerics)**. Not VALIDATED. All engines share the same NASA-7 thermo data, so this verifies solvers and code paths, not the data.
Criteria pre-registered in ACCEPTANCE.md (commit eb240b8). Run: `OMP_NUM_THREADS=1 python -m verification.m08.bench_m08` (31 s, 1 core, Cantera 3.2.0). Raw: results/report.json.
Mechanisms: real = sandiego (CH3OH, C2H5OH) / gri30 (CH4). FH2O variants were rebuilt locally with `python -m sims.08_water_chem.build_mechanisms` (generated, not committed).

| ID | Criterion | Worst case over 48 HP points / 4 UV points | Verdict |
|---|---|---|---|
| E1 | Module 08 `adiabatic_temperature()` vs Cantera element_potential, gibbs and vcs: T spread <= 0.1 K, majors <= 1e-6 | 7.3e-6 K, 6.0e-10 | PASS |
| E2 | Own Gibbs solver (element potentials + enthalpy balance, own NASA-7 evaluation) vs Cantera on the same species subset: T <= 0.05 K, X rel <= 1e-5 | 1.6e-6 K, 1.3e-8 (reactant H own vs Cantera 4e-16) | PASS |
| E3 | Module 08 CV reactor (rtol 1e-9, 0.5 s) end state vs Cantera equilibrate UV: T <= 0.5 K, majors rel <= 1e-3 | 5.8e-5 K, 2.3e-7 | PASS |

**Overall: PASS.**

Disclosed deviation: the pre-registered 12-species subset includes NO, but sandiego.yaml has no NO (N2 is inert there). The subset is therefore 11 species for CH3OH/C2H5OH and 12 for CH4. Tolerances unchanged.

## Dual-temperature table (T_ad from module 08, phi = 1; normal T_u = 360 K, hot T_u = 400 K)
| fuel | w | p | T_ad normal [K] | T_ad hot [K] | hot - normal | FH2O(a,b) - real [K] (E4) |
|---|---|---|---|---|---|---|
| CH3OH | 0 | 1 atm | 2253.2 | 2271.4 | +18.2 | - |
| CH3OH | 0 | 40 bar | 2324.7 | 2347.8 | +23.2 | - |
| CH3OH | 0.3 | 1 atm | 2134.8 | 2155.3 | +20.6 | +8.25 |
| CH3OH | 0.3 | 40 bar | 2179.5 | 2204.2 | +24.7 | +3.39 |
| CH3OH | 0.6 | 1 atm | 1879.8 | 1904.9 | +25.1 | +3.28 |
| CH3OH | 0.6 | 40 bar | 1892.1 | 1919.1 | +27.1 | +1.09 |
| CH3OH | 0.8 | 1 atm | 1483.2 | 1512.2 | +29.0 | +0.26 |
| CH3OH | 0.8 | 40 bar | 1483.8 | 1513.0 | +29.2 | +0.08 |
| C2H5OH | 0 | 1 atm | 2269.3 | 2287.8 | +18.5 | - |
| C2H5OH | 0 | 40 bar | 2344.2 | 2367.9 | +23.7 | - |
| C2H5OH | 0.3 | 1 atm | 2176.6 | 2196.9 | +20.3 | +8.20 |
| C2H5OH | 0.3 | 40 bar | 2229.5 | 2254.4 | +24.9 | +3.52 |
| C2H5OH | 0.6 | 1 atm | 1970.0 | 1994.2 | +24.3 | +4.49 |
| C2H5OH | 0.6 | 40 bar | 1990.2 | 2017.2 | +27.0 | +1.58 |
| C2H5OH | 0.8 | 1 atm | 1614.3 | 1642.9 | +28.5 | +0.68 |
| C2H5OH | 0.8 | 40 bar | 1616.3 | 1645.4 | +29.1 | +0.20 |
| CH4 | 0 | 1 atm | 2254.7 | 2273.8 | +19.1 | - |
| CH4 | 0 | 40 bar | 2321.9 | 2345.9 | +24.0 | - |
| CH4 | 0.3 | 1 atm | 2202.7 | 2222.8 | +20.1 | +8.97 |
| CH4 | 0.3 | 40 bar | 2258.3 | 2283.0 | +24.7 | +3.93 |
| CH4 | 0.6 | 1 atm | 2080.9 | 2103.4 | +22.5 | +6.75 |
| CH4 | 0.6 | 40 bar | 2114.4 | 2140.5 | +26.1 | +2.64 |
| CH4 | 0.8 | 1 atm | 1839.2 | 1865.6 | +26.4 | +2.66 |
| CH4 | 0.8 | 40 bar | 1848.5 | 1876.5 | +28.0 | +0.88 |

CV reactor end state (E3, CH3OH, 40 bar): w = 0: 2963.25 K (T0 900 K, normal) vs 3007.30 K (T0 1000 K, hot); w = 0.6: 2540.17 K vs 2598.27 K.

**Hotter vs normal verdict:** a 40 K hotter charge raises T_ad by 18-29 K. The rise is larger at high water fraction because there is less dissociation. This is an equilibrium thermodynamics check only and makes no efficiency claim. Hotter is "better" only in giving a hotter, faster-burning flame. It also brings more wall heat loss, NOx and knock tendency (see the J2 tau_ig result), so it is **not better on its own**.

## E4 notes (report only)
- Full mechanism vs subset: <= 0.01 K, so dissociation to minor species beyond the subset is negligible for T_ad.
- FH2O-a and FH2O-b give identical equilibria, as they must (third-body efficiencies do not enter equilibrium).
- FH2O mixtures reach up to **+9 K higher T_ad** than real water (largest at w = 0.3, 1 atm). FH2O cannot dissociate, and the water pool is split into H2O + FH2O, which changes the H2O partial pressure in the dissociation equilibria. Module 08's "chemical effect" on S_L therefore includes this equilibrium (burned-state) contribution as well as kinetics. **Flag for Claude/Hermes:** this should be stated in the module 08 interpretation. A rough estimate: S_L ~ exp(-Ea/2RT_ad) makes 8 K worth a few percent of S_L at w = 0.3.
