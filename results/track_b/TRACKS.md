# Water Engine - Track A / Track B status

Generated 2026-10-24 19:17 PDT by `python -m sims.track_b.report` (branch `track-b/incremental-water-20261024`). **NOT YET PEER-REVIEW VERIFIED** - Module 03 and M03-CRN are two in-repo engines from the same toolchain; independent engine review (2+ engine rule) still pending.

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

**Continuation rule history (kept honest):** the original rule, stated before any step ran, was a Module 03 gain > 1e-04 per step plus a positive M03-CRN gain. After seeing the first data (most chains stopped at step 1 with steady sub-threshold gains), **James decided on 2026-10-24 at 19:01 PDT** to continue while each step's gain beats the numerical noise level (about 3e-5). The value used is **3.3e-05 absolute**: the largest measured shift of a 0.5-CAD production-step efficiency in verification/x5_m03/RESULTS_FIX.md (X5 C2H5OH/best_overall, +0.0073 % of 0.45618). The pure 0.5 vs 0.25 CAD step-refinement difference is <= 6.1e-6, and the knock-limited spark bisection tolerance is ~2e-5. Both engines must still gain at every step. The maximum step is still 0.1 pp. The cap is still 100 steps (w = 0.10), raised to 200 only for chains still gaining at 100 (noted per chain). The original-rule results are kept as the recorded variant `rule_1e-4` (files without the `__noise` suffix).

Water modes: **liquid** = water in fuel / port liquid (legacy Module 03: half evaporates in the intake, rest in-cylinder); **humid_evap** = all water atomised and evaporated in the intake with latent cooling (wet-bulb limited; humid air, cooled charge); **humid_ambient** = water vapour already in the intake air at T_intake (no evaporative cooling; pure humidity/dilution effect). p_IVC is fixed, so evaporative cooling raises trapped mass (charge density) and vapour displaces O2 (lower O2 partial pressure) automatically. There is no gas-exchange model, so volumetric-efficiency effects beyond charge density are NOT modelled.

### Current rule (noise threshold 3.3e-5, James 19:01 PDT)

| fuel/regime | mode | dry eta M03 / CRN | best w | steps | d_eta M03 / CRN (pp) | CA50 dry -> best (limit) | knock margin at best | NO proxy change | p_max change | stop / status | rule_1e-4 variant best w (d_eta pp) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C2H5OH_hot | humid_ambient | 0.38970 / 0.38962 | 0.000 | 0 | +0.000 / +0.000 | 14.93 -> 14.93 (knock) | 0.0001 | +0.0 % | +0.0 % | M03 gain 8.60e-06 <= threshold 3.3e-05 | 0.000 (+0.000) |
| C2H5OH_hot | humid_evap | 0.38970 / 0.38962 | 0.052 | 52 | +0.577 / +0.570 | 14.93 -> 12.00 (knock) | 0.0000 | -4.5 % | +11.6 % | in progress (step 52; resumes from file) | 0.045 (+0.508) |
| C2H5OH_hot | liquid | 0.38970 / 0.38962 | 0.046 | 46 | +0.515 / +0.507 | 14.93 -> 12.11 (knock) | 0.0002 | -3.9 % | +9.8 % | in progress (step 46; resumes from file) | 0.040 (+0.456) |
| C2H5OH_normal | humid_ambient | 0.44576 / 0.44556 | 0.000 | 0 | +0.000 / +0.000 | 13.70 -> 13.70 (knock) | 0.0002 | +0.0 % | +0.0 % | M03 gain -1.82e-06 <= threshold 3.3e-05 | 0.000 (+0.000) |
| C2H5OH_normal | humid_evap | 0.44576 / 0.44556 | 0.008 | 8 | +0.063 / +0.062 | 13.70 -> 13.34 (knock) | 0.0007 | -0.9 % | +2.0 % | in progress (step 8; resumes from file) | 0.000 (+0.000) |
| C2H5OH_normal | liquid | 0.44576 / 0.44556 | 0.007 | 7 | +0.051 / +0.050 | 13.70 -> 13.35 (knock) | 0.0005 | -0.8 % | +1.7 % | in progress (step 7; resumes from file) | 0.000 (+0.000) |
| CH3OH_normal | humid_ambient | 0.42379 / 0.42380 | 0.000 | 0 | +0.000 / +0.000 | 14.57 -> 14.57 (knock) | 0.0006 | +0.0 % | +0.0 % | M03 gain 9.28e-06 <= threshold 3.3e-05 | 0.000 (+0.000) |
| CH3OH_normal | humid_evap | 0.42379 / 0.42380 | 0.057 | 57 | +0.730 / +0.720 | 14.57 -> 10.56 (knock) | 0.0007 | -9.6 % | +20.9 % | in progress (step 57; resumes from file) | 0.049 (+0.656) |
| CH3OH_normal | liquid | 0.42379 / 0.42380 | 0.048 | 48 | +0.608 / +0.599 | 14.57 -> 10.90 (knock) | 0.0008 | -8.0 % | +16.4 % | in progress (step 48; resumes from file) | 0.041 (+0.545) |
| CH4_hot | humid_ambient | 0.41178 / 0.41249 | 0.000 | 0 | +0.000 / +0.000 | 14.59 -> 14.59 (knock) | 0.0002 | +0.0 % | +0.0 % | M03 gain 3.46e-06 <= threshold 3.3e-05 | 0.000 (+0.000) |
| CH4_hot | humid_evap | 0.41178 / 0.41249 | 0.003 | 3 | +0.016 / +0.015 | 14.59 -> 14.52 (knock) | 0.0001 | -0.1 % | +0.3 % | in progress (step 3; resumes from file) | 0.000 (+0.000) |
| CH4_hot | liquid | 0.41178 / 0.41249 | 0.003 | 3 | +0.015 / +0.015 | 14.59 -> 14.51 (knock) | 0.0006 | -0.1 % | +0.3 % | in progress (step 3; resumes from file) | 0.000 (+0.000) |
| CH4_normal | humid_ambient | 0.43967 / 0.44017 | 0.000 | 0 | +0.000 / +0.000 | 12.40 -> 12.40 (MBT) | 0.6020 | +0.0 % | +0.0 % | M03 gain -3.44e-06 <= threshold 3.3e-05 | 0.000 (+0.000) |
| CH4_normal | humid_evap | 0.43967 / 0.44017 | 0.000 | 0 | +0.000 / +0.000 | 12.40 -> 12.40 (MBT) | 0.6020 | +0.0 % | +0.0 % | M03 gain 2.41e-05 <= threshold 3.3e-05 | 0.000 (+0.000) |
| CH4_normal | liquid | 0.43967 / 0.44017 | 0.000 | 0 | +0.000 / +0.000 | 12.40 -> 12.40 (MBT) | 0.6020 | +0.0 % | +0.0 % | M03 gain 1.92e-05 <= threshold 3.3e-05 | 0.000 (+0.000) |
| E10_normal | humid_ambient | 0.38472 / 0.38496 | 0.000 | 0 | +0.000 / +0.000 | 12.79 -> 12.79 (knock) | 0.0001 | +0.0 % | +0.0 % | M03 gain 4.56e-06 <= threshold 3.3e-05 | 0.000 (+0.000) |
| E10_normal | humid_evap | 0.38472 / 0.38496 | 0.003 | 3 | +0.012 / +0.012 | 12.79 -> 12.75 (knock) | 0.0000 | -0.4 % | +0.2 % | in progress (step 3; resumes from file) | 0.000 (+0.000) |
| E10_normal | liquid | 0.38472 / 0.38496 | 0.003 | 3 | +0.014 / +0.014 | 12.79 -> 12.73 (knock) | 0.0000 | -0.4 % | +0.2 % | in progress (step 3; resumes from file) | 0.000 (+0.000) |
| E85_hot | humid_ambient | 0.37777 / 0.37793 | 0.000 | 0 | +0.000 / +0.000 | 11.20 -> 11.20 (knock) | 0.0001 | +0.0 % | +0.0 % | M03 gain 3.65e-06 <= threshold 3.3e-05 | 0.000 (+0.000) |
| E85_hot | humid_evap | 0.37777 / 0.37793 | 0.003 | 3 | +0.014 / +0.014 | 11.20 -> 11.15 (knock) | 0.0001 | -0.5 % | +0.3 % | in progress (step 3; resumes from file) | 0.000 (+0.000) |
| E85_hot | liquid | 0.37777 / 0.37793 | 0.003 | 3 | +0.015 / +0.014 | 11.20 -> 11.12 (knock) | 0.0001 | -0.4 % | +0.3 % | in progress (step 3; resumes from file) | 0.000 (+0.000) |
| E85_normal | humid_ambient | 0.40536 / 0.40571 | 0.000 | 0 | +0.000 / +0.000 | 14.83 -> 14.83 (knock) | 0.0001 | +0.0 % | +0.0 % | M03 gain 5.97e-06 <= threshold 3.3e-05 | 0.000 (+0.000) |
| E85_normal | humid_evap | 0.40536 / 0.40571 | 0.003 | 3 | +0.019 / +0.019 | 14.83 -> 14.78 (knock) | 0.0001 | -0.7 % | +0.3 % | in progress (step 3; resumes from file) | 0.000 (+0.000) |
| E85_normal | liquid | | | | | | | | | queued under the new rule | 0.000 |
| PRF87_normal | humid_ambient | 0.37101 / 0.37137 | 0.000 | 0 | +0.000 / +0.000 | 14.66 -> 14.66 (knock) | 0.0001 | +0.0 % | +0.0 % | M03 gain 5.68e-06 <= threshold 3.3e-05 | 0.000 (+0.000) |
| PRF87_normal | humid_evap | | | | | | | | | queued under the new rule | 0.000 |
| PRF87_normal | liquid | | | | | | | | | queued under the new rule | 0.000 |
| PRF91_normal | humid_ambient | 0.37503 / 0.37519 | 0.000 | 0 | +0.000 / +0.000 | 11.81 -> 11.81 (knock) | 0.0000 | +0.0 % | +0.0 % | M03 gain 4.05e-06 <= threshold 3.3e-05 | 0.000 (+0.000) |
| PRF91_normal | humid_evap | | | | | | | | | queued under the new rule | 0.000 |
| PRF91_normal | liquid | | | | | | | | | queued under the new rule | 0.000 |
| PRF97_normal | humid_ambient | 0.38540 / 0.38557 | 0.000 | 0 | +0.000 / +0.000 | 12.28 -> 12.28 (knock) | 0.0000 | +0.0 % | +0.0 % | M03 gain 4.19e-06 <= threshold 3.3e-05 | 0.000 (+0.000) |
| PRF97_normal | humid_evap | | | | | | | | | queued under the new rule | 0.000 |
| PRF97_normal | liquid | | | | | | | | | queued under the new rule | 0.000 |

