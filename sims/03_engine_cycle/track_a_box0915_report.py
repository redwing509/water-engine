"""Report for track_a_box0915.py: best rows (own knock-limited CR), M03-CRN cross-check of every best row,
cost metric vs best dry (same fuel, same regime), Module 11 misfire flags, port-wall flip scan.
Writes results/track_a_box/{points.csv, best_rows.csv, port_wall.csv, misfire_flip_scan.csv, REPORT.md}.
M03-CRN case for a coupled row: evap_mode 'coupled', f_ivc = f_evap_intake_effective (realised, incl. port
evaporation), f_spark = evaporated_fraction_spark (realised), spark_deg = liquid_freeze_deg (realised freeze angle);
CA50 / burn duration from Module 03 (pattern of engines/m03_cantera/compare_coupled.case, realised fractions).
"""
import csv
import importlib
import json
import time
from multiprocessing import get_context

from sims.cost import cost as COST

A = importlib.import_module("sims.03_engine_cycle.track_a_box0915")
OUT = A.OUT
C1_ETA_PP, C1_P = 1.5, 0.05


def load():
    rows = []
    for l in open(OUT / "points.jsonl"):
        rows += json.loads(l)["rows"]
    return [r for r in rows if r.get("status") == "computed"], [r for r in rows if r.get("status") != "computed"]


def crn(r):
    from engines.m03_cantera import engine as E
    f = lambda k: float(r[k])
    kw = {}
    if r["kind"] == "coupled":
        kw = dict(evap_mode="coupled", spark_deg=f("liquid_freeze_deg"), f_ivc=min(1.0, f("f_evap_intake_effective")),
                  f_spark=min(1.0, f("evaporated_fraction_spark")))
    t = time.time()
    try:
        c = E.run_case(E.Case(fuel=r["fuel"], cr=f("CR"), T_ivc=f("T_IVC_K"), m_fuel=f("fuel_mass_kg"), m_air=f("air_mass_kg"),
                              m_residual=f("residual_mass_kg"), m_water=f("water_mass_kg"), e_intake=f("f_evap_intake_effective"),
                              ca50_deg=f("ca50_used_deg"), d1090_deg=f("burn_10_90_deg"), wall_T=f("chamber_wall_K"),
                              heat_transfer="woschni", label="box0915", **kw))
        out = dict(crn_status="ok", crn_efficiency=c["efficiency"], crn_p_max_Pa=c["p_max_Pa"])
    except Exception as exc:
        out = dict(crn_status=f"failed: {type(exc).__name__}: {exc}")
    out["crn_seconds"] = time.time() - t
    if out["crn_status"] == "ok":
        d = 100 * (out["crn_efficiency"] - r["gross_indicated_efficiency"])
        pr = out["crn_p_max_Pa"] / r["peak_pressure_Pa"]
        out.update(d_eta_pp_crn=d, pmax_ratio_crn=pr, c1_pass=bool(abs(d) <= C1_ETA_PP and abs(pr - 1) <= C1_P))
    return out


def best(rows):
    el = [r for r in rows if r.get("eligible")]
    return max(el, key=lambda r: r["gross_indicated_efficiency"]) if el else None


def flip_scan(fuel, regime, row):
    out = []
    for i in range(0, 91):
        T = 350.0 + i
        m = A.misfire(fuel, row, T, A.PLENUM[regime])
        out.append(dict(fuel=fuel, regime=regime, CR=row["CR"], w=row["w"], port_wall_K=T, **m))
    return out


