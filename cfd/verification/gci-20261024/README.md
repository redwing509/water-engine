# Job #8 fine-mesh GCI levels (module 12 spray CFD)

Started on mail 2026-10-24 15:13 PDT (22:13Z) under `ai-job --owner grokbot --resource cpu-heavy` (James t75u: fine meshes run in parallel on mail).
Case inputs: identical to `cfd/runs/A1-BLEND` / `cfd/runs/A2-BLEND` at wme1-cfd ab7f03a except blockMesh cell counts (checked with diff before launch).
Pre-registered criteria: ACCEPTANCE_CRITERIA.md (committed before results).
Mail paths: /opt/water-engine/cfd/gci-20261024/{runs,finish.log,driver.out}.
Results land on this branch (verify/cfd-gci-fine-20261024) automatically when the driver finishes. Not merged to main: one engine only (OpenFOAM); the 2-engine and peer-review rules apply.
Remaining #8 work that is too big or blocked for mail (M13 port-spray GCI in both temperature regimes, time-step study) is packaged under /opt/gpu-queue on mail and on branch gpu-queue/20261024.
