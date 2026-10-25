# Water Engine - Track A / Track B status

Generated 2026-10-24 18:34 PDT by `python -m sims.track_b.report` (branch `track-b/incremental-water-20261024`). **NOT YET PEER-REVIEW VERIFIED** - Module 03 and M03-CRN are two in-repo engines from the same toolchain; independent engine review (2+ engine rule) still pending.

## Rules (James, 2026-10-24)

* **Two tracks, ~50/50 compute.** Track A = existing water-majority work. Track B = start from normal fuels (regular/premium gasoline surrogates, E10, E85, methanol, ethanol, methane) dry, then add water in steps of at most 0.1 percentage point (w = m_water/(m_water+m_fuel) += 0.001), adding more only while efficiency gains; use data from both tracks to help each other.
* **Humid intake (6:22 PM rule)**, both tracks: water atomised into the intake air and fully evaporated before the cylinder (charge = humid air, specific humidity q). Track B: same 0.1-pp steps as humid water. Track A: humid variant of water-majority cases, capped by intake saturation (excess would condense).
* Gain threshold stated before any step ran: **1e-04 absolute (0.01 pp)** per step in Module 03 (~3x the 0.5-CAD step error ~3e-5, ~15x GCI 1.4e-5 relative; verification/x5_m03/RESULTS_FIX.md) AND a positive M03-CRN gain. Spark re-optimised at every step (golden-section MBT on CA50 0-16 deg, else knock/p_max-limited bisection to 0.005 deg).
* **Knock margin, CA50 limit and NO proxy come from Module 03 only** (M03-CRN has no knock or NOx model); M03-CRN gives an independent efficiency and peak pressure at the same CA50 (Woschni, like-for-like; C1 pass = |d_eta| <= 1.5 pp and |p_max ratio - 1| <= 5 %).

## Track B dry baselines (Module 03, spark at MBT or knock limit; best eligible CR x T_intake)

| fuel | regime | eligible pts | CR | T_intake K | eta M03 | CA50 (limit) | p_max bar | NO mol/J |
|---|---|---|---|---|---|---|---|---|
| PRF87 | normal | 1 | 9 | 320 | 0.3710 | 14.66 (knock) | 48.2 | 3.26e-08 |
| PRF87 | hot | 0 | - | - | - | knock-limited CA50 > 15 deg even at CR 9 (no eligible point) | - | - |
| PRF91 | normal | 1 | 9 | 320 | 0.3750 | 11.81 (knock) | 52.0 | 3.49e-08 |
| PRF91 | hot | 0 | - | - | - | knock-limited CA50 > 15 deg even at CR 9 (no eligible point) | - | - |
| PRF97 | normal | 3 | 10 | 320 | 0.3854 | 12.28 (knock) | 55.5 | 3.53e-08 |
| PRF97 | hot | 0 | - | - | - | knock-limited CA50 > 15 deg even at CR 9 (no eligible point) | - | - |
| E10 | normal | 3 | 10 | 320 | 0.3847 | 12.79 (knock) | 54.6 | 3.38e-08 |
| E10 | hot | 0 | - | - | - | knock-limited CA50 > 15 deg even at CR 9 (no eligible point) | - | - |
| E85 | normal | 8 | 13 | 320 | 0.4054 | 14.83 (knock) | 60.5 | 2.28e-08 |
| E85 | hot | 2 | 10 | 400 | 0.3778 | 11.20 (knock) | 46.6 | 3.88e-08 |
| CH3OH | normal | 13 | 17 | 320 | 0.4238 | 14.57 (knock) | 71.8 | 1.66e-08 |
| CH3OH | hot | 0 | - | - | - | knock-limited CA50 > 15 deg even at CR 9 (no eligible point) | - | - |
| C2H5OH | normal | 25 | 24 | 320 | 0.4458 | 13.70 (knock) | 97.8 | 2.68e-08 |
| C2H5OH | hot | 4 | 12 | 400 | 0.3897 | 14.93 (knock) | 47.6 | 4.03e-08 |
| CH4 | normal | 32 | 24 | 320 | 0.4397 | 12.40 (MBT) | 105.7 | 3.07e-08 |
| CH4 | hot | 10 | 18 | 400 | 0.4118 | 14.59 (knock) | 65.2 | 4.24e-08 |

## Track B 0.1-pp water chains

Water modes: **liquid** = water in fuel / port liquid (legacy Module 03: half evaporates in the intake, rest in-cylinder); **humid_evap** = all water atomised and evaporated in the intake with latent cooling (wet-bulb limited; humid air, cooled charge); **humid_ambient** = water vapour already in the intake air at T_intake (no evaporative cooling; pure humidity/dilution effect). p_IVC fixed, so evaporative cooling raises trapped mass (charge density) and vapour displaces O2 (lower O2 partial pressure) automatically; there is no gas-exchange model, so volumetric-efficiency effects beyond charge density are NOT modelled.

| fuel/regime | mode | dry eta M03 / CRN | best w (Track B rule) | steps | stop | best eta M03 / CRN | status |
|---|---|---|---|---|---|---|---|
| C2H5OH_hot | liquid | 0.38970 / 0.38962 | 0.022 | 22 | - | 0.39233 / 0.39222 | in progress (step 22) |
| C2H5OH_hot | humid_ambient | 0.38970 / 0.38962 | 0.000 | 0 | gain 8.60e-06 <= threshold 1e-04 | 0.38970 / 0.38962 | done |
| C2H5OH_hot | humid_evap | 0.38970 / 0.38962 | 0.005 | 5 | - | 0.39031 / 0.39022 | in progress (step 5) |
| C2H5OH_normal | liquid | 0.44576 / 0.44556 | 0.000 | 0 | gain 7.55e-05 <= threshold 1e-04 | 0.44576 / 0.44556 | done |
| C2H5OH_normal | humid_ambient | 0.44576 / 0.44556 | 0.000 | 0 | gain -1.82e-06 <= threshold 1e-04 | 0.44576 / 0.44556 | done |
| C2H5OH_normal | humid_evap | 0.44576 / 0.44556 | 0.000 | 0 | gain 8.04e-05 <= threshold 1e-04 | 0.44576 / 0.44556 | done |
| CH3OH_normal | liquid | 0.42379 / 0.42380 | 0.030 | 30 | - | 0.42804 / 0.42799 | in progress (step 30) |
| CH3OH_normal | humid_ambient | 0.42379 / 0.42380 | 0.000 | 0 | gain 9.28e-06 <= threshold 1e-04 | 0.42379 / 0.42380 | done |
| CH3OH_normal | humid_evap | 0.42379 / 0.42380 | 0.006 | 6 | - | 0.42474 / 0.42473 | in progress (step 6) |
| CH4_hot | liquid | 0.41178 / 0.41249 | 0.000 | 0 | gain 5.25e-05 <= threshold 1e-04 | 0.41178 / 0.41249 | done |
| CH4_hot | humid_ambient | 0.41178 / 0.41249 | 0.000 | 0 | - | 0.41178 / 0.41249 | in progress (step 0) |
| CH4_hot | humid_evap | 0.41178 / 0.41249 | 0.000 | 0 | gain 5.04e-05 <= threshold 1e-04 | 0.41178 / 0.41249 | done |
| CH4_normal | liquid | 0.43967 / 0.44017 | 0.000 | 0 | gain 1.92e-05 <= threshold 1e-04 | 0.43967 / 0.44017 | done |
| CH4_normal | humid_ambient | 0.43967 / 0.44017 | 0.000 | 0 | gain -3.44e-06 <= threshold 1e-04 | 0.43967 / 0.44017 | done |
| CH4_normal | humid_evap | 0.43967 / 0.44017 | 0.000 | 0 | gain 2.41e-05 <= threshold 1e-04 | 0.43967 / 0.44017 | done |
| E10_normal | liquid | 0.38472 / 0.38496 | 0.000 | 0 | gain 4.47e-05 <= threshold 1e-04 | 0.38472 / 0.38496 | done |
| E10_normal | humid_ambient | 0.38472 / 0.38496 | 0.000 | 0 | gain 4.56e-06 <= threshold 1e-04 | 0.38472 / 0.38496 | done |
| E10_normal | humid_evap | 0.38472 / 0.38496 | 0.000 | 0 | gain 4.15e-05 <= threshold 1e-04 | 0.38472 / 0.38496 | done |
| E85_hot | liquid | 0.37777 / 0.37793 | 0.000 | 0 | gain 4.98e-05 <= threshold 1e-04 | 0.37777 / 0.37793 | done |
| E85_hot | humid_ambient | 0.37777 / 0.37793 | 0.000 | 0 | gain 3.65e-06 <= threshold 1e-04 | 0.37777 / 0.37793 | done |
| E85_hot | humid_evap | 0.37777 / 0.37793 | 0.000 | 0 | gain 4.51e-05 <= threshold 1e-04 | 0.37777 / 0.37793 | done |
| E85_normal | liquid | 0.40536 / 0.40571 | 0.000 | 0 | gain 7.25e-05 <= threshold 1e-04 | 0.40536 / 0.40571 | done |
| E85_normal | humid_ambient | 0.40536 / 0.40571 | 0.000 | 0 | gain 5.97e-06 <= threshold 1e-04 | 0.40536 / 0.40571 | done |
| E85_normal | humid_evap | 0.40536 / 0.40571 | 0.000 | 0 | gain 6.43e-05 <= threshold 1e-04 | 0.40536 / 0.40571 | done |
| PRF87_normal | liquid | 0.37101 / 0.37137 | 0.000 | 0 | gain 5.22e-05 <= threshold 1e-04 | 0.37101 / 0.37137 | done |
| PRF87_normal | humid_ambient | 0.37101 / 0.37137 | 0.000 | 0 | gain 5.68e-06 <= threshold 1e-04 | 0.37101 / 0.37137 | done |
| PRF87_normal | humid_evap | 0.37101 / 0.37137 | 0.000 | 0 | gain 4.63e-05 <= threshold 1e-04 | 0.37101 / 0.37137 | done |
| PRF91_normal | liquid | 0.37503 / 0.37519 | 0.000 | 0 | gain 3.93e-05 <= threshold 1e-04 | 0.37503 / 0.37519 | done |
| PRF91_normal | humid_ambient | 0.37503 / 0.37519 | 0.000 | 0 | gain 4.05e-06 <= threshold 1e-04 | 0.37503 / 0.37519 | done |
| PRF91_normal | humid_evap | 0.37503 / 0.37519 | 0.000 | 0 | gain 3.37e-05 <= threshold 1e-04 | 0.37503 / 0.37519 | done |
| PRF97_normal | liquid | 0.38540 / 0.38557 | 0.000 | 0 | gain 4.14e-05 <= threshold 1e-04 | 0.38540 / 0.38557 | done |
| PRF97_normal | humid_ambient | 0.38540 / 0.38557 | 0.000 | 0 | gain 4.19e-06 <= threshold 1e-04 | 0.38540 / 0.38557 | done |
| PRF97_normal | humid_evap | 0.38540 / 0.38557 | 0.000 | 0 | gain 3.54e-05 <= threshold 1e-04 | 0.38540 / 0.38557 | done |

