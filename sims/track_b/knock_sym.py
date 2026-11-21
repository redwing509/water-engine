"""Step 3 of water-engine-box-20261025-1520: independent end-gas knock engine (engines/m03_cantera/knock.py)
applied to M03-CRN cases of the symmetric-DEI Module 03 rows.

  validate N          PRF91 / PRF97 normal DEI dry (w0, liquid) CR scan: Module 03 rows, then the end-gas
                      engine at CA50 = 15 CAD (most retarded eligible phasing) per CR -> independent klCR;
                      pass if klCR(PRF97) > klCR(PRF91) and |klCR_endgas - klCR_M03| <= 1.5 CR.
  rescore IN.jsonl OUT.jsonl N   rows (Module 03 dicts) -> end-gas knock flag at the row's own CA50;
                      row passes only if Module 03 (eligible, knock-free) AND the end-gas engine agree.
Executed, numerically cross-checked, not validated."""
import json, math, sys, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from sims.track_b import chains_sym as CS
from sims.track_b import run as R
from sims.track_b import fuels_b as FB

OUT = R.REPO / "results" / "track_b" / "knock_endgas"
CA50_RET = 15.0


def split_map():
    sp = {}
    for b in FB.BLENDS:
        x = FB.mole_fractions(b)
        m = {k: x[k] * FB.COMPONENTS[k][1] for k in x}
        s = sum(m.values())
        sp[b] = {k: v / s for k, v in m.items()}
    return sp


def endgas_check(r, ca50=None, dtheta=0.05):
    import engines.m03_cantera.knock as K
    E = R.crn_engine()
    credit = float(r.get("fuel_evap_intake_fraction") or 0.0) + float(r.get("fuel_evap_port_fraction") or 0.0)
    ca = float(r["ca50_used_deg"] if ca50 is None else ca50)
    t = time.time()
    c = E.Case(fuel=r["fuel"], cr=r["CR"], T_ivc=r["T_IVC_K"], m_fuel=r["fuel_mass_kg"], m_air=r["air_mass_kg"],
               m_residual=r["residual_mass_kg"], m_water=r["water_mass_kg"], e_intake=r["f_evap_intake_effective"],
               ca50_deg=ca, d1090_deg=r["burn_10_90_deg"], wall_T=r["chamber_wall_K"], heat_transfer="woschni",
               sat_blend_frac=R.CRN_SAT_BLEND, fuel_latent_credit=credit)
    eng = E.Engine(c)
    res = eng.run()
    wb = E.Wiebe(ca * E.RAD, r["burn_10_90_deg"] * E.RAD)
    crn_gas = E.build_gas(False)
    Y0, dropped = K.endgas_Y(crn_gas, eng.anchor["Y"], split_map())
    th0 = min(E.EVAP_END, wb.start)
    out = K.run_endgas(eng.trace, wb, Y0, theta0=th0, dtheta_deg=dtheta, rpm=E.RPM)
    out.update(ca50_deg=ca, crn_efficiency=res["efficiency"], crn_p_max_Pa=res["p_max_Pa"],
               y_dropped=dropped, endgas_seconds=time.time() - t)
    return out


def _m03(task):
    r = CS.point(dict(task, crn=False))
    return r


def _eg(args):
    r, ca50 = args
    base = {k: r.get(k) for k in ("fuel", "regime", "CR", "w", "water_mode", "eligible", "knock_free",
                                  "ca50_used_deg", "gross_indicated_efficiency", "_key")}
    try:
        base.update(endgas_check(r, ca50))
        base["endgas_status"] = "ok"
    except Exception as exc:  # recorded; never retried blindly
        base["endgas_status"] = f"failed: {type(exc).__name__}: {exc}"
    return base