Knock margin (1 - knock integral), CA50 limit and NO proxy are Module 03 only. Efficiency and p_max are both engines.


*probe = exploratory point at w = 1/2/5/10 %, same hardware, spark re-optimised; NOT a Track B step.


#### C2H5OH_hot - humid_ambient (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38970 | 0.38962 | +0.000 | +0.000 | -0.008 | 0.0001 | 14.93 (knock) | 47.6 / 47.7 | 4.03e-08 | - | True |
| step | 0.001 | 0.38971 | 0.38963 | +0.001 | +0.001 | -0.008 | 0.0000 | 14.92 (knock) | 47.6 / 47.7 | 4.02e-08 | 0.11 | True |
| probe* | 0.010 | 0.38977 | 0.38970 | +0.007 | +0.008 | -0.007 | 0.0002 | 14.88 (knock) | 47.6 / 47.7 | 3.97e-08 | 1.13 | True |
| probe* | 0.020 | 0.38985 | 0.38978 | +0.015 | +0.016 | -0.006 | 0.0000 | 14.84 (knock) | 47.6 / 47.7 | 3.92e-08 | 2.28 | True |
| probe* | 0.050 | 0.39006 | 0.39001 | +0.035 | +0.039 | -0.004 | 0.0001 | 14.69 (knock) | 47.6 / 47.7 | 3.76e-08 | 5.89 | True |
| probe* | 0.100 | 0.39039 | 0.39038 | +0.068 | +0.075 | -0.001 | 0.0001 | 14.45 (knock) | 47.6 / 47.6 | 3.46e-08 | 12.42 | True |

#### C2H5OH_hot - humid_evap (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38970 | 0.38962 | +0.000 | +0.000 | -0.008 | 0.0001 | 14.93 (knock) | 47.6 / 47.7 | 4.03e-08 | - | True |
| step | 0.001 | 0.38983 | 0.38975 | +0.012 | +0.012 | -0.008 | 0.0000 | 14.87 (knock) | 47.7 / 47.8 | 4.02e-08 | 0.11 | True |
| step | 0.002 | 0.38994 | 0.38986 | +0.024 | +0.024 | -0.008 | 0.0003 | 14.82 (knock) | 47.8 / 47.8 | 4.02e-08 | 0.22 | True |
| step | 0.003 | 0.39007 | 0.38998 | +0.036 | +0.036 | -0.008 | 0.0002 | 14.77 (knock) | 47.9 / 47.9 | 4.01e-08 | 0.34 | True |
| step | 0.004 | 0.39019 | 0.39010 | +0.049 | +0.048 | -0.008 | 0.0002 | 14.72 (knock) | 48.0 / 48.0 | 4.01e-08 | 0.45 | True |
| step | 0.005 | 0.39031 | 0.39022 | +0.061 | +0.060 | -0.009 | 0.0002 | 14.67 (knock) | 48.1 / 48.1 | 4.01e-08 | 0.56 | True |
| step | 0.010 | 0.39091 | 0.39081 | +0.120 | +0.119 | -0.009 | 0.0003 | 14.40 (knock) | 48.6 / 48.6 | 3.99e-08 | 1.13 | True |
| step | 0.020 | 0.39207 | 0.39197 | +0.237 | +0.234 | -0.011 | 0.0002 | 13.86 (knock) | 49.6 / 49.6 | 3.95e-08 | 2.28 | True |
| step | 0.030 | 0.39320 | 0.39308 | +0.349 | +0.345 | -0.012 | 0.0002 | 13.30 (knock) | 50.7 / 50.7 | 3.92e-08 | 3.46 | True |
| step | 0.040 | 0.39427 | 0.39413 | +0.456 | +0.451 | -0.014 | 0.0003 | 12.72 (knock) | 51.8 / 51.8 | 3.88e-08 | 4.66 | True |
| step | 0.050 | 0.39528 | 0.39513 | +0.558 | +0.551 | -0.015 | 0.0001 | 12.12 (knock) | 52.9 / 53.0 | 3.85e-08 | 5.89 | True |
| step | 0.051 | 0.39538 | 0.39523 | +0.568 | +0.560 | -0.015 | 0.0001 | 12.06 (knock) | 53.0 / 53.1 | 3.85e-08 | 6.01 | True |
| step | 0.052 | 0.39548 | 0.39532 | +0.577 | +0.570 | -0.016 | 0.0000 | 12.00 (knock) | 53.2 / 53.2 | 3.84e-08 | 6.13 | True |
| probe* | 0.010 | 0.39091 | 0.39081 | +0.120 | +0.119 | -0.009 | 0.0003 | 14.40 (knock) | 48.6 / 48.6 | 3.99e-08 | 1.13 | True |
| probe* | 0.020 | 0.39207 | 0.39197 | +0.237 | +0.234 | -0.011 | 0.0002 | 13.86 (knock) | 49.6 / 49.6 | 3.95e-08 | 2.28 | True |
| probe* | 0.050 | 0.39528 | 0.39513 | +0.558 | +0.551 | -0.015 | 0.0001 | 12.12 (knock) | 52.9 / 53.0 | 3.85e-08 | 5.89 | True |
| probe* | 0.100 | 0.39911 | 0.39885 | +0.941 | +0.923 | -0.026 | 0.0001 | 8.78 (knock) | 59.6 / 59.7 | 3.69e-08 | 12.42 | True |

