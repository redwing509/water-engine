# Model verification status (2026-10-24)

Standing rule: every published model must meet the peer-review standard. That means a VERIFICATION.md with tolerances stated in advance, step or grid convergence with GCI, an analytic or published benchmark, energy closure, and CI tests.

- Executed is not verified, and verified is not validated.
- Nothing listed below as partial or none counts toward the 2-engine rule.
- Nothing listed below as partial or none may be merged to `main`.

| Model | Repo / branch | Status | What is missing |
|---|---|---|---|
| 01 energy audit, 02 flame chem, 04 six-stroke, 05 Al-water | all model branches | partial | Only unit and regression tests exist (8–16 per branch). Missing: VERIFICATION.md, pre-stated tolerances, convergence study, benchmark vs. published data. |
| 03 engine cycle (0-D SI, RK2) | xcheck/cycle, rule/dual-temperature, wme1-* | partial | Pre-registered step study on `verify/x5-m03-step-convergence-20261024` (`verification/x5_m03/RESULTS.md`). Energy closure (A3) and ideal Otto (A4) PASS. GCI/order (A1, A2) FAIL: the scheme does not converge asymptotically at second order, although step sensitivity at 0.5° is ≤ 9e-5. Missing: diagnose the convergence, then a rerun or a revised criterion set pre-registered before rerunning. |
| X5 cycle cross-check (`scripts_run/xcheck.py`) | xcheck/cycle | partial, **not an independent engine** | It re-implements the same algorithm, and its ideal-Otto output is bit-identical to 03. Shows a step-independent bias of +0.72–0.76% vs 03 with no cause found. Missing: a method-independent second engine. |
| 06 carburetor, 07 CAD, 10 QD burn | rule/dual-temperature, wme1-dev/hiT/spray11, xcheck/chem | partial | No VERIFICATION.md, convergence study or benchmark. |
| 08 water chemistry | wme1-spray, publish/pc-wme1-spray-20261024 | partial | Unit tests only (oxygen-demand and enthalpy-basis fixes). Missing: benchmark vs. equilibrium reference and pre-stated tolerances. |
| 09 spray evaporation | wme1-spray09, wme1-hiT, wme1-spray11, publish/pc-wme1-dev-20261024 | partial | Unit tests only (three-fraction semantics on pc-dev). Missing: d²-law analytic check with pre-stated tolerance, time-step GCI. |
| 11 spray flame | wme1-hiT, wme1-spray11 | partial | No VERIFICATION.md, convergence study or benchmark. |
| dual_temp | wme1-hiT, wme1-spray11, rule/dual-temperature | partial | No VERIFICATION.md. |
| xcheck_chem (X1/J2 S_L, Aramco vs San Diego) | xcheck/chem | partial | This is a mechanism-to-mechanism cross-check, not verification of in-house numerics. Missing: pre-stated tolerance and grid-independence of the Cantera flame solves. |
| CFD cases (OpenFOAM M13 etc.) | wme1-cfd | none (in-house) | Third-party solver. Missing: mesh-convergence GCI and a time-step study with pre-stated tolerance. |
| Unpublished scripts archive | publish/unpublished-code-20261024 | none | This is an archive of run, compare and diagnostic scripts, not models. |

Queued verification work, with runtime estimates, is listed in the grokbot relay inbox (`ai-relay/grokbot/inbox`). No paid compute.
