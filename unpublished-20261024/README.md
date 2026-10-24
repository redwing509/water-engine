# Unpublished in-house code, archived 2026-10-24

**Verification status: not yet peer-review verified.** Nothing in this directory has been verified to the project's peer-review standard: there is no VERIFICATION.md, no pre-stated tolerances, no convergence/GCI study, and no CI. Nothing here counts toward the 2-engine rule.

## Why this exists

The project rule is that every model and finding should be public. This branch is a verbatim snapshot of model, cross-check and run-script code that existed only on the simulation server, on box clones, or in a PC worktree. It is preserved exactly as found; the only change is CRLF converted to LF. This branch is an archive and should not be merged into `main` in its current form. Each item should move to its proper feature branch once its owner has reviewed it.

## Exclusions

- Credentials and git-key setup scripts.
- `__pycache__` directories.
- Debug scratch: `_dbg_*`, `.scratch/`, `x2_debug*.py`, `logs/`.
- Large generated results and OpenFOAM run directories.
- Third-party mechanism files. For example, `creck_c1c3_ht.yaml` is CRECK/PoliMi and its redistribution licence is unconfirmed. Use `mechanisms_PROVENANCE.md.patch` to regenerate it.

## Index

### `pc-water-engine-xcheck/`

Source: PC worktree `water-engine-xcheck`, branch `xcheck/chem`, untracked files.

| File | Description |
|---|---|
| `sims/xcheck_cycle/run.py` | X5 independent 0-D SI cycle re-implementation, PC variant. It differs from every GitHub branch and from the server copy. |
| `scripts_run/x2_final_new.py` | X2 run script. |
| `results/xcheck/_cmp.json` | X2 run output. |

### `mail-opt-water-engine/`

Source: the simulation server's `/opt/water-engine`.

| File | Description |
|---|---|
| `code/sims/xcheck_cycle/run.py` | X5 server variant: SPEC §6 geometry and CoolProp water. It differs from the PC variant and from GitHub. |
| `code/scripts_run/x2_{compute,extract_hf,verify_thermo}.py` | X2 thermo cross-check scripts. |
| `cfd/run_case.sh`, `cfd/run_cfd.sh` | CFD run scripts. |
| `cfd/scripts/grokbot-20261024/*.sh` | CFD batch, case and restart-probe scripts. |
| `cfd/runs/M13-US20-coarse-mail/write_fields.py` | Field writer. It is identical to the CARB60 copy. |

The server's `code-spray/run.py` is an intermediate copy of `sims/08_water_chem/run.py`. It is superseded by the PC commits published on `publish/pc-wme1-spray-20261024`, so it is not included.

### `box-we-x1-xcheck-chem-local/`

Source: box clone on base commit 9bc59e9 (`origin/xcheck/chem`).

| File | Description |
|---|---|
| `sims/xcheck_chem/{run,compare}_j2_m02_dualT.py` | J2 cross-check of module 02, dual-temperature. |
| `results/xcheck/j2_m02_dualT/*.json` | J2 outputs. |
| `mechanisms_PROVENANCE.md.patch` | CRECK C1-C3 HT provenance, with SHA-256 checksums and ck2yaml conversion steps. |

### `box-we-x3-xcheck-x4-spray/`

Source: box clone on base commit 2f1db58 (`origin/wme1-spray09`).

| File | Description |
|---|---|
| `sims/xcheck_x4/compare_x4.py` | X4 spray cross-check. |
| `results/xcheck/m09_bias_diag.py` | Module 09 bias diagnostic. |
| `results/xcheck/x4_spray/*` | X4 outputs. |

### `box-water-engine-spray09/uncommitted.patch`

Uncommitted edits to `sims/09_spray_evaporation/{design_points,run}.py`, on base 2f1db58.

### `box-water-engine-cfd/`

Source: box clone on base e2481f7 (`origin/wme1-cfd`).

| File | Description |
|---|---|
| `cfd/port13/*` | M13 port-injection case generator, run scripts and post-processing. |
| `cfd/run_batch3.sh` | Batch run script. |
| `make_cases.py.patch` | Uncommitted edit to `make_cases.py`. |

## Reproduction

The scripts expect the layout of the branch named for each item, with `sims/common` available. They need Cantera ≥ 3.0 and CoolProp. The CFD scripts need OpenFOAM, the same version as on `wme1-cfd`. The paths inside the scripts are the server's (`/opt/water-engine`); adjust them before running.
