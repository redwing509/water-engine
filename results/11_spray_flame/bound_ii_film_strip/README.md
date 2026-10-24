# Module 11 sensitivity, bound (ii): wall film stripped into the cylinder as large drops

Code: `sims/11_spray_flame/film_strip.py` (run: `python -m sims.11_spray_flame.film_strip --full`).
Tests: `tests/test_spray_flame_film_strip.py`.

## Labels (kept separate)
- EXECUTED: full run, 6 design points x 7 atomisers x 2 Module 09 variants x 3 SMDs = 252 rows (`design_points.csv`).
- VERIFIED (tests): film species balance closes with Module 09 `wall_impinged_pct` (84/84 rows); zero strip-off
  reproduces the accepted Module 11 baseline to 1e-9; MIE monotonic in strip fraction and SMD; critical strip
  fraction hits the 50/100 mJ thresholds; verdict thresholds.
- NOT VALIDATED: no experiment. Ballal-Lefebvre is EXTRAPOLATED (fitted ~0.1-1 atm, ~300 K, SMD 20-200 um).

## Case
Liquid at spark = Module 09 airborne + all Module 09 wall film (per species: film = injected x (1 - f_evap at spark)
- airborne, from `results/09_spray_evaporation/evap_profiles.json`). No strip-off SMD model exists in the repo
(film is Module 13), so all liquid is lumped at SMD = 200, 350, 500 um. Film not re-evaporated, deposited
composition kept, water as preheat-zone heat sink: every choice pushes toward misfire (upper bound).

## Result (MIE vs 50/100 mJ spark at 25-35 bar)
- Liquid at spark 54-99 % of injected liquid (airborne alone 0-3.8 %).
- 350 and 500 um: MISFIRE (MIE > 100 mJ) at all 84 points per SMD; MIE 199-4092 mJ (350 um), 579-11922 mJ (500 um).
- 200 um: 70 MISFIRE, 10 MARGINAL, 4 IGNITES; the non-misfire rows are all C2H5OH/best_dry (w = 0, no water heat
  sink); MIE 37-765 mJ.
- Flame speed S_eff/S_L,gas = 0.0009-0.008 everywhere (vapour-flame floor not flammable: too little pre-vaporised fuel).
- Worst: CH3OH/water_majority, ultrasonic_120kHz, nominal, 500 um: MIE 11.9 J, S/S_L 0.0028, heat-sink dT 285 K.
- Strip fraction of the film needed for MIE > 100 mJ: 0.21-0.78 at 200 um, 0.053-0.63 at 350 um, 0.015-0.31 at 500 um.

## Caveat
200-500 um drops are pessimistic at 30 bar: aerodynamic breakup (We_crit ~ 12) limits stable drops to roughly
12 sigma / (rho_g u^2) ~ 50-200 um for u ~ 10-20 m/s, sigma ~ 0.02 N/m, rho_g ~ 13 kg/m3. A strip-off SMD and film
evaporation model (Module 13) is needed before this bound can be tightened.
