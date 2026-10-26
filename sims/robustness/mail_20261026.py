"""Claude job water-engine-mail-20261026-0715 (Grok Bot, mail VPS, Oct 26 2026). EXECUTED, cross-checked (Module 03 +
M03-CRN), NOT validated.

  gate     WORKERS   cool_frac 1.0 at the 14 Track B symmetric-DEI w 0 starts must reproduce summary_sym.json dry_eta /
                     dry_crn bit-identically (exit 3 otherwise; the sweep is then not launched).
  step3    WORKERS   cool_frac 0.7 (and 1.0 control) at EVERY Track B symmetric stop point: w 0 start + best_w, same
                     hardware CR, same water mode, both engines. Sign survives = gain(cf 0.7) has the same sign as
                     gain(cf 1.0) in Module 03 AND in M03-CRN.
  ch4 base WORKERS   CH4 Track B DEI hardware scan (dryevap CR grid 6-24, both regimes) + w 0 check.
  ch4 chains WORKERS CH4 Track B chains (normal+hot x liquid+humid_evap), dw 0.001, noise 3.3e-5 + CRN>0, cap 300.
                     CH4 is gaseous: no fuel evaporation in the dry baseline (h_fg 0, the DEI key changes nothing).
  report             CSVs for steps 2 and 3 (step 1 uses robust_20261026 report).
"""
import csv
import importlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
SYM = REPO / "results" / "track_b" / "symmetric_dei"
OUT = REPO / "results" / "mail_20261026"
CH4_OUT = REPO / "results" / "track_b" / "ch4_dei"


def _rb():
    return importlib.import_module("sims.robustness.robust_20261026")


def _summary():
    return json.loads((SYM / "summary_sym.json").read_text())


