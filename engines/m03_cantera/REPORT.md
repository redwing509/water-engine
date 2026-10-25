# M03-CRN: independent Cantera ReactorNet engine for Module 03, verification and 2-engine comparison

Grok Bot, 2026-10-24 (Claude job `reply-verification-20261024-1430`, item V1). Branch `engines/m03-cantera-reactornet`.

The acceptance criteria were pre-registered in `ACCEPTANCE.md` and committed in 69babf3 before any run; they were not changed afterwards.

**Status:**
- **Executed and code-verified** (V-A to V-C PASS).
- **2-engine agreement with Module 03 for eta and p_max: PASS** under C1 (Woschni in both engines, 18/18 rows, both regimes).
- **Not validated** against engine experiments.

## How independent it is
See the table in `ACCEPTANCE.md`. Summary:
- The **solver is independent**:
  - integrator: CVODES BDF instead of an explicit midpoint on a fixed grid;
  - work: a moving Cantera Wall carries the piston motion and the work is a CVODES state;
  - heat release: Wiebe enters as a wall heat flux, not as a dU per step;
  - dissociation: finite-rate GRI product kinetics instead of TP equilibrium;
  - thermo: GRI/NASA-7 instead of San Diego;
  - evaporation: MFC with a latent sink and saturation relaxation instead of a lagged cap;
  - LHV: own value.
- **Shared on purpose** (problem definition): geometry, valve events, the Wiebe a/m/CA50/duration of each row, the IVC charge state from the Module 03 row (masses, T_IVC, intake-evaporated fraction), wall temperature, and the efficiency definition.
- The engine does **not import or copy** `sims/03_engine_cycle`.
- The burn rate is therefore prescribed in both engines and is not an independent output.

## Verification of the engine on its own (`verification.json`, `wiebe_integral.json`; box, 5-6 processes)
| check | criterion | result |
|---|---|---|
| V-A ideal Otto (gamma 1.4, adiabatic) | error ≤ 1e-3, and it shrinks when the burn goes from 1.0 to 0.5 CAD | **PASS**. CR16: −2.9e-5 → −7.3e-6. CR24: −3.7e-5 → −9.5e-6 |
| V-B rtol 1e-6/1e-7/1e-8/1e-9 at the 12 unique design points × {Woschni, Hohenberg} | relative change from 1e-8 to 1e-9 ≤ 1e-5 | **PASS**: max 1.8e-6 (p_max) |
| V-B GCI (Roache, Fs 1.25, r 10) | GCI_fine ≤ 1e-4 where defined | **PASS**: max 3.3e-6. Defined for 102/144 quantity series; the other 42 are non-monotone at the 1e-9 noise floor or have e21 = 0, so no GCI exists. Their 1e-8 → 1e-9 change is still ≤ 1.8e-6 |
| V-B evaporation tau halved (0.05 → 0.025 CAD) | change in eta ≤ 1e-4 | **PASS**: max 3.0e-6 |
| V-B output sampling halved | informational | p_max changes ≤ 2.7e-7 relative |
| V-C energy closure | ≤ 1e-5 of Q_fuel | **PASS**: max 7.9e-8 (verify) and 6.3e-8 (all 72 comparison runs) |
| V-C Wiebe integral vs Q_avail | ≤ 1e-6 relative | **PASS**: max 3.8e-9 (18 rows × 2 heat-transfer models) |
| V-D Cantera `ic_engine.py` | usable as a benchmark? | **Not applicable.** It is a CI engine with gas injection and finite-rate fuel chemistry. Only its moving-wall pattern is reused |

Notes on V-B:
- rtol 1e-6 is **not** converged: wall heat differs by up to 13 % from 1e-9. Production runs use rtol 1e-9.
- Wording slip in ACCEPTANCE.md: it says "atol = 1e-6 × rtol". The engine default is atol 1e-17 at rtol 1e-9, and `verify.py` uses atol = rtol × 1e-8. The convergence result does not depend on this.

