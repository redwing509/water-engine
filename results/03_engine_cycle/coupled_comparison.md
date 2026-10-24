# Coupled design-point comparison (item B)

Coupled evaporation: Module 03 cycle run with the Module 09-derived evaporation profile (IVC/spark interpolation, saturation-capped) instead of the default f_evap_intake schedule. All values below are taken from the actual `design_point.json` outputs of the four item-B runs on mail (`results/03_engine_cycle/<atomiser>_<variant>/design_point.json`); the liquid fraction at spark comes from `inputs/evap_profiles.json` (Module 09 `liquid_spark_pct`).

## Result: does the CH3OH water-majority point (w > 0.5) still match or beat best-dry after coupling?

NO. Once evaporation is coupled, the CH3OH water-majority point falls BEHIND the best-dry point.

- Uncoupled: CH3OH water-majority CR=24/w=0.6/T=360 -> eta = 0.431009, vs best-dry CR=16/w=0 -> 0.420674. Water-majority BEATS best-dry by +0.0103 (1.03 points).

- Coupled (all four atomiser/variant combos give identical cycle results): the CH3OH water-majority point is no longer feasible at CR=24. The knock constraint binds at CR=14 and the sweep lands on CH3OH/CR=18/w=0.6/T_intake=320 with eta = 0.412890. That is -0.00214 (0.21 points) BELOW the coupled best-dry CH3OH/CR=14/w=0/T=320 at 0.415029.

- The coupling loss is real and fuel-specific: CH3OH water-majority loses 0.0181 efficiency vs its uncoupled value (0.4310 -> 0.4129), driven by intake saturation limiting f_evap_intake to 0.054 (the profile target 0.0288 is infeasible) and a knock-limited CA50 of 8.0 deg. Best-dry CH3OH loses only 0.0056.

- CH4 is the only fuel whose water-majority point still beats its own best-dry after coupling (+0.0099), and it is also the only one whose best_overall and water_majority coincide (both CR=18/w=0.6, eta 0.4358). CH4 is reference-only, not a design fuel.

- Recommendation flips: uncoupled recommended C2H5OH/CR=24/w=0.6/T=360 (eta 0.4378); coupled recommends CH3OH/CR=18/w=0.6/T=320 (eta 0.4129) purely because it is the highest-eta feasible w>0.5 point of the design fuels. The CH3OH water-majority advantage over dry CH3OH seen in the uncoupled grid does not survive coupling.

## Coupled comparison table

