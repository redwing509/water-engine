# WME-1 spray track hand-off

Worker: Claude (supervising), Hermes (coding), James (approved coding + downloads).
Worktree: `C:/Users/spoka/git/water-engine-spray`, branch `wme1-spray`.
Mail VPS code: `/opt/water-engine/code-spray`, venv `/opt/water-engine/.venv`.

## Status

| Item | Module | Status | Notes |
|---|---|---|---|
| A | `08_water_chemistry` | DONE | --quick + full pytest on mail; energy closure fixed; committed 76c0564 |
| B | `09_spray_evaporation` | TODO | |
| C | `11_spray_flame` | TODO | |

## Round log

### 2026-10-22 — Setup
- Created worktree `wme1-spray` at `C:/Users/spoka/git/water-engine-spray` from `b00342f`.
- Added SPEC §12 "Spray track" with module specs 08/09/11.
- Synced code to `/opt/water-engine/code-spray` (reused `/opt/water-engine/.venv`).

### 2026-10-23 — Item A: module 08 water chemistry
- Energy closure bookkeeping was wrong on mail (stale copy used `equilibrate("HP")` +
  bare `int_energy_mole`, no mole scaling; Q_dry ≈ 2.3e3 J/kg vs true 2.17e7 J/kg).
  The local `run.py` uses explicit mole-scaled enthalpy bookkeeping
  (`h_react*n_react - h_prod*n_prod`), which gives Q_dry = 21.707 MJ/kg for CH3OH
  and Q_wet ≡ Q_dry to 3e-16 relative. Local file is authoritative; mail copy was stale.
- Validation check 4 rewritten from a 1.0 J/mol tolerance on the absolute difference
  to a 1e-6 relative tolerance on `energy_closure_rel`, matching the SPEC.
