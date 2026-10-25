# WME-1 Engineering & Simulation Spec

This is the contract every module in `sims/` implements. If code and spec disagree, the spec wins until the spec is changed in a reviewed commit.

## 0. Ground rules (non-negotiable)

1. **Energy accounting.** Water has zero heating value. Every joule of work must be traced to a fuel's lower heating value (LHV), a stored-energy reactant (e.g. aluminium), or recovered waste heat that the fuel already paid for. Any result showing net energy from water is a bug.
2. **Honest outputs.** Every assumption is a named parameter with a default and a source or a stated rationale. Every result carries the assumptions it depends on (`summary.json → "assumptions"`).
3. **Validation first.** Each module ships with tests comparing against published data (see §9). A module is not "done" until its validation tests pass.
4. **SI units everywhere** internally (K, Pa, kg, J, m, s). Convert only for display (°C, bar, CAD, cm/s).

## 1. Definitions

- **Water-to-fuel ratio:** `WFR = m_water / m_fuel` (mass, per cycle or per second).
- **Water fraction of liquid intake:** `w = m_water / (m_water + m_fuel) = WFR / (1 + WFR)`. **Water-majority** means `w > 0.5` (WFR > 1).
- **Equivalence ratio** `φ` is defined on fuel and air only (water excluded).
- Fuels: `H2`, `CH4` (validation references), `CH3OH` (methanol), `C2H5OH` (ethanol). Hydrogen and methane are gaseous; for them `w` uses the same mass definition.

## 2. Environment

- Python 3.12 (VPS: Ubuntu 24.04). Pinned deps in `requirements.txt`: `cantera>=3.1`, `CoolProp>=6.6`, `numpy`, `scipy`, `pandas`, `matplotlib`, `pytest`; `cadquery` only in `requirements-cad.txt`.
- Mechanisms in `mechanisms/`:
  - `gri30.yaml` (ships with Cantera) — H2, CH4, and fallback for CH3OH.
  - **San Diego mechanism** (UCSD, latest release) converted with `ck2yaml` → `mechanisms/sandiego.yaml`, used for CH3OH and C2H5OH. Record source URL, download date and SHA-256 of the original files in `mechanisms/PROVENANCE.md`. If the download fails, use `gri30.yaml` for CH3OH, skip C2H5OH, and record `"mechanism_fallback": true` in every affected `summary.json`.

## 3. Module conventions

- Each module is `sims/NN_name/run.py`, runnable as `python -m sims.NN_name.run [--quick|--full] [--workers N] [--out results/NN_name]`.
  - `--quick`: CI-sized, finishes in < 2 min on 2 cores.
  - `--full`: the real sweep. `--workers` uses `multiprocessing` (default 1). **The VPS runs with `--workers 8` under `nice -n 19`; never assume more than 8 cores.**
- Outputs go to `results/NN_name/`: tidy CSV(s), PNG plots (matplotlib, labelled axes with units, 150 dpi), and `summary.json` with keys `module`, `version`, `git_sha`, `mode`, `assumptions`, `key_results`, `validation`, `runtime_s`.
- Deterministic: fixed seeds for any Monte Carlo.
- Shared helpers only in `sims/common/` (`fuels.py`: fuel properties, LHV via Cantera, stoichiometry, mixture builder that adds water vapour for a given `w`; `io.py`: result writing, git SHA). Modules must not import from each other's internals; they exchange data only via `results/*/` files.
- `run_all.sh` runs every module in order with the VPS settings and writes `results/RUNLOG.md`.

## 4. Module 01 — `energy_audit`

Prove the energy ledger quantitatively.

