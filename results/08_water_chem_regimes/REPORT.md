# Module 08 water chemistry: normal vs high-performance temperature regime variant

Date: 2026-10-24 (Grok Bot, taking over Hermes's water-engine-spray r5, which failed on a context-compression timeout).
Track A (water-majority w = 0.6; w = 0 and 0.3 as references). Branch wme1-spray.
Code: `sims/08_water_chem/regime_variant.py`. Data: `results/08_water_chem_regimes/regimes.json`.
Built on the corrected module 08 (Hermes a6da0e8 stoichiometry fix, f55d15d Q enthalpy basis, 3fa95c1 tests).

## Status (kept separate)

- **Executed:** yes. San Diego mechanism with the module's real / FH2O-a / FH2O-b water variants, 3 workers on the box,
  465 s.
- **Verified:** **no** as a second-engine result for the chemical-effect split. Checks C1 to C3 below only show
  self-consistency (code and grid). For the real mixtures only (T_ad, tau_ig, S_L, no chemical-effect split), the
  same TDC construction was run in J2 (`results/xcheck/j2_m02_dualT` on xcheck/chem) with AramcoMech 2.0 and CRECK:
  T_ad 96/96 PASS, tau_ig 19/24 within a factor of 2, S_L 7/12 within 10 %. That is partial cross-engine support for
  the real-mixture numbers, not for the FH2O decomposition.
- **Validated:** **no**. No published alcohol/water flame-speed or ignition data exist at these states
  (/opt/knowledge WE-11).

## Regimes (stated and cited)

| regime | coolant | chamber wall | port wall | T_u (charge at IVC) | source |
|---|---|---|---|---|---|
| normal | 363.15 K (90 C) | 450 K | 363.15 K | 320 K (cold end), 360 K (upper normal) | MAHLE "Vehicle cooling" / VW SSP 222 (85-95 C); Heywood ch. 12 wall band |
| hot (high-performance) | 388.15 K (115 C) | 520 K | 388.15 K | 400 K (un-intercooled boost / heated intake) | SAE 960271 and SAE 2010-01-0802 (high-T / split cooling); SPEC section 6 |
| hot + heated port (bound) | 388.15 K | 520 K | 420 K | 420 K | sensitivity bound only (sims/dual_temp/regimes.py) |

Module 08 has no wall model. The regime enters only through T_u: flames at 1 atm and T_u; ignition at the
TDC-equivalent state reached by frozen isentropic compression from (T_u, 1 bar) by CR 16 and 24 (the same
construction as J2). phi = 1, tau horizon 0.5 s.

**Not computed by module 08:** efficiency, p_max, CA50, wall heat, NOx and MIE. Those come from module 03 dual_temp
(wme1-hiT / wme1-dev) and module 11. Here "hot is better or worse" refers to flame speed, knock margin
(ignition delay) and the size of water's chemical effect.

## Checks (tolerances fixed before the run)

- **C1:** the TDC states reproduce J2 exactly. 24 states, max dT 0.0 K, max dp 0.0 % (tolerance 0.1 K / 0.1 %).
  **PASS**
- **C2:** real-mixture S_L / tau / T_ad match `results/08_water_chem_dualT/dual_temp.json`. 36 values, max relative
  difference 1.05e-7 (tolerance 1e-6). **PASS**
- **C3:** grid refinement of the S_L chemical effect at w = 0.3, 360 K (default grid vs ratio 2 / slope 0.03 /
  curve 0.06, 145 to 318 and 176 to 380 points). The sign must hold and the value must move by less than 1 pp.
  CH3OH +12.20 % to +12.47 %, C2H5OH -11.36 % to -11.23 %. **PASS**

## Results: every case

The chemical effect is real minus FH2O (third body plus direct reactions), as a % of the FH2O value; see module 08.

| fuel | w | regime | T_u K | T_ad K | S_L m/s | S_L chem % | tau CR16 ms | tau CR16 chem % | tau CR24 ms | tau CR24 chem % |
|---|---|---|---|---|---|---|---|---|---|---|
| CH3OH | 0.0 | normal | 320 | 2235 | 0.511 | — | 49.5 | — | 2.47 | — |
| CH3OH | 0.0 | normal | 360 | 2253 | 0.612 | — | 5.89 | — | 0.438 | — |
| CH3OH | 0.0 | hot | 400 | 2271 | 0.723 | — | 1.14 | — | 0.115 | — |
| CH3OH | 0.0 | hot_heated_port_bound | 420 | 2280 | 0.783 | — | 0.574 | — | 0.0654 | — |
| CH3OH | 0.3 | normal | 320 | 2114 | 0.403 | +11.3 | 54.6 | -8.6 | 2.7 | -8.3 |
| CH3OH | 0.3 | normal | 360 | 2135 | 0.489 | +12.2 | 6.25 | -9.5 | 0.463 | -8.9 |
| CH3OH | 0.3 | hot | 400 | 2155 | 0.584 | +13.1 | 1.17 | -10.3 | 0.119 | -9.5 |
| CH3OH | 0.3 | hot_heated_port_bound | 420 | 2166 | 0.636 | +13.6 | 0.585 | -10.5 | 0.067 | -9.7 |
| CH3OH | 0.6 | normal | 320 | 1855 | 0.208 | +0.6 | 71.4 | -17.7 | 3.44 | -17.1 |
| CH3OH | 0.6 | normal | 360 | 1880 | 0.261 | +2.4 | 7.63 | -19.2 | 0.558 | -18.0 |
| CH3OH | 0.6 | hot | 400 | 1905 | 0.321 | +3.1 | 1.36 | -20.5 | 0.138 | -18.9 |
| CH3OH | 0.6 | hot_heated_port_bound | 420 | 1917 | 0.355 | +4.0 | 0.667 | -21.0 | 0.0769 | — |
| C2H5OH | 0.0 | normal | 320 | 2251 | 0.520 | — | 217 | — | 12.8 | — |
| C2H5OH | 0.0 | normal | 360 | 2269 | 0.627 | — | 27.5 | — | 2.21 | — |
| C2H5OH | 0.0 | hot | 400 | 2288 | 0.748 | — | 5.29 | — | 0.542 | — |
| C2H5OH | 0.0 | hot_heated_port_bound | 420 | 2297 | 0.813 | — | 2.61 | — | 0.296 | — |
| C2H5OH | 0.3 | normal | 320 | 2156 | 0.408 | -12.3 | 223 | -6.9 | 13.1 | -6.7 |
| C2H5OH | 0.3 | normal | 360 | 2177 | 0.497 | -11.4 | 27.7 | -7.7 | 2.24 | -7.1 |
| C2H5OH | 0.3 | hot | 400 | 2197 | 0.598 | -10.3 | 5.26 | -8.1 | 0.546 | -6.9 |
| C2H5OH | 0.3 | hot_heated_port_bound | 420 | 2207 | 0.653 | -9.9 | 2.59 | -8.1 | 0.299 | -6.6 |
| C2H5OH | 0.6 | normal | 320 | 1946 | 0.217 | -26.4 | 250 | -15.3 | 14.5 | -14.8 |
| C2H5OH | 0.6 | normal | 360 | 1970 | 0.271 | -25.4 | 29.9 | -16.6 | 2.42 | -15.3 |
| C2H5OH | 0.6 | hot | 400 | 1994 | 0.334 | -24.3 | 5.55 | -17.4 | 0.586 | -15.0 |
| C2H5OH | 0.6 | hot_heated_port_bound | 420 | 2006 | 0.368 | -23.8 | 2.71 | -17.5 | 0.321 | -14.4 |

## Side by side: hot vs normal

dT_ad is hot minus normal. The ratios are hot / normal. A "chem shift" is the hot-minus-normal change, in
percentage points, of water's chemical effect.

| fuel | w | normal T_u | hot T_u | dT_ad K | S_L hot/normal | tau16 hot/normal | tau24 hot/normal | S_L chem shift pp | tau16 chem shift pp | tau24 chem shift pp |
|---|---|---|---|---|---|---|---|---|---|---|
| CH3OH | 0.0 | 320 | 400 | +36.5 | 1.415 | 0.023 | 0.047 | — | — | — |
| CH3OH | 0.0 | 320 | 420 | +45.6 | 1.532 | 0.012 | 0.026 | — | — | — |
| CH3OH | 0.0 | 360 | 400 | +18.2 | 1.181 | 0.193 | 0.262 | — | — | — |
| CH3OH | 0.0 | 360 | 420 | +27.3 | 1.278 | 0.097 | 0.149 | — | — | — |
| CH3OH | 0.3 | 320 | 400 | +41.3 | 1.449 | 0.021 | 0.044 | +1.80 | -1.67 | -1.23 |
| CH3OH | 0.3 | 320 | 420 | +51.5 | 1.578 | 0.011 | 0.025 | +2.27 | -1.95 | -1.47 |
| CH3OH | 0.3 | 360 | 400 | +20.6 | 1.195 | 0.188 | 0.256 | +0.91 | -0.74 | -0.57 |
| CH3OH | 0.3 | 360 | 420 | +30.8 | 1.301 | 0.094 | 0.145 | +1.39 | -1.02 | -0.80 |
| CH3OH | 0.6 | 320 | 400 | +50.3 | 1.546 | 0.019 | 0.040 | +2.53 | -2.76 | -1.78 |
| CH3OH | 0.6 | 320 | 420 | +62.8 | 1.707 | 0.009 | 0.022 | +3.45 | -3.26 | — |
| CH3OH | 0.6 | 360 | 400 | +25.1 | 1.232 | 0.179 | 0.247 | +0.67 | -1.28 | -0.87 |
| CH3OH | 0.6 | 360 | 420 | +37.7 | 1.361 | 0.088 | 0.138 | +1.60 | -1.79 | — |
| C2H5OH | 0.0 | 320 | 400 | +37.2 | 1.438 | 0.024 | 0.042 | — | — | — |
| C2H5OH | 0.0 | 320 | 420 | +46.4 | 1.563 | 0.012 | 0.023 | — | — | — |
| C2H5OH | 0.0 | 360 | 400 | +18.5 | 1.192 | 0.192 | 0.245 | — | — | — |
| C2H5OH | 0.0 | 360 | 420 | +27.8 | 1.296 | 0.095 | 0.134 | — | — | — |
| C2H5OH | 0.3 | 320 | 400 | +40.8 | 1.467 | 0.024 | 0.042 | +1.98 | -1.17 | -0.24 |
| C2H5OH | 0.3 | 320 | 420 | +50.9 | 1.602 | 0.012 | 0.023 | +2.33 | -1.19 | +0.08 |
| C2H5OH | 0.3 | 360 | 400 | +20.3 | 1.203 | 0.190 | 0.244 | +1.07 | -0.43 | +0.11 |
| C2H5OH | 0.3 | 360 | 420 | +30.5 | 1.314 | 0.093 | 0.134 | +1.42 | -0.45 | +0.43 |
| C2H5OH | 0.6 | 320 | 400 | +48.6 | 1.538 | 0.022 | 0.040 | +2.11 | -2.13 | -0.24 |
| C2H5OH | 0.6 | 320 | 420 | +60.7 | 1.698 | 0.011 | 0.022 | +2.59 | -2.22 | +0.35 |
| C2H5OH | 0.6 | 360 | 400 | +24.3 | 1.232 | 0.185 | 0.242 | +1.13 | -0.84 | +0.25 |
| C2H5OH | 0.6 | 360 | 420 | +36.3 | 1.360 | 0.091 | 0.133 | +1.61 | -0.93 | +0.84 |
The "—" for CH3OH w = 0.6, 420 K (heated-port bound), CR 24 is a missing chemical-effect value. The FH2O-b ignition run failed: Cantera reported "reactor solver failed; ignition not established". Real and FH2O-a both ignite at 0.077 ms. It was not retried, because a rerun under the same settings would hit the same solver failure. Changing the integrator tolerances for this one case is listed as open. The case only bounds sensitivity and does not change the verdict.

## Verdict: is hotter better?

**It's a trade-off. Hotter is not simply better, and for a water-majority charge it is worse on knock margin.**

1. **Flame speed (better hot).** Going from 360 K to 400 K raises S_L by 18-23 % for both fuels at every w
   (ratio 1.18-1.23), and 320 K to 400 K raises it by 42-55 %. T_ad rises by 18-25 K (360 to 400 K). A hotter
   charge gives a faster, more complete burn of a water-diluted mixture. At w = 0.6 the water-majority flames
   (0.26 to 0.32 m/s CH3OH, 0.27 to 0.33 m/s C2H5OH at 360 to 400 K) are still about 2x slower than the dry flames.
2. **Knock / auto-ignition margin (worse hot).** tau at TDC shortens 4-6x from 360 K to 400 K
   (tau ratio 0.18-0.19 at CR 16, 0.24-0.26 at CR 24) and 25-50x from 320 K to 400 K. At CR 24 hot,
   w = 0.6 CH3OH has tau = 0.14 ms (about 1.7 CAD at 2000 rpm), against 0.56 ms at 360 K. The hot regime gives
   up most of the knock margin that water dilution buys, so the high-CR water-majority design points need the
   normal regime or retarded spark.
3. **Water's chemical effect (almost regime-independent).** Between 360 and 400 K the effect moves by at most
   1.3 pp (S_L +0.7 to +1.1 pp; tau -1.3 to +0.3 pp). Between 320 and 420 K it moves by at most 3.5 pp. Its sign
   never changes. CH3OH keeps a small S_L benefit (+0.6 to +4.0 % at w = 0.6) and ethanol keeps a large S_L
   penalty (-24 to -26 % at w = 0.6). Both fuels keep a 15-21 % shorter tau from water's chemistry. The regime
   choice does not change the conclusion about water's chemistry.

**Press-release worthy?** No. Executed only, single engine for the decomposition, not validated.

## Reproduce

```
python -m sims.08_water_chem.build_mechanisms      # FH2O-a/b mechanisms (untracked build products)
python -m sims.08_water_chem.regime_variant 3      # 3 workers, about 8 min
```