*probe = exploratory point at w = 1/2/5/10 %, same hardware, spark re-optimised; NOT a Track B step (the 0.1-pp rule stopped earlier). Shown because every gasoline/E-blend chain shows a steady positive slope just under the per-step threshold.


### C2H5OH_hot - liquid

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38970 | 0.38962 | +0.000 | +0.000 | -0.008 | 0.0001 | 14.93 (knock) | 47.6 / 47.7 | 4.03e-08 | - | True |
| step | 0.001 | 0.38982 | 0.38974 | +0.012 | +0.012 | -0.008 | 0.0003 | 14.87 (knock) | 47.7 / 47.7 | 4.02e-08 | - | True |
| step | 0.002 | 0.38995 | 0.38987 | +0.025 | +0.025 | -0.008 | 0.0002 | 14.81 (knock) | 47.8 / 47.8 | 4.02e-08 | - | True |
| step | 0.003 | 0.39008 | 0.38999 | +0.037 | +0.037 | -0.008 | 0.0001 | 14.76 (knock) | 47.9 / 47.9 | 4.02e-08 | - | True |
| step | 0.004 | 0.39020 | 0.39012 | +0.050 | +0.049 | -0.009 | 0.0000 | 14.70 (knock) | 48.0 / 48.0 | 4.01e-08 | - | True |
| step | 0.005 | 0.39032 | 0.39023 | +0.062 | +0.061 | -0.009 | 0.0003 | 14.64 (knock) | 48.1 / 48.1 | 4.01e-08 | - | True |
| step | 0.006 | 0.39044 | 0.39035 | +0.074 | +0.073 | -0.009 | 0.0003 | 14.58 (knock) | 48.2 / 48.2 | 4.01e-08 | - | True |
| step | 0.007 | 0.39057 | 0.39048 | +0.086 | +0.085 | -0.009 | 0.0002 | 14.52 (knock) | 48.3 / 48.3 | 4.00e-08 | - | True |
| step | 0.008 | 0.39069 | 0.39060 | +0.098 | +0.097 | -0.009 | 0.0002 | 14.47 (knock) | 48.4 / 48.4 | 4.00e-08 | - | True |
| step | 0.009 | 0.39081 | 0.39071 | +0.110 | +0.109 | -0.009 | 0.0003 | 14.41 (knock) | 48.5 / 48.5 | 3.99e-08 | - | True |
| step | 0.010 | 0.39093 | 0.39083 | +0.122 | +0.121 | -0.009 | 0.0003 | 14.35 (knock) | 48.6 / 48.6 | 3.99e-08 | - | True |
| step | 0.011 | 0.39105 | 0.39095 | +0.135 | +0.133 | -0.010 | 0.0000 | 14.29 (knock) | 48.7 / 48.7 | 3.99e-08 | - | True |
| step | 0.012 | 0.39117 | 0.39107 | +0.147 | +0.145 | -0.010 | 0.0001 | 14.23 (knock) | 48.8 / 48.8 | 3.98e-08 | - | True |
| step | 0.013 | 0.39129 | 0.39119 | +0.158 | +0.156 | -0.010 | 0.0002 | 14.17 (knock) | 48.9 / 48.9 | 3.98e-08 | - | True |
| step | 0.014 | 0.39141 | 0.39131 | +0.170 | +0.168 | -0.010 | 0.0000 | 14.11 (knock) | 49.0 / 49.0 | 3.98e-08 | - | True |
| step | 0.015 | 0.39152 | 0.39142 | +0.182 | +0.180 | -0.010 | 0.0002 | 14.05 (knock) | 49.0 / 49.1 | 3.97e-08 | - | True |
| step | 0.016 | 0.39164 | 0.39154 | +0.194 | +0.192 | -0.010 | 0.0000 | 13.99 (knock) | 49.1 / 49.2 | 3.97e-08 | - | True |
| step | 0.017 | 0.39176 | 0.39165 | +0.205 | +0.203 | -0.010 | 0.0002 | 13.93 (knock) | 49.2 / 49.3 | 3.97e-08 | - | True |
| step | 0.018 | 0.39187 | 0.39177 | +0.217 | +0.214 | -0.011 | 0.0001 | 13.87 (knock) | 49.3 / 49.4 | 3.96e-08 | - | True |
| step | 0.019 | 0.39199 | 0.39188 | +0.229 | +0.226 | -0.011 | 0.0000 | 13.81 (knock) | 49.4 / 49.5 | 3.96e-08 | - | True |
| step | 0.020 | 0.39210 | 0.39199 | +0.240 | +0.237 | -0.011 | 0.0003 | 13.75 (knock) | 49.5 / 49.6 | 3.96e-08 | - | True |
| step | 0.021 | 0.39222 | 0.39211 | +0.251 | +0.248 | -0.011 | 0.0002 | 13.69 (knock) | 49.6 / 49.7 | 3.95e-08 | - | True |
| step | 0.022 | 0.39233 | 0.39222 | +0.263 | +0.259 | -0.011 | 0.0002 | 13.63 (knock) | 49.7 / 49.8 | 3.95e-08 | - | True |

### C2H5OH_hot - humid_ambient

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38970 | 0.38962 | +0.000 | +0.000 | -0.008 | 0.0001 | 14.93 (knock) | 47.6 / 47.7 | 4.03e-08 | - | True |
| step | 0.001 | 0.38971 | 0.38963 | +0.001 | +0.001 | -0.008 | 0.0000 | 14.92 (knock) | 47.6 / 47.7 | 4.02e-08 | 0.11 | True |
| probe* | 0.010 | 0.38977 | 0.38970 | +0.007 | +0.008 | -0.007 | 0.0002 | 14.88 (knock) | 47.6 / 47.7 | 3.97e-08 | 1.13 | True |
| probe* | 0.020 | 0.38985 | 0.38978 | +0.015 | +0.016 | -0.006 | 0.0000 | 14.84 (knock) | 47.6 / 47.7 | 3.92e-08 | 2.28 | True |
| probe* | 0.050 | 0.39006 | 0.39001 | +0.035 | +0.039 | -0.004 | 0.0001 | 14.69 (knock) | 47.6 / 47.7 | 3.76e-08 | 5.89 | True |
| probe* | 0.100 | 0.39039 | 0.39038 | +0.068 | +0.075 | -0.001 | 0.0001 | 14.45 (knock) | 47.6 / 47.6 | 3.46e-08 | 12.42 | True |