#### C2H5OH_hot - liquid (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38970 | 0.38962 | +0.000 | +0.000 | -0.008 | 0.0001 | 14.93 (knock) | 47.6 / 47.7 | 4.03e-08 | - | True |
| step | 0.001 | 0.38982 | 0.38974 | +0.012 | +0.012 | -0.008 | 0.0003 | 14.87 (knock) | 47.7 / 47.7 | 4.02e-08 | - | True |
| step | 0.002 | 0.38995 | 0.38987 | +0.025 | +0.025 | -0.008 | 0.0002 | 14.81 (knock) | 47.8 / 47.8 | 4.02e-08 | - | True |
| step | 0.003 | 0.39008 | 0.38999 | +0.037 | +0.037 | -0.008 | 0.0001 | 14.76 (knock) | 47.9 / 47.9 | 4.02e-08 | - | True |
| step | 0.004 | 0.39020 | 0.39012 | +0.050 | +0.049 | -0.009 | 0.0000 | 14.70 (knock) | 48.0 / 48.0 | 4.01e-08 | - | True |
| step | 0.005 | 0.39032 | 0.39023 | +0.062 | +0.061 | -0.009 | 0.0003 | 14.64 (knock) | 48.1 / 48.1 | 4.01e-08 | - | True |
| step | 0.010 | 0.39093 | 0.39083 | +0.122 | +0.121 | -0.009 | 0.0003 | 14.35 (knock) | 48.6 / 48.6 | 3.99e-08 | - | True |
| step | 0.020 | 0.39210 | 0.39199 | +0.240 | +0.237 | -0.011 | 0.0003 | 13.75 (knock) | 49.5 / 49.6 | 3.96e-08 | - | True |
| step | 0.030 | 0.39322 | 0.39309 | +0.352 | +0.347 | -0.013 | 0.0000 | 13.14 (knock) | 50.6 / 50.6 | 3.92e-08 | - | True |
| step | 0.040 | 0.39426 | 0.39412 | +0.456 | +0.450 | -0.014 | 0.0001 | 12.50 (knock) | 51.6 / 51.7 | 3.89e-08 | - | True |
| step | 0.044 | 0.39466 | 0.39451 | +0.496 | +0.489 | -0.015 | 0.0001 | 12.24 (knock) | 52.1 / 52.1 | 3.88e-08 | 2.57 | True |
| step | 0.045 | 0.39476 | 0.39460 | +0.505 | +0.498 | -0.015 | 0.0003 | 12.18 (knock) | 52.2 / 52.2 | 3.87e-08 | 2.63 | True |
| step | 0.046 | 0.39485 | 0.39470 | +0.515 | +0.507 | -0.016 | 0.0002 | 12.11 (knock) | 52.3 / 52.3 | 3.87e-08 | 2.70 | True |
| probe* | 0.010 | 0.39093 | 0.39083 | +0.122 | +0.121 | -0.009 | 0.0003 | 14.35 (knock) | 48.6 / 48.6 | 3.99e-08 | - | True |
| probe* | 0.020 | 0.39210 | 0.39199 | +0.240 | +0.237 | -0.011 | 0.0003 | 13.75 (knock) | 49.5 / 49.6 | 3.96e-08 | - | True |
| probe* | 0.050 | 0.39523 | 0.39507 | +0.553 | +0.544 | -0.016 | 0.0002 | 11.85 (knock) | 52.7 / 52.8 | 3.86e-08 | - | True |
| probe* | 0.100 | 0.39839 | 0.39810 | +0.869 | +0.848 | -0.029 | 0.0114 | 8.24 (MBT) | 59.0 / 59.1 | 3.70e-08 | - | True |

#### C2H5OH_normal - humid_ambient (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.44576 | 0.44556 | +0.000 | +0.000 | -0.020 | 0.0002 | 13.70 (knock) | 97.8 / 97.7 | 2.68e-08 | - | True |
| step | 0.001 | 0.44576 | 0.44556 | -0.000 | -0.000 | -0.020 | 0.0007 | 13.70 (knock) | 97.8 / 97.7 | 2.67e-08 | 0.11 | True |
| probe* | 0.010 | 0.44577 | 0.44557 | +0.000 | +0.000 | -0.020 | 0.0006 | 13.67 (knock) | 97.8 / 97.8 | 2.64e-08 | 1.13 | True |
| probe* | 0.020 | 0.44577 | 0.44557 | +0.001 | +0.001 | -0.020 | 0.0008 | 13.65 (knock) | 97.9 / 97.8 | 2.59e-08 | 2.28 | True |
| probe* | 0.050 | 0.44577 | 0.44557 | +0.001 | +0.000 | -0.021 | 0.0006 | 13.56 (knock) | 98.1 / 98.0 | 2.46e-08 | 5.89 | True |
| probe* | 0.100 | 0.44573 | 0.44552 | -0.003 | -0.004 | -0.021 | 0.0006 | 13.42 (knock) | 98.3 / 98.2 | 2.23e-08 | 12.42 | True |

#### C2H5OH_normal - humid_evap (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.44576 | 0.44556 | +0.000 | +0.000 | -0.020 | 0.0002 | 13.70 (knock) | 97.8 / 97.7 | 2.68e-08 | - | True |
| step | 0.001 | 0.44584 | 0.44564 | +0.008 | +0.008 | -0.020 | 0.0004 | 13.66 (knock) | 98.0 / 97.9 | 2.67e-08 | 0.11 | True |
| step | 0.002 | 0.44592 | 0.44572 | +0.016 | +0.016 | -0.021 | 0.0005 | 13.61 (knock) | 98.3 / 98.2 | 2.67e-08 | 0.22 | True |
| step | 0.003 | 0.44600 | 0.44580 | +0.024 | +0.024 | -0.021 | 0.0006 | 13.57 (knock) | 98.5 / 98.4 | 2.67e-08 | 0.34 | True |
| step | 0.004 | 0.44608 | 0.44588 | +0.032 | +0.031 | -0.021 | 0.0008 | 13.52 (knock) | 98.8 / 98.7 | 2.67e-08 | 0.45 | True |
| step | 0.005 | 0.44616 | 0.44596 | +0.040 | +0.039 | -0.021 | 0.0001 | 13.47 (knock) | 99.0 / 98.9 | 2.66e-08 | 0.56 | True |
| step | 0.006 | 0.44624 | 0.44603 | +0.048 | +0.047 | -0.021 | 0.0003 | 13.43 (knock) | 99.3 / 99.2 | 2.66e-08 | 0.67 | True |
| step | 0.007 | 0.44632 | 0.44611 | +0.055 | +0.054 | -0.021 | 0.0005 | 13.39 (knock) | 99.5 / 99.4 | 2.66e-08 | 0.79 | True |
| step | 0.008 | 0.44639 | 0.44618 | +0.063 | +0.062 | -0.021 | 0.0007 | 13.34 (knock) | 99.8 / 99.7 | 2.65e-08 | 0.90 | True |
| probe* | 0.010 | 0.44654 | 0.44633 | +0.078 | +0.077 | -0.022 | 0.0003 | 13.25 (knock) | 100.3 / 100.2 | 2.65e-08 | 1.13 | True |
| probe* | 0.020 | 0.44725 | 0.44702 | +0.148 | +0.146 | -0.023 | 0.0002 | 12.78 (knock) | 102.9 / 102.8 | 2.62e-08 | 2.28 | True |
| probe* | 0.050 | 0.44884 | 0.44858 | +0.307 | +0.302 | -0.026 | 0.0738 | 11.75 (MBT) | 109.3 / 109.2 | 2.49e-08 | 5.89 | True |
| probe* | 0.100 | 0.45128 | 0.45101 | +0.552 | +0.544 | -0.028 | 0.4222 | 11.67 (MBT) | 112.7 / 112.6 | 2.05e-08 | 12.42 | True |

