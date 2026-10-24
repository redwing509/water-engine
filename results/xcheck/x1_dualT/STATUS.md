# X1 dual-temperature sweep: status (Grok Bot takeover, 2026-10-24)

- Hermes job "X1 flame width sweep Aramco" (mail, ai-job water-engine, 18:29:02Z) and
  "X1 T_ad/S_L CH3OH/C2H5OH AramcoMech2.0" (18:12:51Z) both failed with rc=1 in 0 s:
  `ModuleNotFoundError: No module named 'sims'`. The scripts were run by file path over ssh with cwd=/root
  and no PYTHONPATH. Fix: `run_x1.py` and `run_x1_dualT.py` bootstrap the repo root on sys.path; run
  them as `python -m sims.xcheck_chem.<script>` from the repo root.
- The second problem Hermes reported ("FreeFlame hangs >10 min") is cost, not a hang. AramcoMech 2.0 has
  497 unknowns per grid point, so one banded Jacobian at about 170–230 points needs 6–14 GB and minutes of
  CPU. Cold-start solves did not finish in 30 min on the box, and 7 parallel workers ran it out of
  memory. The sweep now seeds each Aramco solve from the converged San Diego flame (initial guess only),
  caps memory per worker, and runs on mail under `ai-job --resource cpu-heavy`.
- San Diego results (all 18 S_L cases, 24 T_ad cases): `x1_dualT_sandiego.json` (box, 90 s).
- Aramco results: `x1_dualT_aramco_mail*.json` are added when the mail runs finish. Then
  `python -m sims.xcheck_chem.compare_x1_dualT` writes `x1_dualT_compare.{md,csv}` with the PASS/FAIL table
  (T_ad ±0.5 %, S_L ±10 %) and the hot-vs-normal comparison.
- Aramco at T_u = 320 K is not scheduled because of memory and CPU cost. Normal = 360 K and hot = 400 K are
  the dual-T comparison points; San Diego also covers 320 K.
