# Provenance – module 12 phase A
- Solver: OpenFOAM v2512 (ESI/OpenCFD), Debian package `openfoam2512` 2512.0-2 and `openfoam2512-tutorials`,
  apt source `deb [arch=amd64] https://dl.openfoam.com/repos/deb trixie main` (added by
  https://dl.openfoam.com/add-debian-repo.sh). Build string: `_bd2b6720-20260127 OPENFOAM=2512`.
- v2606 is in the same repo but only as 2606.0~rc2 (release candidate), so the newest *stable* v2512 was used.
- No container image: run natively on Grok Bot's box (Debian 13, 8 cores, Open MPI 5.0.7, 6 MPI ranks) per James's
  change of plan; the mail VPS / docker image path was not used.
- Base case: `$FOAM_TUTORIALS/lagrangian/sprayFoam/aachenBomb` (v2512), copied unchanged for A0 except
  decomposition 8 -> 6 ranks.
- CH3OH thermo: GRI-Mech 3.0 NASA-7 polynomial. Liquid properties: OpenFOAM built-in H2O, CH3OH.
- Repo base: commit b00342f, branch wme1-cfd.
