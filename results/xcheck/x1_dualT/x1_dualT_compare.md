# X1 dual-temperature cross-check: AramcoMech 2.0 vs San Diego 2016-12-14

Cantera 3.2.0, 1 atm, phi = 1, FreeFlame mixture-averaged, two-stage refinement (final ratio 2 / slope 0.05 / curve 0.1). Aramco SHA-256 (LF) `26c09c2fe6ce3161…`.

Regimes: **normal** T_u = 320 K and 360 K (intake charge), **hot** T_u = 400 K (intake charge, X1 contract point). Source: `sims/dual_temp/regimes.py` (branch wme1-hiT) — coolant 363.15/388.15 K, wall 450/520 K, intake 320–360 / 400 K (MAHLE/VW SSP 222, SAE 960271, SAE 2010-01-0802, Heywood ch. 12, SPEC §6).


## Adiabatic flame temperature [K] (tol ±0.5 %)

| regime | T_u [K] | fuel | w | Aramco | San Diego | dev | verdict |
|---|---|---|---|---|---|---|---|
| normal | 300 | C2H5OH | 0.0 | 2242.0 | 2241.3 | +0.04 % | PASS |
| normal | 300 | C2H5OH | 0.3 | 2146.8 | 2145.8 | +0.04 % | PASS |
| normal | 300 | C2H5OH | 0.6 | 1934.4 | 1933.4 | +0.05 % | PASS |
| normal | 300 | CH3OH | 0.0 | 2225.8 | 2225.7 | +0.01 % | PASS |
| normal | 300 | CH3OH | 0.3 | 2103.9 | 2103.7 | +0.01 % | PASS |
| normal | 300 | CH3OH | 0.6 | 1842.3 | 1842.0 | +0.01 % | PASS |
| normal | 320 | C2H5OH | 0.0 | 2251.4 | 2250.6 | +0.03 % | PASS |
| normal | 320 | C2H5OH | 0.3 | 2157.0 | 2156.1 | +0.04 % | PASS |
| normal | 320 | C2H5OH | 0.6 | 1946.6 | 1945.6 | +0.05 % | PASS |
| normal | 320 | CH3OH | 0.0 | 2235.0 | 2234.9 | +0.00 % | PASS |
| normal | 320 | CH3OH | 0.3 | 2114.3 | 2114.1 | +0.01 % | PASS |
| normal | 320 | CH3OH | 0.6 | 1854.8 | 1854.6 | +0.01 % | PASS |
| normal | 360 | C2H5OH | 0.0 | 2269.9 | 2269.3 | +0.03 % | PASS |
| normal | 360 | C2H5OH | 0.3 | 2177.3 | 2176.6 | +0.03 % | PASS |
| normal | 360 | C2H5OH | 0.6 | 1970.8 | 1970.0 | +0.04 % | PASS |
| normal | 360 | CH3OH | 0.0 | 2253.2 | 2253.2 | +0.00 % | PASS |
| normal | 360 | CH3OH | 0.3 | 2134.9 | 2134.8 | +0.01 % | PASS |
| normal | 360 | CH3OH | 0.6 | 1879.9 | 1879.8 | +0.01 % | PASS |
| hot | 400 | C2H5OH | 0.0 | 2288.3 | 2287.8 | +0.02 % | PASS |
| hot | 400 | C2H5OH | 0.3 | 2197.6 | 2196.9 | +0.03 % | PASS |
| hot | 400 | C2H5OH | 0.6 | 1995.0 | 1994.2 | +0.04 % | PASS |
| hot | 400 | CH3OH | 0.0 | 2271.3 | 2271.4 | -0.00 % | PASS |
| hot | 400 | CH3OH | 0.3 | 2155.3 | 2155.3 | +0.00 % | PASS |
| hot | 400 | CH3OH | 0.6 | 1904.9 | 1904.9 | +0.00 % | PASS |

## Laminar flame speed [m/s] (tol ±10 %)

| regime | T_u [K] | fuel | w | Aramco | San Diego | dev | verdict |
|---|---|---|---|---|---|---|---|
| normal | 320 | C2H5OH | 0.0 | — | 0.5170 | — | n/a |
| normal | 320 | C2H5OH | 0.3 | — | 0.4051 | — | n/a |
| normal | 320 | C2H5OH | 0.6 | — | 0.2149 | — | n/a |
| normal | 320 | CH3OH | 0.0 | — | 0.5058 | — | n/a |
| normal | 320 | CH3OH | 0.3 | — | 0.3994 | — | n/a |
| normal | 320 | CH3OH | 0.6 | — | 0.2071 | — | n/a |
| normal | 360 | C2H5OH | 0.0 | 0.6032 | 0.6235 | -3.26 % | PASS |
| normal | 360 | C2H5OH | 0.3 | 0.4846 | 0.4932 | -1.75 % | PASS |
| normal | 360 | C2H5OH | 0.6 | 0.2716 | 0.2689 | +0.98 % | PASS |
| normal | 360 | CH3OH | 0.0 | 0.5499 | 0.6076 | -9.51 % | PASS |
| normal | 360 | CH3OH | 0.3 | 0.4345 | 0.4834 | -10.11 % | FAIL |
| normal | 360 | CH3OH | 0.6 | 0.2238 | 0.2591 | -13.63 % | FAIL |
| hot | 400 | C2H5OH | 0.0 | 0.7173 | 0.7438 | -3.56 % | PASS |
| hot | 400 | C2H5OH | 0.3 | 0.5812 | 0.5932 | -2.02 % | PASS |
| hot | 400 | C2H5OH | 0.6 | 0.3342 | 0.3315 | +0.80 % | PASS |
| hot | 400 | CH3OH | 0.0 | 0.6505 | 0.7171 | -9.28 % | PASS |
| hot | 400 | CH3OH | 0.3 | 0.5202 | 0.5779 | -9.98 % | PASS |
| hot | 400 | CH3OH | 0.6 | 0.2788 | 0.3191 | -12.65 % | FAIL |

## Hot (400 K) vs normal (360 K) unburned temperature

| fuel | w | S_L 360 K Aramco | S_L 400 K Aramco | ratio | S_L ratio San Diego | T_ad 400−360 Aramco [K] |
|---|---|---|---|---|---|---|
| CH3OH | 0.0 | 0.5499 | 0.6505 | 1.183 | 1.180 | 18.1 |
| CH3OH | 0.3 | 0.4345 | 0.5202 | 1.197 | 1.195 | 20.5 |
| CH3OH | 0.6 | 0.2238 | 0.2788 | 1.246 | 1.232 | 25.0 |
| C2H5OH | 0.0 | 0.6032 | 0.7173 | 1.189 | 1.193 | 18.4 |
| C2H5OH | 0.3 | 0.4846 | 0.5812 | 1.199 | 1.203 | 20.2 |
| C2H5OH | 0.6 | 0.2716 | 0.3342 | 1.231 | 1.233 | 24.1 |

**Totals:** T_ad 24 PASS / 0 FAIL / 0 n/a; S_L 9 PASS / 3 FAIL / 6 n/a.

Aramco grid indicator (stage1→stage2 S_L change): max 15.79 %; grid points 191–265; solve time 1030–2089 s per case (1 thread/case, hosts mail).

Ignition delay (X1 round 3: 40 bar, 800/900/1000 K, factor-1.5 tolerance) is not part of this sweep.