1. **Heating values via Cantera** for H2, CH4, CH3OH, C2H5OH and H2O (LHV of H2O must come out as 0 within numerical tolerance — it is already fully oxidised).
2. **On-board electrolysis (HHO) loop gain** `G = η_engine × η_alternator × η_electrolyser`, where the electrolyser efficiency is LHV-of-H2-out / electrical-energy-in. Parameter ranges (uniform Monte Carlo, 200 000 samples, seed 42): `η_engine` 0.20–0.45, `η_alternator` 0.50–0.75, `η_electrolyser` 0.40–0.80. Report max, p99, p50. A self-sustaining "water engine" needs `G ≥ 1`; plot the gap.
3. **Typical HHO kit:** 20 A at 13.8 V, 100 % Faradaic efficiency → H2 mass flow (Faraday's law), its LHV power, vs. the shaft power the alternator load costs (`P_elec / (η_alt)`), and vs. a 15 kW cruise engine's fuel power. Report net effect (expected: net loss).
4. Plots: `loop_gain_hist.png`, `hho_kit_ledger.png`.

## 5. Module 02 — `flame_chem`

For each fuel at `φ ∈ {0.8, 1.0}` and `w ∈ {0, 0.1, …, 0.9}` (water as vapour in the unburned charge):

1. **Adiabatic flame temperature** (`equilibrate('HP')`) at unburned states (300 K, 1 atm), (400 K, 1 atm), (750 K, 25 bar).
2. **Evaporative cooling:** temperature drop of the intake charge if all water is injected as liquid at 300 K and fully evaporates into air+fuel at 320 K initial (energy balance with `h_fg` from CoolProp). Report the minimum intake temperature needed to keep the mixture above its dew point and to fully evaporate (dew point via water partial pressure and CoolProp saturation).
3. **Laminar flame speed** `S_L` with `ct.FreeFlame` (mixture-averaged transport, `auto=True`, refine ratio 3, slope 0.07, curve 0.14) at (400 K, 1 atm) and (450 K, 5 bar). Stop a sweep when the solver fails or `S_L < 0.02 m/s`; record as `no_flame`.
4. **Ignition delay** in a constant-volume `IdealGasReactor` at 40 bar, `T ∈ {750, 800, …, 1100} K`, `φ = 1`, all `w`; `τ` = time of max `dT/dt`. Fit per fuel `τ = A · p^(-n) · exp(E/(R·T)) · (1 + c·w)` (`n` fixed at 1.0 unless data at a second pressure are computed) and save to `results/02_flame_chem/ignition_fits.json`.
5. **Limits:** per fuel, `w_SI_robust` = max `w` with `S_L(400 K, 1 atm, φ=1) ≥ 0.15 m/s`, and `w_SI_marginal` for `≥ 0.08 m/s`. Save `S_L(w)` fit (cubic in `w`) to `flame_speed_fits.json` for module 03.

## 6. Module 03 — `engine_cycle`

0-D closed-cycle (IVC→EVO) single-cylinder model with a two-zone burned-gas temperature estimate for NO.

- **Geometry (default test engine):** bore 86 mm, stroke 86 mm, con-rod 145 mm, 2000 rpm, IVC at BDC, EVO at 140° aTDC, residual fraction 5 %, `p_IVC = 1.0 bar` (WOT), `T_intake` 320 K (option: 360 K heated intake).
- **First law:** `dU = −p dV + dQ_comb − dQ_wall − dQ_evap`, gas properties from Cantera (unburned frozen composition; burned = equilibrium products; mixture properties by mass fraction burned).
- **Heat release:** Wiebe (`a = 5`, `m = 2`), combustion efficiency 0.98. 10–90 % burn duration `Δθ = Δθ_ref · (S_L,ref / S_L(w))^0.5`, `Δθ_ref = 25 CAD` at `w = 0`, capped at 80 CAD; use `S_L(w)` from module 02 fits. Default CA50 = 8 CAD aTDC (MBT proxy).
- **Wall heat transfer:** Woschni (1967), wall temperature 450 K.
- **Water:** fraction `f_evap_intake` (default 0.5) evaporates before IVC (lowers `T_IVC`); the rest evaporates during compression, removing `h_fg` uniformly from IVC to −30 CAD.
- **Knock:** Livengood–Wu integral on the isentropically compressed unburned end gas using module 02 ignition fits; knock if the integral reaches 1 before `x_b = 0.9`. If knocking, retard CA50 in 2-CAD steps up to 30 CAD aTDC; beyond that mark `knock_limited = true`.
- **NO:** extended Zeldovich rate integrated in the burned zone (equilibrium O, N₂, O₂ from Cantera at the burned-zone T, p). Report NO **relative to `w = 0`** at the same CR; state ±factor-2 uncertainty on absolute values.
- **Sweeps:** fuels CH3OH, C2H5OH (and CH4 reference); `CR ∈ {9, 10, …, 18}`; `w ∈ {0, 0.1, …, 0.8}`; `T_intake ∈ {320, 360} K`; `φ = 1`.
- **Outputs per point:** gross indicated efficiency, IMEP, peak pressure, CA50 used, knock flag, EVO temperature, relative NO.
- **Key result — the water-majority map:** for each fuel, the best (CR, `w`, `T_intake`) maximising efficiency subject to: no knock at CA50 ≤ 15 CAD, `S_L(w) ≥ 0.08 m/s`, peak pressure ≤ 120 bar. Report the best overall point and the best point with `w > 0.5`, each compared with the best dry (`w = 0`) point.
- **Cross-check:** reproduce Cantera's `ic_engine.py` example settings closely enough to compare its efficiency with ours (document differences); compare `w = 0` results to the ideal Otto efficiency trend.

## 7. Module 04 — `six_stroke`

Water-injection six-stroke (Crower; Conklin & Szybist, *Energy* 2010):

- Strokes 1–4 from module 03's chosen design point (read its exhaust state at EVO, or recompute).
- Early exhaust-valve closing traps a fraction of exhaust; it is recompressed; liquid water at 300 K and 100 bar is injected at TDC; the steam + exhaust mixture expands (stroke 5) and is exhausted (stroke 6).
- Thermodynamics: exhaust gas from Cantera; water from CoolProp. Check the water partial pressure against saturation at every step; if it would condense, account for condensation (latent heat) rather than ignoring it.
- Sweep exhaust-valve-closing angle and injected water mass; find the maximum extra net work. Run adiabatic and with Woschni heat transfer.
- Outputs: extra work as % of the four-stroke work, efficiency gain, water mass per cycle, and the combined `w` (intake water + six-stroke water).

## 8. Module 05 — `aluminum_water`

Per kg of Al for `2Al + 6H2O → 2Al(OH)3 + 3H2`, `2Al + 4H2O → 2AlOOH + 3H2`, `2Al + 3H2O → Al2O3 + 3H2`: heat released at 298 K, H2 produced (kg), its LHV, total energy, water consumed, and water mass fraction of the reactants. Use NIST-JANAF standard enthalpies (cite values in the code). Compare with aluminium smelting electricity (13–15 kWh/kg, cite source) to show the round-trip efficiency.

## 9. Module 06 — `carburetor` (sizing) and Module 07 — `cad`

Design for the module 03 design point engine.

- **Option A (preferred): single-circuit carburetor on premixed wet alcohol.** Methanol and ethanol are fully miscible with water, so the "fuel" in the tank is the water-majority blend; a fixed-venturi carburetor meters it like any liquid fuel.
- **Option B: dual-circuit carburetor** (separate fuel and water float bowls and main jets sharing one venturi) for immiscible fuels or a variable WFR. Note: two jets on one venturi signal give a roughly constant WFR ≈ `(Cd_w·A_w·√ρ_w)/(Cd_f·A_f·√ρ_f)` (equal heads); include a vacuum-operated "water power valve" option to raise WFR at high load.
- Sizing physics: compressible isentropic venturi flow with discharge coefficient; Bernoulli jet flow with `Cd` 0.6–0.8; float-level head; viscosity correction for the wet-alcohol blend (cite data). Operating map: 1000–4000 rpm, idle to WOT.
- Atomisation & evaporation: Sauter mean diameter (Nukiyama–Tanasawa), d²-law evaporation time vs intake residence time → required intake heating power (exhaust-heated plenum) in kW.
- Outputs: design table (venturi throat and inlet diameters, main/idle jet diameters, float levels, needle seat), plots of φ and WFR across the map, `carb_design.json`.
- **Module 07** reads `carb_design.json` and builds a CadQuery model (body, venturi with throat, throttle bore and butterfly, float bowl(s), main-jet passages with nozzles at the throat, mounting flange) → `cad/carb_optionA.step`, `.stl`, and a PNG/SVG view; same for Option B.

## 10. Validation targets (tests)

| Case | Target | Tolerance |
|---|---|---|
| CH4/air, φ=1, 300 K, 1 atm, T_ad | 2225 K | ±20 K |
| H2/air, φ=1, 300 K, 1 atm, T_ad | 2380 K | ±25 K |
| CH4/air, φ=1, 300 K, 1 atm, S_L (GRI-3.0) | 0.38 m/s | 0.34–0.42 |
| H2/air, φ=1, 300 K, 1 atm, S_L | 2.2 m/s | 1.9–2.6 |
| LHV H2 / CH4 / CH3OH / C2H5OH | 120.0 / 50.0 / 19.9 / 26.8 MJ/kg | ±2 % |
| LHV H2O | 0 | < 1e-6 MJ/kg |
| Ideal Otto check (engine model, adiabatic, instant burn, constant γ) | `1 − CR^(1−γ)` | ±1 % abs |

Further targets from `docs/research/02-legitimate-water-combustion.md` are added as that research lands.

## 11. Execution plan

| Step | Runs on |
|---|---|
| Code writing | Codex (via Hermes/composer route) on the laptop workspace |
| Simulations | Mail VPS, `nice -n 19`, ≤ 8 workers |
| Final verification | Supervisor (Claude) |

## 12. Spray track

Modules 08, 09 and 11 close the chain from water chemistry to the flame front.

### 12.1 Module 08 — `water_chemistry`

Separate water's chemical effect from its dilution and thermal effect by
comparing the real mechanism against a **fictitious water** species that has
H2O's thermo and transport but takes part in no reactions.

- Add a species `FH2O` to copies of `sandiego.yaml` and `gri30.yaml`. It has
  H2O's thermo and transport but takes part in no reactions. Make two
  variants:
  - (a) FH2O keeps H2O's third-body efficiencies;
  - (b) FH2O uses third-body efficiency 1.0.
- Cases: fuels CH3OH, C2H5OH and CH4 (reference), at φ = 1 and w = 0 to 0.8
  in steps of 0.1. Compute:
  - S_L at 400 K, 1 atm;
  - ignition delay at 40 bar, 800–1000 K;
  - T_ad.
  Run each with real H2O, FH2O-a and FH2O-b.
- Report: the chemical effect is (real − FH2O)/FH2O, for S_L and for τ. Split
  it into a third-body part (a vs b) and a direct-reaction part.
- Oxygen bookkeeping: at w = 0.6 for CH3OH, do a reaction-path or
  element-flux analysis of the O atoms that start in H2O. Show the net O
  transferred to CO2 and the net H2 released. The net energy from water must
  be 0 within tolerance.
- Tests:
  - At w = 0, real and FH2O are identical.
  - FH2O has an LHV of 0.
  - O-atom balance closes to 1e-6 or better.

### 12.2 Module 09 — `spray_evaporation`

Intake atomisation and evaporation, modelled as a Lagrangian droplet
ensemble in a closed-mass-balance intake charge. Vapour accumulates, so
evaporation stops at saturation. This is essential: at w ≥ 0.5 the charge
saturates early, so the evaporation limit is thermodynamic as well as
kinetic.

- Model: Abramzon–Sirignano evaporation with Ranz–Marshall correlations, and
  a Rosin–Rammler size distribution.
- Liquids: water, methanol, and premixed wet-methanol blends. Treat the
  methanol–water mixture as non-ideal, using Wilson or NRTL with cited
  parameters.
- Atomisers:
  1. carburetor venturi (Nukiyama–Tanasawa at the module 06 design
     airflow, or 30 m/s throat speed if module 06 is not yet available);
  2. port-injection pressure-swirl injector at 3 bar and 5 bar (Lefebvre
     SMD correlation);
  3. air-assisted nozzle, 20–30 µm;
  4. ultrasonic atomiser (Lang correlation, 40–120 kHz).
- Sweeps: plenum temperature 320–420 K; runner velocity 10–40 m/s; runner
  length 0.1–0.4 m. Then follow the charge in-cylinder to spark at 2000 rpm,
  with compression heating from module 03's p(θ) if available, otherwise
  isentropic.
- Wall impingement: use a Stokes-number criterion at a 90° bend.
- Outputs per case:
  - % evaporated at IVC and at spark;
  - % wall-impinged;
  - remaining liquid SMD at spark.
  Save `spray_at_spark.json` for module 11. Name the atomiser to recommend
  for module 06.
- Tests:
  - A single water droplet with constant properties matches the d²-law
    analytic solution within 2%.
  - Evaporation never exceeds saturation.
  - Mass is conserved to 1e-8.

### 12.3 Module 11 — `spray_flame`

How much liquid water the flame front tolerates.

- Model: Ballal–Lefebvre spray-flame correlations for flame speed and minimum
  ignition energy in droplet-laden mixtures, with gas-phase S_L from module
  02. Inputs: liquid fraction and SMD at spark from module 09. This is an
  empirical model; cite it and state its validity range.
- Outputs:
  - effective flame speed versus liquid-water fraction and SMD;
  - the misfire boundary, defined as minimum ignition energy above a typical
    50–100 mJ spark;
  - the recommended maximum SMD at spark for each water fraction w.
- Tests:
  - with zero liquid it reduces to gas-phase S_L;
  - the trends are monotonic.
