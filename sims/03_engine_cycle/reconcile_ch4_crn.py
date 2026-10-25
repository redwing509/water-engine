"""Track A reconcile: M03-CRN for the CH4 rows (PR #8 engine has no CH4; uses Track B (PR 9) sims.track_b.run.crn,
which registers CH4). Run with a PR 9 checkout on sys.path:  PR9=/path/to/pr9 python reconcile_ch4_crn.py"""
import csv, json, sys
import os
sys.path.insert(0, os.environ.get("PR9", "../pr9"))
from sims.track_b import run as R
rows = list(csv.DictReader(open("results/03_engine_cycle/reconcile_dualtemp/points.csv")))
out = []
for r in rows:
    if r["fuel"] != "CH4":
        continue
    d = {k: r[k] for k in ("fuel", "status")}
    for k in ("CR", "T_IVC_K", "fuel_mass_kg", "air_mass_kg", "residual_mass_kg", "water_mass_kg",
              "f_evap_intake_effective", "ca50_used_deg", "burn_10_90_deg", "chamber_wall_K", "gross_indicated_efficiency", "peak_pressure_Pa"):
        d[k] = float(r[k])
    c = R.crn(d)
    c.update(kind=r["kind"], regime=r["regime"])
    print(json.dumps(c, default=float), flush=True); out.append(c)
json.dump(out, open("results/03_engine_cycle/reconcile_dualtemp/ch4_crn.json", "w"), indent=1, default=float)