#### C2H5OH_normal - liquid (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.44576 | 0.44556 | +0.000 | +0.000 | -0.020 | 0.0002 | 13.70 (knock) | 97.8 / 97.7 | 2.68e-08 | - | True |
| step | 0.001 | 0.44584 | 0.44564 | +0.008 | +0.007 | -0.020 | 0.0004 | 13.65 (knock) | 98.0 / 97.9 | 2.67e-08 | - | True |
| step | 0.002 | 0.44592 | 0.44571 | +0.015 | +0.015 | -0.021 | 0.0005 | 13.60 (knock) | 98.3 / 98.2 | 2.67e-08 | 0.11 | True |
| step | 0.003 | 0.44599 | 0.44578 | +0.022 | +0.022 | -0.021 | 0.0006 | 13.55 (knock) | 98.5 / 98.4 | 2.67e-08 | 0.17 | True |
| step | 0.004 | 0.44606 | 0.44585 | +0.030 | +0.029 | -0.021 | 0.0008 | 13.50 (knock) | 98.7 / 98.6 | 2.67e-08 | 0.22 | True |
| step | 0.005 | 0.44614 | 0.44593 | +0.037 | +0.037 | -0.021 | 0.0001 | 13.45 (knock) | 99.0 / 98.9 | 2.66e-08 | 0.28 | True |
| step | 0.006 | 0.44621 | 0.44600 | +0.044 | +0.044 | -0.021 | 0.0003 | 13.40 (knock) | 99.2 / 99.1 | 2.66e-08 | 0.34 | True |
| step | 0.007 | 0.44628 | 0.44607 | +0.051 | +0.050 | -0.021 | 0.0005 | 13.35 (knock) | 99.5 / 99.4 | 2.66e-08 | 0.39 | True |
| probe* | 0.010 | 0.44649 | 0.44627 | +0.072 | +0.071 | -0.022 | 0.0004 | 13.20 (knock) | 100.2 / 100.1 | 2.65e-08 | - | True |
| probe* | 0.020 | 0.44710 | 0.44687 | +0.134 | +0.131 | -0.023 | 0.0002 | 12.69 (knock) | 102.7 / 102.6 | 2.62e-08 | - | True |
| probe* | 0.050 | 0.44835 | 0.44809 | +0.258 | +0.253 | -0.026 | 0.1201 | 11.80 (MBT) | 107.4 / 107.3 | 2.46e-08 | - | True |
| probe* | 0.100 | 0.45024 | 0.44997 | +0.448 | +0.440 | -0.028 | 0.4786 | 11.72 (MBT) | 108.8 / 108.7 | 1.99e-08 | - | True |

#### CH3OH_normal - humid_ambient (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.42379 | 0.42380 | +0.000 | +0.000 | +0.001 | 0.0006 | 14.57 (knock) | 71.8 / 71.8 | 1.66e-08 | - | True |
| step | 0.001 | 0.42380 | 0.42380 | +0.001 | +0.001 | +0.001 | 0.0008 | 14.57 (knock) | 71.8 / 71.8 | 1.65e-08 | 0.16 | True |
| probe* | 0.010 | 0.42390 | 0.42390 | +0.011 | +0.011 | +0.001 | 0.0005 | 14.51 (knock) | 71.9 / 71.9 | 1.61e-08 | 1.57 | True |
| probe* | 0.020 | 0.42400 | 0.42400 | +0.021 | +0.021 | +0.000 | 0.0007 | 14.46 (knock) | 72.0 / 71.9 | 1.57e-08 | 3.17 | True |
| probe* | 0.050 | 0.42432 | 0.42431 | +0.053 | +0.051 | -0.001 | 0.0002 | 14.27 (knock) | 72.2 / 72.1 | 1.43e-08 | 8.19 | True |
| probe* | 0.100 | 0.42480 | 0.42477 | +0.101 | +0.098 | -0.003 | 0.0001 | 13.96 (knock) | 72.4 / 72.4 | 1.20e-08 | 17.28 | True |

#### CH3OH_normal - humid_evap (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.42379 | 0.42380 | +0.000 | +0.000 | +0.001 | 0.0006 | 14.57 (knock) | 71.8 / 71.8 | 1.66e-08 | - | True |
| step | 0.001 | 0.42395 | 0.42395 | +0.016 | +0.016 | +0.001 | 0.0007 | 14.51 (knock) | 72.1 / 72.0 | 1.66e-08 | 0.16 | True |
| step | 0.002 | 0.42411 | 0.42411 | +0.032 | +0.031 | +0.000 | 0.0008 | 14.45 (knock) | 72.3 / 72.3 | 1.65e-08 | 0.31 | True |
| step | 0.003 | 0.42427 | 0.42427 | +0.048 | +0.048 | +0.000 | 0.0001 | 14.38 (knock) | 72.5 / 72.5 | 1.65e-08 | 0.47 | True |
| step | 0.004 | 0.42443 | 0.42443 | +0.064 | +0.063 | +0.000 | 0.0004 | 14.31 (knock) | 72.8 / 72.7 | 1.65e-08 | 0.62 | True |
| step | 0.005 | 0.42458 | 0.42458 | +0.079 | +0.078 | -0.000 | 0.0006 | 14.25 (knock) | 73.0 / 73.0 | 1.65e-08 | 0.78 | True |
| step | 0.010 | 0.42535 | 0.42534 | +0.157 | +0.155 | -0.001 | 0.0003 | 13.92 (knock) | 74.2 / 74.1 | 1.63e-08 | 1.57 | True |
| step | 0.020 | 0.42681 | 0.42679 | +0.303 | +0.299 | -0.003 | 0.0005 | 13.25 (knock) | 76.6 / 76.6 | 1.60e-08 | 3.17 | True |
| step | 0.030 | 0.42816 | 0.42812 | +0.438 | +0.432 | -0.004 | 0.0004 | 12.56 (knock) | 79.2 / 79.1 | 1.57e-08 | 4.81 | True |
| step | 0.040 | 0.42938 | 0.42932 | +0.559 | +0.552 | -0.006 | 0.0006 | 11.84 (knock) | 81.9 / 81.9 | 1.54e-08 | 6.48 | True |
| step | 0.050 | 0.43045 | 0.43037 | +0.666 | +0.657 | -0.008 | 0.0005 | 11.09 (knock) | 84.8 / 84.7 | 1.52e-08 | 8.19 | True |
| step | 0.055 | 0.43092 | 0.43083 | +0.713 | +0.703 | -0.009 | 0.0003 | 10.71 (knock) | 86.3 / 86.2 | 1.51e-08 | 9.05 | True |
| step | 0.056 | 0.43100 | 0.43091 | +0.722 | +0.712 | -0.009 | 0.0001 | 10.63 (knock) | 86.6 / 86.6 | 1.50e-08 | 9.23 | True |
| step | 0.057 | 0.43109 | 0.43100 | +0.730 | +0.720 | -0.009 | 0.0007 | 10.56 (knock) | 86.9 / 86.9 | 1.50e-08 | 9.40 | True |
| probe* | 0.010 | 0.42535 | 0.42534 | +0.157 | +0.155 | -0.001 | 0.0003 | 13.92 (knock) | 74.2 / 74.1 | 1.63e-08 | 1.57 | True |
| probe* | 0.020 | 0.42681 | 0.42679 | +0.303 | +0.299 | -0.003 | 0.0005 | 13.25 (knock) | 76.6 / 76.6 | 1.60e-08 | 3.17 | True |
| probe* | 0.050 | 0.43045 | 0.43037 | +0.666 | +0.657 | -0.008 | 0.0005 | 11.09 (knock) | 84.8 / 84.7 | 1.52e-08 | 8.19 | True |
| probe* | 0.100 | 0.43327 | - | +0.948 | - | - | 0.4173 | 9.63 (MBT) | 90.5 / 0.0 | 1.13e-08 | 12.59 | None |

