# Module 09 at the Module 03 design points

Relay job `water-engine-20261023-103500` (with Claude's amendments in
`reply-water-engine-open-items-20261023-1030`). Generator:
`python -m sims.09_spray_evaporation.design_points --cfd-dir <wme1-cfd>/cfd/results`.

## Status labels
* **EXECUTED**: every number here comes from a model run (84 cases, 0 failed, exit 0).
* **Numerically VERIFIED**: `tests/test_spray_evaporation.py` checks the d2-law, the saturation limit,
  mass conservation (max error here 1.2e-11), Wilson vs NRTL agreement (methanol and ethanol), the
  pressure-trace ("pt") mode, the spark-angle formula and the k(p) clamp.
* **Experimentally VALIDATED**: nothing. The CFD comparison is model against model.

## Cases
CH3OH and C2H5OH at Module 03's best_dry, best_overall and water_majority points
(`results/03_engine_cycle/design_point.json`), run for all 7 atomisers, each in two variants:

| variant | meaning |
|---|---|
| `nominal` | The Module 09 model as derived, with transfer multiplier k = 1. It is **not tuned to CFD**. **Known limitation:** compared with OpenFOAM phase A, it evaporates 1.5-2.5x the CFD amount at A1 (1 bar, 360 K) and +1 to +12 pp more at A2 (20 bar, 700 K). |
| `cfd_matched` | **This is a sensitivity bound, not a validated model.** It applies one droplet-gas transfer multiplier per CFD condition to both mass and heat transfer (a Sh/Nu multiplier). The multipliers are least-squares fitted to the A1-BLEND and A2-BLEND evaporated-% histories (0.1 ms grid): k_A1 = 0.340 (RMS 0.89 to 0.03 pp) and k_A2 = 0.707 (RMS 9.7 to 0.8 pp). k_A1 is used in the runner and during induction. In compression, k is interpolated in ln p between 1 and 20 bar and clamped outside that range. The CFD itself is unvalidated (wall bounce, no film). The same k is used for ethanol, which has no CFD case of its own (flagged). |

## Inputs and assumptions
* Module 03 supplies CR, w, T_intake, rpm and the trapped air/alcohol/water masses. Residual gas is
  left out of the Module 09 parcel.
* **Pressure during compression:** Module 03's own pre-spark p(θ), regenerated with
  `integrate_cycle(keep_trace=True)`. That trace includes Woschni wall heat and Module 03's water
  evaporation schedule. The regeneration reproduces the design-point efficiency and peak pressure to
  better than 1e-6 relative. It is imposed in model.Spray mode "pt", where the Module 09 parcel is
  adiabatic. The trace itself is in `m03_pre_spark_p_theta.csv`.
* **Spark timing:** spark = CA50 minus the 0-50 % burn angle. Module 03 reports no 0-50 % angle, so the
  Module 03 Wiebe function (a = 5, m = 2) is used, and spark is its start point:
  θ_spark = CA50 − Δθ·z(0.5), with Δθ = burn₁₀₋₉₀/(z(0.9) − z(0.1)). The resulting spark angles are:

  | point | CH3OH | C2H5OH |
  |---|---|---|
  | best_dry | −12.08° | −12.08° |
  | best_overall | −20.94° | −23.05° |
  | water_majority | −30.97° | −30.91° |

* **Venturi (FLAGGED):** `results/06_carburetor/carb_design.json` is not committed on wme1-dev. An
  uncommitted copy exists in Hermes's working tree but was not used. The carburettor case therefore
  keeps the SPEC fallback of a 30 m/s throat speed (Nukiyama-Tanasawa).
* **Runner:** 30 m/s, 0.2 m long, 35 mm diameter, with the plenum at the Module 03 T_intake and 1 bar.
* **Wall loss:** only the 90° bend is modelled (Pui et al. 1987). Liquid deposited there leaves the
  charge, with no film re-evaporation (that is Module 13). Because of this, "wall-impinged" is the
  liquid lost to the film, and "liquid at spark" counts only airborne droplets.
* **Ethanol:** liquid properties from CoolProp Ethanol, vapour thermo and transport from the San Diego
  mechanism, and DECHEMA/ChemSep Wilson activity (with an NRTL cross-check).

## Findings (EXECUTED, model-only)
* In every case most of the liquid lands on the bend wall: 54-99 % of the injected liquid. The
  ultrasonic 120 kHz and air-assist 20 µm atomisers lose the least. Airborne liquid left at spark is
  small in all cases (≤ 3.2 % nominal, ≤ 3.8 % cfd_matched).
* For each case, % evaporated at spark plus % wall plus % liquid at spark = 100.
* **Consistency flag:** at the wet points, the gas temperature at spark from Module 09 is about 95-305 K
  above Module 03's. The cause is that Module 03 assumes water evaporates in-cylinder (its own
  schedule), while Module 09 puts most of the water into the bend wall film. Fixing this needs the wall
  film model (Module 13) or a runner and bend design with lower Stokes numbers. It is not a numerical
  error.
* The values in `spray_at_spark.json` (also copied to
  `results/09_spray_evaporation/spray_at_spark.json` as the Module 11 input) are model estimates. They
  are not measurements.

## Files
| file | contents |
|---|---|
| `design_point_sweep.csv` | all 84 rows, including T and p diagnostics and closure errors |
| `spray_at_spark.json` | per case, atomiser and variant: % evaporated at IVC and at spark, % liquid at spark, % wall, SMD at spark |
| `summary.json` | labels, assumptions, cfd_matched fit details, spark angles, Module 03 reproduction check |
| `m03_pre_spark_p_theta.csv` | the imposed Module 03 p(θ) |
| `design_point_liquid_wall.png` | plot of liquid at spark and wall-impinged % |