def main(workers=4):
    rows, failed = load()
    keys = list(dict.fromkeys(k for r in rows + failed for k in r))
    with open(OUT / "points.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, keys); w.writeheader(); w.writerows(rows + failed)
    groups = {}
    for r in rows:
        if r["kind"] == "dry":
            g = ("dry", r["fuel"], r["regime"], "", 0.0, "", r["port_wall_K"])
        else:
            g = (f"step{r['step']}", r["fuel"], r["regime"], r["intake"], r["w"], r["bound"], r["port_wall_K"])
        groups.setdefault(g, []).append(r)
    sel = []
    for g, rs in sorted(groups.items(), key=lambda kv: str(kv[0])):
        b = best(rs)
        el = [r["CR"] for r in rs if r.get("eligible")]
        if b:
            sel.append(dict(b, group="|".join(map(str, g)), knock_limited_CR=max(el), n_eligible=len(el), n_rows=len(rs)))
        else:
            r0 = max(rs, key=lambda r: r["gross_indicated_efficiency"] or 0)
            sel.append(dict(r0, group="|".join(map(str, g)), knock_limited_CR=None, n_eligible=0, n_rows=len(rs), not_eligible=True))
    # M03-CRN cache (added 2026-10-25 PM): a CRN case is keyed by its exact input row, so a re-report reuses earlier
    # results (including recorded failures - never re-run blindly) and only computes new best rows.
    cache_path = OUT / "crn_cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    ck = lambda s: "|".join(str(s.get(k)) for k in ("group", "CR", "w", "T_intake_K", "gross_indicated_efficiency"))
    todo = [s for s in sel if ck(s) not in cache]
    if todo:
        with get_context("spawn").Pool(min(4, workers)) as pool:
            for s, c in zip(todo, pool.map(crn, todo)):
                cache[ck(s)] = c
        cache_path.write_text(json.dumps(cache, indent=1, default=float))
    for s in sel:
        s.update(cache[ck(s)])
    dry = {(s["fuel"], s["regime"]): s for s in sel if s["kind"] == "dry" and not s.get("not_eligible")}
    for s in sel:
        if s["kind"] == "dry":
            continue
        d = dry.get((s["fuel"], s["regime"]))
        s["eta_dry_best"] = d and d["gross_indicated_efficiency"]
        s["dry_best_CR"], s["dry_best_T"] = (d["CR"], d["T_intake_K"]) if d else (None, None)
        s["d_eta_pp_vs_best_dry"] = d and 100 * (s["gross_indicated_efficiency"] - d["gross_indicated_efficiency"])
        s["d_eta_pp_vs_best_dry_crn"] = (100 * (s["crn_efficiency"] - d["crn_efficiency"])
                                         if d and s.get("crn_status") == "ok" and d.get("crn_status") == "ok" else None)
        g, gc = s["d_eta_pp_vs_best_dry"], s["d_eta_pp_vs_best_dry_crn"]
        if g is None:
            s["engines"] = "no eligible dry"
        elif s.get("crn_status") != "ok":
            s["engines"] = "CRN failed"
        elif gc is None:
            s["engines"] = "dry CRN failed"
        else:
            s["engines"] = "agree" if (g > 0) == (gc > 0) and s.get("c1_pass") else "disagree"
        if d:
            c = COST.compare(s, d)
            m, k = c["m03"] or {}, c["crn"] or {}
            s.update(power_change_pct=m.get("power_change_pct"), fuel_per_work_pct=m.get("fuel_energy_per_work_pct"),
                     cost_per_kwh_usd=m.get("cost_usd_per_kwh"), cost_per_kwh_dry_usd=m.get("cost_usd_per_kwh_dry"),
                     cost_per_mile_pct=m.get("cost_per_mile_pct"), cost_per_mile_free_pct=m.get("cost_per_mile_water_free_pct"),
                     cost_per_mile_pct_crn=k.get("cost_per_mile_pct"),
                     cost_verdict=COST.verdict(c) + ("" if not s.get("not_eligible") else " (NOT ELIGIBLE)"))
    keys = list(dict.fromkeys(k for s in sel for k in s))
    with open(OUT / "best_rows.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, keys); w.writeheader(); w.writerows(sel)
    # port-wall sensitivity (step 5): bound (i), dryair, w 0.5, three port-wall temperatures
    pw = [s for s in sel if s["kind"] == "coupled" and s["intake"] == "dryair" and s["bound"] == "i" and s["w"] == 0.5]
    with open(OUT / "port_wall.csv", "w", newline="") as fh:
        cols = ["fuel", "regime", "port_wall_K", "CR", "gross_indicated_efficiency", "crn_efficiency", "d_eta_pp_vs_best_dry",
                "d_eta_pp_vs_best_dry_crn", "port_evap_fraction", "port_limit", "film_capacity_mg", "film_deposit_mg",
                "X_strip_max", "misfire_SMD200", "misfire_SMD350", "misfire_SMD500", "cost_verdict"]
        w = csv.DictWriter(fh, cols, extrasaction="ignore"); w.writeheader(); w.writerows(sorted(pw, key=lambda s: (s["fuel"], s["regime"], s["port_wall_K"])))
    scan = []
    for s in pw:
        if abs(s["port_wall_K"] - 363.15) < 1e-6 or abs(s["port_wall_K"] - 388.15) < 1e-6:
            if (s["regime"] == "normal") == (abs(s["port_wall_K"] - 363.15) < 1e-6):
                scan += flip_scan(s["fuel"], s["regime"], s)
    with open(OUT / "misfire_flip_scan.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, list(scan[0].keys())); w.writeheader(); w.writerows(scan)
    flips = []
    for fuel in A.FUELS:
        for regime in ("normal", "hot"):
            sc = [r for r in scan if r["fuel"] == fuel and r["regime"] == regime]
            for smd in A.SMDS:
                t = [r["port_wall_K"] for r in sc if not r[f"misfire_SMD{smd}"]]
                on = [r["port_wall_K"] for r in sc if r[f"misfire_SMD{smd}"]]
                flips.append(dict(fuel=fuel, regime=regime, SMD=smd, misfire_reachable_up_to_K=max(on) if on else None,
                                  misfire_free_from_K=min(t) if t else None))
    with open(OUT / "misfire_flip.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, list(flips[0].keys())); w.writeheader(); w.writerows(flips)
    f = lambda v, d=4: "-" if v is None else (f"{v:.{d}f}" if isinstance(v, float) else str(v))
    md = ["# Track A box0915 (EXECUTED; M03-CRN = verification; NOT validated)", "",
          "| track | fuel | regime | intake | w | bound | port K | CR (klCR) | eta M03/CRN | dpp vs best dry M03/CRN | engines | power % | cost/mile % $0.10/$0 | misfire 200/350/500 | verdict |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in sel:
        mf = "/".join(("Y" if s.get(f"misfire_SMD{k}") else "n") if f"misfire_SMD{k}" in s else "-" for k in A.SMDS)
        md.append(f"| A | {s['fuel']} | {s['regime']} | {s.get('intake') or 'dry'} | {s['w']} | {s.get('bound') or '-'} | {f(s['port_wall_K'],2)} | "
                  f"{f(s['CR'],0)} ({f(s['knock_limited_CR'],0)}) | {f(s['gross_indicated_efficiency'])}/{f(s.get('crn_efficiency'))} | "
                  f"{f(s.get('d_eta_pp_vs_best_dry'),2)}/{f(s.get('d_eta_pp_vs_best_dry_crn'),2)} | {s.get('engines','-')} | "
                  f"{f(s.get('power_change_pct'),1)} | {f(s.get('cost_per_mile_pct'),2)}/{f(s.get('cost_per_mile_free_pct'),2)} | {mf} | "
                  f"{s.get('cost_verdict', 'dry' if s['kind']=='dry' else '-')} |")
    # cost-minimising water fraction at equal-or-better power (2-engine rows only; $0.10/gal headline)
    opt = []
    for fuel in A.FUELS:
        for regime in ("normal", "hot"):
            c = [s for s in sel if s["kind"] == "coupled" and s["step"] == 4 and s["fuel"] == fuel and s["regime"] == regime
                 and s.get("engines") == "agree" and (s.get("power_change_pct") or -1) >= 0 and s.get("cost_per_mile_pct") is not None]
            b = min(c, key=lambda s: s["cost_per_mile_pct"]) if c else None
            if b and b["cost_per_mile_pct"] >= 0:
                opt.append(f"- {fuel} {regime}: stay dry at $0.10/gal (w 0 is cheapest; best wet with equal-or-better power: w {b['w']} "
                           f"{b['intake']} bound {b['bound']} CR {f(b['CR'],0)}, cost/mile {f(b['cost_per_mile_pct'],2)} % ($0.10) / "
                           f"{f(b['cost_per_mile_free_pct'],2)} % ($0), power {f(b['power_change_pct'],1)} %)")
                continue
            opt.append(f"- {fuel} {regime}: " + (f"w {b['w']} {b['intake']} bound {b['bound']} CR {f(b['CR'],0)}: cost/mile "
                       f"{f(b['cost_per_mile_pct'],2)} % ($0.10) / {f(b['cost_per_mile_free_pct'],2)} % ($0), power {f(b['power_change_pct'],1)} %, "
                       f"{b['cost_verdict']}" if b else "no 2-engine row with equal-or-better power (no cost-optimal water fraction; stay dry)"))
    md += ["", "Cost-minimising w at equal-or-better power (step 4, both engines agree; vs best dry same fuel+regime):", ""] + opt
    md += ["", "**How to read this:** wet rows are at their OWN knock-limited CR (grid 9-24); dry = best eligible dry (grid 6-24). "
           "Gains above ~+1 pp come mostly from the higher CR the water allows (knock relief), e.g. C2H5OH hot dry is knock-limited "
           "at CR 11. power % = IMEP change and, for humid_evap, includes evaporative charge cooling (more trapped mass); indicated "
           "upper bounds, not brake power. 'CRN failed' = M03-CRN Cantera integrator failure, recorded, not re-run: such rows are "
           "1-engine only and do NOT meet the 2-engine rule. Status: EXECUTED (Module 03) + cross-checked (M03-CRN); NOT validated."]
    md += ["", "Misfire flip (Module 11 flag vs port-wall T, 1 K scan, best w 0.5 bound-(i) row masses):", ""]
    md += [f"- {x['fuel']} {x['regime']} SMD {x['SMD']}: reachable up to {f(x['misfire_reachable_up_to_K'],0)} K, free from {f(x['misfire_free_from_K'],0)} K" for x in flips]
    md += ["", f"failed rows: {len(failed)}"]
    (OUT / "REPORT.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
