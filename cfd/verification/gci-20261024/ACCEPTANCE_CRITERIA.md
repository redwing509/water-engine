# Job #8 (module 12 spray CFD) 3-mesh GCI: pre-registered acceptance criteria

Written and committed BEFORE the fine-mesh runs finished (Grok Bot, 2026-10-24 ~15:30 PDT, James t75u).
Do not edit after results exist; any change goes in a new dated section with the reason.

## Cases and meshes (uniform hex, 20 x 20 x 100 mm chamber, refinement ratio about 1.5 per level)
| level | cells (x y z) | N | A1-BLEND | A2-BLEND |
|---|---|---|---|---|
| r100 (base) | 41 x 41 x 100 | 168,100 | box run (2956 s) + mail re-run r100-mail | box run (8022 s) + mail re-run r100-mail |
| r150 | 62 x 62 x 150 | 576,600 | done on mail 2026-10-23 (A1-BLEND-fine, 6 ranks) | mail, 3 ranks |
| r225 (finest) | 92 x 92 x 225 | 1,904,400 | mail, 3 ranks | mail, 6 ranks |

Effective ratios: r21 = (N_r225/N_r150)^(1/3) = 1.49, r32 = (N_r150/N_r100)^(1/3) = 1.51.
Image opencfd/openfoam-default:2512 (digest sha256:33fb575aa9980d2bc42fd58c75ae698c489293ba30c991380fe3f899c622f319), sprayFoam,
all physics/numerics identical to wme1-cfd ab7f03a except blockMesh cell counts and rank count. Adaptive dt (maxCo 0.1) so dt refines with the mesh.

## Quantities (end of injection, from cfd/scripts/postprocess.py)
1. Liquid penetration (95 % liquid mass), mm.
2. Evaporated % of injected mass.
3. SMD (um).
Also reported, not gated: the same at the last write time.

## Method
Celik et al. (2008), J. Fluids Eng. 130(7) 078001, GCI with Fs = 1.25 (3 grids), fixed-point iteration for p with non-uniform r.
Primary GCI triplet uses the mail r100-mail / r150 / r225 runs (same machine). The box r100 run is reported as a cross-check of base-level reproducibility.

## Pass criteria (per quantity, per case)
- Monotone convergence (0 < R = e21/e32 < 1) and observed order 0.5 <= p <= 4.
- GCI_fine <= 5 % for penetration, <= 10 % for evaporated %, <= 10 % for SMD.
- Base-level reproducibility: |box r100 - mail r100| / mail r100 <= 3 % (penetration) and <= 5 % (evaporated %). If this fails, the
  stochastic parcel noise (rank-dependent random injection) is at least as big as the discretisation error and the GCI is reported as
  "noise-limited", not passed.
- Oscillatory or divergent triplets are reported as such, never as a pass.

## Status labels
Pass = numerically verified on mesh only (one engine: OpenFOAM). It is not a 2-engine verification and not experimental validation.
The 2-engine rule and peer-review rule (t72u) still apply before any main merge.
Dual-temperature rule: A1/A2 are NON-REACTING spray-chamber cases (chemistry off, combustion none), so the rule does not formally apply.
The combustion-relevant CFD (M13 port spray, port-wall 363 / 388 / 420 K) is queued for the GPU host with both regimes.