#### CH3OH_normal - liquid (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.42379 | 0.42380 | +0.000 | +0.000 | +0.001 | 0.0006 | 14.57 (knock) | 71.8 / 71.8 | 1.66e-08 | - | True |
| step | 0.001 | 0.42395 | 0.42396 | +0.017 | +0.016 | +0.001 | 0.0001 | 14.50 (knock) | 72.1 / 72.0 | 1.66e-08 | - | True |
| step | 0.002 | 0.42411 | 0.42411 | +0.032 | +0.032 | +0.000 | 0.0005 | 14.43 (knock) | 72.3 / 72.2 | 1.65e-08 | - | True |
| step | 0.003 | 0.42427 | 0.42427 | +0.048 | +0.047 | +0.000 | 0.0009 | 14.36 (knock) | 72.5 / 72.5 | 1.65e-08 | - | True |
| step | 0.004 | 0.42443 | 0.42443 | +0.064 | +0.063 | +0.000 | 0.0004 | 14.29 (knock) | 72.7 / 72.7 | 1.65e-08 | - | True |
| step | 0.005 | 0.42459 | 0.42458 | +0.080 | +0.079 | -0.000 | 0.0001 | 14.22 (knock) | 72.9 / 72.9 | 1.65e-08 | - | True |
| step | 0.010 | 0.42535 | 0.42534 | +0.156 | +0.154 | -0.001 | 0.0004 | 13.86 (knock) | 74.1 / 74.0 | 1.63e-08 | - | True |
| step | 0.020 | 0.42677 | 0.42674 | +0.298 | +0.295 | -0.003 | 0.0003 | 13.12 (knock) | 76.4 / 76.4 | 1.60e-08 | - | True |
| step | 0.030 | 0.42804 | 0.42799 | +0.426 | +0.420 | -0.005 | 0.0003 | 12.35 (knock) | 78.9 / 78.8 | 1.57e-08 | - | True |
| step | 0.040 | 0.42914 | 0.42907 | +0.535 | +0.527 | -0.007 | 0.0008 | 11.56 (knock) | 81.4 / 81.4 | 1.55e-08 | - | True |
| step | 0.046 | 0.42970 | 0.42962 | +0.592 | +0.583 | -0.008 | 0.0002 | 11.07 (knock) | 83.1 / 83.0 | 1.53e-08 | 3.75 | True |
| step | 0.047 | 0.42979 | 0.42971 | +0.600 | +0.591 | -0.008 | 0.0000 | 10.98 (knock) | 83.3 / 83.3 | 1.53e-08 | 3.84 | True |
| step | 0.048 | 0.42987 | 0.42979 | +0.608 | +0.599 | -0.009 | 0.0008 | 10.90 (knock) | 83.6 / 83.6 | 1.53e-08 | 3.92 | True |
| probe* | 0.010 | 0.42535 | 0.42534 | +0.156 | +0.154 | -0.001 | 0.0004 | 13.86 (knock) | 74.1 / 74.0 | 1.63e-08 | - | True |
| probe* | 0.020 | 0.42677 | 0.42674 | +0.298 | +0.295 | -0.003 | 0.0003 | 13.12 (knock) | 76.4 / 76.4 | 1.60e-08 | - | True |
| probe* | 0.050 | 0.43003 | 0.42994 | +0.625 | +0.615 | -0.009 | 0.0007 | 10.74 (knock) | 84.2 / 84.1 | 1.52e-08 | - | True |
| probe* | 0.100 | 0.43270 | 0.43257 | +0.891 | +0.877 | -0.013 | 0.4609 | 9.71 (MBT) | 88.5 / 88.4 | 1.10e-08 | - | True |

#### CH4_hot - humid_ambient (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.41178 | 0.41249 | +0.000 | +0.000 | +0.071 | 0.0002 | 14.59 (knock) | 65.2 / 65.2 | 4.24e-08 | - | True |
| step | 0.001 | 0.41179 | 0.41249 | +0.000 | +0.000 | +0.071 | 0.0001 | 14.59 (knock) | 65.2 / 65.2 | 4.24e-08 | 0.06 | True |
| probe* | 0.010 | 0.41181 | 0.41252 | +0.003 | +0.003 | +0.071 | 0.0000 | 14.55 (knock) | 65.3 / 65.3 | 4.23e-08 | 0.59 | True |
| probe* | 0.020 | 0.41183 | 0.41255 | +0.005 | +0.006 | +0.071 | 0.0004 | 14.51 (knock) | 65.4 / 65.4 | 4.21e-08 | 1.19 | True |
| probe* | 0.050 | 0.41191 | 0.41263 | +0.013 | +0.014 | +0.072 | 0.0005 | 14.39 (knock) | 65.6 / 65.6 | 4.16e-08 | 3.07 | True |
| probe* | 0.100 | 0.41205 | 0.41277 | +0.026 | +0.029 | +0.073 | 0.0007 | 14.17 (knock) | 66.0 / 66.0 | 4.08e-08 | 6.49 | True |

#### CH4_hot - humid_evap (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.41178 | 0.41249 | +0.000 | +0.000 | +0.071 | 0.0002 | 14.59 (knock) | 65.2 / 65.2 | 4.24e-08 | - | True |
| step | 0.001 | 0.41183 | 0.41254 | +0.005 | +0.005 | +0.070 | 0.0004 | 14.57 (knock) | 65.3 / 65.3 | 4.24e-08 | 0.06 | True |
| step | 0.002 | 0.41188 | 0.41259 | +0.010 | +0.010 | +0.070 | 0.0006 | 14.55 (knock) | 65.4 / 65.4 | 4.24e-08 | 0.12 | True |
| step | 0.003 | 0.41194 | 0.41264 | +0.016 | +0.015 | +0.070 | 0.0001 | 14.52 (knock) | 65.5 / 65.5 | 4.24e-08 | 0.18 | True |
| probe* | 0.010 | 0.41230 | 0.41299 | +0.051 | +0.050 | +0.069 | 0.0004 | 14.35 (knock) | 66.0 / 66.0 | 4.22e-08 | 0.59 | True |
| probe* | 0.020 | 0.41280 | 0.41348 | +0.102 | +0.100 | +0.068 | 0.0006 | 14.10 (knock) | 66.8 / 66.8 | 4.21e-08 | 1.19 | True |
| probe* | 0.050 | 0.41425 | 0.41489 | +0.247 | +0.240 | +0.064 | 0.0003 | 13.31 (knock) | 69.2 / 69.2 | 4.16e-08 | 3.07 | True |
| probe* | 0.100 | 0.41632 | 0.41689 | +0.454 | +0.440 | +0.057 | 0.0005 | 11.89 (knock) | 73.8 / 73.8 | 4.08e-08 | 6.49 | True |

#### CH4_hot - liquid (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.41178 | 0.41249 | +0.000 | +0.000 | +0.071 | 0.0002 | 14.59 (knock) | 65.2 / 65.2 | 4.24e-08 | - | True |
| step | 0.001 | 0.41184 | 0.41254 | +0.005 | +0.005 | +0.070 | 0.0001 | 14.56 (knock) | 65.3 / 65.3 | 4.24e-08 | - | True |
| step | 0.002 | 0.41188 | 0.41258 | +0.010 | +0.010 | +0.070 | 0.0007 | 14.54 (knock) | 65.4 / 65.4 | 4.24e-08 | 0.06 | True |
| step | 0.003 | 0.41193 | 0.41264 | +0.015 | +0.015 | +0.070 | 0.0006 | 14.51 (knock) | 65.4 / 65.5 | 4.24e-08 | 0.09 | True |
| probe* | 0.010 | 0.41229 | 0.41298 | +0.051 | +0.050 | +0.069 | 0.0001 | 14.32 (knock) | 66.0 / 66.0 | 4.23e-08 | - | True |
| probe* | 0.020 | 0.41278 | 0.41346 | +0.100 | +0.097 | +0.068 | 0.0000 | 14.04 (knock) | 66.7 / 66.7 | 4.21e-08 | - | True |
| probe* | 0.050 | 0.41415 | 0.41478 | +0.236 | +0.229 | +0.063 | 0.0003 | 13.18 (knock) | 69.1 / 69.1 | 4.17e-08 | - | True |
| probe* | 0.100 | 0.41594 | 0.41648 | +0.415 | +0.399 | +0.055 | 0.0003 | 11.60 (knock) | 73.5 / 73.6 | 4.09e-08 | - | True |

#### CH4_normal - humid_ambient (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.43967 | 0.44017 | +0.000 | +0.000 | +0.050 | 0.6020 | 12.40 (MBT) | 105.7 / 105.7 | 3.07e-08 | - | True |
| step | 0.001 | 0.43967 | 0.44017 | -0.000 | -0.000 | +0.050 | 0.6023 | 12.40 (MBT) | 105.7 / 105.7 | 3.07e-08 | 0.06 | True |
| probe* | 0.010 | 0.43964 | 0.44014 | -0.003 | -0.003 | +0.050 | 0.6068 | 12.43 (MBT) | 105.5 / 105.5 | 3.05e-08 | 0.59 | True |
| probe* | 0.020 | 0.43960 | 0.44011 | -0.007 | -0.007 | +0.051 | 0.6093 | 12.43 (MBT) | 105.5 / 105.5 | 3.03e-08 | 1.19 | True |
| probe* | 0.050 | 0.43950 | 0.44001 | -0.017 | -0.016 | +0.051 | 0.6168 | 12.43 (MBT) | 105.4 / 105.4 | 2.97e-08 | 3.07 | True |
| probe* | 0.100 | 0.43935 | 0.43985 | -0.032 | -0.032 | +0.051 | 0.6297 | 12.43 (MBT) | 105.2 / 105.2 | 2.87e-08 | 6.49 | True |

