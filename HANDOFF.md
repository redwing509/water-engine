# WME-1 hand-off log

Worker: Claude, acting for Hermes at James's request. Supervisor verification is still pending. Times are UTC.

## 2026-10-22 — Phase 0: seed and first push
- Seed files confirmed in the repo root and `docs/research/`. Committed `53cd311` "Seed: README, SPEC, research dossier 01". gitleaks: no leaks.
- **Push pending:** `github.com/redwing509/water-engine` does not exist yet ("Repository not found"). James has been asked once to create it (public, empty). Work continues as local commits.
- **Deviation:** `HERMES_PROMPT.md` (the worker brief) is in `.gitignore` and not committed. It names private infrastructure (host aliases, local paths, other services), and the project's secrets rule forbids committing that.

## 2026-10-22 — Phase 1: research doc 02
- Wrote `docs/research/02-legitimate-water-combustion.md` from web research: 71 numbered references with full URLs, and a validation-targets table with 32 rows. Two rows (methanol and ethanol ignition delays) name the datasets but have no extracted numbers.
- Weak or not found, so marked uncertain in the doc:
  - Conklin & Szybist's numeric efficiency gain and water mass per cycle;
  - a measured knock-limited CR gain from water;
  - Mack et al. 2009 test conditions;
  - SI data above 40 % water;
  - absolute methanol S_L with steam;
  - numeric ignition delays for wet alcohols;
  - adiabatic flame temperatures (secondary source only).
- The references were gathered by a research sub-agent. The supervisor should spot-check URLs during verification.

## 2026-10-22 — Phase 2: VPS environment
- Compute host work dir: `/opt/water-engine`, venv `.venv` (Python 3.12.3). Installed with nice 19, inside the venv only: cantera 3.2.0, CoolProp 8.0.0, numpy, scipy, pandas, matplotlib, pytest, cadquery 2.8.0. No apt was used.
- San Diego mechanism release 2016-12-14 downloaded and converted with `ck2yaml` to `mechanisms/sandiego.yaml` (59 species, 271 reactions). URLs, date and SHA-256 are in `mechanisms/PROVENANCE.md`. Converter thermo-discontinuity warnings are recorded there.
- Commands:
  - `python -m venv .venv`;
  - `pip install "cantera>=3.1" "CoolProp>=6.6" numpy scipy pandas matplotlib pytest`, then `pip install cadquery`;
  - `curl` of the three mechanism files;
  - `python -m cantera.ck2yaml --input=... --thermo=... --transport=... --output=sandiego.yaml`.

## 2026-10-22 — Phase 3.1: scaffold, Module 01, Module 05 (Codex)
- Codex (composer route, tier heavy: gpt-6-astra, high effort) wrote `requirements*.txt`, `sims/common/{fuels,io}.py`, `sims/01_energy_audit`, `sims/05_aluminum_water`, `tests/`, `run_all.sh` and `.github/workflows/ci.yml`. Only py_compile was run on the laptop.
- Codex overwrote `mechanisms/PROVENANCE.md` while it ran; the full provenance was restored afterwards.
- VPS check (code mirrored by tarball; `WME_GIT_SHA` set from the laptop HEAD): `pytest` **69 passed**. Both modules exit 0 with `--quick` (about 13 s each).
- Validation in summary.json, all passed:
  - LHV H2 119.95, CH4 50.03, CH3OH(l) 19.93 and C2H5OH(l) 26.80 MJ/kg; LHV H2O 0 J/kg.
  - HHO loop gain max 0.265 (< 1).
  - The HHO kit is a net shaft loss of about 433 W.
  - Al + water bookkeeping closes. Water alone releases no energy.
- Gibbsite and boehmite enthalpies come from Chen & Zeng 1996 (cited in code), because NIST-JANAF does not list them.

## 2026-10-22 — Phase 3.2: Module 02 `flame_chem` (Codex)
- Codex (heavy tier) wrote `sims/02_flame_chem`, `tests/test_flame_chem.py` and `pytest.ini` (registers the `slow` mark; slow tests still run by default). It added an optional `chunksize` to `io.ordered_map`.
- First VPS run: pytest 106 passed, 1 failed; `--quick` exit 0 in 61 s on 2 workers.
  - The failure was `test_ignition_horizon_is_censored`. `ReactorNet.step()` can overshoot the censoring horizon (1.037e-8 s against a 1e-8 s limit).
  - It was fixed in the code, not the test: the final segment now uses `network.advance(max_time_s)`, so the simulated time never passes the horizon.
- Re-run of the flame/fuels/io tests: **89 passed**.
- Added `.gitattributes` (LF for scripts and sources), so the shell scripts stay runnable on Linux.

## 2026-10-22 — Module 02 full run
- `02_flame_chem --full` (nice 19, 8 workers, commit `4daa1f6`): exit 0 in 1873 s. Load-gated: it waited for the host's 1-min load to drop to 8 or below.

## 2026-10-22 — Phase 3.3: Module 03 `engine_cycle`
- Codex hit its usage limit partway through this module (router: 6 h cooldown). Cursor was unauthenticated and the local model was down. So, under the brief's fallback rule, the module was finished by Claude. Codex's draft is kept outside the repo for reference. The draft had defects that were fixed:
  - its intake energy balance overstated the cooling by about γ;
  - wet points failed;
  - its knock fallback fit never knocked;
  - its Otto and closure checks were tautological.
- VPS: `tests/test_engine_cycle.py` 22 passed. `--quick` exit 0 in 33 s, using synthetic fallback fits clearly labelled `mode-quick-fallback`. Maximum energy-closure error 3.1e-4; ideal-Otto error 3.8e-5.
- **Deviations from SPEC §6, stated plainly:**
  1. Latent heat inside the closed cylinder uses u_fg (internal energy), not h_fg; the intake uses h_fg.
  2. `f_evap_intake = 0.5` is physically infeasible for wet charges, because it would supersaturate the intake. Intake evaporation is therefore capped at saturation (5–25 %), and the rest evaporates by −26 to −2 CAD instead of by −30 CAD.
  3. The alcohol's own latent heat is deducted from the heat release, so it gets no charge-cooling credit. The residual gas is dry, at T_intake.
  4. The comparison with Cantera's `ic_engine.py` is documented, not reproduced.
  5. The knock integral extrapolates Module 02's ignition fits, which exist only at 40 bar, in pressure; the share of the integral that is extrapolated is reported.
- Flagged as uncertain: at w ≥ 0.7 the end-gas flame temperature is 1050–1470 K, below a ~1500 K limit-flame temperature. Points are tagged `low_flame_temperature` (a diagnostic, not a constraint). Module 02's S_L comes from all-vapour flames and may overstate flammability there.
