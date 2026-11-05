# Track B chains resumed after the M03-CRN fix - cost metric (EXECUTED, 2 engines; NOT validated)

Headline water $0.10/gal, secondary $0. Each row vs the chain's own dry baseline (same fuel, same regime, same hardware). 'before' = chain as stopped by the CRN failure; 'after' = resumed with the fix.

| fuel | regime | mode | point | w | d_eta pp (M03 / CRN) | power (IMEP) % (M03 / CRN) | fuel volume per unit work % (M03 / CRN) | **cost per mile % at $0.10/gal water** (M03 / CRN) | cost per mile % at $0 water (M03 / CRN) | verdict ($0.10) | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C2H5OH | normal | liquid | before best-eff (last accepted) | 0.173 | +0.765 / +0.754 | +7.794 / +7.767 | -1.688 / -1.663 | -0.854 / -0.829 | -1.688 / -1.663 | COST GAIN | before: 174 steps, last 174, stopped |
| C2H5OH | normal | liquid | before cost-optimal w ($0.10) | 0.173 | +0.765 / +0.754 | +7.794 / +7.767 | -1.688 / -1.663 | -0.854 / -0.829 | -1.688 / -1.663 | COST GAIN | before: 174 steps, last 174, stopped |
| C2H5OH | normal | liquid | after best-eff (last accepted) | 0.237 | +0.994 / +0.978 | +8.782 / +8.745 | -2.181 / -2.147 | -0.949 / -0.915 | -2.181 / -2.147 | COST GAIN | after: 238 steps, last 238, stopped |
| C2H5OH | normal | liquid | after cost-optimal w ($0.10) | 0.238 | +0.997 / +0.981 | +8.790 / +8.752 | -2.188 / -2.154 | -0.949 / -0.915 | -2.188 / -2.154 | COST GAIN | after: 238 steps, last 238, stopped |
| CH3OH | normal | liquid | before best-eff (last accepted) | 0.132 | +1.065 / +1.050 | +8.445 / +8.407 | -2.452 / -2.417 | -2.181 / -2.146 | -2.452 / -2.417 | COST GAIN | before: 133 steps, last 133, stopped |
| CH3OH | normal | liquid | before cost-optimal w ($0.10) | 0.132 | +1.065 / +1.050 | +8.445 / +8.407 | -2.452 / -2.417 | -2.181 / -2.146 | -2.452 / -2.417 | COST GAIN | before: 133 steps, last 133, stopped |
| CH3OH | normal | liquid | after best-eff (last accepted) | 0.227 | +1.453 / +1.429 | +9.826 / +9.768 | -3.314 / -3.263 | -2.796 / -2.744 | -3.314 / -3.263 | COST GAIN | after: 228 steps, last 228, stopped |
| CH3OH | normal | liquid | after cost-optimal w ($0.10) | 0.228 | +1.456 / +1.433 | +9.834 / +9.776 | -3.322 / -3.270 | -2.800 / -2.748 | -3.322 / -3.270 | COST GAIN | after: 228 steps, last 228, stopped |
| CH3OH | normal | humid_evap | before best-eff (last accepted) | 0.080 | +0.873 / +0.860 | +8.373 / +8.342 | -2.018 / -1.990 | -1.863 / -1.834 | -2.018 / -1.990 | COST GAIN | before: 81 steps, last 81, stopped |
| CH3OH | normal | humid_evap | before cost-optimal w ($0.10) | 0.080 | +0.873 / +0.860 | +8.373 / +8.342 | -2.018 / -1.990 | -1.863 / -1.834 | -2.018 / -1.990 | COST GAIN | before: 81 steps, last 81, stopped |
| CH3OH | normal | humid_evap | after best-eff (last accepted) | 0.227 | +1.453 / +1.429 | +9.826 / +9.768 | -3.314 / -3.263 | -2.796 / -2.744 | -3.314 / -3.263 | COST GAIN | after: 228 steps, last 228, stopped |
| CH3OH | normal | humid_evap | after cost-optimal w ($0.10) | 0.228 | +1.456 / +1.433 | +9.834 / +9.776 | -3.322 / -3.270 | -2.800 / -2.748 | -3.322 / -3.270 | COST GAIN | after: 228 steps, last 228, stopped |
| CH3OH | hot | humid_evap | before best-eff (last accepted) | 0.235 | +1.618 / +1.612 | +26.119 / +26.095 | -4.416 / -4.398 | -3.880 / -3.862 | -4.416 / -4.398 | COST GAIN | before: 236 steps, last 236, stopped |
| CH3OH | hot | humid_evap | before cost-optimal w ($0.10) | 0.235 | +1.618 / +1.612 | +26.119 / +26.095 | -4.416 / -4.398 | -3.880 / -3.862 | -4.416 / -4.398 | COST GAIN | before: 236 steps, last 236, stopped |
| CH3OH | hot | humid_evap | after best-eff (last accepted) | 0.325 | +1.941 / +1.927 | +27.230 / +27.181 | -5.251 / -5.214 | -4.418 / -4.381 | -5.251 / -5.214 | COST GAIN | after: 326 steps, last 326, stopped |
| CH3OH | hot | humid_evap | after cost-optimal w ($0.10) | 0.326 | +1.944 / +1.930 | +27.241 / +27.191 | -5.259 / -5.222 | -4.423 / -4.385 | -5.259 / -5.222 | COST GAIN | after: 326 steps, last 326, stopped |

Note (PR 11 review item 2, VERIFIED by fresh-process recompute in mode_check_CH3OH_normal.json): the CH3OH normal liquid and humid_evap 'after' rows are identical by physics, not by a resume bug. Intake evaporation is wet-bulb (saturation) limited; from w 0.140 the liquid mode's 0.5*w also exceeds the intake capacity, so both modes evaporate the same water and give the same charge (M03 eta diff < 1e-12). Below w 0.140 they differ (humid_evap up to +0.084 pp better at w 0.080). The 'before' best w (0.132 vs 0.080) were where each chain hit the CRN failure, not optima. Count the two chains as ONE result.

Track B chains run at the fuel/regime dry-baseline CR chosen by the Module 03 knock model only (single-engine knock); CR choice: Not yet (single-engine knock) validated.