#### CH4_normal - humid_evap (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.43967 | 0.44017 | +0.000 | +0.000 | +0.050 | 0.6020 | 12.40 (MBT) | 105.7 / 105.7 | 3.07e-08 | - | True |
| step | 0.001 | 0.43969 | 0.44020 | +0.002 | +0.002 | +0.050 | 0.6038 | 12.40 (MBT) | 105.7 / 105.7 | 3.06e-08 | 0.06 | True |
| probe* | 0.010 | 0.43991 | 0.44042 | +0.024 | +0.024 | +0.050 | 0.6195 | 12.40 (MBT) | 106.0 / 106.0 | 3.04e-08 | 0.59 | True |
| probe* | 0.020 | 0.44016 | 0.44067 | +0.049 | +0.049 | +0.050 | 0.6366 | 12.40 (MBT) | 106.2 / 106.2 | 3.00e-08 | 1.19 | True |
| probe* | 0.050 | 0.44096 | 0.44145 | +0.129 | +0.128 | +0.050 | 0.6845 | 12.38 (MBT) | 107.2 / 107.2 | 2.90e-08 | 3.07 | True |
| probe* | 0.100 | 0.44242 | 0.44290 | +0.275 | +0.273 | +0.048 | 0.7568 | 12.35 (MBT) | 108.8 / 108.8 | 2.72e-08 | 6.49 | True |

#### CH4_normal - liquid (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.43967 | 0.44017 | +0.000 | +0.000 | +0.050 | 0.6020 | 12.40 (MBT) | 105.7 / 105.7 | 3.07e-08 | - | True |
| step | 0.001 | 0.43969 | 0.44019 | +0.002 | +0.002 | +0.050 | 0.6040 | 12.40 (MBT) | 105.7 / 105.7 | 3.06e-08 | - | True |
| probe* | 0.010 | 0.43986 | 0.44037 | +0.019 | +0.019 | +0.050 | 0.6213 | 12.40 (MBT) | 105.8 / 105.8 | 3.03e-08 | - | True |
| probe* | 0.020 | 0.44006 | 0.44056 | +0.039 | +0.039 | +0.050 | 0.6401 | 12.40 (MBT) | 105.9 / 105.9 | 3.00e-08 | - | True |
| probe* | 0.050 | 0.44070 | 0.44119 | +0.103 | +0.102 | +0.049 | 0.6935 | 12.40 (MBT) | 106.2 / 106.2 | 2.89e-08 | - | True |
| probe* | 0.100 | 0.44187 | 0.44235 | +0.220 | +0.218 | +0.048 | 0.7712 | 12.38 (MBT) | 106.8 / 106.8 | 2.70e-08 | - | True |

#### E10_normal - humid_ambient (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38472 | 0.38496 | +0.000 | +0.000 | +0.023 | 0.0001 | 12.79 (knock) | 54.6 / 54.9 | 3.38e-08 | - | True |
| step | 0.001 | 0.38473 | 0.38496 | +0.000 | +0.001 | +0.023 | 0.0001 | 12.79 (knock) | 54.6 / 54.9 | 3.38e-08 | 0.07 | True |
| probe* | 0.010 | 0.38477 | 0.38501 | +0.005 | +0.005 | +0.024 | 0.0000 | 12.77 (knock) | 54.6 / 54.8 | 3.35e-08 | 0.70 | True |
| probe* | 0.020 | 0.38481 | 0.38505 | +0.009 | +0.010 | +0.024 | 0.0001 | 12.74 (knock) | 54.6 / 54.8 | 3.32e-08 | 1.42 | True |
| probe* | 0.050 | 0.38495 | 0.38521 | +0.023 | +0.025 | +0.026 | 0.0000 | 12.66 (knock) | 54.6 / 54.8 | 3.22e-08 | 3.67 | True |
| probe* | 0.100 | 0.38519 | 0.38547 | +0.047 | +0.052 | +0.028 | 0.0001 | 12.51 (knock) | 54.5 / 54.7 | 3.05e-08 | 7.75 | True |

#### E10_normal - humid_evap (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38472 | 0.38496 | +0.000 | +0.000 | +0.023 | 0.0001 | 12.79 (knock) | 54.6 / 54.9 | 3.38e-08 | - | True |
| step | 0.001 | 0.38476 | 0.38500 | +0.004 | +0.004 | +0.023 | 0.0000 | 12.78 (knock) | 54.7 / 54.9 | 3.37e-08 | 0.07 | True |
| step | 0.002 | 0.38480 | 0.38503 | +0.008 | +0.008 | +0.023 | 0.0001 | 12.76 (knock) | 54.7 / 54.9 | 3.37e-08 | 0.14 | True |
| step | 0.003 | 0.38484 | 0.38508 | +0.012 | +0.012 | +0.023 | 0.0000 | 12.75 (knock) | 54.8 / 55.0 | 3.37e-08 | 0.21 | True |
| probe* | 0.010 | 0.38512 | 0.38535 | +0.040 | +0.040 | +0.023 | 0.0001 | 12.64 (knock) | 55.0 / 55.3 | 3.33e-08 | 0.70 | True |
| probe* | 0.020 | 0.38553 | 0.38576 | +0.081 | +0.080 | +0.023 | 0.0000 | 12.48 (knock) | 55.4 / 55.7 | 3.29e-08 | 1.42 | True |
| probe* | 0.050 | 0.38676 | 0.38698 | +0.204 | +0.203 | +0.023 | 0.0000 | 11.98 (knock) | 56.8 / 57.0 | 3.15e-08 | 3.67 | True |
| probe* | 0.100 | 0.38888 | 0.38909 | +0.416 | +0.413 | +0.021 | 0.0001 | 11.05 (knock) | 59.3 / 59.5 | 2.90e-08 | 7.75 | True |

#### E10_normal - liquid (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38472 | 0.38496 | +0.000 | +0.000 | +0.023 | 0.0001 | 12.79 (knock) | 54.6 / 54.9 | 3.38e-08 | - | True |
| step | 0.001 | 0.38477 | 0.38500 | +0.004 | +0.004 | +0.023 | 0.0001 | 12.77 (knock) | 54.7 / 54.9 | 3.37e-08 | - | True |
| step | 0.002 | 0.38481 | 0.38504 | +0.009 | +0.009 | +0.023 | 0.0002 | 12.75 (knock) | 54.7 / 54.9 | 3.37e-08 | 0.07 | True |
| step | 0.003 | 0.38486 | 0.38509 | +0.014 | +0.014 | +0.023 | 0.0000 | 12.73 (knock) | 54.8 / 55.0 | 3.37e-08 | 0.10 | True |
| probe* | 0.010 | 0.38518 | 0.38540 | +0.045 | +0.045 | +0.023 | 0.0001 | 12.57 (knock) | 55.0 / 55.3 | 3.34e-08 | - | True |
| probe* | 0.020 | 0.38563 | 0.38585 | +0.091 | +0.089 | +0.022 | 0.0001 | 12.33 (knock) | 55.5 / 55.7 | 3.30e-08 | - | True |
| probe* | 0.050 | 0.38698 | 0.38718 | +0.226 | +0.222 | +0.020 | 0.0000 | 11.58 (knock) | 56.8 / 57.1 | 3.17e-08 | - | True |
| probe* | 0.100 | 0.38913 | 0.38929 | +0.441 | +0.433 | +0.016 | 0.0001 | 10.18 (knock) | 59.5 / 59.7 | 2.94e-08 | - | True |

