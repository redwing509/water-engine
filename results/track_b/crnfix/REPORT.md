# M03-CRN integrator failures: cause, fix, verification (Track B + Track A)

Grok Bot self-directed box job `grokbot-selfdirected-20261025-1410`, branch `selfdir/box-20261025-1410`
(from `track-ab/box-20261025`, PR #10). Status labels: fix **EXECUTED** and **VERIFIED** (regression +
reproduction checks below); physics **NOT validated** (no experiment).

## What failed
* Track B chains stopped because the second engine (M03-CRN, Cantera 3.2.0 ReactorNet/CVODES) failed, not
  because the gain ended: C2H5OH normal liquid after w 0.173, CH3OH normal humid_evap after w 0.080, CH3OH normal
  liquid after w 0.132, CH3OH hot humid_evap after w 0.235 (rig1 400-cap extension). Error: CVODES
  "maximum number of timesteps (500000)". One failing humid_evap case had taken 3418 s.
* Track A (PR #10): 24 of 61 M03-CRN cross-checks of best rows failed: 14 x "max steps", 10 x CVODES error -27
  "tout too close to t0".

## Cause 1 - chattering at the saturation switch (max steps)
`engines/m03_cantera/engine.py`, `evap_mdot`: the in-cylinder evaporation source is a relaxation toward
`target = min(target_sched, target_sat)` PLUS a feed-forward rate (`evap_rate_sched`, or `slope` in coupled mode)
that is switched OFF when `sat_limited` (target_sat < target_sched). Early in compression (~-162 CAD) the charge
is cool (~296 K) and near saturation, so target_sat ~ target_sched. Evaporating (feed-forward on) cools the gas and
raises the humidity -> saturation-limited -> feed-forward off -> relaxation lets the state drift back -> on again.
Instrumented run: `sat_limited` flipped True/False ~2:1 at t = 0.00147337 s, rate jumping 5e-8 <-> 5e-4 kg/s; a
discontinuous right-hand side at a sliding (Filippov) surface - CVODES takes ever smaller steps and hits max_steps.
This is a numerical artefact, not physics: both branches give the same mass flow on the surface.

**Fix:** `Case.sat_blend_frac` (default 0.0 = legacy, bit-identical). With frac > 0 the feed-forward term is
multiplied by sigma = clip(0.5 + (target_sat - target_sched) / (frac * m_liq0), 0, 1), i.e. a linear ramp over a
band of frac x the initial liquid mass instead of a step. Outside the band the equations are unchanged.
Production value `CRN_SAT_BLEND = 1e-3` (sims/track_b/run.py, sims/03_engine_cycle/track_a_box0915_report.py).

## Cause 2 - near-duplicate output times (CVODES -27)
`engine.run` builds the output grid as `np.unique(linspace(0.05 CAD) + breaks)`. A break point (spark /
liquid-freeze angle such as -41.0 CAD, stored as -40.99999999999999) lands within ~1e-15 rad of a grid point;
np.unique keeps both, and `net.advance` gets a tout ~1e-17 s after t -> CVODES -27. **Fix** (active only when
sat_blend_frac > 0, so legacy stays bit-identical): drop grid points within 1e-9 rad of a break (the break is kept).

## Verification (executed on the box)
* Legacy rows reproduce: Track B last OK steps recomputed with the fix: C2H5OH normal step 173 0.45309745650806665
  and CH3OH normal step 132 0.43429204047638525 (bit-identical); CH3OH normal humid_evap step 80 0.43239867839
  vs stored 0.43239867848 (9.5e-11; now 0.4 s instead of 3418 s); CH3OH hot humid_evap step 235 0.36643695175 vs
  0.36643695379 (2.0e-9). All << the 3.3e-5 noise threshold.
* Band sensitivity (C2H5OH normal step 174): frac 1e-4 vs 1e-3 differ 1.9e-9, 1e-2 vs 1e-3 differ 9e-9.
* Previously failing steps now run: C2H5OH normal step 174 CRN 0.45314417 (gain 4.67e-5 vs M03 4.74e-5), CH3OH
  normal step 133 0.43434790 (5.59e-5 vs 5.65e-5), CH3OH normal humid_evap step 81 0.43243506 (3.64e-5 vs 3.68e-5),
  CH3OH hot humid_evap step 236 0.36647030.
* Track A: all 24 failed best rows now run (|d_eta| vs Module 03 0.02-0.13 pp, p_max ratio 0.999-1.001, C1 pass);
  the 36 previously OK best rows recomputed with the fix differ by at most 5.4e-7 in efficiency (most bit-identical).
* Failed CRN rows are archived, not edited: `*.failed_crn_rows.jsonl` here; Track A legacy cache
  `results/track_a_box/crn_cache.json` unchanged, fixed-engine cache `crn_cache_satblend0.001.json`.

## Resumed Track B chains
`python -m sims.track_b.crnfix_resume 3` (same rule: 0.1-pp steps, spark re-opt each step, continue while M03 gain
> 3.3e-5 AND CRN gain > 0, cap 400). Results: `steps_*__noise.jsonl` here, `summary_crnfix.json`; cost metric
`python -m sims.track_b.crnfix_cost` -> `COST.md` ($0.10/gal headline, $0 secondary).

## PR 11 review item 2 (Claude reply-selfdir-1410-review-20261025-1725): CH3OH normal liquid vs humid_evap identical after resume

Tags: Track B; EXECUTED + VERIFIED (fresh-process recompute); NOT validated. Verdict: **not a bug - physical convergence. No chain re-run needed.**

- Mode flag is honoured. `sims/track_b/run.py` `point()`: `if mode == "humid_evap": par = replace(par, f_evap_intake=1.0)`; liquid keeps the Module 03 default `f_evap_intake=0.5`. `crnfix_resume.py` passes the mode to `chain_noise(fuel, regime, mode)` and reads/writes per-mode files (`steps_CH3OH_normal__noise.jsonl` vs `steps_CH3OH_normal_humid_evap__noise.jsonl`); every row carries the right `water_mode`.
- Intake evaporation is wet-bulb limited. `sims/03_engine_cycle/run.py`: `# f_evap_intake is infeasible: evaporate only up to saturation (wet bulb).  e = brentq(excess, base, f, xtol=1e-12)`.
- Stored rows (CR 17, T_intake 320 K, dry eta 0.42379): liquid f_evap_effective = 0.5, not saturation-limited up to w 0.139; humid_evap is saturation-limited throughout (f_evap 0.931 at w 0.080, 0.532 at 0.132, 0.5015 at 0.139). From w 0.140 BOTH are saturation-limited at the same f_evap (0.49735 at 0.140, 0.27571 at 0.227) -> same vapour, same excess liquid, same charge.
- Fresh-process recompute (`sims/track_b/crnfix_mode_check.py`, one spawned process per mode, nice 19; `mode_check_CH3OH_normal.json`): all 18 points reproduce the stored rows exactly (max |diff| 0.0). M03 eta liquid - humid_evap: w 0.080 -8.42e-4, 0.132 -1.05e-4, 0.139 -4.9e-6, 0.140 -4e-14, 0.227 8e-14, 0.228 3e-14.
- Before the resume the chains "differed" (best w 0.132 vs 0.080) only because each stopped at a CRN failure (liquid step 133, humid_evap step 81), not at an optimum. Both resumed chains run on to the same w 0.227 (+1.453 / +1.429 pp, power +9.8 %, cost/mile -2.80 % at $0.10/gal) and stop on the same significance rule (gain 3.29e-05 <= noise 3.3e-05).
- Reading: for CH3OH normal, putting all water through the intake (humid_evap) only helps below w 0.140 (up to +0.084 pp at w 0.080); at the efficiency optimum it is the same engine state as liquid injection. Count the two chains as ONE result.
- Track B CR: each chain runs at the dry-baseline CR chosen by the Module 03 knock model only -> CR choice "Not yet (single-engine knock)".
