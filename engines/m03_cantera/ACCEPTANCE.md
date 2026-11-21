# M03-CRN: independent Cantera ReactorNet engine for Module 03 — pre-registered acceptance criteria

Written and committed **before** any verification or comparison run (Grok Bot, 2026-10-24, job
`reply-verification-20261024-1430`, item V1). Criteria are not changed after results are seen; every FAIL is reported as is.

## What is independent of Module 03 (build-your-own rule)
| element | Module 03 (`sims/03_engine_cycle/run.py`) | M03-CRN (`engines/m03_cantera/engine.py`) |
|---|---|---|
| integrator | hand-rolled explicit midpoint on a fixed crank-angle grid + secant U->T inversion | Cantera `ReactorNet` (SUNDIALS CVODES, variable-order BDF, adaptive step) on an `ExtensibleIdealGasReactor` |
| volume / work | V(theta) evaluated on the grid, work = p_mid dV | moving `ct.Wall` with slider-crank piston *velocity* (Cantera `ic_engine.py` pattern); work integrated as an extra CVODES state |
| heat release | Q_avail * dx_b added to U per step | separate `ct.Wall` whose `heat_flux` is the Wiebe rate dQ/dt(t) (external heat source); composition converted fuel+O2 -> CO2+H2O at the same rate with a sensible-energy-neutral source term |
| burned-gas dissociation | TP-equilibrium of the burned mass at bulk T (Cantera `equilibrate`) | finite-rate H/O/C/N product kinetics (GRI-Mech 3.0 reaction subset with no fuel reactions) inside the reactor |
| wall heat transfer | Woschni (1967) | **Hohenberg (1979), SAE 790825** (production); Woschni (1967) only as sensitivity, own implementation (motored polytrope from the Wiebe start-of-combustion state) |
| properties | UCSD San Diego mechanism thermo, own U(T,p) inversion | GRI-Mech 3.0 NASA-7 thermo (C2H5OH from Cantera `nasa_gas.yaml`, NASA Glenn/McBride et al.) evaluated by Cantera inside the reactor; water latent heat and p_sat from Cantera `ct.Water()` (not CoolProp) |
| evaporation cap | lagged saturation cap evaluated at nodes | continuous mass inflow (`MassFlowController` from an H2O(g) reservoir) + latent-heat sink, saturation cap as a stiff relaxation (time constant tau) |
| LHV | `sims.common.fuels.lhv` (San Diego thermo) | own reaction enthalpy from GRI/NASA thermo at 298.15 K minus NIST SRD 69 vaporisation enthalpy |

Shared on purpose (they are the *problem definition*, not the solver): engine geometry, IVC/EVO, Wiebe a=5, m=2, CA50 and 10-90 % duration per point,
combustion efficiency 0.98, the trapped-charge boundary condition at IVC (fuel, air, residual, water masses, T_IVC, intake-evaporated fraction taken from
the Module 03 row), wall temperature per regime, the evaporation schedule IVC -> -30 CAD, and the efficiency definition (W_IVC->EVO / (m_fuel LHV_liquid)).

## Verification criteria (engine on its own)
- **V-A ideal Otto**: constant-cp ideal gas (gamma 1.4, R 287 J/kg/K), adiabatic, Wiebe 10-90 % = 1 CAD centred at TDC.
  |eta - (1 - CR^(1-gamma))| <= 1e-3 absolute at CR 16 and 24, and the error must shrink when the burn is shortened (0.5 CAD).
- **V-B solver convergence**: rtol 1e-6, 1e-7, 1e-8, 1e-9 (atol = 1e-6 x rtol... scaled, see engine). For eta, IMEP, p_max, T_max, Q_wall at the
  design points: relative change between rtol 1e-8 and 1e-9 <= 1e-5 and GCI_fine (Roache, Fs = 1.25, three finest levels, r = 10) <= 1e-4 (0.01 %).
  Evaporation relaxation time tau halved: |delta eta| <= 1e-4 absolute.
- **V-C energy closure**: |U(EVO) - U(IVC) + W + Q_wall - Q_comb + Q_latent - H_in - E_conv| / Q_fuel <= 1e-5, and the integrated Wiebe heat equals
  Q_avail (x_b(EVO) - x_b(IVC)) to 1e-6 relative.
- **V-D Cantera ic_engine.py benchmark**: used only if it can be run without changing its physics; it is a CI engine with finite-rate chemistry, so it
  cannot benchmark an SI Wiebe cycle. Reported as "not applicable" if so (no pass/fail).

## Comparison criteria vs Module 03 (two-engine check)
Design points: Module 03 `design_point.json` selections (CH3OH and C2H5OH: best_dry, best_overall, water_majority) in the **normal** regime
(coolant 363 K, chamber wall 450 K) and the **hot** regime (coolant 388 K, chamber wall 520 K, intake up to 400 K), Module 03 rows from
`results/03_engine_cycle/cycle_points.csv` (normal) and `results/dual_temp/03_engine_cycle_hot/cycle_points.csv` (wme1-hiT, hot).
Each design point is also run in the other regime (same CR, w, T_intake if that row exists) so hot vs normal is like for like.

- **C1 (like-for-like, Woschni in both engines)**: |eta_CRN - eta_M03| <= 1.5 percentage points and |p_max,CRN / p_max,M03 - 1| <= 5 % at every point,
  both regimes. **Only if C1 passes at every point is "2-engine agreement" claimed for Module 03 eta and p_max** (executed + verified, not validated).
- **C2 (production M03-CRN, Hohenberg)**: same tolerances, reported. A C2 failure with a C1 pass is reported as heat-transfer model-form uncertainty,
  quantified as eta(Hohenberg) - eta(Woschni) inside M03-CRN; it does not void C1.
- Reported side by side without pass/fail (informational): IMEP, T_max (bulk), T_EVO, wall heat Q_wall/Q_fuel, end-gas peak temperature (knock
  indicator), bulk-zone NO (indicative only: single zone, not comparable with Module 03's two-zone NO), burn rate (prescribed: CA50, 10-90 %),
  hot minus normal deltas from each engine. Misfire/ignition margin is not computed by either engine (Module 11 scope).
- Dissociation (kinetic vs equilibrium) and frozen-products sensitivity are reported as explicit model deltas.

## What a PASS means
Executed and code-verified (V-A..V-C) and, for C1, a second independent implementation agrees with Module 03 within the stated tolerances.
It is **not validated** against engine experiments.