#### E85_hot - humid_ambient (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37777 | 0.37793 | +0.000 | +0.000 | +0.016 | 0.0001 | 11.20 (knock) | 46.6 / 46.8 | 3.88e-08 | - | True |
| step | 0.001 | 0.37777 | 0.37793 | +0.000 | +0.000 | +0.016 | 0.0001 | 11.20 (knock) | 46.6 / 46.8 | 3.88e-08 | 0.10 | True |
| probe* | 0.010 | 0.37781 | 0.37798 | +0.004 | +0.005 | +0.016 | 0.0001 | 11.17 (knock) | 46.5 / 46.8 | 3.84e-08 | 1.04 | True |
| probe* | 0.020 | 0.37786 | 0.37803 | +0.009 | +0.011 | +0.017 | 0.0001 | 11.13 (knock) | 46.5 / 46.7 | 3.80e-08 | 2.09 | True |
| probe* | 0.050 | 0.37800 | 0.37819 | +0.023 | +0.027 | +0.020 | 0.0001 | 11.02 (knock) | 46.5 / 46.7 | 3.67e-08 | 5.39 | True |
| probe* | 0.100 | 0.37823 | 0.37847 | +0.046 | +0.055 | +0.024 | 0.0001 | 10.81 (knock) | 46.4 / 46.6 | 3.43e-08 | 11.39 | True |

#### E85_hot - humid_evap (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37777 | 0.37793 | +0.000 | +0.000 | +0.016 | 0.0001 | 11.20 (knock) | 46.6 / 46.8 | 3.88e-08 | - | True |
| step | 0.001 | 0.37781 | 0.37797 | +0.005 | +0.005 | +0.016 | 0.0001 | 11.19 (knock) | 46.6 / 46.8 | 3.87e-08 | 0.10 | True |
| step | 0.002 | 0.37786 | 0.37802 | +0.009 | +0.009 | +0.016 | 0.0001 | 11.17 (knock) | 46.6 / 46.9 | 3.87e-08 | 0.21 | True |
| step | 0.003 | 0.37790 | 0.37806 | +0.014 | +0.014 | +0.016 | 0.0001 | 11.15 (knock) | 46.7 / 46.9 | 3.86e-08 | 0.31 | True |
| probe* | 0.010 | 0.37822 | 0.37838 | +0.045 | +0.045 | +0.016 | 0.0000 | 11.01 (knock) | 47.0 / 47.2 | 3.82e-08 | 1.04 | True |
| probe* | 0.020 | 0.37867 | 0.37883 | +0.090 | +0.091 | +0.016 | 0.0001 | 10.81 (knock) | 47.4 / 47.6 | 3.76e-08 | 2.09 | True |
| probe* | 0.050 | 0.38004 | 0.38020 | +0.227 | +0.227 | +0.016 | 0.0000 | 10.18 (knock) | 48.7 / 48.9 | 3.57e-08 | 5.39 | True |
| probe* | 0.100 | 0.38231 | 0.38245 | +0.454 | +0.453 | +0.015 | 0.0001 | 9.00 (knock) | 51.2 / 51.4 | 3.22e-08 | 11.39 | True |

#### E85_hot - liquid (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37777 | 0.37793 | +0.000 | +0.000 | +0.016 | 0.0001 | 11.20 (knock) | 46.6 / 46.8 | 3.88e-08 | - | True |
| step | 0.001 | 0.37782 | 0.37797 | +0.005 | +0.005 | +0.016 | 0.0000 | 11.17 (knock) | 46.6 / 46.8 | 3.87e-08 | - | True |
| step | 0.002 | 0.37787 | 0.37802 | +0.010 | +0.010 | +0.015 | 0.0001 | 11.15 (knock) | 46.6 / 46.9 | 3.87e-08 | 0.10 | True |
| step | 0.003 | 0.37792 | 0.37807 | +0.015 | +0.014 | +0.015 | 0.0001 | 11.12 (knock) | 46.7 / 46.9 | 3.86e-08 | 0.15 | True |
| probe* | 0.010 | 0.37826 | 0.37840 | +0.049 | +0.048 | +0.015 | 0.0000 | 10.91 (knock) | 47.0 / 47.2 | 3.83e-08 | - | True |
| probe* | 0.020 | 0.37873 | 0.37887 | +0.096 | +0.095 | +0.014 | 0.0001 | 10.60 (knock) | 47.4 / 47.6 | 3.77e-08 | - | True |
| probe* | 0.050 | 0.38009 | 0.38020 | +0.232 | +0.228 | +0.011 | 0.0001 | 9.63 (knock) | 48.8 / 49.1 | 3.60e-08 | - | True |
| probe* | 0.100 | 0.38200 | 0.38205 | +0.423 | +0.412 | +0.005 | 0.0001 | 7.77 (knock) | 51.6 / 51.8 | 3.29e-08 | - | True |

#### E85_normal - humid_ambient (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.40536 | 0.40571 | +0.000 | +0.000 | +0.035 | 0.0001 | 14.83 (knock) | 60.5 / 60.6 | 2.28e-08 | - | True |
| step | 0.001 | 0.40536 | 0.40571 | +0.001 | +0.001 | +0.035 | 0.0001 | 14.83 (knock) | 60.5 / 60.6 | 2.27e-08 | 0.10 | True |
| probe* | 0.010 | 0.40542 | 0.40577 | +0.006 | +0.006 | +0.035 | 0.0000 | 14.80 (knock) | 60.5 / 60.6 | 2.24e-08 | 1.04 | True |
| probe* | 0.020 | 0.40549 | 0.40583 | +0.013 | +0.013 | +0.035 | 0.0000 | 14.77 (knock) | 60.5 / 60.6 | 2.20e-08 | 2.09 | True |
| probe* | 0.050 | 0.40568 | 0.40603 | +0.033 | +0.032 | +0.034 | 0.0001 | 14.68 (knock) | 60.5 / 60.5 | 2.08e-08 | 5.39 | True |
| probe* | 0.100 | 0.40603 | 0.40636 | +0.068 | +0.066 | +0.033 | 0.0001 | 14.52 (knock) | 60.4 / 60.4 | 1.87e-08 | 11.39 | True |

#### E85_normal - humid_evap (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.40536 | 0.40571 | +0.000 | +0.000 | +0.035 | 0.0001 | 14.83 (knock) | 60.5 / 60.6 | 2.28e-08 | - | True |
| step | 0.001 | 0.40542 | 0.40577 | +0.006 | +0.006 | +0.035 | 0.0001 | 14.81 (knock) | 60.6 / 60.6 | 2.27e-08 | 0.10 | True |
| step | 0.002 | 0.40549 | 0.40583 | +0.013 | +0.013 | +0.035 | 0.0001 | 14.79 (knock) | 60.7 / 60.7 | 2.27e-08 | 0.21 | True |
| step | 0.003 | 0.40555 | 0.40590 | +0.019 | +0.019 | +0.035 | 0.0001 | 14.78 (knock) | 60.7 / 60.8 | 2.26e-08 | 0.31 | True |
| probe* | 0.010 | 0.40601 | 0.40635 | +0.065 | +0.064 | +0.034 | 0.0001 | 14.64 (knock) | 61.2 / 61.2 | 2.22e-08 | 1.04 | True |
| probe* | 0.020 | 0.40667 | 0.40700 | +0.131 | +0.129 | +0.033 | 0.0000 | 14.45 (knock) | 61.8 / 61.9 | 2.16e-08 | 2.09 | True |
| probe* | 0.050 | 0.40868 | 0.40898 | +0.332 | +0.327 | +0.030 | 0.0000 | 13.84 (knock) | 64.0 / 64.0 | 1.99e-08 | 5.39 | True |
| probe* | 0.100 | 0.41211 | 0.41236 | +0.676 | +0.666 | +0.025 | 0.0002 | 12.73 (knock) | 68.1 / 68.2 | 1.69e-08 | 11.39 | True |

#### PRF87_normal - humid_ambient (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37101 | 0.37137 | +0.000 | +0.000 | +0.036 | 0.0001 | 14.66 (knock) | 48.2 / 48.5 | 3.26e-08 | - | True |
| step | 0.001 | 0.37102 | 0.37137 | +0.001 | +0.001 | +0.036 | 0.0001 | 14.66 (knock) | 48.2 / 48.5 | 3.25e-08 | 0.07 | True |
| probe* | 0.010 | 0.37107 | 0.37143 | +0.006 | +0.006 | +0.036 | 0.0000 | 14.63 (knock) | 48.2 / 48.5 | 3.23e-08 | 0.67 | True |
| probe* | 0.020 | 0.37112 | 0.37149 | +0.011 | +0.012 | +0.037 | 0.0001 | 14.61 (knock) | 48.2 / 48.5 | 3.20e-08 | 1.36 | True |
| probe* | 0.050 | 0.37129 | 0.37167 | +0.028 | +0.030 | +0.038 | 0.0001 | 14.52 (knock) | 48.2 / 48.4 | 3.10e-08 | 3.50 | True |
| probe* | 0.100 | 0.37158 | 0.37199 | +0.057 | +0.062 | +0.040 | 0.0001 | 14.37 (knock) | 48.2 / 48.4 | 2.93e-08 | 7.39 | True |