| fuel | point | atomiser | variant | w | CR | efficiency | d_eff vs uncoupled | knock-limited CA50 | peak p (MPa) | NO relative | liquid fraction at spark |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CH3OH | best_dry | carb_venturi | nominal | 0.0 | 14 | 0.415029 | -0.005644 | 10.0 | 7.327278 | 1.0 | 4e-06 |
| CH3OH | best_overall | carb_venturi | nominal | 0.0 | 14 | 0.415029 | -0.039244 | 10.0 | 7.327278 | 1.0 | 0.0 |
| CH3OH | water_majority | carb_venturi | nominal | 0.6 | 18 | 0.41289 | -0.018119 | 8.0 | 8.410536 | 3e-06 | 0.0 |
| CH4 | best_dry | carb_venturi | nominal | 0.0 | 18 | 0.425864 | -0.006866 | 8.0 | 9.787067 | 1.0 |  |
| CH4 | best_overall | carb_venturi | nominal | 0.6 | 18 | 0.4358 | -0.01265 | 8.0 | 9.324774 | 0.016462 |  |
| CH4 | water_majority | carb_venturi | nominal | 0.6 | 18 | 0.4358 | -0.010516 | 8.0 | 9.324774 | 0.016462 |  |
| CH3OH | best_dry | carb_venturi | cfd_matched | 0.0 | 14 | 0.415029 | -0.005644 | 10.0 | 7.327278 | 1.0 | 4e-06 |
| CH3OH | best_overall | carb_venturi | cfd_matched | 0.0 | 14 | 0.415029 | -0.039244 | 10.0 | 7.327278 | 1.0 | 0.0 |
| CH3OH | water_majority | carb_venturi | cfd_matched | 0.6 | 18 | 0.41289 | -0.018119 | 8.0 | 8.410536 | 3e-06 | 0.0 |
| CH4 | best_dry | carb_venturi | cfd_matched | 0.0 | 18 | 0.425864 | -0.006866 | 8.0 | 9.787067 | 1.0 |  |
| CH4 | best_overall | carb_venturi | cfd_matched | 0.6 | 18 | 0.4358 | -0.01265 | 8.0 | 9.324774 | 0.016462 |  |
| CH4 | water_majority | carb_venturi | cfd_matched | 0.6 | 18 | 0.4358 | -0.010516 | 8.0 | 9.324774 | 0.016462 |  |
| CH3OH | best_dry | ultrasonic_120kHz | nominal | 0.0 | 14 | 0.415029 | -0.005644 | 10.0 | 7.327278 | 1.0 | 0.335494 |
| CH3OH | best_overall | ultrasonic_120kHz | nominal | 0.0 | 14 | 0.415029 | -0.039244 | 10.0 | 7.327278 | 1.0 | 1.74943 |
| CH3OH | water_majority | ultrasonic_120kHz | nominal | 0.6 | 18 | 0.41289 | -0.018119 | 8.0 | 8.410536 | 3e-06 | 3.196676 |
| CH4 | best_dry | ultrasonic_120kHz | nominal | 0.0 | 18 | 0.425864 | -0.006866 | 8.0 | 9.787067 | 1.0 |  |
| CH4 | best_overall | ultrasonic_120kHz | nominal | 0.6 | 18 | 0.4358 | -0.01265 | 8.0 | 9.324774 | 0.016462 |  |
| CH4 | water_majority | ultrasonic_120kHz | nominal | 0.6 | 18 | 0.4358 | -0.010516 | 8.0 | 9.324774 | 0.016462 |  |
| CH3OH | best_dry | ultrasonic_120kHz | cfd_matched | 0.0 | 14 | 0.415029 | -0.005644 | 10.0 | 7.327278 | 1.0 | 1.057596 |
| CH3OH | best_overall | ultrasonic_120kHz | cfd_matched | 0.0 | 14 | 0.415029 | -0.039244 | 10.0 | 7.327278 | 1.0 | 2.936175 |
| CH3OH | water_majority | ultrasonic_120kHz | cfd_matched | 0.6 | 18 | 0.41289 | -0.018119 | 8.0 | 8.410536 | 3e-06 | 3.806044 |
| CH4 | best_dry | ultrasonic_120kHz | cfd_matched | 0.0 | 18 | 0.425864 | -0.006866 | 8.0 | 9.787067 | 1.0 |  |
| CH4 | best_overall | ultrasonic_120kHz | cfd_matched | 0.6 | 18 | 0.4358 | -0.01265 | 8.0 | 9.324774 | 0.016462 |  |
| CH4 | water_majority | ultrasonic_120kHz | cfd_matched | 0.6 | 18 | 0.4358 | -0.010516 | 8.0 | 9.324774 | 0.016462 |  |

Notes:

- d_eff vs uncoupled = coupled gross indicated efficiency minus the same (fuel, point) efficiency from the uncoupled `design_point.json` (default f_evap_intake schedule). Negative = coupling hurts.
- CH4 rows have no liquid fraction at spark because CH4 is a gaseous fuel with no injected liquid; the Module 09 spray model only covers CH3OH/C2H5OH design points.
- carb_venturi nominal and cfd_matched give identical cycle results (liquid fractions differ only in the profile input, and both are far below the intake saturation limit for the points that matter). ultrasonic_120kHz nominal vs cfd_matched likewise give identical cycle results.
- All four design-point combinations (carb_venturi / ultrasonic_120kHz x nominal / cfd_matched) are represented: 6 rows each = 24 rows total.
- Source: `results/03_engine_cycle/inputs/evap_profiles.json` (Module 09, commit e32288e, IVC/spark linear interpolation). Model-relative; not experimentally validated.
