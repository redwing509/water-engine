# Item 1: diagnosis and fix of sub-second-order step convergence (pre-registered before the re-run)

Written and pushed **before** `gci_study.py` was re-run on the fixed code (2026-10-24, Grok Bot, verification-queue-20261024 item 1).
Baseline study: `RESULTS.md` @ a229803 (A3, A4 PASS; A1, A1-pmax, A2, A5 FAIL; p from −0.8 to 1.0).

## Diagnosis (`diag/diag_convergence.py`, output `diag/diag_results.json`)
Variant runs at frozen CA50/duration, steps 2, 1, 0.5, 0.25, 0.125 ° CA, points CH3OH/best_dry, CH3OH/water_majority, C2H5OH/best_overall. Observed order p of gross efficiency from (1, 0.5, 0.25) / (0.5, 0.25, 0.125):

| variant | best_dry | water_majority | C2H5OH best_overall |
|---|---|---|---|
| base | 0.84 / 4.86 (erratic) | 0.30 / 0.73 | −0.65 / 0.94 |
| inner-solve rtol 1e-8 → 1e-11 | unchanged | unchanged | unchanged |
| no frozen/equilibrium switch at 1000 K | unchanged | unchanged | unchanged |
| saturation cap removed | unchanged | 0.99 / 0.98 | −0.80 / 0.95 |
| **start-of-burn anchor on a node** | **2.01 / 2.01** | 2.02 / 1.91 (T_EVO 1.15 / 1.07) | **2.03 / 1.76** |
| anchor on node + cap removed (+tol, +frozen) | 2.01 / 2.01 | 2.02 / 2.02 | 2.04 / 2.03 |
| **anchor on node + cap evaluated on predictor state** | **2.01 / 2.01** | 1.39 / 2.62 (changes < 1e-5 abs) | **2.35 / 2.39** |

Causes, in order of size:
1. **Step-dependent start-of-burn anchor (dominant, every point).** The Woschni combustion term uses a motored-pressure polytrope anchored at the *left* state of the first step whose *right* node has x_b ≥ 1e-3. The anchor position therefore moves by up to one step with h, an O(h) error in the wall heat after ignition.
2. **Lagged saturation cap (wet points only).** The evaporation cap at mid and right nodes was evaluated from the left-node state compressed isentropically, ignoring the heat release, wall heat and work within the step: an O(h) error in the evaporated fraction.
3. Not causes: the inner state-inversion tolerance (noise floor < 1e-9 in eff), and the frozen/equilibrium switch at 1000 K.

## Fix (same continuous model; only the discretisation changes)
Applied identically to module 03 (`sims/03_engine_cycle/run.py`, `integrate_cycle`) and X5 (`scripts_run/xcheck.py`, `integrate`):
1. A grid node is inserted at θ_a = burn_angle(endgas_anchor_xb), and the anchor is taken at the state on that node.
2. The saturation cap at mid and right is evaluated on the no-evaporation predictor state at the same node (one extra state inversion per active node), not the isentropically compressed left state.
Both limits h → 0 are unchanged: the anchor still sits at x_b = 1e-3 and the cap is still saturation of the local gas. Production results shift by the old O(h) error, which is reported in RESULTS_FIX.md.

## Criteria for the re-run
**Unchanged.** A1, A1-pmax, A2, A3, A4 and A5 exactly as in `ACCEPTANCE_CRITERIA.md`, same points, same steps (2, 1, 0.5, 0.25), same `gci_study.py` (no edits). Output goes to `results_fix/`; the baseline `results/` is kept.
Every FAIL is reported as-is. Neither the criteria nor the fix is tuned after the run.
Caveat stated in advance: the fix removes the dominant O(h) term. Residual non-smooth events remain (the cap switching on/off inside a step, the knock-retard CA50 grid, and pmax sampled at nodes), so A2 may still fail for some quantity at a wet point.

## What a PASS means
Same as in ACCEPTANCE_CRITERIA.md: code-verified for these outputs, **not validated**. X5 is a re-implementation of the same scheme, so it is not an independent second engine. That needs item 3 (BDF/Radau engine).