#### PRF91_normal - humid_ambient (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.37503 | 0.37519 | +0.000 | +0.000 | +0.016 | 0.0000 | 11.81 (knock) | 52.0 / 52.3 | 3.49e-08 | - | True |
| step | 0.001 | 0.37503 | 0.37520 | +0.000 | +0.000 | +0.016 | 0.0000 | 11.81 (knock) | 52.0 / 52.2 | 3.49e-08 | 0.07 | True |
| probe* | 0.010 | 0.37507 | 0.37524 | +0.004 | +0.005 | +0.017 | 0.0000 | 11.78 (knock) | 52.0 / 52.2 | 3.46e-08 | 0.67 | True |
| probe* | 0.020 | 0.37511 | 0.37528 | +0.008 | +0.009 | +0.017 | 0.0001 | 11.75 (knock) | 51.9 / 52.2 | 3.43e-08 | 1.36 | True |
| probe* | 0.050 | 0.37524 | 0.37543 | +0.021 | +0.024 | +0.019 | 0.0001 | 11.66 (knock) | 51.9 / 52.2 | 3.34e-08 | 3.50 | True |
| probe* | 0.100 | 0.37546 | 0.37569 | +0.043 | +0.050 | +0.022 | 0.0001 | 11.50 (knock) | 51.9 / 52.1 | 3.17e-08 | 7.39 | True |

#### PRF97_normal - humid_ambient (current rule; steps 1-5, every 10th, and the last 3)

| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dry_baseline | 0.000 | 0.38540 | 0.38557 | +0.000 | +0.000 | +0.017 | 0.0000 | 12.28 (knock) | 55.5 / 55.8 | 3.53e-08 | - | True |
| step | 0.001 | 0.38540 | 0.38557 | +0.000 | +0.000 | +0.017 | 0.0000 | 12.27 (knock) | 55.5 / 55.8 | 3.53e-08 | 0.07 | True |
| probe* | 0.010 | 0.38544 | 0.38561 | +0.004 | +0.004 | +0.018 | 0.0001 | 12.25 (knock) | 55.5 / 55.7 | 3.50e-08 | 0.67 | True |
| probe* | 0.020 | 0.38547 | 0.38566 | +0.008 | +0.009 | +0.018 | 0.0001 | 12.23 (knock) | 55.5 / 55.7 | 3.47e-08 | 1.36 | True |
| probe* | 0.050 | 0.38560 | 0.38580 | +0.020 | +0.023 | +0.020 | 0.0001 | 12.14 (knock) | 55.5 / 55.7 | 3.38e-08 | 3.50 | True |
| probe* | 0.100 | 0.38582 | 0.38605 | +0.042 | +0.048 | +0.023 | 0.0001 | 12.00 (knock) | 55.4 / 55.6 | 3.22e-08 | 7.39 | True |

## Track A humid-intake variant (water-majority cases, w = 0.5-0.8)

197 computed points so far (of 756). Best eligible per fuel x regime x mode (both engines):

| fuel | regime | mode | best CR / T / w | eta M03 | eta CRN | CA50 (limit) | q g/kg | fraction of water evaporated in intake | saturation-limited |
|---|---|---|---|---|---|---|---|---|---|
| CH3OH | normal | liquid | 24 / 360 / 0.5 | 0.4484 | - | 11.17 (MBT) | 29.0 | 0.187 | True |
| CH3OH | normal | humid_evap | 24 / 360 / 0.5 | 0.4484 | - | 11.17 (MBT) | 29.0 | 0.187 | True |
| CH3OH | normal | humid_ambient | 24 / 320 / 0.5 | 0.4520 | - | 11.70 (MBT) | 78.3 | 0.504 | True |
| CH3OH | hot | liquid | 18 / 400 / 0.5 | 0.4382 | - | 9.68 (MBT) | 47.1 | 0.302 | True |
| CH3OH | hot | humid_evap | 18 / 400 / 0.5 | 0.4382 | - | 9.68 (MBT) | 47.1 | 0.302 | True |
| CH3OH | hot | humid_ambient | none eligible yet | | | | | | |
| C2H5OH | normal | liquid | none eligible yet | | | | | | |
| C2H5OH | normal | humid_evap | none eligible yet | | | | | | |
| C2H5OH | normal | humid_ambient | none eligible yet | | | | | | |
| C2H5OH | hot | liquid | none eligible yet | | | | | | |
| C2H5OH | hot | humid_evap | none eligible yet | | | | | | |
| C2H5OH | hot | humid_ambient | none eligible yet | | | | | | |
| CH4 | normal | liquid | none eligible yet | | | | | | |
| CH4 | normal | humid_evap | none eligible yet | | | | | | |
| CH4 | normal | humid_ambient | none eligible yet | | | | | | |
| CH4 | hot | liquid | none eligible yet | | | | | | |
| CH4 | hot | humid_evap | none eligible yet | | | | | | |
| CH4 | hot | humid_ambient | none eligible yet | | | | | | |

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

0. **Continuation rule changed by James after seeing the first data (2026-10-24 19:01 PDT).** Old rule (pre-stated):
   step gain > 1e-4 absolute in Module 03 plus positive M03-CRN gain. New rule: gain > numerical noise,
   **3.3e-5 absolute** (largest measured shift of the 0.5-CAD production-step efficiency, verification/x5_m03/RESULTS_FIX.md,
   X5 C2H5OH/best_overall +0.0073 % of 0.45618; the pure 0.5 vs 0.25 CAD refinement difference is only <= 6.1e-6 and
   the spark-bisection tolerance is ~2e-5, so 3.3e-5 is a conservative noise floor). Both engines must still gain on
   every step, the step is still 0.1 pp, the cap is 100 steps, raised to 200 only for chains still gaining at 100 (recorded per
   chain). Old-rule results are kept as the variant `rule_1e-4` (files without `__noise`).
1. **Under the old rule** gasoline / E-blends / CH4 / ethanol-normal stopped at step 1 (first-step gains 2-8e-5,
   both engines within 0.001 pp of each other); methanol-normal stopped at w = 0.041 (liquid) / 0.049 (humid_evap), and
   ethanol-hot stopped at w = 0.040 / 0.045, when per-step gains fell just under 1e-4.
2. **Under the noise rule** every gasoline, E10, E85 (normal and hot), CH4-hot and ethanol-normal chain passes
   step 1 in liquid and humid_evap mode, and the chains are walking on (see the current-rule table for live best w and
   d_eta). CH4-normal stops at step 0 in both modes (first-step gain 1.9e-5 liquid / 2.4e-5 humid_evap: CA50 is already MBT-limited,
   so there is little knock relief to collect). **humid_ambient stops at step 0 for every fuel** (gain -3.4e-6 to +9.3e-6:
   vapour at intake temperature dilutes and lowers O2 partial pressure without the cooling that relieves knock).
   The labelled probes (not steps) suggest near-linear gains up to w = 10 %: PRF87 +0.53 pp, PRF91 +0.38,
   PRF97 +0.40, E10 +0.44, E85 +0.72 / +0.42 (hot), C2H5OH-normal +0.45, CH4-hot +0.42. So many chains are expected
   to reach cap 100 still gaining and be extended to 200.
3. **Mechanism (Module 03, both engines agree on efficiency):** knock relief lets the knock-limited CA50 advance
   (e.g. CH3OH 14.6 -> ~11 deg, C2H5OH-hot 14.9 -> ~12.3 deg), the NO proxy falls (-4 to -9 % at the alcohol chains so far,
   10-25 % at the 10 % probes), and p_max rises (+9 to +18 % on the alcohol chains so far). That p_max rise is the cost to watch against hardware limits.
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