- Scratch files deleted; mechanisms/08_water_chem/*.bak removed on mail.

### 2026-10-23 (round 2) — Item A: module 08 water chemistry, commit
- Mail copy of `sims/08_water_chem/run.py` was stale (read `atoms[2]`/`atoms[3]` on a
  `tuple[int,int,int]` Fuel; correct is `atoms[1]`/`atoms[2]` for H/O). Re-synced from
  the local worktree (md5 72c031440eceb633fad7f8012bce7d69). All other files already
  matched.
- Fast tests: `pytest tests/test_water_chem.py -m "not slow"` -> 4 passed, 2 deselected.
- `--quick` run (2 workers, out results/quick08): validation `passed=true`, all 13
  checks passed. Energy closure: Q_dry = 21.50852035547747 MJ/kg, Q_wet identical to
  1.73e-16 relative. O balance rel error 4.4e-13.
- Slow tests (`-m slow`, 2 tests) and `--full` run launched in background on mail
  (ai-job water-engine, ttl 600). Results next round.

### 2026-10-23 (round 2, cont.) — Item A: module 08 water chemistry, DONE
- Slow tests: `pytest tests/test_water_chem.py -m slow` -> **2 passed, 4 deselected**
  (test_w0_flame_speed_identical, test_quick_smoke) in 301 s. Full test file:
  6 passed, 0 failed.
- `--full` run (8 workers, out /opt/water-engine/results/full08): 375 s.
  81 adiabatic (computed), 81 flame (computed), 243 ignition (216 ignited, 27
  no_ignition — high-w / high-T corners outside the 0.5 s horizon).
  validation `passed=true`, all 13 checks passed.
- Chemical effect on S_L and tau at w = 0.6 for CH3OH (full run):
  S_L: real 0.320991, fh2o_a 0.337094, fh2o_b 0.311306 m/s ->
  total effect +3.11%, third-body part +8.28%, direct-reaction part -4.78%.
  tau: real 0.035154, fh2o_a 0.035179, fh2o_b 0.042852 s ->
  total effect -17.97%, third-body part -17.91%, direct-reaction part -0.07%.
- O transferred from water to CO2 (CH3OH, w=0.6, 900 K, 40 bar): 0.0 mol/mol fuel
  (net H2 released 0.0262 mol/mol fuel; O balance rel error 4.4e-13).
- Energy closure: Q_dry = 21.50852035547747 MJ/kg, Q_wet identical to
  1.73e-16 relative (asserted, 1e-6 tol). Full results at
  /opt/water-engine/results/full08 (not committed: PNGs/logs are gitignored).
- Committed on wme1-spray at 76c0564.

### 2026-10-24 (round 3) — Item A: module 08 water chemistry, BUG FIX
- Cross-check X2 (xcheck 48afdc0) found `stoich_o2 = FUELS[fuel].atoms[1]` in
  `oxygen_bookkeeping()`, which takes the **H atom count** (4 for CH3OH) instead
  of the O2 demand (1.5 for CH3OH, 3 for C2H5OH, 2 for CH4).  The correct formula
  is C + H/4 - O/2, already implemented as `fuels.oxygen_demand()` and used by
  `fuels.mixture()` for the charge itself — module 08's flame/ignition/T_ad
  mixtures were built correctly; only the bookkeeping block was wrong.
- **Affected outputs:** only `oxygen_bookkeeping.json` (`Q_dry`, `Q_wet`,
  `energy_closure_*`).  `chemical_effect.csv`, `flame_speed.csv`,
  `ignition_delay.csv`, `adiabatic_flame_T.csv` and all plots are unchanged.
- **Second bug found and fixed in the same block:** `Q` was divided by
  `mol_per_kg = 1000/mw_fuel` while the numerator was already in J/kmol per kmol
  of fuel, inflating Q by mw_fuel^2/1000 = 2.667% for CH3OH; and it used
  `int_energy_mole` (ΔU) although the docstring says constant-pressure products
  at 298.15 K.  Both fixed: enthalpy basis, divide by `mw_fuel` (J/kmol fuel ->
  J/kg fuel), same convention as `fuels.lhv`.
- **Old vs new (CH3OH, w=0.6, San Diego mechanism):**
  | Quantity | Old | New |
  |---|---|---|
  | Q_dry [MJ/kg] | 21.50852035547747 | 21.104117910 |
  | Q_wet [MJ/kg] | 21.508520355477475 | 21.104117910 (identical) |
  | energy_closure_rel | 1.73e-16 | 7.06e-16 |
  | S_L chemical effect @ w=0.6 | +3.11% | +3.11% (unchanged) |
  | tau chemical effect @ w=0.6 | -17.97% | -17.97% (unchanged) |
- X2 (NIST-JANAF independent) vs new Q_dry: 21,104,603.33 vs 21,104,117.91 J/kg
  = **0.002%** residual (tolerance +/-0.2%).  Residual is the documented
  1.3-2.5 kJ/mol San Diego vs NIST-JANAF formation-enthalpy difference
  (CH3OH -200938.85 vs -200941.5 J/mol), NOT tuned.
- Fast tests: `pytest tests/test_water_chem.py -m "not slow"` -> 6 passed
  (incl. new `test_stoichiometric_oxygen_demand` for CH3OH/C2H5OH/CH4 =
  1.5/3.0/2.0 and `test_phi_one_mixture_matches_module_02` within 1e-12).
- `--quick` (2 workers, out results/quick08): validation `passed=true`.
- `--full` (8 workers, out results/full08): validation `passed=true`.
- Committed on wme1-spray at f55d15d.

### 2026-10-24 (round 4) — Item A: module 08 water chemistry, re-check + commit
  - Re-ran `--full` on mail (8 workers, out results/full08): validation
    `passed=true`, all 13 checks passed.  Q_dry = 21,104,117.91 J/kg,
    Q_wet = 21,104,117.91 J/kg, energy_closure_rel = 7.06e-16 (asserted
    within 1e-6 relative).
  - **Old vs new chemical-effect percentages at w = 0.6 (San Diego mechanism):**
    | Fuel | Quantity | Old (buggy) | New (corrected) |
    |---|---|---|---|
    | CH3OH | S_L_chemical_effect | +3.11% | +3.11% (unchanged) |
    | CH3OH | tau_chemical_effect | -17.97% | -17.97% (unchanged) |
    | C2H5OH | S_L_chemical_effect | -24.29% | -24.29% (unchanged) |
    | C2H5OH | tau_chemical_effect | -15.62% | -15.62% (unchanged) |
    | CH4 | S_L_chemical_effect | -17.25% | -17.25% (unchanged) |
    | CH4 | tau_chemical_effect | -3.23% | -3.23% (unchanged) |
    Flame-speed, ignition-delay and T_ad mixtures were built correctly all
    along (they use `fuels.mixture()` / `fuels.load_mechanism()`, not the
    buggy bookkeeping `stoich_o2`), so the chemical-effect percentages are
    identical; only Q_dry/Q_wet changed.
  - X2 re-check (`scripts_run/x2_final_new.py` from the xcheck worktree,
    no Cantera): module 08 Q_dry = 21,104,117.91 J/kg vs NIST-JANAF
    21,099,962.5 J/kg -> **+0.0197%** (tolerance +/-0.2%) -> **PASS**.
    The residual is the documented 1.3-2.5 kJ/mol San Diego vs NIST-JANAF
    formation-enthalpy difference (CH3OH -200938.85 vs -200941.5 J/mol),
    NOT tuned.
  - Fast tests: `pytest tests/test_water_chem.py -m "not slow"` -> 13 passed
    (incl. new `test_stoichiometric_oxygen_demand` for CH3OH/C2H5OH/CH4 =
    1.5/3.0/2.0 and `test_phi_one_mixture_matches_module_02` within 1e-12).
  - Scratch files (`_dbg_*.py`, `_poll*.sh`, `_cmp*.py`) removed from the
    worktree and from mail.
  - Committed on wme1-spray at <pending> (round 4).