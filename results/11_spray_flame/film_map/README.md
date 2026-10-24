# Module 11 bound (ii): port-film sensitivity map (Claude box-queue job J4, 2026-10-24)

**Status: EXECUTED.** This is one engine (the Module 11 film-strip criterion plus the `sims/dual_temp/port_film_wall_T.py` per-cycle film budget). It is **not verified** (no second engine) and **not validated** (no port-film measurements). Treat the boundaries as screening numbers, not design values.

## Question
The bound-(ii) case is a Module 09 wall film that reaches the cylinder as 200-500 µm drops. For which port-wall temperatures, wetted lengths, film heat-transfer coefficients and film loadings is a misfire still reachable? Reachable means the largest strippable film fraction, X_strip_max = 1 − f_film_evaporated, is at least the x_crit needed to push MIE above 100 mJ.

## Grid (68,040 case-rows; 84 Module 09 cases = case × atomiser × variant)
| axis | values |
|---|---|
| port wall T | 350-440 K in 1 K steps, plus 363.15 and 388.15 K exactly |
| wetted length L_wet | 0.02-0.10 m in 0.01 m steps (port D 35 mm) |
| film h | 5, 10, 20, 30, 50 kW/m²K (wall heat capped at CHF 1 MW/m²) |
| film loading | 0.5×, 1×, 2× the Module 09 deposit; mean film thickness 1.7-183 µm (median 18 µm) |
| plenum gas T | 360 K (normal intake) and 400 K (hot intake) |
| stripped-drop SMD | 200, 350, 500 µm |

### Dual-temperature regimes (as required for every module)
| regime | port wall | intake | source |
|---|---|---|---|
| normal | 363.15 K (90 °C coolant) | 360 K | production coolant 88-95 °C (MAHLE/VW SSP 222), SPEC §6 |
| hot (performance) | 388.15 K (115 °C coolant) | 400 K | high-temp/precision cooling SAE 960271, Heywood ch. 12 |
| heated port (option) | 420 K | — | coolant-jacket or exhaust-heated runner, design option |

## Results
Full per-case data is in `film_map_cases.csv`. Aggregates are in `film_map_boundary.csv`, which gives n_reach vs T_wall for every (film, plenum T, L, h, SMD). The plenum T has **no effect**: the 360 K and 400 K maps are identical. The film bubble point is ≤ 368 K in every case, so above about 365 K the budget is wall-heat limited (boiling). Below that, the gas-side branch is never the binding one. **Hot intake air does nothing for the film, and J1 shows it costs knock margin, so heat the port wall, not the charge.**

#### Film x0.5, SMD 350 um: T_all_safe [K], the lowest port-wall T at and above which none of the 84 cases can misfire (`>440` = some case still misfires at 440 K)

| L_wet [m] | h=5k | h=10k | h=20k | h=30k | h=50k |
|---|---|---|---|---|---|
| 0.02 | >440 | >440 | >440 | >440 | >440 |
| 0.03 | >440 | 430 | 394 | 384 | 377 |
| 0.04 | >440 | 412 | 386 | 380 | 375 |
| 0.05 | >440 | 402 | 382 | 377 | 373 |
| 0.06 | 430 | 394 | 380 | 376 | 372 |
| 0.07 | 420 | 389 | 378 | 375 | 366 |
| 0.08 | 412 | 386 | 377 | 374 | 366 |
| 0.09 | 406 | 384 | 376 | 373 | 365 |
| 0.10 | 402 | 382 | 375 | 372 | 364 |

#### Film x1, SMD 350 um: T_all_safe [K], the lowest port-wall T at and above which none of the 84 cases can misfire (`>440` = some case still misfires at 440 K)

| L_wet [m] | h=5k | h=10k | h=20k | h=30k | h=50k |
|---|---|---|---|---|---|
| 0.02 | >440 | >440 | >440 | >440 | >440 |
| 0.03 | >440 | >440 | >440 | >440 | >440 |
| 0.04 | >440 | >440 | >440 | >440 | >440 |
| 0.05 | >440 | >440 | 402 | 387 | 379 |
| 0.06 | >440 | 430 | 394 | 384 | 377 |
| 0.07 | >440 | 420 | 389 | 381 | 376 |
| 0.08 | >440 | 412 | 386 | 380 | 375 |
| 0.09 | >440 | 406 | 384 | 378 | 374 |
| 0.10 | >440 | 402 | 382 | 377 | 373 |

#### Film x2, SMD 350 um: T_all_safe [K], the lowest port-wall T at and above which none of the 84 cases can misfire (`>440` = some case still misfires at 440 K)

