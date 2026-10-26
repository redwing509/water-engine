"""Track A symmetric-DEI water-majority sweep (Claude reply-dryevap-verdict-and-trackb-rebase-20261025-2035, task 5;
Grok Bot, box, Oct 25 2026).

Every point (dry AND wet) runs with the dryevap DEI fuel-evaporation keys (fuel evaporated in the intake, dew-point
capped; M03-CRN gets the same fuel latent credit) - the fair, symmetric comparison accepted in 0bdf532.
  wet   : humid_evap intake (track_a_box0915.humid), bound (i) reported (bound (ii) kept in the raw file),
          CH3OH / C2H5OH, w 0.55 / 0.60 / 0.70, CR 9 .. 30, both regimes (normal: chamber wall 450 K, port wall
          363.15 K, T_intake 360 K, ~90 C coolant; hot: 520 K / 388.15 K / 400 K).
  dry   : DEI w = 0, CR 6 .. 30, T_intake normal 320 & 360 K, hot 400 K (extends the 0bdf532 grid 6..24 to 30 so
          the baseline is not grid-capped); baseline = best SPEC-eligible eta (dryevap 'rule'), checked against
          results/dryevap/baselines.csv.
  row   : each (fuel, regime, w) at its own knock-limited CR (highest SPEC-eligible CR, bound i) and at its best-eta
          eligible CR; both engines (Module 03 + M03-CRN with the same latent credit), cost via dryevap_report.compare.
Run:  python -m sims.03_engine_cycle.track_a_sym_box run WORKERS ;  ... report
Status: EXECUTED, numerically cross-checked (2 in-repo engines), NOT validated.
"""
import csv
import importlib
import json
import os
import sys
import time
from multiprocessing import get_context
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
OUT = REPO / "results" / os.environ.get("TA_OUT", "track_a_sym")  # env overrides: box queue
FUELS = tuple(os.environ.get("TA_FUELS", "CH3OH,C2H5OH").split(","))
WS = tuple(float(x) for x in os.environ.get("TA_WS", "0.55,0.6,0.7").split(","))
CR_WET = tuple(range(9, 31))
CR_DRY = tuple(range(6, 31))
DRY_T = {"normal": (320.0, 360.0), "hot": (400.0,)}
T_IN = {"normal": 360.0, "hot": 400.0}
PW = {"normal": 363.15, "hot": 388.15}


def specs():
    out = []
    for g in ("hot", "normal"):
        for f in FUELS:
            for cr in CR_DRY:
                for T in DRY_T[g]:
                    out.append(dict(step=4, kind="dry", fuel=f, regime=g, CR=cr, w=0.0, T_intake_K=T))
            for w in WS:
                for cr in CR_WET:
                    out.append(dict(step=4, kind="coupled", intake="humid_evap", fuel=f, regime=g, CR=cr, w=w,
                                    T_intake_K=T_IN[g], port_wall_K=PW[g]))
    return out


def key(s):
    return json.dumps(s, sort_keys=True)


def job(s):
    D = importlib.import_module("sims.03_engine_cycle.dryevap_baseline")
    return D.job(dict(track="A", variant="DEI", spec=s))


def run(workers):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "points.jsonl"
    done = set()
    if path.exists():
        for l in open(path):
            done.add(json.loads(l)["_spec"])
    todo = [s for s in specs() if key(s) not in done]
    print(f"{len(todo)} specs ({len(done)} done)", flush=True)
    t0 = time.time()
    with get_context("spawn").Pool(workers) as pool, open(path, "a") as fh:
        for i, (s, rows) in enumerate(zip(todo, pool.imap(job, todo))):
            fh.write(json.dumps(dict(_spec=key(s), rows=rows), default=float) + "\n"); fh.flush()
            print(f"{i + 1}/{len(todo)} {time.time() - t0:.0f}s {s['kind']} {s['fuel']} {s['regime']} CR={s['CR']} w={s['w']} | "
                  + " ".join(f"{r.get('bound') or 'dry'}:{(r.get('gross_indicated_efficiency') or 0):.4f}{'E' if r.get('eligible') else ''}"
                             for r in rows), flush=True)


