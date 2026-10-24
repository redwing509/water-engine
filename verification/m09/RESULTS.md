# Module 09 verification (queue item 4) - results

Status: **EXECUTED. overall_pass = false (V4a fails). Code-verification only; not validated.**
Run on the box by the verification-queue-20261024 worker on 2026-10-24 (runtime 145.5 s); the worker died before
committing. These results are committed unchanged by Grok Bot during reply-verification-20261024-1430 (no rerun).
Criteria: `ACCEPTANCE.md` (pre-registered, c3e8e7c; deviations 923a5cd, ca4ca88).

| check | result |
|---|---|
| V1 d2-law analytic (single droplet) | PASS: V1a/V1b/V1c; max rel. error 3.6e-7 at rtol 1e-9; error falls with rtol |
| V2 integrator tolerance, full run_case chain | PASS: all quantities, metric <= 1e-6 |
| V3 injection-packet GCI (5/10/20/40, deviation 2) | PASS: V3a; no V3b flags |
| V4a size-class GCI (8/16/32/64) | **FAIL**: SMD_spark_um does not converge with class count (GCI 195-286 %, or undefined at the ultrasonic case where most classes are fully evaporated). evaporated_spark_pct changes by <= 0.1 % between 8 and 64 classes, but its observed order is negative (non-asymptotic), so GCI is not meaningful; production (8-class) error is <= 0.57 pp vs the 64-class value |

Reading: the evaporation integrator and d2-law core are code-verified. The spark-timing SMD is a poorly posed output for a
discrete Rosin-Rammler class set (classes vanish one by one), so it should not be used as a model output without a
continuous-distribution treatment. Evaporated fraction is numerically settled to well under the CFD model spread
(1.5-3x, xcheck/x4-spray 06abb30). Module 09 physics is **unverified** against an independent engine (X4: 1/12 PASS).

Files: `verify_m09.py`, `results/report.json`, `results/raw.json`.