### C2H5OH_hot - humid_evap

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38970 | 0.38962 | +0.000 | +0.000 | -0.008 | 0.0001 | 14.93 (knock) | 47.6 / 47.7 | 4.03e-08 | - | True |
| step | 0.001 | 0.38983 | 0.38975 | +0.012 | +0.012 | -0.008 | 0.0000 | 14.87 (knock) | 47.7 / 47.8 | 4.02e-08 | 0.11 | True |
| step | 0.002 | 0.38994 | 0.38986 | +0.024 | +0.024 | -0.008 | 0.0003 | 14.82 (knock) | 47.8 / 47.8 | 4.02e-08 | 0.22 | True |
| step | 0.003 | 0.39007 | 0.38998 | +0.036 | +0.036 | -0.008 | 0.0002 | 14.77 (knock) | 47.9 / 47.9 | 4.01e-08 | 0.34 | True |
| step | 0.004 | 0.39019 | 0.39010 | +0.049 | +0.048 | -0.008 | 0.0002 | 14.72 (knock) | 48.0 / 48.0 | 4.01e-08 | 0.45 | True |
| step | 0.005 | 0.39031 | 0.39022 | +0.061 | +0.060 | -0.009 | 0.0002 | 14.67 (knock) | 48.1 / 48.1 | 4.01e-08 | 0.56 | True |

### C2H5OH_normal - liquid

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.44576 | 0.44556 | +0.000 | +0.000 | -0.020 | 0.0002 | 13.70 (knock) | 97.8 / 97.7 | 2.68e-08 | - | True |
| step | 0.001 | 0.44584 | 0.44564 | +0.008 | +0.007 | -0.020 | 0.0004 | 13.65 (knock) | 98.0 / 97.9 | 2.67e-08 | - | True |
| probe* | 0.010 | 0.44649 | 0.44627 | +0.072 | +0.071 | -0.022 | 0.0004 | 13.20 (knock) | 100.2 / 100.1 | 2.65e-08 | - | True |
| probe* | 0.020 | 0.44710 | 0.44687 | +0.134 | +0.131 | -0.023 | 0.0002 | 12.69 (knock) | 102.7 / 102.6 | 2.62e-08 | - | True |
| probe* | 0.050 | 0.44835 | 0.44809 | +0.258 | +0.253 | -0.026 | 0.1201 | 11.80 (MBT) | 107.4 / 107.3 | 2.46e-08 | - | True |
| probe* | 0.100 | 0.45024 | 0.44997 | +0.448 | +0.440 | -0.028 | 0.4786 | 11.72 (MBT) | 108.8 / 108.7 | 1.99e-08 | - | True |

### C2H5OH_normal - humid_ambient

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.44576 | 0.44556 | +0.000 | +0.000 | -0.020 | 0.0002 | 13.70 (knock) | 97.8 / 97.7 | 2.68e-08 | - | True |
| step | 0.001 | 0.44576 | 0.44556 | -0.000 | -0.000 | -0.020 | 0.0007 | 13.70 (knock) | 97.8 / 97.7 | 2.67e-08 | 0.11 | True |
| probe* | 0.010 | 0.44577 | 0.44557 | +0.000 | +0.000 | -0.020 | 0.0006 | 13.67 (knock) | 97.8 / 97.8 | 2.64e-08 | 1.13 | True |
| probe* | 0.020 | 0.44577 | 0.44557 | +0.001 | +0.001 | -0.020 | 0.0008 | 13.65 (knock) | 97.9 / 97.8 | 2.59e-08 | 2.28 | True |
| probe* | 0.050 | 0.44577 | 0.44557 | +0.001 | +0.000 | -0.021 | 0.0006 | 13.56 (knock) | 98.1 / 98.0 | 2.46e-08 | 5.89 | True |
| probe* | 0.100 | 0.44573 | 0.44552 | -0.003 | -0.004 | -0.021 | 0.0006 | 13.42 (knock) | 98.3 / 98.2 | 2.23e-08 | 12.42 | True |

### C2H5OH_normal - humid_evap

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.44576 | 0.44556 | +0.000 | +0.000 | -0.020 | 0.0002 | 13.70 (knock) | 97.8 / 97.7 | 2.68e-08 | - | True |
| step | 0.001 | 0.44584 | 0.44564 | +0.008 | +0.008 | -0.020 | 0.0004 | 13.66 (knock) | 98.0 / 97.9 | 2.67e-08 | 0.11 | True |
| probe* | 0.010 | 0.44654 | 0.44633 | +0.078 | +0.077 | -0.022 | 0.0003 | 13.25 (knock) | 100.3 / 100.2 | 2.65e-08 | 1.13 | True |
| probe* | 0.020 | 0.44725 | 0.44702 | +0.148 | +0.146 | -0.023 | 0.0002 | 12.78 (knock) | 102.9 / 102.8 | 2.62e-08 | 2.28 | True |
| probe* | 0.050 | 0.44884 | 0.44858 | +0.307 | +0.302 | -0.026 | 0.0738 | 11.75 (MBT) | 109.3 / 109.2 | 2.49e-08 | 5.89 | True |
| probe* | 0.100 | 0.45128 | 0.45101 | +0.552 | +0.544 | -0.028 | 0.4222 | 11.67 (MBT) | 112.7 / 112.6 | 2.05e-08 | 12.42 | True |

