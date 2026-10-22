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
