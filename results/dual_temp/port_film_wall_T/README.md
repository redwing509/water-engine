# Port wall-film budget, normal vs hot port wall (dual-temperature rule, 2026-10-24)

Status: EXECUTED estimate only. It is NOT verified (no second engine yet) and NOT validated against experiment. It stands in until Module 13 (port film dynamics) exists.

Question: does a hotter intake-port wall evaporate enough of the Module 09 wall film that the Module 11 bound (ii) misfire (film stripped into the cylinder as 200, 350 or 500 um drops) can no longer happen?

Method: see the docstring of `sims/dual_temp/port_film_wall_T.py`.
- Deposit per cycle comes from Module 11 film_strip.
- Capacity per cycle is the smaller of gas-side Spalding mass transfer and wall heat supply (h_film * superheat, capped at CHF 1 MW/m2).
- The film budget is steady state.
- Misfire stays "reachable" if (1 - film evaporated fraction) >= Module 11 x_strip for MIE 100 mJ.

Sensitivity grid: wetted length 0.02, 0.05 or 0.10 m, and h_film 1e4 or 3e4 W/m2K.

| regime | port wall | cases where misfire is still reachable at SMD 350 um (range over grid, of 84) | mean film evaporated |
|---|---|---|---|
| normal | 363 K | 39-82 | 0.19-0.75 |
| hot | 388 K | 0-56 | 0.47-1.00 |
| hot + heated port | 420 K | 0-56 | 0.64-1.00 |

Reading: hotter port walls clearly reduce the film and the bound (ii) misfire risk. At nominal parameters (0.05 m, 3e4) misfire becomes unreachable at 388 K and above. The answer still depends strongly on wetted area and film heat transfer, which Module 13 must pin down.

Caveat: the heat needed per cycle can be several kW per cylinder at 2000 rpm, which a real port wall may not supply without dropping its temperature. The heat limit here is therefore probably optimistic.