### CH3OH_normal - liquid

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.42379 | 0.42380 | +0.000 | +0.000 | +0.001 | 0.0006 | 14.57 (knock) | 71.8 / 71.8 | 1.66e-08 | - | True |
| step | 0.001 | 0.42395 | 0.42396 | +0.017 | +0.016 | +0.001 | 0.0001 | 14.50 (knock) | 72.1 / 72.0 | 1.66e-08 | - | True |
| step | 0.002 | 0.42411 | 0.42411 | +0.032 | +0.032 | +0.000 | 0.0005 | 14.43 (knock) | 72.3 / 72.2 | 1.65e-08 | - | True |
| step | 0.003 | 0.42427 | 0.42427 | +0.048 | +0.047 | +0.000 | 0.0009 | 14.36 (knock) | 72.5 / 72.5 | 1.65e-08 | - | True |
| step | 0.004 | 0.42443 | 0.42443 | +0.064 | +0.063 | +0.000 | 0.0004 | 14.29 (knock) | 72.7 / 72.7 | 1.65e-08 | - | True |
| step | 0.005 | 0.42459 | 0.42458 | +0.080 | +0.079 | -0.000 | 0.0001 | 14.22 (knock) | 72.9 / 72.9 | 1.65e-08 | - | True |
| step | 0.006 | 0.42474 | 0.42473 | +0.095 | +0.094 | -0.000 | 0.0006 | 14.15 (knock) | 73.2 / 73.1 | 1.64e-08 | - | True |
| step | 0.007 | 0.42489 | 0.42489 | +0.111 | +0.109 | -0.001 | 0.0003 | 14.07 (knock) | 73.4 / 73.4 | 1.64e-08 | - | True |
| step | 0.008 | 0.42504 | 0.42503 | +0.125 | +0.124 | -0.001 | 0.0009 | 14.00 (knock) | 73.6 / 73.6 | 1.64e-08 | - | True |
| step | 0.009 | 0.42520 | 0.42519 | +0.141 | +0.139 | -0.001 | 0.0006 | 13.93 (knock) | 73.8 / 73.8 | 1.63e-08 | - | True |
| step | 0.010 | 0.42535 | 0.42534 | +0.156 | +0.154 | -0.001 | 0.0004 | 13.86 (knock) | 74.1 / 74.0 | 1.63e-08 | - | True |
| step | 0.011 | 0.42550 | 0.42548 | +0.171 | +0.169 | -0.001 | 0.0002 | 13.78 (knock) | 74.3 / 74.3 | 1.63e-08 | - | True |
| step | 0.012 | 0.42564 | 0.42562 | +0.185 | +0.183 | -0.001 | 0.0009 | 13.71 (knock) | 74.5 / 74.5 | 1.62e-08 | - | True |
| step | 0.013 | 0.42579 | 0.42577 | +0.200 | +0.197 | -0.002 | 0.0008 | 13.64 (knock) | 74.7 / 74.7 | 1.62e-08 | - | True |
| step | 0.014 | 0.42593 | 0.42591 | +0.214 | +0.212 | -0.002 | 0.0007 | 13.56 (knock) | 75.0 / 74.9 | 1.62e-08 | - | True |
| step | 0.015 | 0.42607 | 0.42605 | +0.229 | +0.226 | -0.002 | 0.0007 | 13.49 (knock) | 75.2 / 75.2 | 1.62e-08 | - | True |
| step | 0.016 | 0.42622 | 0.42619 | +0.243 | +0.240 | -0.002 | 0.0007 | 13.42 (knock) | 75.4 / 75.4 | 1.61e-08 | - | True |
| step | 0.017 | 0.42636 | 0.42633 | +0.257 | +0.254 | -0.002 | 0.0008 | 13.34 (knock) | 75.7 / 75.6 | 1.61e-08 | - | True |
| step | 0.018 | 0.42649 | 0.42647 | +0.271 | +0.267 | -0.003 | 0.0009 | 13.27 (knock) | 75.9 / 75.9 | 1.61e-08 | - | True |
| step | 0.019 | 0.42664 | 0.42661 | +0.285 | +0.281 | -0.003 | 0.0001 | 13.19 (knock) | 76.2 / 76.1 | 1.60e-08 | - | True |
| step | 0.020 | 0.42677 | 0.42674 | +0.298 | +0.295 | -0.003 | 0.0003 | 13.12 (knock) | 76.4 / 76.4 | 1.60e-08 | - | True |
| step | 0.021 | 0.42690 | 0.42687 | +0.312 | +0.308 | -0.003 | 0.0005 | 13.04 (knock) | 76.6 / 76.6 | 1.60e-08 | - | True |
| step | 0.022 | 0.42704 | 0.42700 | +0.325 | +0.321 | -0.003 | 0.0008 | 12.97 (knock) | 76.9 / 76.8 | 1.60e-08 | - | True |
| step | 0.023 | 0.42717 | 0.42713 | +0.338 | +0.334 | -0.004 | 0.0002 | 12.89 (knock) | 77.1 / 77.1 | 1.59e-08 | - | True |
| step | 0.024 | 0.42730 | 0.42726 | +0.351 | +0.346 | -0.004 | 0.0006 | 12.82 (knock) | 77.4 / 77.3 | 1.59e-08 | - | True |
| step | 0.025 | 0.42743 | 0.42739 | +0.364 | +0.359 | -0.004 | 0.0001 | 12.74 (knock) | 77.6 / 77.6 | 1.59e-08 | - | True |
| step | 0.026 | 0.42755 | 0.42751 | +0.377 | +0.372 | -0.004 | 0.0006 | 12.66 (knock) | 77.8 / 77.8 | 1.58e-08 | - | True |
| step | 0.027 | 0.42768 | 0.42764 | +0.389 | +0.384 | -0.004 | 0.0002 | 12.58 (knock) | 78.1 / 78.1 | 1.58e-08 | - | True |
| step | 0.028 | 0.42780 | 0.42775 | +0.401 | +0.396 | -0.005 | 0.0008 | 12.51 (knock) | 78.3 / 78.3 | 1.58e-08 | - | True |
| step | 0.029 | 0.42792 | 0.42788 | +0.414 | +0.408 | -0.005 | 0.0005 | 12.43 (knock) | 78.6 / 78.6 | 1.58e-08 | - | True |
| step | 0.030 | 0.42804 | 0.42799 | +0.426 | +0.420 | -0.005 | 0.0003 | 12.35 (knock) | 78.9 / 78.8 | 1.57e-08 | - | True |

### CH3OH_normal - humid_ambient

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.42379 | 0.42380 | +0.000 | +0.000 | +0.001 | 0.0006 | 14.57 (knock) | 71.8 / 71.8 | 1.66e-08 | - | True |
| step | 0.001 | 0.42380 | 0.42380 | +0.001 | +0.001 | +0.001 | 0.0008 | 14.57 (knock) | 71.8 / 71.8 | 1.65e-08 | 0.16 | True |
| probe* | 0.010 | 0.42390 | 0.42390 | +0.011 | +0.011 | +0.001 | 0.0005 | 14.51 (knock) | 71.9 / 71.9 | 1.61e-08 | 1.57 | True |
| probe* | 0.020 | 0.42400 | 0.42400 | +0.021 | +0.021 | +0.000 | 0.0007 | 14.46 (knock) | 72.0 / 71.9 | 1.57e-08 | 3.17 | True |
| probe* | 0.050 | 0.42432 | 0.42431 | +0.053 | +0.051 | -0.001 | 0.0002 | 14.27 (knock) | 72.2 / 72.1 | 1.43e-08 | 8.19 | True |
| probe* | 0.100 | 0.42480 | 0.42477 | +0.101 | +0.098 | -0.003 | 0.0001 | 13.96 (knock) | 72.4 / 72.4 | 1.20e-08 | 17.28 | True |

### CH3OH_normal - humid_evap

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.42379 | 0.42380 | +0.000 | +0.000 | +0.001 | 0.0006 | 14.57 (knock) | 71.8 / 71.8 | 1.66e-08 | - | True |
| step | 0.001 | 0.42395 | 0.42395 | +0.016 | +0.016 | +0.001 | 0.0007 | 14.51 (knock) | 72.1 / 72.0 | 1.66e-08 | 0.16 | True |
| step | 0.002 | 0.42411 | 0.42411 | +0.032 | +0.031 | +0.000 | 0.0008 | 14.45 (knock) | 72.3 / 72.3 | 1.65e-08 | 0.31 | True |
| step | 0.003 | 0.42427 | 0.42427 | +0.048 | +0.048 | +0.000 | 0.0001 | 14.38 (knock) | 72.5 / 72.5 | 1.65e-08 | 0.47 | True |
| step | 0.004 | 0.42443 | 0.42443 | +0.064 | +0.063 | +0.000 | 0.0004 | 14.31 (knock) | 72.8 / 72.7 | 1.65e-08 | 0.62 | True |
| step | 0.005 | 0.42458 | 0.42458 | +0.079 | +0.078 | -0.000 | 0.0006 | 14.25 (knock) | 73.0 / 73.0 | 1.65e-08 | 0.78 | True |
| step | 0.006 | 0.42474 | 0.42473 | +0.095 | +0.094 | -0.000 | 0.0008 | 14.19 (knock) | 73.2 / 73.2 | 1.64e-08 | 0.94 | True |

### CH4_hot - liquid

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.41178 | 0.41249 | +0.000 | +0.000 | +0.071 | 0.0002 | 14.59 (knock) | 65.2 / 65.2 | 4.24e-08 | - | True |
| step | 0.001 | 0.41184 | 0.41254 | +0.005 | +0.005 | +0.070 | 0.0001 | 14.56 (knock) | 65.3 / 65.3 | 4.24e-08 | - | True |
| probe* | 0.010 | 0.41229 | 0.41298 | +0.051 | +0.050 | +0.069 | 0.0001 | 14.32 (knock) | 66.0 / 66.0 | 4.23e-08 | - | True |
| probe* | 0.020 | 0.41278 | 0.41346 | +0.100 | +0.097 | +0.068 | 0.0000 | 14.04 (knock) | 66.7 / 66.7 | 4.21e-08 | - | True |
| probe* | 0.050 | 0.41415 | 0.41478 | +0.236 | +0.229 | +0.063 | 0.0003 | 13.18 (knock) | 69.1 / 69.1 | 4.17e-08 | - | True |
| probe* | 0.100 | 0.41594 | 0.41648 | +0.415 | +0.399 | +0.055 | 0.0003 | 11.60 (knock) | 73.5 / 73.6 | 4.09e-08 | - | True |

### CH4_hot - humid_ambient

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.41178 | 0.41249 | +0.000 | +0.000 | +0.071 | 0.0002 | 14.59 (knock) | 65.2 / 65.2 | 4.24e-08 | - | True |

### CH4_hot - humid_evap

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.41178 | 0.41249 | +0.000 | +0.000 | +0.071 | 0.0002 | 14.59 (knock) | 65.2 / 65.2 | 4.24e-08 | - | True |
| step | 0.001 | 0.41183 | 0.41254 | +0.005 | +0.005 | +0.070 | 0.0004 | 14.57 (knock) | 65.3 / 65.3 | 4.24e-08 | 0.06 | True |