| L_wet [m] | h=5k | h=10k | h=20k | h=30k | h=50k |
|---|---|---|---|---|---|
| 0.02 | >440 | >440 | >440 | >440 | >440 |
| 0.03 | >440 | >440 | >440 | >440 | >440 |
| 0.04 | >440 | >440 | >440 | >440 | >440 |
| 0.05 | >440 | >440 | >440 | >440 | >440 |
| 0.06 | >440 | >440 | >440 | >440 | >440 |
| 0.07 | >440 | >440 | >440 | >440 | >440 |
| 0.08 | >440 | >440 | >440 | >440 | >440 |
| 0.09 | >440 | >440 | 406 | 390 | 381 |
| 0.10 | >440 | >440 | 402 | 387 | 379 |

#### Film x1, SMD 350 um: cases (of 84) where misfire is reachable at 363.15 / 388.15 / 420 K

| L_wet [m] | h=5k | h=10k | h=20k | h=30k | h=50k |
|---|---|---|---|---|---|
| 0.02 | 84 / 73 / 63 | 82 / 56 / 56 | 56 / 55 / 28 | 56 / 39 / 28 | 56 / 28 / 28 |
| 0.03 | 83 / 66 / 56 | 69 / 56 / 28 | 56 / 39 / 17 | 56 / 28 / 17 | 42 / 17 / 17 |
| 0.04 | 82 / 56 / 56 | 56 / 55 / 28 | 56 / 28 / 10 | 52 / 28 / 10 | 42 / 10 / 10 |
| 0.05 | 78 / 56 / 49 | 56 / 42 / 26 | 56 / 28 / 0 | 42 / 0 / 0 | 42 / 0 / 0 |
| 0.06 | 69 / 56 / 28 | 56 / 39 / 14 | 52 / 28 / 0 | 42 / 0 / 0 | 39 / 0 / 0 |
| 0.07 | 57 / 56 / 28 | 56 / 28 / 0 | 42 / 9 / 0 | 42 / 0 / 0 | 28 / 0 / 0 |
| 0.08 | 56 / 55 / 28 | 56 / 28 / 0 | 42 / 0 / 0 | 42 / 0 / 0 | 28 / 0 / 0 |
| 0.09 | 56 / 50 / 28 | 56 / 28 / 0 | 42 / 0 / 0 | 42 / 0 / 0 | 28 / 0 / 0 |
| 0.10 | 56 / 42 / 26 | 56 / 28 / 0 | 42 / 0 / 0 | 39 / 0 / 0 | 28 / 0 / 0 |

The 200 µm and 500 µm SMD maps have the same shape. Their boundaries are 2-17 K lower and 1-6 K higher respectively (see the CSV).

## Findings
1. **Normal regime (363 K port wall):** misfire is reachable in 28-84 of 84 cases in every cell of the map. No wetted length or h in this range makes a 90 °C port safe, because the wall sits at or below the film bubble point.
2. **Hot regime (388 K):** at nominal loading the risk goes to **0/84** once L_wet ≥ 0.05 m with h ≥ 30 kW/m²K, or L_wet ≥ 0.08 m with h ≥ 20 kW/m²K. Short wetted patches (≤ 0.04 m) or low h (≤ 10 kW/m²K) still leave 10-73 cases reachable.
3. **Heated port (420 K):** this clears L_wet ≥ 0.05 m at h ≥ 20 kW/m²K and L_wet ≥ 0.07 m even at h = 10 kW/m²K. 10-63 cases stay open for L ≤ 0.04 m or h = 5 kW/m²K.
4. **Film loading dominates.** At 2× the Module 09 deposit, only L_wet ≥ 0.09 m with h ≥ 20 kW/m²K has any safe temperature below 440 K. At 0.5× the boundary drops by roughly 5-35 K.
5. **Is hotter better?** Yes, clearly, for this failure mode. Going from 363 to 388 K moves most of the realistic (L ≥ 0.05 m, h ≥ 20 kW/m²K) map from "misfire reachable" to "safe". Combined with J1 (hot walls +0.2-0.3 pp η_i at the same intake T, hot intake −0.3 to −0.4 pp from knock), the best combination is a **hot port wall with a normal-temperature charge**.

## Caveats
- The budget assumes the deposited composition evaporates in proportion (no preferential methanol boil-off) and uses a CHF of 1 MW/m² (a water value, optimistic for alcohols).
- The film h is a free parameter, so the map is the result. No port-film measurement constrains it.
- x_crit is taken from Module 11 `bound_ii_film_strip/design_points.csv`. Any error there carries straight through.
- Next steps: a second engine (e.g. a 1-D transient film-conduction/evaporation model) for verification, and port-film rig data (Shin/Cheng-type LIF film thickness) for validation.

## Reproduce
```
python -m sims.11_spray_flame.film_map --workers 6     # ~14 min on 6 cores, <1 GB
pytest tests/test_spray_flame_film_map.py
```
