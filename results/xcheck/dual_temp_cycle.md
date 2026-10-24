# J1: dual-temperature cycle cross-check, X5 vs Module 03 (normal vs hot regime)

Job: Claude box-queue water-engine-box-queue-20261024-1230, step J1. Run by Grok Bot on the box, 2026-10-24 (PDT).
Branch: wme1-hiT, on top of 23f22b0 (Module 03/04 normal vs hot regime runs).

## Status: executed + code-verified (2 implementations agree). Not validated against experiment.
- **Executed:** Module 03 normal and hot runs (23f22b0) and the X5 runs in this commit.
- **Verified (second implementation):** X5 (`sims/xcheck_cycle/x5_engine.py`) is the independent re-implementation of the SPEC 0-D cycle from xcheck/cycle 0d47bc7, unchanged apart from two repo-path lines. It shares no code with `sims/03_engine_cycle` and has its own integrator, Wiebe, Woschni, Livengood-Wu and thermo calls. It implements the *same model*, so this is a code check, not an independent-physics check. Model-form error in Woschni, Wiebe or Livengood-Wu is not tested.
- **Validated:** no. There is no engine-test data for these regimes.

## Temperatures (James's dual-temperature rule) and sources
Source: `sims/dual_temp/regimes.py`.
| | normal | hot (high-performance) | source |
|---|---|---|---|
| coolant | 363.15 K (90 °C) | 388.15 K (115 °C) | MAHLE / VW SSP 222; SAE 960271 |
| chamber gas-side wall (Woschni T_w) | 450 K | 520 K | SPEC §6; Heywood ch. 12 (400-600 K range) |
| intake charge at IVC | 320 / 360 K | 320 / 360 / 400 K | Module 03 sweep; 400 K = un-intercooled boost / heated intake |
In X5, only `WALL_T` (450 or 520 K) and T_intake change between regimes. Everything else matches the Module 03 SPEC: CA50 8° aTDC, knock retard in 2° steps up to 30°, and burn duration 25°·(S_L(0)/S_L(w))^0.5 capped at 80°, using the Module 02 flame-speed fits.

## Criterion (from the job, stated before the run)
For each pair, Δη = η_hot − η_normal in percentage points (pp).
- **PASS** if |Δη_X5 − Δη_M03| ≤ max(0.1 pp, 0.3·|Δη_M03|) and the signs agree.
- The sign test is waived when |Δη_M03| < 0.02 pp, which is below the solver noise of the two codes.
- Pairing is the same as in `sims/dual_temp/compare_m03.py`: same (fuel, CR, w, T_intake), plus hot at 400 K vs normal at 360 K.

## Result: PASS at all design points (27/27); 1284/1296 grid pairs PASS (99.1 %)
- **Design points:** 12 wme1-hiT design points (best dry / overall / water-majority × CH3OH, C2H5OH × normal, hot). This gives 6 best-vs-best deltas plus 21 same-point deltas. All 27 PASS.
- **Full Module 03 grid:** 2160 X5 runs (both regimes, 3 fuels including CH4, CR 9-24, w 0-0.8). Of 1296 pairs, 1284 PASS.
- **The 12 grid FAILs** (listed in `dual_temp_cycle/pairs.csv`, PASS=False) are all at the knock boundary. In each one, X5 and Module 03 pick a knock-limited CA50 that differs by one retard step (2°) in one of the two regimes. The Livengood-Wu integral sits within the step resolution of 1.0 there, so this is discretisation, not a physics disagreement. None of these points is a design point.
- **Knock-retarded point counts agree:**
  - CH3OH at 400 K vs 360 K: M03 31 (normal) / 44 (hot); X5 31 / 45.
  - C2H5OH: 19 / 39 in both codes.
- **Absolute offset:** X5 η is +0.29 pp above Module 03 in both regimes (normal +0.286, hot +0.283). This matches the 0d47bc7 X5 report (cycle.md) and cancels in Δη.

