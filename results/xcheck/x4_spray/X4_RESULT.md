# X4 — third spray model for the Module 09 vs CFD cross-check (box-queue 20261024-1230, J3)

Status: **EXECUTED. Module 09 NOT VERIFIED against CFD at the pre-stated tolerance. Not validated (no experiment).**

## Pre-stated tolerance
From job `water-engine-xcheck-20261023-1445` (X4) and hard-coded as `TOL = 0.15` in
`sims/xcheck_x4/compare_x4.py` (written 13:26 PDT, before the last three CFD runs finished at 13:55 PDT):
Module 09 evaporated fraction must agree with CFD within **±15 % relative**, at EOI and at end of run.
Module 09 is rerun at each CFD variant's own SMD at EOI, so breakup-model SMD differences are not charged to Module 09.

## CFD variants (OpenFOAM v2512 sprayFoam, aachenBomb-derived, coarse mesh, 4 ranks on the box)
| tag | phaseChangeModel | breakupModel |
|---|---|---|
| KHRT (base, wme1-cfd) | liquidEvaporationBoil | ReitzKHRT |
| RD | liquidEvaporationBoil | ReitzDiwakar |
| LE-RD | liquidEvaporation | ReitzDiwakar |
Exact dictionary changes: `sims/xcheck_x4/cases/*.diff` (nothing else differs: mesh, injector, chemistry, time step identical).

## PASS/FAIL (ratio = Module 09 / CFD evaporated %)
| case | CFD model | SMD@EOI µm | CFD EOI % | M09 EOI % | ratio EOI | CFD end % | M09 end % | ratio end | EOI | end |
|---|---|---|---|---|---|---|---|---|---|---|
| A1-H2O | KHRT | 125.7 | 0.359 | 0.558 | 1.56 | 0.506 | 0.758 | 1.50 | FAIL | FAIL |
| A1-H2O | RD | 65.2 | 0.851 | 1.414 | 1.66 | 1.199 | 1.872 | 1.56 | FAIL | FAIL |
| A1-H2O | LE-RD | 65.4 | 1.085 | 1.409 | 1.30 | 1.509 | 1.866 | 1.24 | FAIL | FAIL |
| A2-BLEND | KHRT | 22.9 | 21.40 | 32.90 | 1.54 | 39.84 | 51.45 | 1.29 | FAIL | FAIL |
| A2-BLEND | RD | 18.0 | 25.92 | 41.77 | 1.61 | 47.20 | 61.89 | 1.31 | FAIL | FAIL |
| A2-BLEND | LE-RD | 16.9 | 37.04 | 44.25 | 1.19 | 58.43 | 64.74 | 1.11 | FAIL | **PASS** |

1 of 12 comparisons pass. Module 09 over-predicts evaporation in every case (+11 % to +66 %).

## CFD model spread (end of run)
- A1-H2O: 0.506–1.509 % (max/min **2.98×**) across the three spray models.
- A2-BLEND: 39.8–58.4 % (max/min **1.47×**). Module 09 end values at each CFD SMD all lie inside the CFD band widened by 15 % for A2-BLEND; only KHRT for A1-H2O.
- The CFD's own spray-submodel sensitivity is far larger than the ±15 % criterion, so the coarse-mesh CFD is not a tight reference.
  The LE-RD (no boiling branch) variant is closest to Module 09's evaporation physics and gives the best agreement (1.11–1.30).

## Bias bounds (Module 09 sensitivity, end of run)
Confining vapour to the spray cone lowers M09 by 1–11 %; halving initial slip lowers it by 3–18 % (see `x4_summary.json`
fields `m09_cone_end_pct`, `m09_halfslip_end_pct`). Neither bias alone closes the gap for the KHRT/RD variants.

## Verdict
Module 09 vs CFD is **not verified** (fails ±15 % in 11/12). The disagreement is dominated by (a) Module 09's systematic
over-prediction and (b) spray-model uncertainty in the CFD itself (1.5–3× spread). The 2-engine rule is not met; nothing goes to main.
Next: fine-mesh LE-RD runs on mail (ai-job) and the Module 09 d²-law analytic test + time-step GCI (verification queue item 4).

Dual-temperature note: these are non-reacting constant-volume spray-bomb cases at the CFD chamber conditions; they are not
combustion runs, so the normal/hot regime rule does not apply here.

## Files
- `sims/xcheck_x4/compare_x4.py` — post-processing (reads CFD logs with the CFD repo's own `scripts/postprocess.py` parser)
- `results/xcheck/x4_spray/x4_summary.json`, `x4_timeseries.csv` — numbers above
- `results/xcheck/m09_bias_diag.py` — bias bound logic
- CFD run directories (not committed, ~1.4 GB): `/workspace/water-engine-cfd/cfd/runs/X4-*` on the box; log `/workspace/self-jobs/j3/run.log`
Reproduce: `python -m sims.xcheck_x4.compare_x4 --cfd <water-engine-cfd>/cfd` (≈85 s).
