"""Report for dryevap_baseline.py (Claude job water-engine-dryevap-baseline-20261025-1420).

Writes results/dryevap/{points.csv, baselines.csv, headline_rows.csv, wet_sym.csv, crn_cache.json, REPORT.md}.
Baselines (same fuel + regime; Track B also same knock criterion): OLD (PR 10 dry), DEI (dry-evap intake, PRIMARY),
DEP (dry-evap port); each 'rule' (eligible: knock-free, CA50 <= 15, S_L, p_max, closure) and 'anyCA50' (same but
ignoring the CA50 <= 15 limit). 2-engine rule: M03 and M03-CRN gains same sign and both rows pass C1
(|d_eta| <= 1.5 pp, |p_max ratio - 1| <= 5 %); else labelled.
"""
import csv
import importlib
import json
from multiprocessing import get_context
from pathlib import Path

from sims.cost import cost as COST

D = importlib.import_module("sims.03_engine_cycle.dryevap_baseline")
REPO, OUT = D.REPO, D.OUT
TA = REPO / "results" / "track_a_box"
TB = REPO / "results" / "track_b" / "box0915"
RAD_CA50, SL_MIN, PMAX, CLOS = 15.0, 0.08, 120e5, 0.02


def anyca50_ok(r):
    return (r.get("status") == "computed" and not r.get("knock") and (r.get("S_L_m_s") or 0) >= SL_MIN
            and (r.get("peak_pressure_Pa") or 1e99) <= PMAX and abs(r.get("energy_closure_error_fraction") or 1) <= CLOS)


def best(rows, any_ca50=False):
    el = [r for r in rows if (anyca50_ok(r) if any_ca50 else r.get("eligible"))]
    return max(el, key=lambda r: r["gross_indicated_efficiency"]) if el else None


def klcr(rows):
    el = [r["CR"] for r in rows if r.get("eligible")]
    return max(el) if el else None


def _crn_job(a):
    r, track = a
    return D.crn_case(r, track)


def with_crn(rows_tracks, cache):
    ck = lambda r: "|".join(str(r.get(k)) for k in ("track", "variant", "kind", "intake", "bound", "chain", "criterion", "fuel",
                                                    "regime", "CR", "w", "T_intake_K", "gross_indicated_efficiency"))
    todo = [(r, t) for r, t in rows_tracks if r is not None and r.get("crn_status") is None and ck(r) not in cache]
    if todo:
        with get_context("spawn").Pool(3) as pool:
            for (r, t), c in zip(todo, pool.map(_crn_job, todo)):
                cache[ck(r)] = c
    for r, t in rows_tracks:
        if r is not None and r.get("crn_status") is None:
            r.update(cache[ck(r)])


def compare(wet, base):
    """M03/CRN gain (pp), 2-engine label and cost columns of a wet row against one baseline row."""
    if not wet or not base:
        return dict(d_eta=None, d_eta_crn=None, engines="no baseline", verdict="-")
    g = 100 * (wet["gross_indicated_efficiency"] - base["gross_indicated_efficiency"])
    ok = wet.get("crn_status") == "ok" and base.get("crn_status") == "ok"
    gc = 100 * (wet["crn_efficiency"] - base["crn_efficiency"]) if ok else None
    if wet.get("crn_status") != "ok":
        eng = "CRN failed (wet)"
    elif base.get("crn_status") != "ok":
        eng = "CRN failed (dry)"
    else:
        eng = "agree" if ((g > 0) == (gc > 0) and wet.get("c1_pass") and base.get("c1_pass")) else "disagree"
    c = COST.compare(wet, base)
    cf = COST.compare(wet, base, water="free")
    m, k = c["m03"] or {}, c["crn"] or {}
    return dict(d_eta=g, d_eta_crn=gc, engines=eng, power_pct=m.get("power_change_pct"),
                fuel_per_work_pct=m.get("fuel_energy_per_work_pct"), cost_kwh=m.get("cost_usd_per_kwh"),
                cost_kwh_dry=m.get("cost_usd_per_kwh_dry"), cost_mile_usd=m.get("cost_per_mile_usd"),
                cost_mile_pct=m.get("cost_per_mile_pct"), cost_mile_free_pct=m.get("cost_per_mile_water_free_pct"),
                cost_mile_pct_crn=k.get("cost_per_mile_pct"), verdict=COST.verdict(c), verdict_free=COST.verdict(cf))


