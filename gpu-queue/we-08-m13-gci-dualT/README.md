# we-08-m13-gci-dualT — remainder of queue item #8 (M13 3-mesh GCI, both temperature regimes)

Status: **BLOCKED + waiting for James's HF hardware.** The M13 coarse case still dies (SIGFPE in the k-epsilon
matrix ~1 ms after SOI; latest coarse attempt failed at 2026-10-24 21:59 UTC) and `cfd/port13` is not committed
to any branch yet. When the M13 owner (Claude) has a coarse run that completes and commits it, set `M13_REF` to
that commit and run `GENERATE_ONLY=1` once (meshes + fields only, ~20 min) before the full job.

## Honest hardware note — CPU job; a GPU buys ~nothing
reactingParcelFoam time goes to Lagrangian parcels, the wall-film region, k-epsilon and thermo, all CPU-only.
A GPU (petsc4Foam + PETSc CUDA/AmgX, or OGL/Ginkgo) only offloads the pressure solve; at <1–3 M cells the
realistic overall gain is **1.0–1.3x**, and swapping solvers inside a GCI changes the numerics. So the GCI runs
CPU-only. `Dockerfile.gpu-ab` is an optional, untested image to MEASURE the GPU gain on one case, nothing more.

| HF flavor | vCPU / RAM | Matrix A wall time | approx. cost* |
|---|---|---|---|
| cpu-performance (recommended) | 32 / 256 GB | ~12–15 h | ~$25–30 |
| a10g-largex4 / l40sx4 (only if James wants a GPU box anyway) | 48 / 184–382 GB | ~9–11 h | ~$50–90 |
| cpu-xl | 16 / 124 GB | ~24–30 h | ~$25–30 |
\* HF list prices 2026-10-24; paid compute is James's decision. Matrix B adds ~3–4 h on 32 vCPU.

## What runs
Matrix A (GCI): US20 x {coarse, med, fine} x {normal 363/360 K, hot 388/400 K} = 6 runs (fine at 16 ranks,
med 8, coarse 4). Matrix B (regime spread, med mesh): CARB60 x {normal, hot, heated 420/400 K} + US20 heated = 4 runs.
Runtime basis: coarse M13 reached 9.6 ms of 23 ms in 4,505 s on 2 ranks before failing (peak RSS 368 MB), so
coarse ~3 h/2 ranks; med ~4x and fine ~16x coarse work. RAM: fine ~3–6 GB/run, total < 30 GB. VRAM: 0.
All estimates ±50 % until a coarse run completes.

## Files
`Dockerfile` (pinned opencfd/openfoam-default:2512@sha256:33fb575a… + git/python3), `run.sh` (fetches cfd/port13 at
M13_REF, generates, runs with a rank-budget scheduler, GCI, pushes), `gen_m13_case.py` (mesh level + regime
overrides without editing the committed generator), `gci_m13.py`, `push_results.sh`, `ACCEPTANCE_CRITERIA.md`,
`Dockerfile.gpu-ab` (optional/experimental).

## Launch (James; nothing has been launched)
```
hf jobs run --flavor cpu-performance --timeout 24h --secrets GH_TOKEN -e M13_REF=<commit> -e MATRIX=A \
  opencfd/openfoam-default:2512 bash -c 'apt-get update -qq && apt-get install -y -qq git python3-numpy; \
  git clone -q --depth 1 -b gpu-queue/20261024 https://github.com/redwing509/water-engine /q && \
  bash /q/gpu-queue/we-08-m13-gci-dualT/run.sh'
```
or build `Dockerfile`, push it to a registry/HF Docker Space James controls, and run that image.

## Results return path
New branch `hf-results/<RUN_ID>` of redwing509/water-engine, folder `cfd/verification/hf/<RUN_ID>/`
(gci_summary.json, case_meta, run.status, post.json, log tails, postProcessing tarballs). Never main/wme1-cfd,
never force. Merged only after 2-engine/peer review. Secret: **GH_TOKEN** (fine-grained PAT, redwing509/water-engine
only, Contents read/write), read from env via GIT_ASKPASS, never stored.