### CH4_normal - liquid

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.43967 | 0.44017 | +0.000 | +0.000 | +0.050 | 0.6020 | 12.40 (MBT) | 105.7 / 105.7 | 3.07e-08 | - | True |
| step | 0.001 | 0.43969 | 0.44019 | +0.002 | +0.002 | +0.050 | 0.6040 | 12.40 (MBT) | 105.7 / 105.7 | 3.06e-08 | - | True |
| probe* | 0.010 | 0.43986 | 0.44037 | +0.019 | +0.019 | +0.050 | 0.6213 | 12.40 (MBT) | 105.8 / 105.8 | 3.03e-08 | - | True |
| probe* | 0.020 | 0.44006 | 0.44056 | +0.039 | +0.039 | +0.050 | 0.6401 | 12.40 (MBT) | 105.9 / 105.9 | 3.00e-08 | - | True |
| probe* | 0.050 | 0.44070 | 0.44119 | +0.103 | +0.102 | +0.049 | 0.6935 | 12.40 (MBT) | 106.2 / 106.2 | 2.89e-08 | - | True |
| probe* | 0.100 | 0.44187 | 0.44235 | +0.220 | +0.218 | +0.048 | 0.7712 | 12.38 (MBT) | 106.8 / 106.8 | 2.70e-08 | - | True |

### CH4_normal - humid_ambient

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.43967 | 0.44017 | +0.000 | +0.000 | +0.050 | 0.6020 | 12.40 (MBT) | 105.7 / 105.7 | 3.07e-08 | - | True |
| step | 0.001 | 0.43967 | 0.44017 | -0.000 | -0.000 | +0.050 | 0.6023 | 12.40 (MBT) | 105.7 / 105.7 | 3.07e-08 | 0.06 | True |
| probe* | 0.010 | 0.43964 | 0.44014 | -0.003 | -0.003 | +0.050 | 0.6068 | 12.43 (MBT) | 105.5 / 105.5 | 3.05e-08 | 0.59 | True |
| probe* | 0.020 | 0.43960 | 0.44011 | -0.007 | -0.007 | +0.051 | 0.6093 | 12.43 (MBT) | 105.5 / 105.5 | 3.03e-08 | 1.19 | True |

### CH4_normal - humid_evap

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.43967 | 0.44017 | +0.000 | +0.000 | +0.050 | 0.6020 | 12.40 (MBT) | 105.7 / 105.7 | 3.07e-08 | - | True |
| step | 0.001 | 0.43969 | 0.44020 | +0.002 | +0.002 | +0.050 | 0.6038 | 12.40 (MBT) | 105.7 / 105.7 | 3.06e-08 | 0.06 | True |
| probe* | 0.010 | 0.43991 | 0.44042 | +0.024 | +0.024 | +0.050 | 0.6195 | 12.40 (MBT) | 106.0 / 106.0 | 3.04e-08 | 0.59 | True |
| probe* | 0.020 | 0.44016 | 0.44067 | +0.049 | +0.049 | +0.050 | 0.6366 | 12.40 (MBT) | 106.2 / 106.2 | 3.00e-08 | 1.19 | True |
| probe* | 0.050 | 0.44096 | 0.44145 | +0.129 | +0.128 | +0.050 | 0.6845 | 12.38 (MBT) | 107.2 / 107.2 | 2.90e-08 | 3.07 | True |
| probe* | 0.100 | 0.44242 | 0.44290 | +0.275 | +0.273 | +0.048 | 0.7568 | 12.35 (MBT) | 108.8 / 108.8 | 2.72e-08 | 6.49 | True |

### E10_normal - liquid

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38472 | 0.38496 | +0.000 | +0.000 | +0.023 | 0.0001 | 12.79 (knock) | 54.6 / 54.9 | 3.38e-08 | - | True |
| step | 0.001 | 0.38477 | 0.38500 | +0.004 | +0.004 | +0.023 | 0.0001 | 12.77 (knock) | 54.7 / 54.9 | 3.37e-08 | - | True |
| probe* | 0.010 | 0.38518 | 0.38540 | +0.045 | +0.045 | +0.023 | 0.0001 | 12.57 (knock) | 55.0 / 55.3 | 3.34e-08 | - | True |
| probe* | 0.020 | 0.38563 | 0.38585 | +0.091 | +0.089 | +0.022 | 0.0001 | 12.33 (knock) | 55.5 / 55.7 | 3.30e-08 | - | True |
| probe* | 0.050 | 0.38698 | 0.38718 | +0.226 | +0.222 | +0.020 | 0.0000 | 11.58 (knock) | 56.8 / 57.1 | 3.17e-08 | - | True |
| probe* | 0.100 | 0.38913 | 0.38929 | +0.441 | +0.433 | +0.016 | 0.0001 | 10.18 (knock) | 59.5 / 59.7 | 2.94e-08 | - | True |

### E10_normal - humid_ambient

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38472 | 0.38496 | +0.000 | +0.000 | +0.023 | 0.0001 | 12.79 (knock) | 54.6 / 54.9 | 3.38e-08 | - | True |
| step | 0.001 | 0.38473 | 0.38496 | +0.000 | +0.001 | +0.023 | 0.0001 | 12.79 (knock) | 54.6 / 54.9 | 3.38e-08 | 0.07 | True |
| probe* | 0.010 | 0.38477 | 0.38501 | +0.005 | +0.005 | +0.024 | 0.0000 | 12.77 (knock) | 54.6 / 54.8 | 3.35e-08 | 0.70 | True |
| probe* | 0.020 | 0.38481 | 0.38505 | +0.009 | +0.010 | +0.024 | 0.0001 | 12.74 (knock) | 54.6 / 54.8 | 3.32e-08 | 1.42 | True |
| probe* | 0.050 | 0.38495 | 0.38521 | +0.023 | +0.025 | +0.026 | 0.0000 | 12.66 (knock) | 54.6 / 54.8 | 3.22e-08 | 3.67 | True |
| probe* | 0.100 | 0.38519 | 0.38547 | +0.047 | +0.052 | +0.028 | 0.0001 | 12.51 (knock) | 54.5 / 54.7 | 3.05e-08 | 7.75 | True |

### E10_normal - humid_evap

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38472 | 0.38496 | +0.000 | +0.000 | +0.023 | 0.0001 | 12.79 (knock) | 54.6 / 54.9 | 3.38e-08 | - | True |
| step | 0.001 | 0.38476 | 0.38500 | +0.004 | +0.004 | +0.023 | 0.0000 | 12.78 (knock) | 54.7 / 54.9 | 3.37e-08 | 0.07 | True |
| probe* | 0.010 | 0.38512 | 0.38535 | +0.040 | +0.040 | +0.023 | 0.0001 | 12.64 (knock) | 55.0 / 55.3 | 3.33e-08 | 0.70 | True |
| probe* | 0.020 | 0.38553 | 0.38576 | +0.081 | +0.080 | +0.023 | 0.0000 | 12.48 (knock) | 55.4 / 55.7 | 3.29e-08 | 1.42 | True |
| probe* | 0.050 | 0.38676 | 0.38698 | +0.204 | +0.203 | +0.023 | 0.0000 | 11.98 (knock) | 56.8 / 57.0 | 3.15e-08 | 3.67 | True |
| probe* | 0.100 | 0.38888 | 0.38909 | +0.416 | +0.413 | +0.021 | 0.0001 | 11.05 (knock) | 59.3 / 59.5 | 2.90e-08 | 7.75 | True |

### E85_hot - liquid

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37777 | 0.37793 | +0.000 | +0.000 | +0.016 | 0.0001 | 11.20 (knock) | 46.6 / 46.8 | 3.88e-08 | - | True |
| step | 0.001 | 0.37782 | 0.37797 | +0.005 | +0.005 | +0.016 | 0.0000 | 11.17 (knock) | 46.6 / 46.8 | 3.87e-08 | - | True |
| probe* | 0.010 | 0.37826 | 0.37840 | +0.049 | +0.048 | +0.015 | 0.0000 | 10.91 (knock) | 47.0 / 47.2 | 3.83e-08 | - | True |
| probe* | 0.020 | 0.37873 | 0.37887 | +0.096 | +0.095 | +0.014 | 0.0001 | 10.60 (knock) | 47.4 / 47.6 | 3.77e-08 | - | True |
| probe* | 0.050 | 0.38009 | 0.38020 | +0.232 | +0.228 | +0.011 | 0.0001 | 9.63 (knock) | 48.8 / 49.1 | 3.60e-08 | - | True |
| probe* | 0.100 | 0.38200 | 0.38205 | +0.423 | +0.412 | +0.005 | 0.0001 | 7.77 (knock) | 51.6 / 51.8 | 3.29e-08 | - | True |