def gate(workers):
    RB = _rb()
    OUT.mkdir(parents=True, exist_ok=True)
    ref = {}
    for s in _summary():
        ref.setdefault((s["fuel"], s["regime"]), (s["CR"], s["dry_eta"], s["dry_crn"]))
    tasks = [dict(cf=1.0, fuel=f, regime=g, CR=float(v[0]), w=0.0, mode="liquid", key=f"gate/{f}/{g}")
             for (f, g), v in sorted(ref.items())]
    p = OUT / "gate_cf1_points.jsonl"
    p.unlink(missing_ok=True)
    RB._pool(tasks, workers, p)
    rows, bad = [], 0
    for l in open(p):
        r = json.loads(l)
        _, f, g = r["_key"].split("/")
        cr, e, c = ref[(f, g)]
        de = None if r.get("gross_indicated_efficiency") is None else r["gross_indicated_efficiency"] - e
        dc = None if r.get("crn_efficiency") is None or c is None else r["crn_efficiency"] - c
        ok = de == 0.0 and dc == 0.0
        bad += not ok
        rows.append(dict(fuel=f, regime=g, CR=cr, eta=r.get("gross_indicated_efficiency"), ref_eta=e, d_eta=de,
                         eta_crn=r.get("crn_efficiency"), ref_crn=c, d_crn=dc, bit_identical=ok, status=r.get("status")))
    with open(OUT / "gate_cf1.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"GATE {'PASS' if not bad else 'FAIL'}: {len(rows) - bad}/{len(rows)} bit-identical", flush=True)
    sys.exit(0 if not bad and len(rows) == 14 else 3)


def step3(workers):
    RB = _rb()
    OUT.mkdir(parents=True, exist_ok=True)
    tasks, seen = [], set()
    for s in _summary():
        for cf in (0.7, 1.0):
            for w, m in ((0.0, "liquid"), (float(s["best_w"] or 0.0), s["mode"])):
                k = f"cf{cf}/{s['fuel']}/{s['regime']}/{m if w else 'liquid'}/{w}"
                if k not in seen:
                    seen.add(k)
                    tasks.append(dict(cf=cf, fuel=s["fuel"], regime=s["regime"], CR=float(s["CR"]), w=w,
                                      mode=m if w else "liquid", key=k))
    RB._pool(tasks, workers, OUT / "step3_points.jsonl")


def _ch4():
    C = importlib.import_module("sims.track_b.chains_sym")
    C.FUELS = ("CH4",)
    C.OUT = CH4_OUT
    return C


def ch4(sub, workers):
    C = _ch4()
    CH4_OUT.mkdir(parents=True, exist_ok=True)
    if sub == "smoke":
        r = C.point(dict(fuel="CH4", regime="normal", CR=12.0, w=0.0, mode="liquid", crn=True, key="smoke/w0"))
        r2 = C.point(dict(fuel="CH4", regime="normal", CR=12.0, w=0.01, mode="humid_evap", crn=True, key="smoke/w001"))
        for x in (r, r2):
            print(json.dumps({k: x.get(k) for k in ("_key", "status", "reason", "eligible", "gross_indicated_efficiency",
                  "crn_status", "crn_efficiency", "T_IVC_K", "fuel_evap_intake_fraction", "m03_plus_crn_seconds")},
                  default=float), flush=True)
        sys.exit(0 if r.get("crn_status") == "ok" and r2.get("crn_status") == "ok" else 3)
    {"base": C.baselines, "chains": C.chains}[sub](workers)


def _load(p):
    return [json.loads(l) for l in open(p)] if Path(p).exists() else []


def report():
    RP = importlib.import_module("sims.03_engine_cycle.dryevap_report")
    OUT.mkdir(parents=True, exist_ok=True)
    pts = {r["_key"]: r for r in _load(OUT / "step3_points.jsonl")}
    rows = []
    for s in _summary():
        w = float(s["best_w"] or 0.0)
        row = dict(fuel=s["fuel"], regime=s["regime"], mode=s["mode"], CR=s["CR"], best_w=w,
                   gain_m03_cf1_chain=100 * (s["best_eta"] - s["dry_eta"]),
                   gain_crn_cf1_chain=None if s.get("best_crn") is None else 100 * (s["best_crn"] - s["dry_crn"]))
        for cf in (1.0, 0.7):
            b = pts.get(f"cf{cf}/{s['fuel']}/{s['regime']}/liquid/0.0")
            t = pts.get(f"cf{cf}/{s['fuel']}/{s['regime']}/{s['mode'] if w else 'liquid'}/{w}")
            ok = b and t and b.get("status") == "computed" and t.get("status") == "computed"
            c = RP.compare(t, b) if ok and w else {}
            row[f"gain_m03_cf{cf}"] = c.get("d_eta") if w else 0.0
            row[f"gain_crn_cf{cf}"] = c.get("d_eta_crn") if w else 0.0
            row[f"cost_mile_pct_cf{cf}"] = c.get("cost_mile_pct")
            row[f"status_cf{cf}"] = "computed" if ok else f"FAILED: {(t or {}).get('reason') or (b or {}).get('reason') or 'missing'}"
        row["cf1_reproduces_chain"] = (row["gain_m03_cf1.0"] is not None
                                       and abs(row["gain_m03_cf1.0"] - row["gain_m03_cf1_chain"]) < 1e-9)
        sg = lambda x: None if x is None else (x > 0) - (x < 0)
        row["sign_survives"] = (None if row["gain_m03_cf0.7"] is None else
                                sg(row["gain_m03_cf0.7"]) == sg(row["gain_m03_cf1.0"])
                                and sg(row["gain_crn_cf0.7"]) == sg(row["gain_crn_cf1.0"]))
        rows.append(row)
    with open(OUT / "step3_cf07_stop_points.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    # step 2 CH4
    rows2 = []
    sp = CH4_OUT / "summary_sym.json"
    for s in (json.loads(sp.read_text()) if sp.exists() else []):
        f = CH4_OUT / s["file"]
        steps = _load(f)
        best = next((r for r in steps if abs(r.get("w", -1) - (s["best_w"] or 0.0)) < 1e-9), None)
        dry = next((r for r in steps if r.get("w") == 0.0), None)
        c = RP.compare(best, dry) if best and dry and (s["best_w"] or 0) > 0 else {}
        rows2.append(dict(fuel="CH4", regime=s["regime"], mode=s["mode"], CR=s["CR"], best_w=s["best_w"], steps=s["steps"],
                          stop_reason=s["stop_reason"], gain_m03_pp=None if s.get("best_eta") is None else 100 * (s["best_eta"] - s["dry_eta"]),
                          gain_crn_pp=None if s.get("best_crn") is None else 100 * (s["best_crn"] - s["dry_crn"]),
                          engines=c.get("engines"), cost_mile_pct=c.get("cost_mile_pct"),
                          cost_mile_free_pct=c.get("cost_mile_free_pct"), verdict=c.get("verdict"),
                          price="cng 3.10 USD/GGE (AFDC Jul 2026, cost.py prices_20261025.json)",
                          dry_fuel_evap="none (gaseous fuel)"))
    if rows2:
        with open(OUT / "step2_ch4_chains.csv", "w", newline="") as fh:
            wr = csv.DictWriter(fh, fieldnames=list(rows2[0])); wr.writeheader(); wr.writerows(rows2)
    print(f"step3 rows {len(rows)}, step2 rows {len(rows2)}", flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "gate":
        gate(int(a[1]))
    elif a[0] == "step3":
        step3(int(a[1]))
    elif a[0] == "ch4":
        ch4(a[1], int(a[2]) if len(a) > 2 else 1)
    elif a[0] == "report":
        report()
