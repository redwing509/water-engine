# Job #8 3-mesh GCI result (Grok Bot, 2026-10-25 ~03:05 PDT)
Evaluated exactly per ACCEPTANCE_CRITERIA.md (Celik 2008, Fs 1.25, r21 1.49, r32 1.51), quantities at end of injection
(A1 5.0 ms, A2 2.0 ms), triplet = mail r225 / r150 / r100-mail. Script gci.py, raw output gci_result.json.

| case | qty | r225 | r150 | r100 | R | p | GCI_fine % | status |
|---|---|---|---|---|---|---|---|---|
| A1 | penetration mm | 97.14 | 97.24 | 97.12 | -0.86 | 0.38 | 0.79 | oscillatory |
| A1 | evaporated % | 0.729 | 0.745 | 0.729 | -1.00 | 0.01 | n/a | oscillatory |
| A1 | SMD um | 124.7 | 123.8 | 126.0 | -0.39 | 2.31 | 0.56 | oscillatory |
| A2 | penetration mm | 53.71 | 50.97 | 51.24 | -10.0 | 5.97 | 0.65 | oscillatory |
| A2 | evaporated % | 20.85 | 21.14 | 21.22 | 3.91 | 3.58 | 0.56 | divergent |
| A2 | SMD um | 23.90 | 23.33 | 22.90 | 1.33 | 0.82 | 7.77 | divergent |

Base reproducibility (box r100 vs mail r100): A1 pen 0.07 %, evap 0.82 %, SMD 0.33 %; A2 pen 0.06 %, evap 0.84 %, SMD 0.15 % -> PASS.

Verdict (pre-registered rules): NO quantity passes the GCI criteria (all triplets oscillatory or divergent). Reported as such.
Interpretation (not a pass): A1 is mesh-insensitive within 0.1 % (penetration) and 1.8 % (SMD) across a 11x cell-count range, the same size as
parcel noise, so A1 is noise-limited rather than mesh-limited. A2 is still mesh-dependent: penetration jumps +5.4 % at r225 and SMD rises
about 2 % per level without converging. Next: A2 at r225 with 2-3 random-seed repeats to separate parcel noise from mesh error, and/or a
4th level (r340) on the GPU host. One engine (OpenFOAM sprayFoam) only.
