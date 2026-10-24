# Module 09 verification: pre-registered acceptance criteria (queue item 4, 2026-10-24)

Committed BEFORE any run of verification/m09/verify_m09.py. Base: origin/wme1-spray09 7fc305f.
Labels: these are numerical VERIFICATION checks only (code vs analytic, discretisation convergence). Nothing here is VALIDATED against experiment.

Module 09 integrates with scipy BDF (adaptive step, production rtol = 1e-7), so a fixed "time step" does not exist. The time-discretisation study therefore covers (a) integrator tolerance and (b) the two explicit discretisations: injection packets in time (chamber mode) and Rosin-Rammler size classes.

## V1 d2-law analytic (constant properties, Sh = 2, fixed T_d, infinite gas)
Exact: d^2(t) = d0^2 - K t, K = 8 rho_g D ln(1+B_M) / rho_l.
Matrix: d0 in {20, 50, 100} um x (Ys, Yinf) in {(0.05, 0), (0.20, 0.02)}, rtol 1e-9, 9 samples from 10 % to 90 % of the lifetime.
- V1a: max |d2_model - d2_exact| / d2_exact <= 1e-4 at every sample of every case (the production check uses 2e-2).
- V1b: error shrinks with rtol: max rel err at rtol 1e-9 <= max rel err at rtol 1e-6 (reported for 1e-5..1e-9).
- V1c: d^2 vs t linear-fit R^2 >= 0.999999 and fitted slope within 1e-4 of K.

## V2 integrator-tolerance convergence (full run_case chain)
Cases: carb_venturi w=0.6, psi_3bar w=0.6, ultrasonic_120kHz w=0.0, at the REFERENCE condition (360 K, 30 m/s, 0.2 m).
rtol in {1e-5, 1e-6, 1e-7 (production), 1e-8, 1e-9}; reference = 1e-9.
- V2: |Q(1e-7) - Q(1e-9)| <= 0.05 percentage points for evaporated_IVC_pct, evaporated_spark_pct, wall_impinged_pct; <= 1e-3 relative for SMD_spark_um and T_spark_K.

## V3 injection-packet GCI (chamber mode, A1-H2O and A2-CH3OH metadata, SMD 30 um, 8 classes)
packets in {10 (production), 20, 40, 80}, r = 2; Celik et al. 2008 (Fs = 1.25) on the finest triplet (20/40/80).
Quantities: evaporated % at end of injection and at t_end = 10 ms.
- V3a: GCI_fine <= 1 % (relative) for each quantity, OR absolute change 80 vs 40 <= 0.05 pp when the value is within round-off of monotone convergence.
- V3b: the production setting (10 packets) is within 1 pp of the Richardson-extrapolated value (reported as a production-error estimate).
- Observed order p is reported; no criterion on p (piecewise-constant injection gives p ~ 1 expected).

## V4 size-class GCI (run_case, same cases as V2)
rr_classes in {8 (production), 16, 32, 64}, r = 2, GCI on 16/32/64.
- V4a: GCI_fine <= 1 % (relative) for evaporated_spark_pct (when > 1 %) and SMD_spark_um.
- V4b: production (8 classes) within 2 pp of the extrapolated evaporated_spark_pct (reported).

Overall PASS = V1a, V1b, V1c, V2, V3a and V4a all pass. Production-error estimates (V3b, V4b) are reported and flagged if exceeded, but they do not fail verification. They would feed a caveat or a production-setting change request to Claude.
Compute: at most 4 processes, OMP_NUM_THREADS=1.

## Deviation (committed before the first run)
V3 uses **A2-BLEND** (x_CH3OH 0.4) instead of A2-CH3OH, because only A1-H2O and A2-BLEND phase-A metadata exist in the repo (xcheck/x4-spray cases). The criteria are unchanged.

## Deviation 2 (2026-10-24 ~14:45 PDT, committed before the re-run; no V3 results had been seen)
The first run was aborted. The A2-BLEND 80-packet chamber case reached 4.7 GB RSS, which is over the box's 4 GB budget. In a capped probe it failed allocating the dense BDF Jacobian: state ~1987, so 80 packets x 8 classes builds a dense ~2000x2000 LU in module 09. Diagnosis: memory grows as (packets x classes)^2 because the Jacobian is dense. This is a performance limitation of module 09, not a correctness issue. It is flagged to Claude: supply a `jac_sparsity` (block-diagonal per packet plus gas coupling).
The V3 packet ladder therefore becomes **{5, 10 (production), 20, 40}**, with GCI on 10/20/40 (r = 2). V3a's fallback is |40 - 20| <= 0.05 pp. V3b compares production (10) with the extrapolated value from that triplet. Thresholds are unchanged.
