# J2 — Module 02 dual-temperature variant, cross-checked on independent mechanisms (box-queue 20261024-1230)

Status: **EXECUTED and cross-checked by 2 chemistry engines (same Cantera solver, independent mechanisms). Not validated against experiment.**
Note: both engines share Cantera's equilibrium/reactor/FreeFlame solvers; the independence is in the kinetics + thermo + transport data.

## Regimes (temperatures cited)
- **Normal:** unburned intake charge T_u = **360 K** (coolant ~90 °C class engine, upper normal intake), p_IVC = 1 bar.
- **Hot (high-performance):** T_u = **400 K** (un-intercooled boost / heated intake).
- TDC-equivalent states: isentropic compression by CR 16 and 24 (normal: T_TDC 846–966 K; hot: 920–1044 K), phi = 1, w ∈ {0, 0.3, 0.6}.

## Engines
| quantity | engine A (Module 02) | engine B |
|---|---|---|
| T_ad (1 atm and TDC) | San Diego 2016 | AramcoMech 2.0 (493 sp, full) and CRECK C1–C3 HT (114 sp) |
| tau_ig (const-V, TDC state) | San Diego | AramcoMech 2.0 (full); CRECK HT info only (no LT chemistry) |
| S_L (1 atm, T_u) | San Diego (X1 run) | CRECK C1–C3 HT (Hermes's note: full Aramco FreeFlame hangs; choice recorded) |

## Pre-stated tolerances (in the run-script docstring and `compare_j2_m02_dualT.py`, written before the run)
T_ad ±0.5 %; S_L ±10 %; tau_ig within a factor 2; the hot-minus-normal change must have the same sign in both engines.

## PASS/FAIL
| check | n | PASS | max |err| | hot-vs-normal sign agreement |
|---|---|---|---|---|
| T_ad 1 atm, Aramco | 24 | 24 | 0.04 % | 12/12 |
| T_ad TDC, Aramco | 24 | 24 | 0.06 % | 12/12 |
| T_TDC, Aramco | 24 | 24 | 0.24 % | 12/12 |
| **tau_ig, Aramco** | 24 | **19** | factor 2.24 | 12/12 |
| T_ad 1 atm / TDC, CRECK | 24 / 24 | 24 / 24 | 0.11 % / 0.13 % | 12/12 |
| tau_ig, CRECK (info) | 24 | 24 | factor 1.82 | 12/12 |
| **S_L, CRECK** | 12 | **7** | 13.3 % | 6/6 |

FAILs: tau_ig — 5 C2H5OH **normal-regime** cases (CR16 all w, CR24 w = 0, 0.3): Aramco ignites 2.0–2.24× faster than San Diego.
S_L — 5 CH3OH cases (normal w = 0/0.3/0.6, hot w = 0.3/0.6): CRECK 10.0–13.3 % slower than San Diego. All C2H5OH S_L within 7.6 %.

## Normal vs hot, side by side (ratio hot/normal; engine A / engine B)
| quantity | CH3OH | C2H5OH |
|---|---|---|
| T_ad 1 atm | 1.008–1.013 / same | 1.008–1.012 / same |
| S_L | 1.18–1.23 / 1.19–1.24 | 1.19–1.23 / 1.19–1.24 |
| tau_ig CR16 | 0.18–0.19 / 0.18–0.19 | 0.19 / 0.21–0.22 |
| tau_ig CR24 | 0.25–0.26 / 0.24–0.26 | 0.24 / 0.26 |

## Verdict: is hotter better?
- **Flame side, yes (both engines agree):** the 400 K charge burns ~19–24 % faster (S_L) and ~1 % hotter (T_ad), i.e. shorter burn duration → closer to constant-volume combustion.
- **Knock side, no:** autoignition delay at TDC is **4–5.5× shorter** in the hot regime (both engines agree within 12 %); at CR 24 the hot CH3OH tau_ig is 0.11–0.23 ms (~1–2 °CA at 1500 rpm-class speeds), i.e. a strong knock penalty that forces CA50 retard.
  Net cycle effect must come from Module 03 (wme1-hiT J1): this module alone does not show that hotter is better.
- Water (w = 0.6) slows S_L by ~55 % and lengthens tau_ig ~1.2× in both regimes; the hot/normal ratios are nearly independent of w.

## Module 08 (chemical-effect split at the hot condition)
**Deferred.** Hermes's stoichiometry fix (relay task water-engine-spray-20261024-082000) has not landed on `wme1-spray`: last commit there is 35166ff (2026-10-23 09:23 PDT). Per the job spec, J2 = Module 02 only; Module 08 to follow when the fix lands.

## Runs (box, 2 workers)
- `tad_ign` San Diego 3.9 s; CRECK 15.3 s; Aramco 152.6 s (retry, see below); `sl` CRECK 13:22–13:38 PDT.
- First Aramco run hung at 18/24 cases (13:41–14:09 PDT). Diagnosis: RLIMIT_AS 1.5 GiB vs Aramco worker VmPeak 1.43 GB → a worker died on allocation; fork Pool with maxtasksperchild then waits forever for the lost task. Fix in `run_j2_m02_dualT.py` (spawn pool, no worker recycling, per-case error capture, checkpoint file), limit raised to 3 GiB; rerun complete in 153 s. No physics or tolerance change.
- Files: `tad_ign_{sandiego,aramco,creck}.json`, `sl_creck.json`, `compare.{csv,json}`. CRECK yaml regenerated per `mechanisms/PROVENANCE.md` (not committed, licence unclear).