### E85_hot - humid_ambient

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37777 | 0.37793 | +0.000 | +0.000 | +0.016 | 0.0001 | 11.20 (knock) | 46.6 / 46.8 | 3.88e-08 | - | True |
| step | 0.001 | 0.37777 | 0.37793 | +0.000 | +0.000 | +0.016 | 0.0001 | 11.20 (knock) | 46.6 / 46.8 | 3.88e-08 | 0.10 | True |
| probe* | 0.010 | 0.37781 | 0.37798 | +0.004 | +0.005 | +0.016 | 0.0001 | 11.17 (knock) | 46.5 / 46.8 | 3.84e-08 | 1.04 | True |
| probe* | 0.020 | 0.37786 | 0.37803 | +0.009 | +0.011 | +0.017 | 0.0001 | 11.13 (knock) | 46.5 / 46.7 | 3.80e-08 | 2.09 | True |
| probe* | 0.050 | 0.37800 | 0.37819 | +0.023 | +0.027 | +0.020 | 0.0001 | 11.02 (knock) | 46.5 / 46.7 | 3.67e-08 | 5.39 | True |
| probe* | 0.100 | 0.37823 | 0.37847 | +0.046 | +0.055 | +0.024 | 0.0001 | 10.81 (knock) | 46.4 / 46.6 | 3.43e-08 | 11.39 | True |

### E85_hot - humid_evap

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37777 | 0.37793 | +0.000 | +0.000 | +0.016 | 0.0001 | 11.20 (knock) | 46.6 / 46.8 | 3.88e-08 | - | True |
| step | 0.001 | 0.37781 | 0.37797 | +0.005 | +0.005 | +0.016 | 0.0001 | 11.19 (knock) | 46.6 / 46.8 | 3.87e-08 | 0.10 | True |
| probe* | 0.010 | 0.37822 | 0.37838 | +0.045 | +0.045 | +0.016 | 0.0000 | 11.01 (knock) | 47.0 / 47.2 | 3.82e-08 | 1.04 | True |
| probe* | 0.020 | 0.37867 | 0.37883 | +0.090 | +0.091 | +0.016 | 0.0001 | 10.81 (knock) | 47.4 / 47.6 | 3.76e-08 | 2.09 | True |
| probe* | 0.050 | 0.38004 | 0.38020 | +0.227 | +0.227 | +0.016 | 0.0000 | 10.18 (knock) | 48.7 / 48.9 | 3.57e-08 | 5.39 | True |
| probe* | 0.100 | 0.38231 | 0.38245 | +0.454 | +0.453 | +0.015 | 0.0001 | 9.00 (knock) | 51.2 / 51.4 | 3.22e-08 | 11.39 | True |

### E85_normal - liquid

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.40536 | 0.40571 | +0.000 | +0.000 | +0.035 | 0.0001 | 14.83 (knock) | 60.5 / 60.6 | 2.28e-08 | - | True |
| step | 0.001 | 0.40543 | 0.40578 | +0.007 | +0.007 | +0.035 | 0.0002 | 14.80 (knock) | 60.6 / 60.6 | 2.27e-08 | - | True |
| probe* | 0.010 | 0.40611 | 0.40645 | +0.075 | +0.074 | +0.034 | 0.0001 | 14.55 (knock) | 61.2 / 61.3 | 2.22e-08 | - | True |
| probe* | 0.020 | 0.40686 | 0.40718 | +0.150 | +0.147 | +0.032 | 0.0001 | 14.26 (knock) | 61.9 / 62.0 | 2.17e-08 | - | True |
| probe* | 0.050 | 0.40907 | 0.40936 | +0.372 | +0.365 | +0.028 | 0.0001 | 13.36 (knock) | 64.1 / 64.2 | 2.01e-08 | - | True |
| probe* | 0.100 | 0.41259 | 0.41280 | +0.723 | +0.710 | +0.021 | 0.0000 | 11.68 (knock) | 68.4 / 68.5 | 1.73e-08 | - | True |

### E85_normal - humid_ambient

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.40536 | 0.40571 | +0.000 | +0.000 | +0.035 | 0.0001 | 14.83 (knock) | 60.5 / 60.6 | 2.28e-08 | - | True |
| step | 0.001 | 0.40536 | 0.40571 | +0.001 | +0.001 | +0.035 | 0.0001 | 14.83 (knock) | 60.5 / 60.6 | 2.27e-08 | 0.10 | True |
| probe* | 0.010 | 0.40542 | 0.40577 | +0.006 | +0.006 | +0.035 | 0.0000 | 14.80 (knock) | 60.5 / 60.6 | 2.24e-08 | 1.04 | True |
| probe* | 0.020 | 0.40549 | 0.40583 | +0.013 | +0.013 | +0.035 | 0.0000 | 14.77 (knock) | 60.5 / 60.6 | 2.20e-08 | 2.09 | True |
| probe* | 0.050 | 0.40568 | 0.40603 | +0.033 | +0.032 | +0.034 | 0.0001 | 14.68 (knock) | 60.5 / 60.5 | 2.08e-08 | 5.39 | True |
| probe* | 0.100 | 0.40603 | 0.40636 | +0.068 | +0.066 | +0.033 | 0.0001 | 14.52 (knock) | 60.4 / 60.4 | 1.87e-08 | 11.39 | True |

### E85_normal - humid_evap

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.40536 | 0.40571 | +0.000 | +0.000 | +0.035 | 0.0001 | 14.83 (knock) | 60.5 / 60.6 | 2.28e-08 | - | True |
| step | 0.001 | 0.40542 | 0.40577 | +0.006 | +0.006 | +0.035 | 0.0001 | 14.81 (knock) | 60.6 / 60.6 | 2.27e-08 | 0.10 | True |
| probe* | 0.010 | 0.40601 | 0.40635 | +0.065 | +0.064 | +0.034 | 0.0001 | 14.64 (knock) | 61.2 / 61.2 | 2.22e-08 | 1.04 | True |
| probe* | 0.020 | 0.40667 | 0.40700 | +0.131 | +0.129 | +0.033 | 0.0000 | 14.45 (knock) | 61.8 / 61.9 | 2.16e-08 | 2.09 | True |
| probe* | 0.050 | 0.40868 | 0.40898 | +0.332 | +0.327 | +0.030 | 0.0000 | 13.84 (knock) | 64.0 / 64.0 | 1.99e-08 | 5.39 | True |
| probe* | 0.100 | 0.41211 | 0.41236 | +0.676 | +0.666 | +0.025 | 0.0002 | 12.73 (knock) | 68.1 / 68.2 | 1.69e-08 | 11.39 | True |

### PRF87_normal - liquid

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37101 | 0.37137 | +0.000 | +0.000 | +0.036 | 0.0001 | 14.66 (knock) | 48.2 / 48.5 | 3.26e-08 | - | True |
| step | 0.001 | 0.37106 | 0.37142 | +0.005 | +0.005 | +0.036 | 0.0002 | 14.64 (knock) | 48.3 / 48.5 | 3.25e-08 | - | True |
| probe* | 0.010 | 0.37154 | 0.37189 | +0.053 | +0.052 | +0.035 | 0.0001 | 14.43 (knock) | 48.6 / 48.8 | 3.22e-08 | - | True |
| probe* | 0.020 | 0.37207 | 0.37242 | +0.106 | +0.105 | +0.035 | 0.0001 | 14.19 (knock) | 49.0 / 49.2 | 3.18e-08 | - | True |
| probe* | 0.050 | 0.37367 | 0.37400 | +0.266 | +0.263 | +0.033 | 0.0001 | 13.44 (knock) | 50.1 / 50.4 | 3.05e-08 | - | True |
| probe* | 0.100 | 0.37634 | 0.37663 | +0.533 | +0.526 | +0.029 | 0.0001 | 12.03 (knock) | 52.3 / 52.6 | 2.83e-08 | - | True |

### PRF87_normal - humid_ambient

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37101 | 0.37137 | +0.000 | +0.000 | +0.036 | 0.0001 | 14.66 (knock) | 48.2 / 48.5 | 3.26e-08 | - | True |
| step | 0.001 | 0.37102 | 0.37137 | +0.001 | +0.001 | +0.036 | 0.0001 | 14.66 (knock) | 48.2 / 48.5 | 3.25e-08 | 0.07 | True |
| probe* | 0.010 | 0.37107 | 0.37143 | +0.006 | +0.006 | +0.036 | 0.0000 | 14.63 (knock) | 48.2 / 48.5 | 3.23e-08 | 0.67 | True |
| probe* | 0.020 | 0.37112 | 0.37149 | +0.011 | +0.012 | +0.037 | 0.0001 | 14.61 (knock) | 48.2 / 48.5 | 3.20e-08 | 1.36 | True |
| probe* | 0.050 | 0.37129 | 0.37167 | +0.028 | +0.030 | +0.038 | 0.0001 | 14.52 (knock) | 48.2 / 48.4 | 3.10e-08 | 3.50 | True |
| probe* | 0.100 | 0.37158 | 0.37199 | +0.057 | +0.062 | +0.040 | 0.0001 | 14.37 (knock) | 48.2 / 48.4 | 2.93e-08 | 7.39 | True |

