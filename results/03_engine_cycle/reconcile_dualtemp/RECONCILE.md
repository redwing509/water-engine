# Track A reconcile: dual-temperature rerun vs PR #8 coupled verdict (2026-10-25)

**Tags:** Track A; both temperature regimes; executed (Module 03) + verified (M03-CRN second engine); NOT validated against experiment.

Regimes: normal = coolant 363.15 K, chamber wall 450 K, port wall 363.15 K; hot = coolant 388.15 K, chamber wall 520 K, port wall 388.15 K (MAHLE/VW SSP 222; SAE 960271; Heywood 1988 ch. 12; docs/DUAL_TEMPERATURE_RULE.md).

## Finding

The dual-temperature rerun (`sims/dual_temp/run_m03.py`, results/dual_temp/03_engine_cycle_*_fixed) called Module 03 without `--evap-profile`, i.e. with `evap_profile=None, coupling=None`: the **legacy, uncoupled** water schedule (no retained liquid, no wall film). Its water-majority numbers are reproduced here exactly and are the same numbers as PR #8's 'legacy schedule' rows. They are **uncoupled (superseded)**. With the PR #8 coupled model, every water-majority case loses to the best dry point or is not SPEC-eligible, in both bounds and both engines (table below). The hot-regime +2.05 pp also compared a 400 K-intake wet point with a 320 K-intake dry point.

## Water-majority points, both engines