def validate(n):
    OUT.mkdir(parents=True, exist_ok=True)
    import importlib
    D = importlib.import_module("sims.03_engine_cycle.dryevap_baseline")
    crs = [c for c in D.CR_B if 7.0 <= c <= 18.0]
    tasks = [dict(fuel=f, regime="normal", CR=c, w=0.0, mode="liquid", key=f"{f}|{c}") for f in ("PRF91", "PRF97")
             for c in crs]
    with ProcessPoolExecutor(n) as ex:
        rows = list(ex.map(_m03, tasks))
    with open(OUT / "validate_m03_rows.jsonl", "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, default=str) + "\n")
    ok = [r for r in rows if r.get("status") == "computed"]
    with ProcessPoolExecutor(n) as ex:
        eg = list(ex.map(_eg, [(r, CA50_RET) for r in ok]))
    with open(OUT / "validate_endgas.jsonl", "w") as fh:
        for e in eg:
            fh.write(json.dumps(e, default=str) + "\n")
    summ = {}
    for f in ("PRF91", "PRF97"):
        m = [r for r in rows if r["fuel"] == f]
        kl_m03 = max([r["CR"] for r in m if r.get("eligible")], default=None)
        e = sorted([x for x in eg if x["fuel"] == f and x["endgas_status"] == "ok"], key=lambda x: x["CR"])
        # independent klCR: highest CR below the first knocking CR (monotone scan)
        kl_eg = None
        for x in e:
            if x["knock"]:
                break
            kl_eg = x["CR"]
        summ[f] = dict(klCR_M03=kl_m03, klCR_endgas=kl_eg,
                       diff=None if None in (kl_m03, kl_eg) else kl_eg - kl_m03,
                       non_monotone=any(x["knock"] for x in e) and any((not x["knock"]) and x["CR"] > (kl_eg or 0)
                                                                      for x in e))
    v = summ["PRF97"]["klCR_endgas"] is not None and summ["PRF91"]["klCR_endgas"] is not None
    summ["ranking_PRF97_gt_PRF91"] = bool(v and summ["PRF97"]["klCR_endgas"] > summ["PRF91"]["klCR_endgas"])
    summ["within_1p5_CR"] = all(summ[f]["diff"] is not None and abs(summ[f]["diff"]) <= 1.5 for f in ("PRF91", "PRF97"))
    summ["PASS"] = summ["ranking_PRF97_gt_PRF91"] and summ["within_1p5_CR"]
    json.dump(summ, open(OUT / "VALIDATE.json", "w"), indent=1)
    import csv
    with open(OUT / "validate_endgas.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["fuel", "CR", "m03_eligible", "m03_knock_free", "ca50_endgas", "endgas_knock", "trigger",
                    "theta_knock_deg", "max_dTdt_K_s", "max_X_OH", "T0_K", "status"])
        for x in sorted(eg, key=lambda x: (x["fuel"], x["CR"])):
            w.writerow([x["fuel"], x["CR"], x.get("eligible"), x.get("knock_free"), x.get("ca50_deg"), x.get("knock"),
                        x.get("knock_trigger"), x.get("theta_knock_deg"), x.get("max_dTdt_K_s"), x.get("max_X_OH"),
                        x.get("T0_K"), x["endgas_status"]])
    print(json.dumps(summ, indent=1))


def rescore(inp, outp, n):
    rows = [json.loads(l) for l in open(inp) if l.strip()]
    rows = [r for r in rows if r.get("status") == "computed"]
    with ProcessPoolExecutor(n) as ex:
        eg = list(ex.map(_eg, [(r, None) for r in rows]))
    with open(outp, "w") as fh:
        for r, e in zip(rows, eg):
            m03_ok = bool(r.get("eligible"))
            eg_ok = e["endgas_status"] == "ok" and not e["knock"]
            e.update(m03_knock_free_eligible=m03_ok, endgas_knock_free=eg_ok,
                     engines_agree=(m03_ok == eg_ok) if e["endgas_status"] == "ok" else None,
                     row_pass=m03_ok and eg_ok)
            fh.write(json.dumps(e, default=str) + "\n")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "validate":
        validate(int(sys.argv[2]))
    elif cmd == "rescore":
        rescore(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif cmd == "one":
        f, c = sys.argv[2], float(sys.argv[3])
        r = _m03(dict(fuel=f, regime="normal", CR=c, w=0.0, mode="liquid"))
        print(r.get("status"), r.get("eligible"), r.get("ca50_used_deg"), r.get("burn_10_90_deg"))
        print(json.dumps(_eg((r, CA50_RET)), default=str))