## Side by side at the design points
Module 03 and X5 numbers. Wall heat and NO come from Module 03 only, because X5 does not output them.
| fuel | design pt | regime | CR / w / T_intake | η M03 | η X5 | peak p M03/X5 [bar] | peak T M03/X5 [K] | wall heat M03 [J] | CA50 M03/X5 [°aTDC] | burn 10-90 [°] | rel. NO M03 | knock-retarded M03/X5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C2H5OH | dry | normal | 24 / 0 / 320 K | 44.54 % | 44.87 % | 96 / 97 | 2216 / 2227 | 249 | 14 / 14 | 25.0 | 1.00 | yes / yes |
| C2H5OH | dry | hot | 24 / 0 / 320 K | 44.50 % | 44.83 % | 88 / 89 | 2226 / 2237 | 219 | 16 / 16 | 25.0 | 1.00 | yes / yes |
| C2H5OH | overall | normal | 24 / 0.4 / 320 K | 45.44 % | 45.77 % | 122 / 123 | 1894 / 1905 | 277 | 8 / 8 | 29.8 | 0.04 | no / no |
| C2H5OH | overall | hot | 24 / 0.4 / 320 K | 45.86 % | 46.19 % | 123 / 124 | 1909 / 1919 | 259 | 8 / 8 | 29.8 | 0.04 | no / no |
| C2H5OH | water_majority | normal | 24 / 0.5 / 360 K | 44.89 % | 45.22 % | 116 / 116 | 1785 / 1794 | 254 | 8 / 8 | 32.6 | 0.01 | no / no |
| C2H5OH | water_majority | hot | 24 / 0.5 / 360 K | 45.35 % | 45.68 % | 117 / 117 | 1799 / 1809 | 236 | 8 / 8 | 32.6 | 0.01 | no / no |
| CH3OH | dry | normal | 20 / 0 / 320 K | 42.59 % | 42.91 % | 69 / 70 | 2196 / 2207 | 197 | 18 / 18 | 25.0 | 1.00 | yes / yes |
| CH3OH | dry | hot | 17 / 0 / 320 K | 42.30 % | 42.61 % | 68 / 69 | 2236 / 2248 | 188 | 16 / 16 | 25.0 | 1.00 | yes / yes |
| CH3OH | overall | normal | 24 / 0.3 / 320 K | 45.58 % | 45.91 % | 121 / 122 | 1919 / 1929 | 270 | 8 / 8 | 27.7 | 0.09 | no / no |
| CH3OH | overall | hot | 24 / 0.3 / 320 K | 45.97 % | 46.31 % | 122 / 123 | 1934 / 1944 | 253 | 8 / 8 | 27.7 | 0.12 | no / no |
| CH3OH | water_majority | normal | 24 / 0.5 / 360 K | 44.61 % | 44.95 % | 111 / 111 | 1663 / 1672 | 222 | 8 / 8 | 32.5 | 0.00 | no / no |
| CH3OH | water_majority | hot | 24 / 0.5 / 400 K | 45.21 % | 45.55 % | 110 / 110 | 1701 / 1711 | 206 | 8 / 8 | 32.5 | 0.00 | no / no |

| fuel | design pt | Δη hot−normal M03 [pp] | Δη X5 [pp] | tol [pp] | result |
|---|---|---|---|---|---|
| C2H5OH | dry (best vs best) | -0.046 | -0.047 | 0.100 | PASS |
| C2H5OH | same point CR24 w0, hot 320 K vs normal 320 K | -0.046 | -0.047 | 0.100 | PASS |
| C2H5OH | same point CR24 w0, hot 360 K vs normal 360 K | -1.536 | -1.549 | 0.461 | PASS |
| C2H5OH | same point CR24 w0, hot 400 K vs normal 360 K | -4.124 | -4.156 | 1.237 | PASS |
| C2H5OH | overall (best vs best) | +0.417 | +0.419 | 0.125 | PASS |
| C2H5OH | same point CR24 w0.4, hot 320 K vs normal 320 K | +0.417 | +0.419 | 0.125 | PASS |
| C2H5OH | same point CR24 w0.4, hot 360 K vs normal 360 K | +0.391 | +0.392 | 0.117 | PASS |
| C2H5OH | same point CR24 w0.4, hot 400 K vs normal 360 K | -0.155 | -0.157 | 0.100 | PASS |
| C2H5OH | water_majority (best vs best) | +0.462 | +0.463 | 0.138 | PASS |
| C2H5OH | same point CR24 w0.5, hot 320 K vs normal 320 K | +0.456 | +0.457 | 0.137 | PASS |
| C2H5OH | same point CR24 w0.5, hot 360 K vs normal 360 K | +0.462 | +0.463 | 0.138 | PASS |
| C2H5OH | same point CR24 w0.5, hot 400 K vs normal 360 K | +0.451 | +0.451 | 0.135 | PASS |
| CH3OH | dry (best vs best) | -0.298 | -0.304 | 0.100 | PASS |
| CH3OH | same point CR17 w0, hot 320 K vs normal 320 K | +0.195 | +0.196 | 0.100 | PASS |
| CH3OH | same point CR17 w0, hot 360 K vs normal 360 K | -0.676 | -0.683 | 0.203 | PASS |
| CH3OH | same point CR17 w0, hot 400 K vs normal 360 K | -3.034 | -3.058 | 0.910 | PASS |
| CH3OH | same point CR20 w0, hot 320 K vs normal 320 K | -0.416 | -0.420 | 0.125 | PASS |
| CH3OH | same point CR20 w0, hot 360 K vs normal 360 K | +0.160 | +0.159 | 0.100 | PASS |
| CH3OH | same point CR20 w0, hot 400 K vs normal 360 K | -0.395 | -0.399 | 0.119 | PASS |
| CH3OH | overall (best vs best) | +0.393 | +0.394 | 0.118 | PASS |
| CH3OH | same point CR24 w0.3, hot 320 K vs normal 320 K | +0.393 | +0.394 | 0.118 | PASS |
| CH3OH | same point CR24 w0.3, hot 360 K vs normal 360 K | +0.369 | +0.370 | 0.111 | PASS |
| CH3OH | same point CR24 w0.3, hot 400 K vs normal 360 K | -0.102 | -0.097 | 0.100 | PASS |
| CH3OH | water_majority (best vs best) | +0.600 | +0.599 | 0.180 | PASS |
| CH3OH | same point CR24 w0.5, hot 320 K vs normal 320 K | +0.475 | +0.476 | 0.142 | PASS |
| CH3OH | same point CR24 w0.5, hot 360 K vs normal 360 K | +0.478 | +0.479 | 0.143 | PASS |
| CH3OH | same point CR24 w0.5, hot 400 K vs normal 360 K | +0.600 | +0.599 | 0.180 | PASS |