### PRF87_normal - humid_evap

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37101 | 0.37137 | +0.000 | +0.000 | +0.036 | 0.0001 | 14.66 (knock) | 48.2 / 48.5 | 3.26e-08 | - | True |
| step | 0.001 | 0.37106 | 0.37141 | +0.005 | +0.005 | +0.036 | 0.0001 | 14.64 (knock) | 48.3 / 48.5 | 3.25e-08 | 0.07 | True |
| probe* | 0.010 | 0.37145 | 0.37181 | +0.044 | +0.044 | +0.036 | 0.0001 | 14.50 (knock) | 48.6 / 48.8 | 3.22e-08 | 0.67 | True |
| probe* | 0.020 | 0.37191 | 0.37226 | +0.090 | +0.089 | +0.035 | 0.0000 | 14.34 (knock) | 48.9 / 49.2 | 3.17e-08 | 1.36 | True |
| probe* | 0.050 | 0.37329 | 0.37363 | +0.228 | +0.227 | +0.035 | 0.0001 | 13.83 (knock) | 50.1 / 50.3 | 3.04e-08 | 3.50 | True |
| probe* | 0.100 | 0.37569 | 0.37603 | +0.468 | +0.466 | +0.033 | 0.0000 | 12.88 (knock) | 52.2 / 52.5 | 2.79e-08 | 7.39 | True |

### PRF91_normal - liquid

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37503 | 0.37519 | +0.000 | +0.000 | +0.016 | 0.0000 | 11.81 (knock) | 52.0 / 52.3 | 3.49e-08 | - | True |
| step | 0.001 | 0.37507 | 0.37523 | +0.004 | +0.004 | +0.016 | 0.0001 | 11.79 (knock) | 52.0 / 52.3 | 3.49e-08 | - | True |
| probe* | 0.010 | 0.37543 | 0.37559 | +0.040 | +0.040 | +0.015 | 0.0001 | 11.57 (knock) | 52.3 / 52.6 | 3.45e-08 | - | True |
| probe* | 0.020 | 0.37584 | 0.37599 | +0.081 | +0.079 | +0.015 | 0.0001 | 11.32 (knock) | 52.7 / 53.0 | 3.41e-08 | - | True |
| probe* | 0.050 | 0.37703 | 0.37715 | +0.200 | +0.196 | +0.013 | 0.0001 | 10.53 (knock) | 54.0 / 54.3 | 3.29e-08 | - | True |
| probe* | 0.100 | 0.37887 | 0.37895 | +0.384 | +0.376 | +0.008 | 0.0001 | 9.04 (knock) | 56.4 / 56.7 | 3.08e-08 | - | True |

### PRF91_normal - humid_ambient

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37503 | 0.37519 | +0.000 | +0.000 | +0.016 | 0.0000 | 11.81 (knock) | 52.0 / 52.3 | 3.49e-08 | - | True |
| step | 0.001 | 0.37503 | 0.37520 | +0.000 | +0.000 | +0.016 | 0.0000 | 11.81 (knock) | 52.0 / 52.2 | 3.49e-08 | 0.07 | True |
| probe* | 0.010 | 0.37507 | 0.37524 | +0.004 | +0.005 | +0.017 | 0.0000 | 11.78 (knock) | 52.0 / 52.2 | 3.46e-08 | 0.67 | True |
| probe* | 0.020 | 0.37511 | 0.37528 | +0.008 | +0.009 | +0.017 | 0.0001 | 11.75 (knock) | 51.9 / 52.2 | 3.43e-08 | 1.36 | True |
| probe* | 0.050 | 0.37524 | 0.37543 | +0.021 | +0.024 | +0.019 | 0.0001 | 11.66 (knock) | 51.9 / 52.2 | 3.34e-08 | 3.50 | True |
| probe* | 0.100 | 0.37546 | 0.37569 | +0.043 | +0.050 | +0.022 | 0.0001 | 11.50 (knock) | 51.9 / 52.1 | 3.17e-08 | 7.39 | True |

### PRF91_normal - humid_evap

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37503 | 0.37519 | +0.000 | +0.000 | +0.016 | 0.0000 | 11.81 (knock) | 52.0 / 52.3 | 3.49e-08 | - | True |
| step | 0.001 | 0.37506 | 0.37522 | +0.003 | +0.003 | +0.016 | 0.0001 | 11.79 (knock) | 52.0 / 52.3 | 3.49e-08 | 0.07 | True |
| probe* | 0.010 | 0.37539 | 0.37555 | +0.036 | +0.036 | +0.016 | 0.0000 | 11.65 (knock) | 52.3 / 52.6 | 3.45e-08 | 0.67 | True |
| probe* | 0.020 | 0.37575 | 0.37591 | +0.072 | +0.072 | +0.016 | 0.0001 | 11.48 (knock) | 52.7 / 53.0 | 3.41e-08 | 1.36 | True |
| probe* | 0.050 | 0.37686 | 0.37701 | +0.183 | +0.182 | +0.015 | 0.0001 | 10.95 (knock) | 53.9 / 54.2 | 3.27e-08 | 3.50 | True |
| probe* | 0.100 | 0.37874 | 0.37888 | +0.371 | +0.369 | +0.014 | 0.0001 | 9.97 (knock) | 56.2 / 56.5 | 3.04e-08 | 7.39 | True |

### PRF97_normal - liquid

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38540 | 0.38557 | +0.000 | +0.000 | +0.017 | 0.0000 | 12.28 (knock) | 55.5 / 55.8 | 3.53e-08 | - | True |
| step | 0.001 | 0.38544 | 0.38561 | +0.004 | +0.004 | +0.017 | 0.0000 | 12.26 (knock) | 55.6 / 55.8 | 3.53e-08 | - | True |
| probe* | 0.010 | 0.38581 | 0.38597 | +0.041 | +0.041 | +0.017 | 0.0000 | 12.06 (knock) | 55.9 / 56.2 | 3.49e-08 | - | True |
| probe* | 0.020 | 0.38622 | 0.38638 | +0.082 | +0.081 | +0.016 | 0.0001 | 11.83 (knock) | 56.3 / 56.6 | 3.45e-08 | - | True |
| probe* | 0.050 | 0.38743 | 0.38757 | +0.203 | +0.200 | +0.014 | 0.0000 | 11.11 (knock) | 57.7 / 57.9 | 3.33e-08 | - | True |
| probe* | 0.100 | 0.38935 | 0.38945 | +0.396 | +0.388 | +0.010 | 0.0001 | 9.75 (knock) | 60.2 / 60.5 | 3.12e-08 | - | True |

### PRF97_normal - humid_ambient

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38540 | 0.38557 | +0.000 | +0.000 | +0.017 | 0.0000 | 12.28 (knock) | 55.5 / 55.8 | 3.53e-08 | - | True |
| step | 0.001 | 0.38540 | 0.38557 | +0.000 | +0.000 | +0.017 | 0.0000 | 12.27 (knock) | 55.5 / 55.8 | 3.53e-08 | 0.07 | True |
| probe* | 0.010 | 0.38544 | 0.38561 | +0.004 | +0.004 | +0.018 | 0.0001 | 12.25 (knock) | 55.5 / 55.7 | 3.50e-08 | 0.67 | True |
| probe* | 0.020 | 0.38547 | 0.38566 | +0.008 | +0.009 | +0.018 | 0.0001 | 12.23 (knock) | 55.5 / 55.7 | 3.47e-08 | 1.36 | True |
| probe* | 0.050 | 0.38560 | 0.38580 | +0.020 | +0.023 | +0.020 | 0.0001 | 12.14 (knock) | 55.5 / 55.7 | 3.38e-08 | 3.50 | True |
| probe* | 0.100 | 0.38582 | 0.38605 | +0.042 | +0.048 | +0.023 | 0.0001 | 12.00 (knock) | 55.4 / 55.6 | 3.22e-08 | 7.39 | True |

