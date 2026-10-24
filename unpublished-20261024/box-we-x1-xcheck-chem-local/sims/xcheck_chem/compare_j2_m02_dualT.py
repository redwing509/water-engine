"""J2 comparison: Module 02 dual-temperature quantities, San Diego (Module 02 mechanism) vs AramcoMech 2.0 / CRECK C1-C3 HT.
Inputs  results/xcheck/j2_m02_dualT/{tad_ign_*.json, sl_creck.json}, results/xcheck/x1_dualT/x1_dualT_sandiego.json (S_L SD)
Output  results/xcheck/j2_m02_dualT/compare.{csv,json} + printed tables used in J2_REPORT.md
Tolerances (stated before running): T_ad +-0.5 %; S_L +-10 %; tau_ig factor 2 (|log10 ratio| <= 0.301);
the hot-minus-normal change must have the same sign in both engines."""
import csv, json, math
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
D = REPO / "results" / "xcheck" / "j2_m02_dualT"
TOL = dict(T_ad_1atm_K=("rel", 0.005), T_ad_TDC_K=("rel", 0.005), T_TDC_K=("rel", 0.005), tau_ig_s=("log", math.log10(2)), S_L_m_s=("rel", 0.10))


def load(fn):
    p = D / fn
    return json.loads(p.read_text())["rows"] if p.exists() else None


def ok(q, ref, val):
    kind, t = TOL[q]
    if ref is None or val is None: return None, None
    e = math.log10(val / ref) if kind == "log" else (val - ref) / ref
    return e, abs(e) <= t + 1e-12


def main():
    sd = load("tad_ign_sandiego.json") or []
    key = lambda r: (r["fuel"], r["w"], r["regime"], r.get("CR"))
    out, rows = {}, []
    for alt in ("aramco", "creck"):
        A = load(f"tad_ign_{alt}.json")
        if not A: continue
        ai = {key(r): r for r in A}
        for r in sd:
            a = ai.get(key(r))
            if a is None: continue
            for q in ("T_ad_1atm_K", "T_TDC_K", "T_ad_TDC_K", "tau_ig_s"):
                e, p = ok(q, r.get(q), a.get(q))
                rows.append(dict(engine=alt, qty=q, fuel=r["fuel"], w=r["w"], regime=r["regime"], CR=r["CR"], sandiego=r.get(q), other=a.get(q),
                                 err=e, PASS=p))
    # S_L: San Diego from the X1 dual-T sweep (same solver settings) vs CRECK
    x1 = json.loads((REPO / "results/xcheck/x1_dualT/x1_dualT_sandiego.json").read_text())["S_L"]
    sdl = {(r["fuel"], r["w"], r["T_u_K"]): r["S_L_m_s"] for r in x1 if r["status"] == "computed"}
    T = {"normal": 360.0, "hot": 400.0}
    for alt in ("creck", "aramco"):
        L = load(f"sl_{alt}.json")
        if not L: continue
        for r in L:
            e, p = ok("S_L_m_s", sdl.get((r["fuel"], r["w"], T[r["regime"]])), r["S_L_m_s"])
            rows.append(dict(engine=alt, qty="S_L_m_s", fuel=r["fuel"], w=r["w"], regime=r["regime"], CR=None,
                             sandiego=sdl.get((r["fuel"], r["w"], T[r["regime"]])), other=r["S_L_m_s"], err=e, PASS=p))
    # hot-minus-normal sign test per engine pair
    sign = []
    idx = {(r["engine"], r["qty"], r["fuel"], r["w"], r["CR"], r["regime"]): r for r in rows}
    for (eng, q, f, w, cr, reg), r in idx.items():
        if reg != "hot": continue
        n = idx.get((eng, q, f, w, cr, "normal"))
        if not n or None in (r["sandiego"], r["other"], n["sandiego"], n["other"]): continue
        ds, do = r["sandiego"] - n["sandiego"], r["other"] - n["other"]
        rs, ro = r["sandiego"] / n["sandiego"], r["other"] / n["other"]
        sign.append(dict(engine=eng, qty=q, fuel=f, w=w, CR=cr, ratio_hot_over_normal_sd=rs, ratio_hot_over_normal_other=ro,
                         same_sign=(ds > 0) == (do > 0)))
    with (D / "compare.csv").open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    summ = {}
    for eng in ("aramco", "creck"):
        for q in TOL:
            rr = [r for r in rows if r["engine"] == eng and r["qty"] == q and r["PASS"] is not None]
            ss = [s for s in sign if s["engine"] == eng and s["qty"] == q]
            if rr:
                summ[f"{eng}:{q}"] = dict(n=len(rr), n_pass=sum(r["PASS"] for r in rr), max_abs_err=max(abs(r["err"]) for r in rr),
                                          n_missing=sum(1 for r in rows if r["engine"] == eng and r["qty"] == q and r["PASS"] is None),
                                          sign_pairs=len(ss), sign_agree=sum(s["same_sign"] for s in ss))
    (D / "compare.json").write_text(json.dumps(dict(tolerances=TOL, summary=summ, rows=rows, hot_vs_normal=sign), indent=1) + "\n")
    for k, v in summ.items(): print(k, v)
    return summ


if __name__ == "__main__":
    main()
