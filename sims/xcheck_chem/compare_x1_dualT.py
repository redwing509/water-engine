"""Compare X1 dual-temperature results: AramcoMech 2.0 (independent) vs San Diego (baseline).

python -m sims.xcheck_chem.compare_x1_dualT  -> results/xcheck/x1_dualT/x1_dualT_compare.{md,csv}
Tolerances (X1 contract): T_ad +/-0.5 %, S_L +/-10 %. Same Cantera solver for both, so this is an
independent-MECHANISM check, not an independent-code check.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
D = REPO_ROOT / "results" / "xcheck" / "x1_dualT"
TOL = {"T_ad_K": 0.005, "S_L_m_s": 0.10}


def _idx(rows, key):
    return {(r["fuel"], r["w"], r["T_u_K"]): r.get(key) for r in rows}


def main():
    def load(mech):  # merge partial runs (x1_dualT_<mech>[_tag].json); later files win per case
        parts = [json.loads(p.read_text()) for p in sorted(D.glob(f"x1_dualT_{mech}*.json"))]
        if not parts:
            raise SystemExit(f"no results for {mech} in {D}")
        m = dict(parts[0])
        for k in ("T_ad", "S_L"):
            seen = {}
            for p in parts:
                for r in p[k]:
                    if r.get("status", "computed") == "computed" or (r["fuel"], r["w"], r["T_u_K"]) not in seen:
                        seen[(r["fuel"], r["w"], r["T_u_K"])] = r
            m[k] = list(seen.values())
        m["hosts"] = sorted({p["host"] for p in parts})
        return m
    ar, sd = load("aramco"), load("sandiego")
    rows, lines = [], []
    for kind, key, tol in (("T_ad", "T_ad_K", TOL["T_ad_K"]), ("S_L", "S_L_m_s", TOL["S_L_m_s"])):
        a, s = _idx(ar[kind], key), _idx(sd[kind], key)
        for k in sorted(set(a) | set(s), key=lambda k: (k[2], k[0], k[1])):
            va, vs = a.get(k), s.get(k)
            dev = (va - vs) / vs if (va is not None and vs) else None
            verdict = "n/a" if dev is None else ("PASS" if abs(dev) <= tol else "FAIL")
            rows.append(dict(quantity=key, fuel=k[0], w=k[1], T_u_K=k[2],
                             regime="hot" if k[2] >= 400 else "normal",
                             aramco=va, sandiego=vs, rel_dev=dev, tol=tol, verdict=verdict))
    with open(D / "x1_dualT_compare.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    def fmt(v, n=4):
        return "—" if v is None else f"{v:.{n}f}"
    L = lines.append
    L("# X1 dual-temperature cross-check: AramcoMech 2.0 vs San Diego 2016-12-14\n")
    L(f"Cantera {ar['cantera']}, 1 atm, phi = 1, FreeFlame mixture-averaged, two-stage refinement "
      f"(final ratio 2 / slope 0.05 / curve 0.1). Aramco SHA-256 (LF) `{ar['mechanism_sha256_lf'][:16]}…`.\n")
    L("Regimes: **normal** T_u = 320 K and 360 K (intake charge), **hot** T_u = 400 K (intake charge, "
      "X1 contract point). Source: `sims/dual_temp/regimes.py` (branch wme1-hiT) — coolant 363.15/388.15 K, "
      "wall 450/520 K, intake 320–360 / 400 K (MAHLE/VW SSP 222, SAE 960271, SAE 2010-01-0802, Heywood ch. 12, SPEC §6).\n")
    for q, title, n in (("T_ad_K", "Adiabatic flame temperature [K] (tol ±0.5 %)", 1),
                        ("S_L_m_s", "Laminar flame speed [m/s] (tol ±10 %)", 4)):
        L(f"\n## {title}\n")
        L("| regime | T_u [K] | fuel | w | Aramco | San Diego | dev | verdict |")
        L("|---|---|---|---|---|---|---|---|")
        for r in rows:
            if r["quantity"] != q:
                continue
            dev = "—" if r["rel_dev"] is None else f"{100*r['rel_dev']:+.2f} %"
            L(f"| {r['regime']} | {r['T_u_K']:.0f} | {r['fuel']} | {r['w']} | {fmt(r['aramco'], n)} | "
              f"{fmt(r['sandiego'], n)} | {dev} | {r['verdict']} |")
    # hot vs normal
    L("\n## Hot (400 K) vs normal (360 K) unburned temperature\n")
    L("| fuel | w | S_L 360 K Aramco | S_L 400 K Aramco | ratio | S_L ratio San Diego | T_ad 400−360 Aramco [K] |")
    L("|---|---|---|---|---|---|---|")
    aS, sS = _idx(ar["S_L"], "S_L_m_s"), _idx(sd["S_L"], "S_L_m_s")
    aT = _idx(ar["T_ad"], "T_ad_K")
    for fuel in ("CH3OH", "C2H5OH"):
        for w in (0.0, 0.3, 0.6):
            a3, a4 = aS.get((fuel, w, 360.0)), aS.get((fuel, w, 400.0))
            s3, s4 = sS.get((fuel, w, 360.0)), sS.get((fuel, w, 400.0))
            t3, t4 = aT.get((fuel, w, 360.0)), aT.get((fuel, w, 400.0))
            L(f"| {fuel} | {w} | {fmt(a3)} | {fmt(a4)} | {fmt(a4/a3 if a3 and a4 else None, 3)} | "
              f"{fmt(s4/s3 if s3 and s4 else None, 3)} | {fmt(t4-t3 if t3 and t4 else None, 1)} |")
    sl = [r for r in rows if r["quantity"] == "S_L_m_s"]
    ta = [r for r in rows if r["quantity"] == "T_ad_K"]
    cnt = lambda rs, v: sum(r["verdict"] == v for r in rs)
    L(f"\n**Totals:** T_ad {cnt(ta,'PASS')} PASS / {cnt(ta,'FAIL')} FAIL / {cnt(ta,'n/a')} n/a; "
      f"S_L {cnt(sl,'PASS')} PASS / {cnt(sl,'FAIL')} FAIL / {cnt(sl,'n/a')} n/a.\n")
    grid = [r for r in ar["S_L"] if r.get("grid_rel_change") is not None]
    if grid:
        L(f"Aramco grid indicator (stage1→stage2 S_L change): max {100*max(r['grid_rel_change'] for r in grid):.2f} %; "
          f"grid points {min(r['grid_points'] for r in grid)}–{max(r['grid_points'] for r in grid)}; "
          f"solve time {min(r['secs'] for r in grid):.0f}–{max(r['secs'] for r in grid):.0f} s per case "
          f"(1 thread/case, hosts {', '.join(ar['hosts'])}).\n")
    L("Ignition delay (X1 round 3: 40 bar, 800/900/1000 K, factor-1.5 tolerance) is not part of this sweep.\n")
    (D / "x1_dualT_compare.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0 if cnt(sl, "FAIL") + cnt(ta, "FAIL") == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