| fuel | hot T_intake vs normal | n pairs | PASS | mean Δη M03 | mean Δη X5 | max abs diff | knock-retarded pts M03 n/h | X5 n/h |
|---|---|---|---|---|---|---|---|---|
| C2H5OH | 320 K vs 320 K | 144 | 143 | +0.298 | +0.296 | 0.293 | 0/0 | 7/9 |
| C2H5OH | 360 K vs 360 K | 144 | 141 | +0.245 | +0.246 | 0.369 | 0/0 | 20/23 |
| C2H5OH | 400 K vs 360 K | 144 | 143 | -0.400 | -0.407 | 0.772 | 0/6 | 20/39 |
| CH3OH | 320 K vs 320 K | 144 | 143 | +0.253 | +0.255 | 0.144 | 0/0 | 17/19 |
| CH3OH | 360 K vs 360 K | 144 | 141 | +0.220 | +0.212 | 0.831 | 4/5 | 31/33 |
| CH3OH | 400 K vs 360 K | 144 | 143 | -0.411 | -0.415 | 0.191 | 4/16 | 31/45 |
| CH4 | 320 K vs 320 K | 144 | 144 | +0.278 | +0.278 | 0.004 | 0/0 | 0/1 |
| CH4 | 360 K vs 360 K | 144 | 143 | +0.272 | +0.271 | 0.204 | 0/0 | 9/11 |
| CH4 | 400 K vs 360 K | 144 | 143 | -0.288 | -0.295 | 0.626 | 0/0 | 9/28 |

## Does hotter do better?
- **Same intake temperature, hotter coolant and walls (450 → 520 K):** yes, slightly. Mean Δη is +0.22 to +0.30 pp in both engines.
  - Wall heat drops by 6-12 %.
  - Peak T rises by 10-15 K.
  - Relative NO rises a little (CH3OH overall: 0.09 → 0.12).
  - A few more points need knock retard.
- **Hot regime with a 400 K intake (vs normal 360 K):** no. Mean Δη is −0.29 to −0.41 pp. The hotter charge is more knock-prone (knock-retarded points rise 1.4× for CH3OH, 2× for C2H5OH, 3.5× for CH4), and the retard costs more than the wall-heat saving gains.
  - Dry CR24 C2H5OH: −1.5 pp at 360 K, −4.1 pp at 400 K.
  - Dry CR17 CH3OH: −3.0 pp.
- **Best design points:**
  - Water-injected (overall / water-majority): hot is better by +0.39 to +0.60 pp. Water suppresses knock, so CA50 stays at 8°.
  - Dry: hot is worse or equal. CH3OH −0.30 pp (best CR drops from 20 to 17); C2H5OH −0.05 pp.
- **Bottom line:** in the 0-D model, hotter walls help only when water keeps the charge out of knock. A hot intake charge always costs efficiency. Both engines agree to within 0.01 pp at these points, but this is a model-to-model agreement. The knock and Woschni sub-models have not been validated.

## Reproduce (from the repo root, Cantera venv)
```
python -W ignore -m sims.xcheck_cycle.dual_temp --workers 6 --grid    # 2160 runs, about 9 min on 6 cores
python -m sims.xcheck_cycle.compare_dual_temp                         # pairs.csv + summary.json
```
- **Files:** `results/xcheck/dual_temp_cycle/{x5_runs.json,pairs.csv,summary.json}`
- **Inputs:** `results/dual_temp/03_engine_cycle_{normal,hot}/cycle_points.csv`, `results/dual_temp/03_compare/summary.json` and `results/02_flame_chem/*_fits.json`.
- **Note:** `sims/xcheck_cycle/run.py` on wme1-dev 62a151f is truncated (152 lines, no entry point), so X5 was taken from xcheck/cycle 0d47bc7 instead.