def load_new():
    rows = []
    for fn in sorted(OUT.glob("points*.jsonl")):
        for l in open(fn):
            d = json.loads(l)
            for r in d["rows"]:
                r["phase"] = d["phase"]
                rows.append(r)
    return rows


def main():
    new = load_new()
    ok = [r for r in new if r.get("status") == "computed"]
    failed = [r for r in new if r.get("status") != "computed"]
    keys = list(dict.fromkeys(k for r in new for k in r))
    with open(OUT / "points.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, keys); w.writeheader(); w.writerows(new)
    cache_path = OUT / "crn_cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}

    # ---------------- Track A
    oldA = []
    for l in open(TA / "points.jsonl"):
        oldA += json.loads(l)["rows"]
    oldA = [r for r in oldA if r.get("status") == "computed"]
    best_old = list(csv.DictReader(open(TA / "best_rows.csv")))
    num = lambda v: (None if v in ("", None) else (v == "True" if v in ("True", "False") else float(v)))
    best_old = [{k: (num(v) if k not in ("kind", "intake", "fuel", "regime", "bound", "group", "crn_status", "engines",
                                         "cost_verdict", "variant", "atomiser", "status", "reason", "port_limit",
                                         "budget_history", "film_regime") else v) for k, v in r.items()} for r in best_old]
    for r in best_old:
        r["step"] = int(r["step"])
    bases, base_rows = {}, []
    for fuel in D.TA_FUELS:
        for regime in ("normal", "hot"):
            od = [r for r in oldA if r["kind"] == "dry" and r["fuel"] == fuel and r["regime"] == regime and r["step"] == 4]
            bases[("A", fuel, regime, "OLD", "rule")] = next(r for r in best_old if r["kind"] == "dry" and r["fuel"] == fuel and r["regime"] == regime)
            bases[("A", fuel, regime, "OLD", "anyCA50")] = dict(best(od, True) or {}, track="A", variant="OLD") or None
            for v in ("DEI", "DEP"):
                rs = [r for r in ok if r["track"] == "A" and r["variant"] == v and r["kind"] == "dry" and r["fuel"] == fuel
                      and r["regime"] == regime and r["phase"] == 1]
                bases[("A", fuel, regime, v, "rule")] = best(rs)
                bases[("A", fuel, regime, v, "anyCA50")] = best(rs, True)
                bases[("A", fuel, regime, v, "klcr")] = klcr(rs)
            bases[("A", fuel, regime, "OLD", "klcr")] = klcr(od)
    # ---------------- Track B
    oldB = [json.loads(l) for l in open(TB / "points.jsonl")]
    B = importlib.import_module("sims.track_b.box0915")
    for fuel in D.TB_FUELS:
        for regime in ("normal", "hot"):
            for crit in ("LW", "DE"):
                for v in ("DEI", "DEP"):
                    c2 = crit if (v == "DEI" and fuel in ("CH3OH", "C2H5OH")) else "LW"
                    rs = [r for r in ok if r["track"] == "B" and r["variant"] == v and r["kind"] == "dry" and r["fuel"] == fuel
                          and r["regime"] == regime and r["criterion"] == c2]
                    bases[("B", fuel, regime, v, "rule", crit)] = best(rs)
                    bases[("B", fuel, regime, v, "anyCA50", crit)] = best(rs, True)
                    bases[("B", fuel, regime, v, "klcr", crit)] = klcr(rs)
    for name, ch in B.CHAINS.items():
        for crit in ("LW", "DE"):
            od = [r for r in oldB if r["chain"] == name and r["criterion"] == crit and r["w"] == 0.0]
            bases[("B", ch["fuel"], ch["regime"], "OLD", "rule", crit)] = best(od)
            a = best(od, True)
            bases[("B", ch["fuel"], ch["regime"], "OLD", "anyCA50", crit)] = a and dict(a, track="B", variant="OLD")
            bases[("B", ch["fuel"], ch["regime"], "OLD", "klcr", crit)] = klcr(od)
    # CRN for every baseline row that lacks it
    rt = []
    for k, r in bases.items():
        if isinstance(r, dict) and r:
            r.setdefault("track", k[0])
            r.setdefault("variant", k[3])
            rt.append((r, k[0]))
    with_crn(rt, cache)

    # ---------------- headline rows
    heads = []
    for s in best_old:
        if s["kind"] != "coupled" or s["step"] != 4:
            continue
        sym = [r for r in ok if r["track"] == "A" and r["kind"] == "coupled" and r["phase"] in (3, 7) and r["fuel"] == s["fuel"]
               and r["regime"] == s["regime"] and r["intake"] == s["intake"] and r["w"] == s["w"] and r["bound"] == s["bound"]]
        heads.append(dict(track="A", label=f"A {s['fuel']} {s['regime']} {s['intake']} w{s['w']:g} {s['bound']}", fuel=s["fuel"],
                          regime=s["regime"], intake=s["intake"], crit="LW", wet=dict(s, track="A"), sym=best(sym),
                          sym_variant=D.WET_SYM[s["intake"]], key=("A", s["fuel"], s["regime"])))
    for name, ch in B.CHAINS.items():
        _, wb, _ = B.chain_best(name)
        for crit in ("LW", "DE"):
            W = [r for r in oldB if r["chain"] == name and r["criterion"] == crit and r["w"] == float(wb["w"])]
            c2 = crit if ch["fuel"] in ("CH3OH", "C2H5OH") else "LW"
            sym = [r for r in ok if r["track"] == "B" and r["kind"] == "wet" and r.get("chain") == name and r["criterion"] == c2]
            heads.append(dict(track="B", label=f"B {name} {crit} w{float(wb['w']):g}", fuel=ch["fuel"], regime=ch["regime"],
                              intake=ch["mode"], crit=crit, wet=dict(best(W), track="B"), sym=best(sym),
                              sym_variant=D.WET_SYM[ch["mode"]], key=("B", ch["fuel"], ch["regime"])))
    with_crn([(h["sym"], h["track"]) for h in heads if h["sym"]], cache)
    cache_path.write_text(json.dumps(cache, indent=1, default=float))

    def base(h, v, kind):
        k = h["key"] + (v, kind) + ((h["crit"],) if h["track"] == "B" else ())
        return bases.get(k)

    out = []
    for h in heads:
        wet = h["wet"]
        row = dict(track=h["track"], row=h["label"], fuel=h["fuel"], regime=h["regime"], intake=h["intake"], criterion=h["crit"],
                   wet_CR=wet["CR"], wet_eta=wet["gross_indicated_efficiency"], wet_eta_crn=wet.get("crn_efficiency"),
                   wet_T_IVC=wet.get("T_IVC_K"))
        for v in ("OLD", "DEI", "DEP"):
            for kind in ("rule", "anyCA50"):
                b = base(h, v, kind)
                c = compare(wet, b)
                tag = f"{v}_{kind}"
                row[f"{tag}_CR"] = b and b["CR"]
                row[f"{tag}_eta"] = b and b["gross_indicated_efficiency"]
                row[f"{tag}_ca50"] = b and b.get("ca50_used_deg")
                row.update({f"{tag}_{k}": x for k, x in c.items()})
        # symmetric: wet row re-run with the same fuel treatment as its matching dry-evap baseline
        sv = h["sym_variant"]
        sym = h["sym"]
        row.update(sym_variant=sv, sym_CR=sym and sym["CR"], sym_eta=sym and sym["gross_indicated_efficiency"],
                   sym_T_IVC=sym and sym.get("T_IVC_K"), sym_fuel_evap=sym and sym.get("fuel_evap_intake_fraction"))
        c = compare(sym, base(h, sv, "rule"))
        row.update({f"sym_vs_{sv}_{k}": x for k, x in c.items()})
        out.append(row)
    with open(OUT / "headline_rows.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, list(dict.fromkeys(k for r in out for k in r))); w.writeheader(); w.writerows(out)
    bl = []
    for k, r in bases.items():
        if k[4] == "klcr" or not isinstance(r, dict) or not r:
            continue
        bl.append(dict(track=k[0], fuel=k[1], regime=k[2], variant=k[3], selection=k[4], criterion=k[5] if len(k) > 5 else "LW",
                       CR=r["CR"], klCR=bases.get(k[:4] + ("klcr",) + k[5:]), T_intake_K=r.get("T_intake_K"), T_IVC_K=r.get("T_IVC_K"),
                       fuel_evap_intake=r.get("fuel_evap_intake_fraction"), fuel_evap_port=r.get("fuel_evap_port_fraction"),
                       fuel_dewpoint_limited=r.get("fuel_evap_saturation_limited"), ca50=r.get("ca50_used_deg"),
                       eta=r["gross_indicated_efficiency"], eta_crn=r.get("crn_efficiency"), crn_status=r.get("crn_status"),
                       c1_pass=r.get("c1_pass"), IMEP_bar=(r.get("IMEP_Pa") or 0) / 1e5))
    with open(OUT / "baselines.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, list(bl[0].keys())); w.writeheader(); w.writerows(bl)

    f = lambda v, d=2: "-" if v is None else (f"{v:.{d}f}" if isinstance(v, float) else str(v))
    md = ["# Dry-evap baseline check of PR 10 (Track A + Track B; EXECUTED, M03-CRN cross-check; NOT validated)", "",
          "## Dry baselines (best eligible, CA50 <= 15 rule; any-CA50 in baselines.csv)", "",
          "| track | fuel | regime | crit | variant | CR (klCR) | T_IVC K | fuel evap intake | eta M03/CRN | C1 |", "|---|---|---|---|---|---|---|---|---|---|"]
    for b in bl:
        if b["selection"] == "rule":
            md.append(f"| {b['track']} | {b['fuel']} | {b['regime']} | {b['criterion']} | {b['variant']} | {f(b['CR'],1)} ({f(b['klCR'],1)}) | "
                      f"{f(b['T_IVC_K'],1)} | {f(b['fuel_evap_intake'],3)} | {f(b['eta'],4)}/{f(b['eta_crn'],4)} | {b['c1_pass']} |")
    md += ["", "## PR 10 headline rows vs each baseline (M03 d_eta pp; cost/mile % at $0.10/gal water; engines = 2-engine rule)", "",
           "| row | wet CR | wet eta | OLD d_eta / cost% | DEI d_eta / CRN / cost% / verdict | DEP d_eta / cost% | DEI any-CA50 d_eta | OLD any-CA50 d_eta | sym wet vs own baseline d_eta / cost% / verdict |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in out:
        sv = r["sym_variant"]
        md.append(f"| {r['row']} | {f(r['wet_CR'],1)} | {f(r['wet_eta'],4)} | {f(r['OLD_rule_d_eta'])} / {f(r['OLD_rule_cost_mile_pct'])} | "
                  f"{f(r['DEI_rule_d_eta'])} / {f(r['DEI_rule_d_eta_crn'])} / {f(r['DEI_rule_cost_mile_pct'])} / {r['DEI_rule_verdict']} [{r['DEI_rule_engines']}] | "
                  f"{f(r['DEP_rule_d_eta'])} / {f(r['DEP_rule_cost_mile_pct'])} | {f(r['DEI_anyCA50_d_eta'])} | {f(r['OLD_anyCA50_d_eta'])} | "
                  f"{sv}: {f(r[f'sym_vs_{sv}_d_eta'])} / {f(r[f'sym_vs_{sv}_cost_mile_pct'])} / {r[f'sym_vs_{sv}_verdict']} [{r[f'sym_vs_{sv}_engines']}] |")
    md += ["", f"failed rows: {len(failed)}" + "".join(f"\n- {r.get('track')} {r.get('variant')} {r.get('fuel')} CR {r.get('CR')}: {r.get('reason')}" for r in failed)]
    md += ["", "## Summary (side-by-side, cost-optimal w)", ""] + summary(out, bl, f)
    (OUT / "REPORT.md").write_text("\n".join(md) + "\n")
    (OUT / "SUMMARY.md").write_text("\n".join(summary(out, bl, f)) + "\n")
    print("\n".join(md))


REGIME_NOTE = ("Regimes as in sims/03_engine_cycle/coupled_dual_temp.py and sims/track_b/run.py (wme1-hiT "
               "sims/dual_temp/regimes.py, docs/DUAL_TEMPERATURE_RULE.md, PR #5; MAHLE/VW SSP 222, SAE 960271, Heywood 1988 "
               "ch. 12): normal = coolant 363.15 K, chamber wall 450 K, port wall 363.15 K, T_intake 320 K (Track A dry also "
               "360 K; Track B chains 320 K); hot/high-performance = coolant 388.15 K, chamber wall 520 K, port wall 388.15 K, "
               "T_intake 400 K. Water price $0.10/gal headline, $0/gal tap secondary; fuel prices sims/cost/prices_20261025.json.")


def summary(out, bl, f):
    """Plain summary: per PR 10 headline row, the gain vs OLD dry and vs the fairer DEI (dry-evap intake) baseline,
    normal vs hot side by side, plus the cost-optimal w per track/fuel/regime at equal-or-better power vs DEI."""
    s = ["Status: EXECUTED on the box (Module 03 primary + M03-CRN second engine); VERIFIED only by unit tests "
         "(tests/test_m03_fuel_evap.py: zero-fuel-evap bit-exact, energy closure, dew-point cap, CRN zero credit bit-exact); "
         "**NOT validated** against experiment.", "", REGIME_NOTE, "",
         "DEI = dry fuel entering as liquid at 298 K, evaporated in the intake air (charge cooling, capped at the fuel dew point) - "
         "the fair counterpart of humid_evap water rows. DEP = fuel evaporated off the port wall (latent heat credited, no charge "
         "cooling) - counterpart of dryair rows. OLD = PR 10 dry baseline (fuel premixed vapour, no evaporative cooling). "
         "sym = the PR 10 wet row re-run with the same fuel treatment as its baseline (wet+fuel-evap vs dry+fuel-evap).", "",
         "| track | fuel | regime | row | d_eta vs OLD M03 | d_eta vs DEI M03 / CRN [engines] | power % vs DEI | fuel energy per work % | "
         "cost/kWh $ (DEI dry) | cost/mile % vs DEI $0.10 / $0 | verdict vs DEI | sym vs own baseline d_eta M03/CRN, cost/mile %, verdict | any-CA50: d_eta vs DEI |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    order = sorted(out, key=lambda r: (r["track"], r["fuel"], r["intake"], r["criterion"], r["regime"] != "normal", r["row"]))
    for r in order:
        sv = r["sym_variant"]
        s.append(f"| {r['track']} | {r['fuel']} | {r['regime']} | {r['row']} | {f(r['OLD_rule_d_eta'])} | "
                 f"{f(r['DEI_rule_d_eta'])} / {f(r['DEI_rule_d_eta_crn'])} [{r['DEI_rule_engines']}] | {f(r.get('DEI_rule_power_pct'),1)} | "
                 f"{f(r.get('DEI_rule_fuel_per_work_pct'))} | {f(r.get('DEI_rule_cost_kwh'),4)} ({f(r.get('DEI_rule_cost_kwh_dry'),4)}) | "
                 f"{f(r.get('DEI_rule_cost_mile_pct'))} / {f(r.get('DEI_rule_cost_mile_free_pct'))} | {r['DEI_rule_verdict']} | "
                 f"{sv}: {f(r[f'sym_vs_{sv}_d_eta'])}/{f(r[f'sym_vs_{sv}_d_eta_crn'])}, {f(r[f'sym_vs_{sv}_cost_mile_pct'])}, {r[f'sym_vs_{sv}_verdict']} | "
                 f"{f(r['DEI_anyCA50_d_eta'])} |")
    # survival of the hot gains
    s += ["", "### Do the PR 10 hot-regime gains survive the fairer (DEI) baseline?", ""]
    for r in order:
        if r["regime"] != "hot":
            continue
        a, b = r["OLD_rule_d_eta"], r["DEI_rule_d_eta"]
        if a is None or b is None:
            s.append(f"- {r['row']}: no comparable baseline ({r['DEI_rule_engines']})")
            continue
        keep = 100 * b / a if a else float("nan")
        s.append(f"- {r['row']}: {a:+.2f} pp vs OLD -> {b:+.2f} pp vs DEI (M03; CRN {f(r['DEI_rule_d_eta_crn'])}; "
                 f"{keep:.0f} % of the old gain kept), cost/mile {f(r.get('DEI_rule_cost_mile_pct'))} %, {r['DEI_rule_verdict']} "
                 f"[{r['DEI_rule_engines']}]")
    # cost-optimal w per track / fuel / regime / criterion, equal-or-better power, both engines, vs DEI
    s += ["", "### Cost-optimal water fraction vs the DEI baseline (equal-or-better power, $0.10/gal; COST GAIN in both engines)", ""]
    groups = {}
    for r in out:
        groups.setdefault((r["track"], r["fuel"], r["regime"], r["criterion"]), []).append(r)
    for k in sorted(groups):
        c = [r for r in groups[k] if r["DEI_rule_verdict"] == "COST GAIN" and r.get("DEI_rule_cost_mile_pct") is not None]
        if c:
            b = min(c, key=lambda r: r["DEI_rule_cost_mile_pct"])
            s.append(f"- Track {k[0]} {k[1]} {k[2]} ({k[3]}): {b['row']} (CR {f(b['wet_CR'],1)}), cost/mile {f(b['DEI_rule_cost_mile_pct'])} % "
                     f"(CRN {f(b.get('DEI_rule_cost_mile_pct_crn'))} %), power {f(b.get('DEI_rule_power_pct'),1)} %")
        else:
            s.append(f"- Track {k[0]} {k[1]} {k[2]} ({k[3]}): w = 0 (no PR 10 headline row is a 2-engine cost gain vs DEI) - stay dry")
    return s


if __name__ == "__main__":
    main()
