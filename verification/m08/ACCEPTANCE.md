# Module 08 equilibrium benchmark: pre-registered tolerances (queue item 5, 2026-10-24)

Committed BEFORE verification/m08/bench_m08.py was first run. Base: origin/wme1-spray 35166ff (wme1-spray itself is not modified).
Labels: numerical VERIFICATION only. Every engine here uses the same NASA-7 thermo data from the mechanism files, so agreement verifies the equilibrium and reactor numerics, not the thermo data. Nothing is VALIDATED against experiment.

Mixtures: sims.common.fuels.mixture(fuel, phi = 1, w) for fuel in {CH3OH, C2H5OH (sandiego), CH4 (gri30)} and w in {0, 0.3, 0.6, 0.8}.
Dual-temperature rule: unburned T_u = **360 K (normal, coolant ~90 C)** and **400 K (hot / high-performance)**, at p = 1 atm and 40 bar. Results are reported side by side with a hotter-vs-normal verdict.

| ID | Check | Tolerance |
|---|---|---|
| E1 | Module 08 `adiabatic_temperature()` (Cantera equilibrate HP, default element-potential solver) vs Cantera `solver="gibbs"` and `solver="vcs"` on the full mechanism | max abs T_ad spread <= 0.1 K; major species (X > 1e-4) abs diff <= 1e-6 |
| E2 | Independent Gibbs-minimisation solver written here (scipy, element-potential/Lagrange formulation with T found by enthalpy balance) on a 12-species C/H/O/N subset (CO2, CO, H2O, H2, O2, OH, H, O, N2, NO, HO2, H2O2; CH4 for gri30 not needed at phi = 1), vs Cantera equilibrate HP on a Solution restricted to the same 12 species | abs T_ad diff <= 0.05 K; X_k rel diff <= 1e-5 for X_k > 1e-6 |
| E3 | Module 08 constant-volume reactor (the `ignition_delay` / `oxygen_bookkeeping` configuration: rtol 1e-9, atol 1e-15, horizon 0.5 s) end state vs Cantera equilibrate("UV") of the initial charge. CH3OH, w in {0, 0.6}, 40 bar, T0 = 900 K (normal) and 1000 K (hot) | abs T diff <= 0.5 K; major species (X > 1e-3) rel diff <= 1e-3 |
| E4 | Report only: subset (12 sp) vs full-mechanism T_ad difference; real vs FH2O-a and FH2O-b equilibrium T_ad (FH2O is inert, so it cannot dissociate). No pass/fail. |

Overall PASS = E1, E2 and E3 all pass. Compute: 1 process, a few minutes.