def report(workers=3):
    D = importlib.import_module("sims.03_engine_cycle.dryevap_baseline")
    RP = importlib.import_module("sims.03_engine_cycle.dryevap_report")
    rows = []
    for l in open(OUT / "points.jsonl"):
        rows += json.loads(l)["rows"]
    ref = {(r["fuel"], r["regime"]): r for r in csv.DictReader(open(REPO / "results" / "dryevap" / "baselines.csv"))
           if r["track"] == "A" and r["variant"] == "DEI" and r["selection"] == "rule"}
    cache_p = OUT / "crn_cache.json"
    cache = json.loads(cache_p.read_text()) if cache_p.exists() else {}
    sel, md, csvrows = [], [], []
    for g in ("normal", "hot"):
        for f in FUELS:
            dry = [r for r in rows if r.get("kind") == "dry" and r["fuel"] == f and r["regime"] == g]
            base = RP.best(dry)
            items = [("DEI dry baseline", base)]
            for w in WS:
                wet = [r for r in rows if r.get("kind") == "coupled" and r.get("bound") == "i" and r["fuel"] == f
                       and r["regime"] == g and abs(r["w"] - w) < 1e-9]
                k = RP.klcr(wet)
                kl = next((r for r in wet if r.get("eligible") and r["CR"] == k), None)
                items += [(f"w {w} @ klCR", kl), (f"w {w} @ best eta", RP.best(wet))]
            sel.append((f, g, items))
    RP.with_crn([(r, "A") for _, _, it in sel for _, r in it if r is not None], cache)
    cache_p.write_text(json.dumps(cache, default=float))
    md.append("| fuel | regime | row | CR | T_in K | T_IVC K | eta M03 | eta CRN | gain pp M03 / CRN | power % | cost/mile % $0.10 / $0 (M03) | CRN cost/mile % | engines | verdict ($0.10 / $0) |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    chk = []
    for f, g, items in sel:
        base = items[0][1]
        rr = ref.get((f, g))
        if base and rr:
            chk.append(f"{f} {g}: sweep DEI rule CR {base['CR']} T_in {base['T_intake_K']} eta {base['gross_indicated_efficiency']:.5f}"
                       f" vs baselines.csv CR {rr['CR']} T_in {rr['T_intake_K']} eta {float(rr['eta']):.5f}"
                       f" (diff {base['gross_indicated_efficiency'] - float(rr['eta']):+.2e})")
        for lab, r in items:
            if r is None:
                md.append(f"| {f} | {g} | {lab} | - | - | - | - | - | no SPEC-eligible point | | | | | not run/failed |")
                csvrows.append(dict(fuel=f, regime=g, row=lab, status="no eligible point"))
                continue
            c = RP.compare(r, base) if lab != "DEI dry baseline" else {}
            fmt = lambda x, p="%+.2f": "-" if x is None else p % x
            md.append(f"| {f} | {g} | {lab} | {r['CR']} | {r['T_intake_K']:.0f} | {r.get('T_IVC_K', 0):.1f} | "
                      f"{r['gross_indicated_efficiency']:.4f} | {fmt(r.get('crn_efficiency'), '%.4f')} | "
                      f"{fmt(c.get('d_eta'))} / {fmt(c.get('d_eta_crn'))} | {fmt(c.get('power_pct'))} | "
                      f"{fmt(c.get('cost_mile_pct'))} / {fmt(c.get('cost_mile_free_pct'))} | {fmt(c.get('cost_mile_pct_crn'))} | "
                      f"{c.get('engines', '-')} | {c.get('verdict', '-')} / {c.get('verdict_free', '-')} |")
            csvrows.append(dict(fuel=f, regime=g, row=lab, CR=r["CR"], T_intake_K=r["T_intake_K"], T_IVC_K=r.get("T_IVC_K"),
                                eta=r["gross_indicated_efficiency"], eta_crn=r.get("crn_efficiency"), crn_status=r.get("crn_status"),
                                c1_pass=r.get("c1_pass"), **{k: v for k, v in c.items()}))
    keys = sorted({k for r in csvrows for k in r})
    with open(OUT / "track_a_sym_rows.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=keys); wr.writeheader(); wr.writerows(csvrows)
    txt = ["# Track A - symmetric DEI water-majority sweep (box, Oct 25 2026)", "",
           "Status: **EXECUTED, numerically cross-checked (Module 03 + M03-CRN, same toolchain), NOT validated.**",
           "All rows DEI (fuel evaporated in the intake, dew-point capped) for dry AND wet; humid_evap bound (i); "
           "normal = 450 K wall / 363 K port wall / T_in 360 K (~90 C coolant); hot = 520 K / 388 K / 400 K. "
           "CR grid 9-30 (wet), 6-30 (dry). Cost vs the fuel's DEI dry baseline from this sweep "
           "(sims/cost prices 2026-10-25; $0.10/gal water headline, $0 secondary). 'COST GAIN' only if power >= baseline "
           "AND cost lower in both engines.", "", "## DEI dry baseline check vs results/dryevap/baselines.csv", ""]
    txt += [f"* {x}" for x in chk] + ["", "## Rows", ""] + md + [""]
    (OUT / "TRACK_A_SYM.md").write_text("\n".join(txt))
    print("\n".join(txt))


if __name__ == "__main__":
    cmd = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    if cmd == "run":
        run(n)
    elif cmd == "report":
        report()
    elif cmd == "smoke":
        print(job(dict(step=4, kind="coupled", intake="humid_evap", fuel="CH3OH", regime="hot", CR=24, w=0.6, T_intake_K=400.0, port_wall_K=388.15)))
