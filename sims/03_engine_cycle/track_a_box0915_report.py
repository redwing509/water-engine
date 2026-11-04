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
# M03-CRN numerical fix (selfdir 2026-10-25 14:10, see results/track_b/crnfix/REPORT.md): smooth the saturation-limit
# switch of the evaporation source over a 1e-3 * m_liq0 band and drop output times within 1e-9 rad of a break point.
# The 24 earlier CRN failures (max steps / CVODES -27) were integrator problems, not physics. 0.0 = legacy engine.
CRN_SAT_BLEND = 1.0e-3
# PR 11 review (Claude reply-selfdir-1410-review-20261025-1725), report-only labels, no physics change:
#  1. Track A = water-majority, w > 0.5. Wet rows with w <= 0.5 go to a separate "intermediate w" table and never
#     feed the Track A best rows or the cost-minimising w.
#  3. every "vs best dry" number uses the OLD dry baseline (best eligible dry, CR 8 / CR 11 for the hot alcohols, no
#     fuel evaporative cooling) -> "pending dryevap verdict"; re-scored in dryevap step 3.
#  4. dryair rows at CR > 24 reuse the CR-24 Module 09 spray point -> "extrapolated", outside the 2-engine rule.
#  5. every CR here is the Module 03 knock-limited CR (klCR, single knock engine) -> validation status
#     "Not yet (single-engine knock)" until the 1520 step-3 knock engine validates.
TRACK_A_MIN_W = 0.5          # Track A strictly w > TRACK_A_MIN_W
M09_MAX_CR = 24              # Module 09 spray point exists up to CR 24 only
BASELINE_LABEL = "pending dryevap verdict"
KNOCK_LABEL = "Not yet (single-engine knock)"


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
                              heat_transfer="woschni", label="box0915", sat_blend_frac=CRN_SAT_BLEND, **kw))
        out = dict(crn_status="ok", crn_efficiency=c["efficiency"], crn_p_max_Pa=c["p_max_Pa"], crn_sat_blend_frac=CRN_SAT_BLEND)
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
    # The legacy cache (crn_cache.json, 24 recorded failures) is kept unchanged as the archive; the fixed engine
    # writes its own cache so legacy and fixed results never mix.
    cache_path = OUT / ("crn_cache.json" if CRN_SAT_BLEND == 0.0 else f"crn_cache_satblend{CRN_SAT_BLEND:g}.json")
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
    for s in sel:
        wet = s["kind"] != "dry"
        s["track_label"] = ("dry baseline" if not wet else
                            ("Track A (w > 0.5)" if s["w"] > TRACK_A_MIN_W + 1e-9 else "intermediate w (w <= 0.5, NOT Track A)"))
        s["extrapolated"] = bool(wet and s.get("intake") == "dryair" and s["CR"] > M09_MAX_CR)
        s["two_engine_rule"] = ("extrapolated: CR > 24 reuses the CR-24 Module 09 spray point; outside the 2-engine rule"
                                if s["extrapolated"] else s.get("engines", "-"))
        s["baseline_label"] = BASELINE_LABEL if wet else "old dry baseline (no fuel evaporative cooling)"
        s["validation"] = KNOCK_LABEL
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
    hdr = ["| track | fuel | regime | intake | w | bound | port K | CR (klCR) | eta M03/CRN | dpp vs best dry M03/CRN (pending dryevap verdict) | engines / 2-engine rule | power % | cost/mile % $0.10/$0 (pending dryevap verdict) | misfire 200/350/500 | verdict | validation |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]

    def line(s, tag):
        mf = "/".join(("Y" if s.get(f"misfire_SMD{k}") else "n") if f"misfire_SMD{k}" in s else "-" for k in A.SMDS)
        eng = "EXTRAPOLATED (CR>24 on CR-24 M09 spray; outside 2-engine rule)" if s.get("extrapolated") else s.get("engines", "-")
        return (f"| {tag} | {s['fuel']} | {s['regime']} | {s.get('intake') or 'dry'} | {s['w']} | {s.get('bound') or '-'} | {f(s['port_wall_K'],2)} | "
                f"{f(s['CR'],0)} ({f(s['knock_limited_CR'],0)}) | {f(s['gross_indicated_efficiency'])}/{f(s.get('crn_efficiency'))} | "
                f"{f(s.get('d_eta_pp_vs_best_dry'),2)}/{f(s.get('d_eta_pp_vs_best_dry_crn'),2)} | {eng} | "
                f"{f(s.get('power_change_pct'),1)} | {f(s.get('cost_per_mile_pct'),2)}/{f(s.get('cost_per_mile_free_pct'),2)} | {mf} | "
                f"{s.get('cost_verdict', 'dry' if s['kind']=='dry' else '-')} | {s['validation']} |")
    trackA = [s for s in sel if s["track_label"].startswith("Track A")]
    inter = [s for s in sel if s["track_label"].startswith("intermediate")]
    dryrows = [s for s in sel if s["kind"] == "dry"]
    # Track A best rows (w > 0.5 only; step 4 = nominal port wall; extrapolated rows excluded from "best", noted apart)
    bestA = []
    for fuel in A.FUELS:
        for regime in ("normal", "hot"):
            c = [s for s in trackA if s["step"] == 4 and s["fuel"] == fuel and s["regime"] == regime and s.get("eligible")
                 and not s.get("not_eligible") and s.get("d_eta_pp_vs_best_dry") is not None]
            ok = [s for s in c if not s["extrapolated"] and s.get("engines") == "agree"]
            b = max(ok, key=lambda s: s["d_eta_pp_vs_best_dry"]) if ok else None
            bx = max(c, key=lambda s: s["d_eta_pp_vs_best_dry"]) if c else None
            txt = (f"- {fuel} {regime}: " + (f"w {b['w']} {b['intake']} bound {b['bound']} CR {f(b['CR'],0)}: "
                   f"{f(b['d_eta_pp_vs_best_dry'],2)}/{f(b['d_eta_pp_vs_best_dry_crn'],2)} pp vs best dry M03/CRN ({BASELINE_LABEL}), "
                   f"power {f(b['power_change_pct'],1)} %, cost/mile {f(b['cost_per_mile_pct'],2)} % ($0.10), {b['cost_verdict']}; {KNOCK_LABEL}"
                   if b else "no 2-engine non-extrapolated w > 0.5 row"))
            if bx is not None and bx is not b and bx["extrapolated"] and (b is None or bx["d_eta_pp_vs_best_dry"] > b["d_eta_pp_vs_best_dry"]):
                txt += (f" [higher but EXTRAPOLATED, not counted: w {bx['w']} {bx['intake']} bound {bx['bound']} CR {f(bx['CR'],0)} "
                        f"{f(bx['d_eta_pp_vs_best_dry'],2)} pp]")
            bestA.append(txt)
    md = ["# Track A box0915 (EXECUTED; M03-CRN = verification; NOT validated)", "",
          "PR 11 review labels (Claude reply-selfdir-1410-review-20261025-1725): Track A = w > 0.5 only (w <= 0.5 rows are in the "
          "separate 'intermediate w' table and never count as Track A); every 'vs best dry' and cost number is "
          f"'{BASELINE_LABEL}' (old dry baseline: best eligible dry, CR 8 (CH3OH hot) / CR 11 (C2H5OH hot), "
          "no fuel evaporative cooling; re-scored in dryevap step 3); dryair rows at CR > 24 reuse the CR-24 Module 09 spray "
          "point and are 'extrapolated', outside the 2-engine rule; every CR is the Module 03 knock-limited CR, so every row is "
          f"'{KNOCK_LABEL}' until the 1520 step-3 knock engine validates.", "",
          "## Track A best rows (w > 0.5, step 4 nominal port wall, both engines agree, not extrapolated)", ""] + bestA + [
          "", "## Dry baselines (old; no fuel evaporative cooling)", ""] + hdr + [line(s, "dry") for s in dryrows] + [
          "", "## Track A rows (w > 0.5)", ""] + hdr + [line(s, "A") for s in trackA] + [
          "", "## Intermediate w (w <= 0.5; NOT Track A, not used for Track A best rows or cost-minimising w)", ""] + hdr + [
          line(s, "int") for s in inter]
    # cost-minimising water fraction at equal-or-better power (2-engine rows only; $0.10/gal headline)
    opt = []
    for fuel in A.FUELS:
        for regime in ("normal", "hot"):
            c = [s for s in sel if s["kind"] == "coupled" and s["step"] == 4 and s["fuel"] == fuel and s["regime"] == regime
                 and s["w"] > TRACK_A_MIN_W + 1e-9 and not s["extrapolated"] and s.get("engines") == "agree" and (s.get("power_change_pct") or -1) >= 0 and s.get("cost_per_mile_pct") is not None]
            b = min(c, key=lambda s: s["cost_per_mile_pct"]) if c else None
            if b and b["cost_per_mile_pct"] >= 0:
                opt.append(f"- {fuel} {regime}: stay dry at $0.10/gal (w 0 is cheapest; best wet with equal-or-better power: w {b['w']} "
                           f"{b['intake']} bound {b['bound']} CR {f(b['CR'],0)}, cost/mile {f(b['cost_per_mile_pct'],2)} % ($0.10) / "
                           f"{f(b['cost_per_mile_free_pct'],2)} % ($0), power {f(b['power_change_pct'],1)} %)")
                continue
            opt.append(f"- {fuel} {regime}: " + (f"w {b['w']} {b['intake']} bound {b['bound']} CR {f(b['CR'],0)}: cost/mile "
                       f"{f(b['cost_per_mile_pct'],2)} % ($0.10) / {f(b['cost_per_mile_free_pct'],2)} % ($0), power {f(b['power_change_pct'],1)} %, "
                       f"{b['cost_verdict']}" if b else "no 2-engine w > 0.5 row with equal-or-better power (no Track A cost-optimal water fraction; stay dry)"))
    md += ["", "## Track A cost-minimising w at equal-or-better power (w > 0.5 only, step 4, both engines agree, not extrapolated; vs best dry same fuel+regime, " + BASELINE_LABEL + "):", ""] + opt
    md += ["", "**How to read this:** wet rows are at their OWN knock-limited CR (grid 9-30 since the 2026-10-25 14:20 extension; '30 (30)' = still grid-capped); dry = best eligible dry (grid 6-30). "
           "Gains above ~+1 pp come mostly from the higher CR the water allows (knock relief), e.g. C2H5OH hot dry is knock-limited "
           "at CR 11. power % = IMEP change and, for humid_evap, includes evaporative charge cooling (more trapped mass); indicated "
           "upper bounds, not brake power. M03-CRN runs with the 2026-10-25 integrator fix (saturation-switch smoothing 1e-3 + break-point grid fix; legacy failures archived in crn_cache.json). 'CRN failed' = M03-CRN Cantera integrator failure, recorded, not re-run: such rows are "
           "1-engine only and do NOT meet the 2-engine rule; 'EXTRAPOLATED' rows (dryair CR > 24, CR-24 Module 09 spray point) are also outside it. Status: EXECUTED (Module 03) + cross-checked (M03-CRN); NOT validated."]
    md += ["", "Misfire flip (Module 11 flag vs port-wall T, 1 K scan, best w 0.5 bound-(i) row masses; w 0.5 = intermediate w, NOT Track A):", ""]
    md += [f"- {x['fuel']} {x['regime']} SMD {x['SMD']}: reachable up to {f(x['misfire_reachable_up_to_K'],0)} K, free from {f(x['misfire_free_from_K'],0)} K" for x in flips]
    md += ["", f"failed rows: {len(failed)}"]
    (OUT / "REPORT.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