### PRF97_normal - humid_evap

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38540 | 0.38557 | +0.000 | +0.000 | +0.017 | 0.0000 | 12.28 (knock) | 55.5 / 55.8 | 3.53e-08 | - | True |
| step | 0.001 | 0.38543 | 0.38560 | +0.004 | +0.004 | +0.017 | 0.0001 | 12.26 (knock) | 55.6 / 55.8 | 3.53e-08 | 0.07 | True |
| probe* | 0.010 | 0.38576 | 0.38593 | +0.037 | +0.037 | +0.017 | 0.0000 | 12.13 (knock) | 55.9 / 56.2 | 3.49e-08 | 0.67 | True |
| probe* | 0.020 | 0.38613 | 0.38630 | +0.074 | +0.073 | +0.017 | 0.0001 | 11.98 (knock) | 56.3 / 56.6 | 3.45e-08 | 1.36 | True |
| probe* | 0.050 | 0.38726 | 0.38743 | +0.187 | +0.186 | +0.017 | 0.0000 | 11.49 (knock) | 57.6 / 57.8 | 3.31e-08 | 3.50 | True |
| probe* | 0.100 | 0.38920 | 0.38935 | +0.380 | +0.378 | +0.015 | 0.0001 | 10.60 (knock) | 60.0 / 60.3 | 3.08e-08 | 7.39 | True |

## Track A humid-intake variant (water-majority cases, w = 0.5-0.8)

Grid still queued/running (results/track_b/trackA_humid_grid.json not yet written).

Saturation check done by hand (CH3OH, CR 20, 320 K, w = 0.6): with intake evaporative cooling the air saturates after ~5.4 % of the water (q ~ 12.6 g/kg, T_IVC 296 K); without cooling (vapour at 320 K) ~34 %. The remaining 66-95 % of water-majority water cannot be carried as vapour - it would condense on the runners/ports and arrive as liquid film or droplets. A water-majority charge therefore can NOT be a humid-air charge; Track A humid results are saturation-capped by construction.

## Track A references (existing water-majority work, best per fuel)

Source: results/03_engine_cycle/design_point.json (legacy) and results/03_engine_cycle/coupled_points.csv (PR 8 coupled).

| fuel | legacy best overall | legacy water-majority | legacy dry | coupled normal | coupled hot |
|---|---|---|---|---|---|
| CH3OH | CR 23, w 0.30, 320 K: 0.4543 | CR 24, w 0.60, 360 K: 0.4310 | CR 16: 0.4207 | wet 0.4543 (CR 23, w 0.3) vs dry 0.4207 | wet 0.4488 (CR 23, w 0.3); no eligible hot dry point |
| C2H5OH | CR 23, w 0.40: 0.4529 | w >= 0.5: 0.4378 | CR 24: 0.4455 | wet 0.4529 vs dry 0.4455 | wet 0.4493 (CR 23, w 0.4) vs dry 0.3837 (CR 11) |
| CH4 | CR 23, w 0.50: 0.4484 | CR 23, w 0.60: 0.4463 | CR 22: 0.4327 | not in coupled set | not in coupled set |

Note: Track A legacy points used the 2-CAD retard search; Track B dry baselines use the continuous spark optimiser, so Track B dry values differ slightly from Track A dry values (e.g. CH3OH dry 0.4238 vs 0.4207).

## Findings so far (hand-written; numbers from the tables above)

1. **Pre-stated 0.1-pp rule stops gasoline / E-blends / CH4 / ethanol-normal at step 1.** Each first step
   gains 2-8e-5 absolute (both engines agree to < 0.001 pp on the gain), below the 1e-4 threshold, so the
   Track B best stays w = 0 for those chains. The threshold was NOT changed after seeing data.
2. **But the gain is real and steady:** the labelled probes (not Track B steps) at the same hardware show a
   near-linear rise in both engines up to w = 10 %: PRF87 +0.53 pp, PRF91 +0.38, PRF97 +0.40, E10 +0.44,
   E85 +0.72 (normal) / +0.42 (hot), C2H5OH-normal +0.45, CH4 +0.22 (normal, MBT-limited) / +0.42 (hot).
   Mechanism (Module 03): knock relief lets CA50 advance towards MBT (e.g. E85 14.8 -> 11.7 deg); NO proxy
   falls 10-25 %; p_max rises 1-13 %. **Decision for James:** keep the per-step 0.01-pp rule (strict), or
   judge gains per 1-pp block (10 steps) / at the 3e-5 step-error level, which would let these chains walk on.
3. **Methanol (normal) and ethanol (hot) pass the rule** (~1.5e-4 and ~1.2e-4 per step, CRN gain positive
   each step) and are still stepping; MAX_STEPS = 100 caps them at w = 0.10.
4. **Humid intake (Track B):** per 0.1-pp step, fully-evaporated intake water (humid_evap) gives ~85-110 %
   of the liquid-mode gain (evaporative cooling -> denser, cooler charge, knock relief); water vapour already
   at intake temperature (humid_ambient, no cooling) gives only ~10 % (dilution + lower O2 partial pressure
   roughly cancel the small knock relief). So the benefit of humid air is cooling- and knock-limited - it
   only helps where spark is knock-limited and is re-optimised.
5. **Humid intake (Track A):** water-majority water cannot be carried as vapour. With intake evaporative
   cooling the charge saturates after ~5 % of the water (q ~ 12-13 g/kg dry air at 320 K intake); without
   cooling ~34 %. The rest would condense in the runners/ports (liquid film/droplets), i.e. it reverts to the
   liquid-injection case. See the Track A humid grid table for both engines.
6. **Hot regime:** PRF87/91/97, E10 and CH3OH have no eligible dry point (knock-limited CA50 > 15 deg even at
   CR 9), so there is no Track B hot chain for them; E85, C2H5OH and CH4 have hot chains.

## Literature check (humid intake)

* mail:/opt/knowledge/water-engine has **no intake-humidity entries** (grep "humid": none). Literature used:
  - Gasoline FAQ s7.12 / CRC data (refs [27,28,38] there): +1 g H2O/kg dry air lowers octane requirement by
    0.25-0.32 MON. One Track B gasoline step (w += 0.001) = q ~ 0.067 g/kg -> ~0.02 MON per step - consistent
    with the tiny per-step gains; w = 10 % (q ~ 7 g/kg) -> ~2 MON, consistent with the 0.4-0.5 pp probe gains.
  - ASTM D2699/D2700 hold CFR intake humidity at 3.6-7.2 g/kg because humidity shifts knock ratings.
  - SAE J1349 power correction uses dry-air pressure: vapour displaces O2 and lowers power/IMEP - the model
    captures this through fixed p_IVC (vapour replaces air).
  - Khatri et al., Int. J. Engine Res. 2021 (doi:10.1177/1468087420940854): knock suppression scales with
    total in-cylinder water (kappa effect), not relative humidity per se - supports comparing modes by w.
  - J. Eng. Gas Turbines Power 139(5) 051501 (SACI, 32 -> 60 % RH at fixed controls): CA50 retarded, BSFC
    288 -> 301 g/kWh, NOx down - humidity hurts efficiency when spark is NOT re-optimised; the benefit is
    knock-limited.
  - Library entries already in use: WE-14 Hoppe 2016 (water injection +3.3-3.8 % near min BSFC, up to +16 %
    at full knock-limited load), WE-20 Skippon (port vaporisation fraction), WE-21 Lauer (E85 film).

## What each track can borrow from the other

* **A -> B:** Track A shows water lets CR rise (alcohol optima at CR 23, w 0.3-0.4). Track B holds CR at the
  dry optimum; next Track B step: re-optimise CR at the best/probe w (hardware + water co-optimisation),
  and use Track A's w ~ 0.3 optimum as the expected far end of the methanol chain.
* **A -> B:** Track A's Module 09 film/retained-liquid coupling (PR 8) is the right model for any water above
  the intake saturation limit found here.
* **B -> A:** Track B's continuous spark optimiser gives better dry references (CH3OH 0.4238 vs Track A's
  0.4207 with the 2-CAD retard search) - quote Track A gains against these and port the optimiser.
* **B -> A:** humid-intake saturation (~5 % of water-majority water as vapour) means Track A water-majority
  cases must be treated as liquid/film delivery; humid intake only helps the first few % of water.
* **Both:** gasoline surrogates now exist in mechanisms/trackb_fuels.yaml for comparisons.

## Caveats

* Gasoline/E-blend knock uses the Douaud & Eyzat 1978 (SAE 780080) octane correlation; alcohol and CH4 knock
  uses Module 02 kinetic fits - different methodologies, compare across families with care. E85 octane
  (108.5) is extrapolated beyond the correlation range.
* Knock margin, CA50 limit and NO proxy are Module 03 only; M03-CRN has no knock/NOx model.
* Fixed p_IVC; no gas-exchange model, so volumetric-efficiency effects beyond charge density are not modelled.
* Liquid mode uses legacy Module 03 water handling (half evaporates in the intake); no Module 09 film profile
  for these points.
* Not yet peer-review verified (2+ independent engines pending).