| fuel | regime | model | atomiser / variant | bound | CR / w / T_in K | eta M03 | eta CRN | eligible | d vs rerun best dry pp (M03 / CRN) | d vs PR8 best dry pp (M03 / CRN) | power IMEP % | cost/mile % at 0.10 USD/gal water (M03 / CRN) | cost/mile % at free water (M03 / CRN) | cost verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CH3OH | normal | uncoupled (superseded) | - / - | - | 24 / 0.6 / 360 | 0.4311 | 0.4312 | yes | +1.04 / +1.05 | +1.04 / +1.05 | +1.0 | +0.3 / +0.2 | -2.4 / -2.4 | fuel saved, but water cost eats it |
| CH3OH | normal | coupled (PR #8) | carb_venturi / cfd_matched | i | 24 / 0.6 / 360 | 0.3499 | 0.3497 | no (knock, CA50 30) | -7.08 / -7.10 | -7.08 / -7.10 | -33.4 | +23.5 / +23.6 | +20.2 / +20.3 | power loss; wet point not SPEC-eligible |
| CH3OH | normal | coupled (PR #8) | carb_venturi / cfd_matched | ii | 24 / 0.6 / 360 | 0.3369 | 0.3367 | no (knock, CA50 30) | -8.37 / -8.40 | -8.37 / -8.40 | -29.6 | +28.3 / +28.4 | +24.9 / +25.0 | power loss; wet point not SPEC-eligible |
| CH3OH | normal | coupled (PR #8) | carb_venturi / nominal | i | 24 / 0.6 / 360 | 0.3512 | 0.3510 | no (knock, CA50 30) | -6.95 / -6.97 | -6.95 / -6.97 | -31.9 | +23.1 / +23.2 | +19.8 / +19.9 | power loss; wet point not SPEC-eligible |
| CH3OH | normal | coupled (PR #8) | carb_venturi / nominal | ii | 24 / 0.6 / 360 | 0.3387 | 0.3385 | no (knock, CA50 30) | -8.19 / -8.22 | -8.19 / -8.22 | -28.0 | +27.6 / +27.7 | +24.2 / +24.3 | power loss; wet point not SPEC-eligible |
| CH3OH | normal | coupled (PR #8) | ultrasonic_120kHz / cfd_matched | i | 24 / 0.6 / 360 | 0.4109 | 0.4106 | yes | -0.98 / -1.01 | -0.98 / -1.01 | -14.6 | +5.2 / +5.3 | +2.4 / +2.5 | power loss |
| CH3OH | normal | coupled (PR #8) | ultrasonic_120kHz / cfd_matched | ii | 24 / 0.6 / 360 | 0.3983 | 0.3980 | yes | -2.24 / -2.27 | -2.24 / -2.27 | -6.8 | +8.5 / +8.6 | +5.6 / +5.7 | power loss |
| CH3OH | normal | coupled (PR #8) | ultrasonic_120kHz / nominal | i | 24 / 0.6 / 360 | 0.4139 | 0.4136 | yes | -0.68 / -0.71 | -0.68 / -0.71 | -13.9 | +4.4 / +4.5 | +1.6 / +1.7 | power loss |
| CH3OH | normal | coupled (PR #8) | ultrasonic_120kHz / nominal | ii | 24 / 0.6 / 360 | 0.4020 | 0.4018 | yes | -1.87 / -1.89 | -1.87 / -1.89 | -5.8 | +7.5 / +7.6 | +4.6 / +4.7 | power loss |
| C2H5OH | normal | uncoupled (superseded) | - / - | - | 24 / 0.6 / 360 | 0.4378 | 0.4380 | yes | -0.76 / -0.73 | -0.76 / -0.73 | -0.9 | +7.9 / +7.9 | +1.7 / +1.7 | power loss |
| C2H5OH | normal | coupled (PR #8) | carb_venturi / cfd_matched | i | 24 / 0.6 / 360 | 0.3852 | 0.3848 | no (CA50 24) | -6.03 / -6.04 | -6.03 / -6.04 | -29.2 | +22.7 / +22.7 | +15.6 / +15.7 | power loss; wet point not SPEC-eligible |
| C2H5OH | normal | coupled (PR #8) | carb_venturi / cfd_matched | ii | 24 / 0.6 / 360 | 0.3725 | 0.3721 | no (CA50 24) | -7.29 / -7.31 | -7.29 / -7.31 | -25.2 | +26.9 / +26.9 | +19.6 / +19.7 | power loss; wet point not SPEC-eligible |
| C2H5OH | normal | coupled (PR #8) | carb_venturi / nominal | i | 24 / 0.6 / 360 | 0.3926 | 0.3923 | no (CA50 22) | -5.28 / -5.30 | -5.28 / -5.30 | -26.9 | +20.4 / +20.4 | +13.5 / +13.5 | power loss; wet point not SPEC-eligible |
| C2H5OH | normal | coupled (PR #8) | carb_venturi / nominal | ii | 24 / 0.6 / 360 | 0.3739 | 0.3735 | no (CA50 24) | -7.16 / -7.18 | -7.16 / -7.18 | -24.0 | +26.4 / +26.5 | +19.2 / +19.2 | power loss; wet point not SPEC-eligible |
| C2H5OH | normal | coupled (PR #8) | ultrasonic_120kHz / cfd_matched | i | 24 / 0.6 / 360 | 0.4158 | 0.4155 | yes | -2.97 / -2.98 | -2.97 / -2.98 | -15.7 | +13.7 / +13.7 | +7.1 / +7.2 | power loss |
| C2H5OH | normal | coupled (PR #8) | ultrasonic_120kHz / cfd_matched | ii | 24 / 0.6 / 360 | 0.4051 | 0.4047 | no (p_max 121 bar) | -4.04 / -4.05 | -4.04 / -4.05 | -10.0 | +16.7 / +16.7 | +10.0 / +10.0 | power loss; wet point not SPEC-eligible |
| C2H5OH | normal | coupled (PR #8) | ultrasonic_120kHz / nominal | i | 24 / 0.6 / 360 | 0.4199 | 0.4195 | yes | -2.56 / -2.58 | -2.56 / -2.58 | -14.4 | +12.5 / +12.6 | +6.1 / +6.1 | power loss |
| C2H5OH | normal | coupled (PR #8) | ultrasonic_120kHz / nominal | ii | 24 / 0.6 / 360 | 0.4103 | 0.4100 | no (p_max 122 bar) | -3.51 / -3.53 | -3.51 / -3.53 | -7.1 | +15.2 / +15.2 | +8.6 / +8.6 | power loss; wet point not SPEC-eligible |
| CH4 | normal | uncoupled (superseded) | - / - | - | 23 / 0.6 / 320 | 0.4463 | 0.4463 | yes | +1.36 / +1.33 | not in PR #8 | +9.8 | +0.1 / +0.2 | -3.0 / -3.0 | fuel saved, but water cost eats it |
| CH3OH | hot | uncoupled (superseded) | - / - | - | 24 / 0.6 / 400 | 0.4385 | 0.4387 | yes | +2.05 / +2.06 | no eligible dry | -1.5 | -2.1 / -2.1 | -4.7 / -4.7 | power loss |
| CH3OH | hot | coupled (PR #8) | carb_venturi / cfd_matched | i | 24 / 0.6 / 400 | 0.3727 | 0.3725 | no (knock, CA50 30) | -4.53 / -4.55 | no eligible dry | -46.5 | +15.2 / +15.3 | +12.2 / +12.2 | power loss; wet point not SPEC-eligible |
| CH3OH | hot | coupled (PR #8) | carb_venturi / cfd_matched | ii | 24 / 0.6 / 400 | 0.3338 | 0.3335 | no (knock, CA50 30) | -8.42 / -8.45 | no eligible dry | -37.2 | +28.7 / +28.8 | +25.2 / +25.3 | power loss; wet point not SPEC-eligible |
| CH3OH | hot | coupled (PR #8) | carb_venturi / nominal | i | 24 / 0.6 / 400 | 0.3738 | 0.3735 | no (knock, CA50 30) | -4.42 / -4.45 | no eligible dry | -45.5 | +14.9 / +15.0 | +11.8 / +11.9 | power loss; wet point not SPEC-eligible |
| CH3OH | hot | coupled (PR #8) | carb_venturi / nominal | ii | 24 / 0.6 / 400 | 0.3355 | 0.3352 | no (knock, CA50 30) | -8.25 / -8.28 | no eligible dry | -35.9 | +28.0 / +28.1 | +24.6 / +24.7 | power loss; wet point not SPEC-eligible |
| CH3OH | hot | coupled (PR #8) | ultrasonic_120kHz / cfd_matched | i | 24 / 0.6 / 400 | 0.3801 | 0.3798 | no (knock, CA50 30) | -3.79 / -3.82 | no eligible dry | -38.2 | +13.0 / +13.1 | +10.0 / +10.1 | power loss; wet point not SPEC-eligible |
| CH3OH | hot | coupled (PR #8) | ultrasonic_120kHz / cfd_matched | ii | 24 / 0.6 / 400 | 0.3573 | 0.3570 | no (CA50 28) | -6.07 / -6.11 | no eligible dry | -25.8 | +20.2 / +20.3 | +17.0 / +17.1 | power loss; wet point not SPEC-eligible |
| CH3OH | hot | coupled (PR #8) | ultrasonic_120kHz / nominal | i | 24 / 0.6 / 400 | 0.4000 | 0.3997 | no (CA50 26) | -1.80 / -1.84 | no eligible dry | -33.4 | +7.4 / +7.5 | +4.5 / +4.6 | power loss; wet point not SPEC-eligible |
| CH3OH | hot | coupled (PR #8) | ultrasonic_120kHz / nominal | ii | 24 / 0.6 / 400 | 0.3756 | 0.3753 | no (CA50 24) | -4.24 / -4.27 | no eligible dry | -20.3 | +14.3 / +14.4 | +11.3 / +11.4 | power loss; wet point not SPEC-eligible |
| C2H5OH | hot | uncoupled (superseded) | - / - | - | 24 / 0.6 / 400 | 0.4441 | 0.4442 | yes | -0.00 / +0.03 | +6.04 / +6.06 | -4.0 | +6.1 / +6.0 | +0.0 / -0.1 | power loss |
| C2H5OH | hot | coupled (PR #8) | carb_venturi / cfd_matched | i | 24 / 0.6 / 400 | 0.3749 | 0.3747 | no (knock, CA50 30) | -6.92 / -6.92 | -0.87 / -0.88 | -45.3 | +25.7 / +25.7 | +18.5 / +18.5 | power loss; wet point not SPEC-eligible |
| C2H5OH | hot | coupled (PR #8) | carb_venturi / cfd_matched | ii | 24 / 0.6 / 400 | 0.3463 | 0.3460 | no (knock, CA50 30) | -9.78 / -9.80 | -3.74 / -3.76 | -37.5 | +36.0 / +36.1 | +28.2 / +28.3 | power loss; wet point not SPEC-eligible |
| C2H5OH | hot | coupled (PR #8) | carb_venturi / nominal | i | 24 / 0.6 / 400 | 0.3756 | 0.3754 | no (knock, CA50 30) | -6.84 / -6.85 | -0.80 / -0.81 | -44.6 | +25.4 / +25.4 | +18.2 / +18.2 | power loss; wet point not SPEC-eligible |
| C2H5OH | hot | coupled (PR #8) | carb_venturi / nominal | ii | 24 / 0.6 / 400 | 0.3475 | 0.3471 | no (knock, CA50 30) | -9.66 / -9.68 | -3.62 / -3.64 | -36.6 | +35.6 / +35.7 | +27.8 / +27.9 | power loss; wet point not SPEC-eligible |
| C2H5OH | hot | coupled (PR #8) | ultrasonic_120kHz / cfd_matched | i | 24 / 0.6 / 400 | 0.4139 | 0.4135 | no (CA50 22) | -3.02 / -3.04 | +3.02 / +3.00 | -32.3 | +13.8 / +13.9 | +7.3 / +7.3 | power loss; wet point not SPEC-eligible |
| C2H5OH | hot | coupled (PR #8) | ultrasonic_120kHz / cfd_matched | ii | 24 / 0.6 / 400 | 0.3948 | 0.3944 | no (CA50 20) | -4.93 / -4.95 | +1.12 / +1.09 | -22.2 | +19.3 / +19.4 | +12.5 / +12.5 | power loss; wet point not SPEC-eligible |
| C2H5OH | hot | coupled (PR #8) | ultrasonic_120kHz / nominal | i | 24 / 0.6 / 400 | 0.4276 | 0.4272 | no (CA50 18) | -1.65 / -1.67 | +4.39 / +4.37 | -27.2 | +10.2 / +10.2 | +3.9 / +3.9 | power loss; wet point not SPEC-eligible |
| C2H5OH | hot | coupled (PR #8) | ultrasonic_120kHz / nominal | ii | 24 / 0.6 / 400 | 0.4075 | 0.4071 | no (CA50 16) | -3.66 / -3.69 | +2.38 / +2.35 | -16.7 | +15.6 / +15.7 | +9.0 / +9.1 | power loss; wet point not SPEC-eligible |
| CH4 | hot | uncoupled (superseded) | - / - | - | 23 / 0.6 / 320 | 0.4506 | 0.4506 | yes | +0.95 / +0.91 | not in PR #8 | +9.2 | +1.1 / +1.2 | -2.1 / -2.0 | fuel saved, but water cost eats it |

## Best-dry baselines

| fuel | regime | definition | CR | T_in K | eta M03 | eta CRN |
|---|---|---|---|---|---|---|
| CH3OH | normal | rerun (hot also at 320/360 K intake) | 16 | 320 | 0.4207 | 0.4207 |
| CH3OH | normal | PR #8 (hot: 400 K intake only) | 16 | 320 | 0.4207 | 0.4207 |
| C2H5OH | normal | rerun (hot also at 320/360 K intake) | 24 | 320 | 0.4455 | 0.4453 |
| C2H5OH | normal | PR #8 (hot: 400 K intake only) | 24 | 320 | 0.4455 | 0.4453 |
| CH4 | normal | rerun (hot also at 320/360 K intake) | 22 | 320 | 0.4328 | 0.4330 |
| CH3OH | hot | rerun (hot also at 320/360 K intake) | 15 | 320 | 0.4180 | 0.4180 |
| CH3OH | hot | PR #8 (hot: 400 K intake only) | - | 400 | none SPEC-eligible | - |
| C2H5OH | hot | rerun (hot also at 320/360 K intake) | 22 | 320 | 0.4441 | 0.4439 |
| C2H5OH | hot | PR #8 (hot: 400 K intake only) | 11 | 400 | 0.3837 | 0.3835 |
| CH4 | hot | rerun (hot also at 320/360 K intake) | 24 | 320 | 0.4411 | 0.4415 |

## Notes

- Coupled rows reproduce PR #8 `coupled_points.csv` exactly (same code, `coupled_dual_temp.task`).
- M03-CRN: coupled rows run with `evap_mode="coupled"` (compare_coupled.case); every coupled row within the C1 tolerance (|d_eta| <= 1.5 pp, |p_max ratio - 1| <= 5 %): see `c1_pass` in reconcile.json.
- CH4: Module 09 has no CH4 spray profile and Module 06 has no CH4 latent budget, so no coupled CH4 number exists. The CH4 'beats dry' rows are **uncoupled (superseded); coupled model not available for CH4**. (CH4 is a gas fuel; the 'water-majority' liquid there is water only.)
- Cost: sims/cost (PR 9 027f9d7; USD prices dated 2026-10-25; headline water 0.10 USD/gal = James's test-case cost, 2026-10-25 07:32 PDT; free water 0 USD/gal shown for comparison); power = IMEP vs the rerun best dry. Cost per mile is judged only at equal-or-better power.
- Eligibility = SPEC selection (knock-free at CA50 <= 15 CAD, S_L >= 0.08 m/s, p_max <= 120 bar, closure <= 2 %).
