"""X4 bias diagnostic for module 09's CFD cross-check (0-D chamber).
Bias 1 (spray-cone saturation): 0-D mixes vapour into the whole 8e-6 m3 chamber;
  in the CFD the vapour stays near the spray cone. Sensitivity: gas volume = cone
  volume pi (L tan th)^2 L / 3 at the CFD end-of-run penetration L, th = 10 deg
  (sprayCloudProperties thetaOuter), air mass scaled with volume.
Bias 2 (held relative velocity): 0-D droplets start at U_bernoulli into quiescent
  gas; in the CFD the entrained gas co-flows, so slip decays faster. Sensitivity:
  initial slip = 0.5 U_bernoulli.
Diagnostic only (sensitivity bounds); nominal module 09 results unchanged.
usage: python -m results.xcheck.m09_bias_diag <cfd_results_dir> <out.json>  (run from repo root)"""
import json, math, sys
import numpy as np
import importlib
R = importlib.import_module("sims.09_spray_evaporation.run")

def end_evap(meta, smd, t_end):
    s = R.chamber_run(meta, smd, t_end, "wilson")
    return 100 * s[-1]["evaporated_frac"]

cfd = R.read_cfd(sys.argv[1]); out = {}
for c in ["A1-H2O", "A2-BLEND", "A1-BLEND", "A2-H2O", "A1-CH3OH", "A2-CH3OH"]:
    if c not in cfd: continue
    meta = dict(cfd[c]["meta"]); smd = cfd[c]["summary"]["SMD_eoi_um"] * 1e-6
    t_end = float(cfd[c]["t"][-1]); e_cfd = float(cfd[c]["evap"][-1])
    base = end_evap(meta, smd, t_end)
    L = float(cfd[c]["pen"][-1]) * 1e-3
    Vc = math.pi * (L * math.tan(math.radians(10))) ** 2 * L / 3
    V0 = R.CFD_CHAMBER_V_m3
    R.CFD_CHAMBER_V_m3 = Vc; cone = end_evap(meta, smd, t_end); R.CFD_CHAMBER_V_m3 = V0
    m2 = dict(meta); m2["U_bernoulli_m_s"] = 0.5 * meta["U_bernoulli_m_s"]
    slip = end_evap(m2, smd, t_end)
    out[c] = dict(t_end_ms=1e3 * t_end, evap_cfd_pct=e_cfd, evap_m09_pct=base,
                  evap_m09_cone_volume_pct=cone, cone_volume_over_chamber=Vc / V0,
                  evap_m09_half_slip_pct=slip, penetration_end_mm=L * 1e3)
    print(c, out[c], flush=True)
json.dump(out, open(sys.argv[2], "w"), indent=1)