## 2-engine comparison against Module 03 (`compare.csv`, `compare.json`)
**Module 03 input:** wme1-hiT 23f22b0 dual-temperature rows (`results/dual_temp/03_engine_cycle_{normal,hot}`). That is Module 03 v1.0.0, before the c0385a7 step-convergence fix (PR #6). The fix moves eta by ≤ 0.007 % relative, which is far below the tolerance here.

**Rows:** 18 rows (9 per regime). They are the 12 design points of `design_point.json` (best_dry, best_overall, water_majority for each fuel and regime), each also run in the other regime.

**Regimes:**
- normal: wall 450 K, coolant 363 K
- hot: wall 520 K, coolant 388 K, intake up to 400 K

| variant | criterion | within tolerance | max abs d eta | max abs d p_max | max abs d T_max |
|---|---|---|---|---|---|
| **C1, Woschni in both (the 2-engine gate)** | ±1.5 pp eta, ±5 % p_max at every row | **18/18 PASS** | 0.042 pp | 0.096 % | 13 K |
| C2, M03-CRN production (Hohenberg) | same, reported only | 8/18. Eta fails at 10 rows; p_max is within tolerance at all rows | 2.49 pp | 1.98 % | 82 K |
| S1, Woschni with frozen products (no dissociation kinetics) | model delta | 18/18 | 0.13 pp | 0.11 % | 34 K |
| S2, adiabatic | model delta | 0/18 | 7.06 pp | 3.8 % | 169 K |

### Heat-transfer deltas (explicit)
- **Hohenberg vs Woschni.** In the same engine, Hohenberg loses **4–29 % less heat** to the wall (117–221 J against 164–271 J per cycle), so eta is **+0.4 to +2.5 pp** higher.
  - The gap is largest at the high-CR water points (+1.8 to +2.5 pp).
  - It is smallest at dry CR15/16 CH3OH (+0.4 to +0.7 pp).
  - This is **heat-transfer model-form uncertainty**, not a solver disagreement: C1 shows the solvers agree when the correlation is the same. Treat Module 03's eta as carrying about **−0 / +2.5 pp model-form uncertainty** from the choice of wall heat-transfer correlation.
- **Adiabatic limit.** Wall heat costs 3.9–7.1 pp of eta.
- **Dissociation model.** Kinetic dissociation (CRN) and TP-equilibrium dissociation (M03) differ by ≤ 0.04 pp eta. Freezing the products entirely changes eta by ≤ 0.13 pp and raises T_max by up to 34 K.
- **T_max.** CRN T_max is 1–13 K above M03. The largest gap is at the dry points, consistent with kinetic dissociation lagging equilibrium near peak T.

### C1 (Woschni in both engines): all 18 module-03 rows

| regime | point | roles | eta M03 | eta CRN | d eta [pp] | pmax M03/CRN [MPa] | d pmax | Tmax M03/CRN [K] | Qwall M03/CRN [J] | IMEP M03/CRN [bar] | peak burn rate [J/deg] | T_endgas@pmax CRN [K] | knock int. M03 | NO M03 / CRN bulk | in tol |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hot | C2H5OH/CR=22/w=0.0/T_intake=320 | hot:C2H5OH:best_dry | 0.4441 | 0.4439 | -0.016 | 9.09/9.08 | -0.10 % | 2245/2258 | 229/229 | 13.38/13.38 | 58.8 | 941 | 0.86 | 2.86e-08 / 2.38e-09 | True |
| normal | C2H5OH/CR=22/w=0.0/T_intake=320 |  | 0.4430 | 0.4428 | -0.020 | 9.85/9.84 | -0.09 % | 2239/2251 | 260/261 | 13.35/13.35 | 58.8 | 949 | 0.98 | 2.92e-08 / 2.30e-09 | True |
| hot | C2H5OH/CR=23/w=0.4/T_intake=320 | hot:C2H5OH:best_overall | 0.4569 | 0.4565 | -0.042 | 11.85/11.84 | -0.09 % | 1919/1922 | 254/254 | 14.62/14.61 | 52.5 | 708 | 0.00 | 1.11e-09 / 1.91e-11 | True |
| normal | C2H5OH/CR=23/w=0.4/T_intake=320 | normal:C2H5OH:best_overall | 0.4529 | 0.4525 | -0.042 | 11.75/11.74 | -0.08 % | 1905/1908 | 271/271 | 14.49/14.48 | 52.5 | 699 | 0.00 | 9.73e-10 / 1.47e-11 | True |
| hot | C2H5OH/CR=24/w=0.0/T_intake=320 |  | 0.4450 | 0.4449 | -0.013 | 8.85/8.84 | -0.09 % | 2226/2238 | 219/219 | 13.35/13.36 | 58.6 | 935 | 0.83 | 2.60e-08 / 1.76e-09 | True |
| normal | C2H5OH/CR=24/w=0.0/T_intake=320 | normal:C2H5OH:best_dry | 0.4454 | 0.4453 | -0.018 | 9.64/9.64 | -0.09 % | 2216/2227 | 249/250 | 13.37/13.37 | 58.6 | 943 | 0.94 | 2.64e-08 / 1.62e-09 | True |
| hot | C2H5OH/CR=24/w=0.6/T_intake=360 |  | 0.4426 | 0.4427 | +0.006 | 11.30/11.30 | -0.02 % | 1623/1625 | 204/202 | 13.40/13.40 | 39.6 | 677 | 0.00 | 8.05e-12 / 5.01e-14 | True |
| normal | C2H5OH/CR=24/w=0.6/T_intake=360 | normal:C2H5OH:water_majority;normal:C2H5OH:comparison_vs_best_dry | 0.4378 | 0.4380 | +0.011 | 11.20/11.20 | -0.01 % | 1610/1611 | 221/220 | 13.25/13.26 | 39.6 | 675 | 0.00 | 7.10e-12 / 3.56e-14 | True |
| hot | C2H5OH/CR=24/w=0.6/T_intake=400 | hot:C2H5OH:water_majority;hot:C2H5OH:comparison_vs_best_dry | 0.4441 | 0.4442 | +0.008 | 11.10/11.10 | -0.02 % | 1647/1649 | 205/203 | 12.85/12.85 | 37.9 | 682 | 0.00 | 1.63e-11 / 9.13e-14 | True |
| hot | CH3OH/CR=15/w=0.0/T_intake=320 | hot:CH3OH:best_dry | 0.4180 | 0.4180 | +0.005 | 6.76/6.75 | -0.02 % | 2263/2277 | 192/192 | 12.51/12.51 | 58.4 | 898 | 0.86 | 1.77e-08 / 2.54e-09 | True |
| normal | CH3OH/CR=15/w=0.0/T_intake=320 |  | 0.4187 | 0.4187 | +0.000 | 7.22/7.22 | -0.01 % | 2263/2277 | 216/217 | 12.53/12.53 | 58.4 | 903 | 0.95 | 1.84e-08 / 2.63e-09 | True |
| hot | CH3OH/CR=16/w=0.0/T_intake=320 |  | 0.4188 | 0.4189 | +0.008 | 6.55/6.55 | -0.04 % | 2245/2258 | 184/185 | 12.48/12.48 | 58.2 | 891 | 0.77 | 1.61e-08 / 1.94e-09 | True |
| normal | CH3OH/CR=16/w=0.0/T_intake=320 | normal:CH3OH:best_dry | 0.4207 | 0.4207 | +0.003 | 7.04/7.03 | -0.04 % | 2243/2255 | 208/208 | 12.53/12.53 | 58.2 | 897 | 0.87 | 1.68e-08 / 1.95e-09 | True |
| hot | CH3OH/CR=23/w=0.3/T_intake=320 | hot:CH3OH:best_overall | 0.4581 | 0.4578 | -0.033 | 11.78/11.78 | -0.07 % | 1943/1946 | 248/248 | 14.20/14.19 | 54.6 | 756 | 0.02 | 1.11e-09 / 2.57e-11 | True |
| normal | CH3OH/CR=23/w=0.3/T_intake=320 | normal:CH3OH:best_overall | 0.4543 | 0.4539 | -0.033 | 11.69/11.68 | -0.06 % | 1929/1932 | 265/265 | 14.08/14.07 | 54.6 | 746 | 0.01 | 9.66e-10 / 1.98e-11 | True |
| hot | CH3OH/CR=24/w=0.6/T_intake=360 |  | 0.4360 | 0.4362 | +0.018 | 10.72/10.72 | -0.01 % | 1482/1483 | 166/164 | 12.81/12.81 | 38.4 | 675 | 0.00 | 1.38e-13 / 7.35e-16 | True |
| normal | CH3OH/CR=24/w=0.6/T_intake=360 | normal:CH3OH:water_majority;normal:CH3OH:comparison_vs_best_dry | 0.4310 | 0.4312 | +0.024 | 10.63/10.63 | -0.00 % | 1470/1471 | 183/182 | 12.66/12.67 | 38.4 | 673 | 0.00 | 1.20e-13 / 4.85e-16 | True |
| hot | CH3OH/CR=24/w=0.6/T_intake=400 | hot:CH3OH:water_majority;hot:CH3OH:comparison_vs_best_dry | 0.4385 | 0.4387 | +0.019 | 10.55/10.55 | -0.00 % | 1504/1505 | 167/166 | 12.32/12.33 | 36.7 | 680 | 0.00 | 2.85e-13 / 1.52e-15 | True |

### Sensitivity variants: d eta [pp] and d pmax vs module 03, per row

| regime | point | C2 Hohenberg d eta | C2 d pmax | C2 Qwall CRN [J] | frozen d eta | adiabatic d eta |
|---|---|---|---|---|---|---|
| hot | C2H5OH/CR=22/w=0.0/T_intake=320 | +1.09 | +0.36 % | 199 | +0.079 | +5.51 |
| normal | C2H5OH/CR=22/w=0.0/T_intake=320 | +1.49 | +0.45 % | 221 | +0.060 | +6.43 |
| hot | C2H5OH/CR=23/w=0.4/T_intake=320 | +2.39 | +1.98 % | 181 | -0.031 | +6.62 |
| normal | C2H5OH/CR=23/w=0.4/T_intake=320 | +2.49 | +1.90 % | 197 | -0.031 | +7.02 |
| hot | C2H5OH/CR=24/w=0.0/T_intake=320 | +0.89 | +0.01 % | 196 | +0.078 | +5.25 |
| normal | C2H5OH/CR=24/w=0.0/T_intake=320 | +1.27 | +0.06 % | 217 | +0.059 | +6.16 |
| hot | C2H5OH/CR=24/w=0.6/T_intake=360 | +2.14 | +1.84 % | 144 | +0.009 | +5.63 |
| normal | C2H5OH/CR=24/w=0.6/T_intake=360 | +2.22 | +1.76 % | 160 | +0.014 | +6.11 |
| hot | C2H5OH/CR=24/w=0.6/T_intake=400 | +2.21 | +1.88 % | 146 | +0.011 | +5.94 |
| hot | CH3OH/CR=15/w=0.0/T_intake=320 | +0.51 | +0.37 % | 182 | +0.129 | +4.03 |
| normal | CH3OH/CR=15/w=0.0/T_intake=320 | +0.71 | +0.36 % | 201 | +0.112 | +4.62 |
| hot | CH3OH/CR=16/w=0.0/T_intake=320 | +0.41 | +0.22 % | 178 | +0.126 | +3.86 |
| normal | CH3OH/CR=16/w=0.0/T_intake=320 | +0.60 | +0.18 % | 197 | +0.109 | +4.45 |
| hot | CH3OH/CR=23/w=0.3/T_intake=320 | +2.28 | +1.83 % | 181 | -0.020 | +6.68 |
| normal | CH3OH/CR=23/w=0.3/T_intake=320 | +2.37 | +1.72 % | 196 | -0.021 | +7.06 |
| hot | CH3OH/CR=24/w=0.6/T_intake=360 | +1.79 | +1.55 % | 117 | +0.020 | +4.71 |
| normal | CH3OH/CR=24/w=0.6/T_intake=360 | +1.85 | +1.44 % | 134 | +0.025 | +5.20 |
| hot | CH3OH/CR=24/w=0.6/T_intake=400 | +1.85 | +1.59 % | 120 | +0.021 | +4.98 |

### Hot minus normal at the same point (both engines)

| variant | point | d eta M03 [pp] | d eta CRN [pp] | d Qwall CRN [J] | d pmax CRN [MPa] | d Tmax CRN [K] | d NO CRN (rel) | same sign |
|---|---|---|---|---|---|---|---|---|
| C1_woschni | C2H5OH/CR=22/w=0.0/T_intake=320 | +0.105 | +0.110 | -31.8 | -0.76 | +6.7 | +3 % | True |
| C1_woschni | C2H5OH/CR=23/w=0.4/T_intake=320 | +0.404 | +0.404 | -17.2 | +0.09 | +14.6 | +30 % | True |
| C1_woschni | C2H5OH/CR=24/w=0.0/T_intake=320 | -0.046 | -0.041 | -30.9 | -0.80 | +10.7 | +9 % | True |
| C1_woschni | C2H5OH/CR=24/w=0.6/T_intake=360 | +0.479 | +0.474 | -17.4 | +0.10 | +13.3 | +41 % | True |
| C1_woschni | CH3OH/CR=15/w=0.0/T_intake=320 | -0.071 | -0.066 | -24.2 | -0.47 | +0.0 | -4 % | True |
| C1_woschni | CH3OH/CR=16/w=0.0/T_intake=320 | -0.189 | -0.184 | -23.6 | -0.48 | +2.7 | -0 % | True |
| C1_woschni | CH3OH/CR=23/w=0.3/T_intake=320 | +0.381 | +0.381 | -16.6 | +0.09 | +14.6 | +29 % | True |
| C1_woschni | CH3OH/CR=24/w=0.6/T_intake=360 | +0.497 | +0.492 | -17.3 | +0.09 | +12.4 | +51 % | True |
| C2_hohenberg | C2H5OH/CR=22/w=0.0/T_intake=320 | +0.105 | -0.294 | -21.7 | -0.77 | -1.7 | -7 % | False |
| C2_hohenberg | C2H5OH/CR=23/w=0.4/T_intake=320 | +0.404 | +0.308 | -15.9 | +0.11 | +13.7 | +27 % | True |
| C2_hohenberg | C2H5OH/CR=24/w=0.0/T_intake=320 | -0.046 | -0.427 | -21.3 | -0.80 | +2.5 | -2 % | True |
| C2_hohenberg | C2H5OH/CR=24/w=0.6/T_intake=360 | +0.479 | +0.405 | -16.6 | +0.11 | +12.4 | +33 % | True |
| C2_hohenberg | CH3OH/CR=15/w=0.0/T_intake=320 | -0.071 | -0.269 | -19.3 | -0.47 | -3.1 | -7 % | True |
| C2_hohenberg | CH3OH/CR=16/w=0.0/T_intake=320 | -0.189 | -0.377 | -19.0 | -0.48 | -0.4 | -4 % | True |
| C2_hohenberg | CH3OH/CR=23/w=0.3/T_intake=320 | +0.381 | +0.285 | -15.5 | +0.11 | +14.3 | +27 % | True |
| C2_hohenberg | CH3OH/CR=24/w=0.6/T_intake=360 | +0.497 | +0.437 | -16.8 | +0.11 | +11.7 | +44 % | True |

Column notes:
- **peak burn rate** is the prescribed Wiebe rate, identical in both engines by construction.
- **T_endgas@pmax** is the CRN end-gas temperature: unburned charge compressed isentropically to p_max. It is a knock indicator only. Module 03's knock integral is shown next to it for reference.
- **NO.** Module 03 NO is from its burned-zone model. CRN NO is single-zone bulk with product kinetics, which is 1–3 orders lower. **NO is not cross-checked.** The bulk value is indicative only.

## Is hot better? (each engine, same point, hot minus normal)
- **Woschni (C1).** The two engines agree on the sign at **8/8** points, and their d eta values differ by ≤ 0.006 pp.
  - Hot is **better** at the water points: +0.38 to +0.50 pp at CH3OH CR23 w0.3, CH3OH CR24 w0.6, C2H5OH CR23 w0.4 and C2H5OH CR24 w0.6. It is also +0.11 pp better at C2H5OH CR22 dry.
  - Hot is **slightly worse** at the other dry points: −0.07 to −0.19 pp at CH3OH CR15/16 and −0.05 pp at C2H5OH CR24.
  - In the hot regime, wall heat is 16–32 J lower per cycle.
  - Dry-point p_max is 0.5–0.8 MPa lower, following the Module 03 hot-regime IVC state.
  - Bulk NO is +29 to +51 % higher at the water points.
- **Hohenberg (C2).** 7/8 points have the same sign. C2H5OH CR22 dry flips: −0.29 pp against M03's +0.11 pp. Every hot-minus-normal delta is about 0.1–0.4 pp lower than with Woschni.
- **Hot-regime design points.** The hot regime's water_majority point uses T_intake 400 K. Its eta is 0.4387 for CH3OH and 0.4442 for C2H5OH, against 0.4312 and 0.4380 at the normal regime's T_intake 360 K. That is +0.6 to +0.75 pp in both engines.
- **Verdict.** Hotter helps efficiency by ≤ 0.5 pp at the same point, and only where water is present. For dry operation it is neutral to slightly negative.
  - The size of the gain depends on the wall heat-transfer correlation by about 0.1–0.4 pp.
  - Knock is **not** settled by these two engines; J2 (module 02/08) shows ignition delays 4–5× shorter in the hot regime.
- **Misfire** is not computed by either engine (Module 11 scope).

## What this does and does not establish
- **Establishes:** for Module 03 eta and p_max at all 12 design points in both regimes, a second implementation with an independent integrator, thermo, wall/work formulation, dissociation model and evaporation model agrees within ±1.5 pp and ±5 %. The actual spread is 0.04 pp and 0.1 %.
- **Does not establish:**
  - Agreement when the Wiebe parameters and IVC state differ, since they are shared problem inputs.
  - The heat-transfer correlation itself: Hohenberg vs Woschni is ±2.5 pp of model-form uncertainty, and only experiment can settle it.
  - NO, knock and misfire.
  - Any validation against measured engine data.

## Reproduce
```
python engines/m03_cantera/verify.py 5             # V-A..V-D -> results/engines/m03_cantera/verification.json (~7 min, 5 procs)
python engines/m03_cantera/check_wiebe_integral.py # V-C Wiebe integral -> wiebe_integral.json (~3 min, 6 procs)
python engines/m03_cantera/compare_m03.py 6        # C1/C2/S1/S2 -> compare.csv, compare.json (~10 min, 6 procs)
pytest tests/test_m03_cantera.py                   # fast checks (<2 s)
```
Requires Cantera 3.2.0 (tested). Module 03 rows are frozen in `engines/m03_cantera/m03_rows.json`, with provenance inside the file.
