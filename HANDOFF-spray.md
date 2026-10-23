# WME-1 spray track hand-off

Worker: Claude (supervising), Hermes (coding), James (approved coding + downloads).
Worktree: `C:/Users/spoka/git/water-engine-spray`, branch `wme1-spray`.
Mail VPS code: `/opt/water-engine/code-spray`, venv `/opt/water-engine/.venv`.

## Status

| Item | Module | Status | Notes |
|---|---|---|---|
| A | `08_water_chemistry` | IN PROGRESS | --quick + full pytest on mail; energy closure fixed |
| B | `09_spray_evaporation` | TODO | |
| C | `11_spray_flame` | TODO | |

## Round log

### 2026-10-22 — Setup
- Created worktree `wme1-spray` at `C:/Users/spoka/git/water-engine-spray` from `b00342f`.
- Added SPEC §12 "Spray track" with module specs 08/09/11.
- Synced code to `/opt/water-engine/code-spray` (reused `/opt/water-engine/.venv`).

### 2026-10-23 — Item A: module 08 water chemistry
|- Energy closure bookkeeping was wrong on mail (stale copy used `equilibrate("HP")` +
  bare `int_energy_mole`, no mole scaling; Q_dry ≈ 2.3e3 J/kg vs true 2.17e7 J/kg).
  The local `run.py` uses explicit mole-scaled enthalpy bookkeeping
  (`h_react*n_react - h_prod*n_prod`), which gives Q_dry = 21.707 MJ/kg for CH3OH
  and Q_wet ≡ Q_dry to 3e-16 relative. Local file is authoritative; mail copy was stale.
|- Validation check 4 rewritten from a 1.0 J/mol tolerance on the absolute difference
  to a 1e-6 relative tolerance on `energy_closure_rel`, matching the SPEC.
|- Scratch files deleted; mechanisms/08_water_chem/*.bak removed on mail.

### 2026-10-23 (round 2) — Item A: module 08 water chemistry, commit
|- Mail copy of `sims/08_water_chem/run.py` was stale (read `atoms[2]`/`atoms[3]` on a
  `tuple[int,int,int]` Fuel; correct is `atoms[1]`/`atoms[2]` for H/O). Re-synced from
  the local worktree (md5 72c031440eceb633fad7f8012bce7d69). All other files already
  matched.
|- Fast tests: `pytest tests/test_water_chem.py -m "not slow"` -> 4 passed, 2 deselected.
|- `--quick` run (2 workers, out results/quick08): validation `passed=true`, all 13
  checks passed. Energy closure: Q_dry = 21.50852035547747 MJ/kg, Q_wet identical to
  1.73e-16 relative. O balance rel error 4.4e-13.
|- Slow tests (`-m slow`, 2 tests) and `--full` run launched in background on mail
  (ai-job water-engine, ttl 600). Results next round.