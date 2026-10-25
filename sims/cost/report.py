"""Cost-metric report for Track B chains and Track A Module 03 results (no new combustion runs).

Run:  python -m sims.cost.report [--track-a-reopt PATH.jsonl]
Writes results/track_b/COST.md, results/track_b/cost_trackb.json, results/track_a_cost/COST_TRACK_A.md and
results/track_a_cost/cost_tracka.json. Called automatically by `python -m sims.track_b.report`.
"""
import argparse
import glob
import json
import time
from pathlib import Path

from sims.cost import cost as C

REPO = Path(__file__).resolve().parents[2]
TB = REPO / "results" / "track_b"
TA = REPO / "results" / "track_a_cost"
MODES = ("liquid", "humid_evap", "humid_ambient")
BANNER = ("**NOT YET PEER-REVIEW VERIFIED** - Module 03 and M03-CRN are two in-repo engines from the same "
          "toolchain; independent engine review (2+ engine rule) still pending.")
CAVEATS = """## Caveats carried over (still apply to every cost number)

* **Fixed burn duration model gap.** Module 03 holds the 10-90 % burn duration essentially fixed as water is
  added (flame-speed fits only reduce S_L; the burn-duration penalty of water dilution measured in engines is not
  reproduced). The B1 sign test (spark held at the dry setting) still gains, while published engine tests lose
  efficiency at fixed timing, so every efficiency - and therefore every fuel-saving and cost gain - here is an
  **upper bound**.
* **Knock is modelled only in Module 03.** M03-CRN has no knock model; it re-runs the Module 03 spark timing. The
  part of a gain that comes from knock relief therefore rests on one engine.
* **Lower bounds at w = 0.10 for the gasoline blends** (PRF87/91/97, E10, E85): those chains stop at the end of the
  flame-speed fit validity (w <= 0.10), not because the gain ran out, so their cost gains could be larger.
* No gas-exchange / friction model: power is IMEP (indicated). Brake power is not modelled; at equal speed and
  friction the brake-power change has the same sign and a larger % magnitude.
* Absolute $/mile is NOT comparable across fuels (road fuels at retail, alcohols at wholesale, CNG quarterly
  retail). Compare each fuel only with its own dry baseline (the % columns).
"""


def read_jsonl(path):
    rows = []
    for line in open(path):
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:  # file still being appended by a running chain
            pass
    return rows


def chain_files():
    """{(fuel, regime, mode, source): path} - current-rule (__noise) files preferred."""
    out = {}
    for d, src in ((TB, "track_b"), (TB / "h1_hot", "h1_low_cr_hot")):
        for p in sorted(glob.glob(str(d / "steps_*.jsonl"))):
            name = Path(p).stem[6:]
            noise = name.endswith("__noise")
            name = name[: -len("__noise")] if noise else name
            mode = "liquid"
            for m in ("humid_evap", "humid_ambient"):
                if name.endswith("_" + m):
                    mode, name = m, name[: -len(m) - 1]
            fuel, regime = name.rsplit("_", 1)
            key = (fuel, regime, mode, src)
            if noise or key not in out:
                out[key] = p
    return out


def _ok(r):
    return r.get("status") == "computed" and r.get("eligible") and r.get("gross_indicated_efficiency") is not None


def chain_cost(path, prices=None):
    rows = read_jsonl(path)
    dry = next((r for r in rows if r.get("kind") == "dry_baseline"), None)
    if dry is None:
        return None
    steps = sorted((r for r in rows if r.get("kind") == "step" and _ok(r)), key=lambda r: r["w"])
    # Track B "best" = last step the continuation rule accepted (both engines gaining); fall back to max eta.
    accepted = [r for r in steps if r.get("decision") == "continue"]
    eff = accepted[-1] if accepted else dry
    cbest, cc = C.best_cost(steps, dry, prices)
    last = max((r.get("step") or 0 for r in rows if r.get("kind") == "step"), default=0)
    stopped = any(r.get("decision") == "stop" for r in rows if r.get("kind") == "step")
    return dict(dry=dry, eff_row=eff, eff=C.compare(eff, dry, prices), cost_row=cbest, cost=cc,
                n_steps=len(steps), last_step=last, stopped=stopped,
                all=[C.compare(r, dry, prices) for r in steps])


def _p(x, fmt="%+.3f"):
    return "-" if x is None else fmt % x


def _two(c, key, fmt="%+.3f"):
    a = (c.get("m03") or {}).get(key)
    b = (c.get("crn") or {}).get(key)
    return f"{_p(a, fmt)} / {_p(b, fmt)}"


def line(fuel, regime, mode, label, row, c, status=""):
    return (f"| {fuel} | {regime} | {mode} | {label} | {row.get('w', 0):.3f} | {_two(c, 'd_eta_pp')} | "
            f"{_two(c, 'power_change_pct')} | {_two(c, 'fuel_volume_per_work_pct')} | {_two(c, 'cost_per_mile_pct')} | "
            f"{_p((c.get('m03') or {}).get('cost_per_mile_water_free_pct'))} | {C.verdict(c)} | {status} |")


HDR = ("| fuel | regime | mode | point | w | d_eta pp (M03 / CRN) | power (IMEP) % (M03 / CRN) | fuel volume per unit "
       "work % (M03 / CRN) | **cost per mile %** (M03 / CRN) | cost/mile if water free % (M03) | verdict | status |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|---|")


def prices_md(P):
    L = ["## Prices used (dated, cited; `sims/cost/prices_20261025.json`)\n",
         "| key | price | basis | date | source |", "|---|---|---|---|---|"]
    for k, v in P["prices"].items():
        L.append(f"| {k} | {v['usd']} {v['unit']} | {v['basis']} | {v['date']} | [{v['source']}]({v['url']}) |")
    L.append("\nFuel -> price: " + ", ".join(f"{f} = {k}" for f, k in P["fuel_to_price"].items())
             + f". {P['fuel_to_price_note']} USD/kg: " + ", ".join(
                 f"{f} {C.usd_per_kg(f, P):.3f}" for f in P["fuel_to_price"]) + f", water {C.usd_per_kg('water', P):.3f}.")
    return "\n".join(L)


def method_md():
    return f"""## Method (how fuel use per unit work is defined)

* w = m_water/(m_water + m_fuel); water per kg fuel r = w/(1-w) (checked against the saved masses for every row).
* The charge is stoichiometric on the fuel; water is **added**, it does not replace fuel inside the
  stoichiometric mix. What water "displaces" is fuel **per unit of work**: efficiency is
  eta = W_ind / (m_fuel x LHV_fuel) (water has no heating value and is not in the denominator), so
  fuel energy, mass and volume per unit work all change by **eta_dry/eta - 1** vs the same fuel's dry baseline.
* Power = IMEP (Module 03 `IMEP_Pa`; M03-CRN IMEP derived as IMEP_M03 x eta_CRN/eta_M03 at the same fuel mass).
  Equal-or-better = IMEP change >= -{100 * C.POWER_TOL_REL:.2f} % (the 3.3e-5 efficiency noise level is ~1e-4 relative).
* Cost per kWh of indicated work = (p_fuel + r x p_water) / (eta x LHV); cost per mile = that x
  {C.WORK_KWH_PER_MILE} kWh indicated work per mile (reference vehicle: 30 mpg gasoline car, 33.7 kWh/gal / 30 x ~0.35
  indicated efficiency). The % changes do not depend on the vehicle; they are the primary numbers.
* **Verdict COST GAIN** = power equal or better in every engine AND cost per mile lower by more than
  {100 * C.COST_TOL_REL:.2f} % in every engine (Track B: both engines; Track A grid: Module 03 only, labelled).
* Two points per chain: **eff-opt** = the best-efficiency point the Track B rule accepted; **cost-opt** = the
  water fraction with the lowest cost per mile among points with equal-or-better power (w = 0 means water never pays).
"""


def track_b(prices):
    P = prices
    files = chain_files()
    res, L = {}, []
    order = ("PRF87", "PRF91", "PRF97", "E10", "E85", "CH3OH", "C2H5OH", "CH4")
    keys = sorted(files, key=lambda k: (order.index(k[0]) if k[0] in order else 99, k[1] != "normal",
                                        MODES.index(k[2]), k[3]))
    for k in keys:
        c = chain_cost(files[k], P)
        if c is None:
            continue
        res[k] = c
        fuel, regime, mode, src = k
        reg = regime + (" (H1 low-CR)" if src != "track_b" else "")
        st = ("stopped" if c["stopped"] else f"in progress (step {c['last_step']})")
        L.append(line(fuel, reg, mode, "eff-opt", c["eff_row"], c["eff"], st))
        L.append(line(fuel, reg, mode, "cost-opt", c["cost_row"], c["cost"], ""))
    return res, L


def headline(res):
    """Per fuel: (a) best cost-per-mile change (M03) at equal-or-better power, any regime/mode; (b) the biggest
    fuel-per-work saving (Track B eff-opt) with its cost change; (c) the highest break-even water price."""
    H = {}
    for (fuel, regime, mode, src), c in res.items():
        cc, ce = c["cost"], c["eff"]
        if not cc["m03"]:
            continue
        where = regime + ("/H1" if src != "track_b" else "") + " / " + mode
        h = H.setdefault(fuel, dict(cost=None, eff=None, be=None))
        if h["cost"] is None or cc["m03"]["cost_per_mile_pct"] < h["cost"][0]:
            h["cost"] = (cc["m03"]["cost_per_mile_pct"], where, c["cost_row"].get("w", 0), cc)
        if ce["m03"] and (h["eff"] is None or ce["m03"]["fuel_volume_per_work_pct"] < h["eff"][0]):
            h["eff"] = (ce["m03"]["fuel_volume_per_work_pct"], where, c["eff_row"].get("w", 0), ce)
        for a in c["all"]:
            b = (a["m03"] or {}).get("breakeven_water_usd_per_gal")
            if b is not None and a["power_ok_all_engines"] and (h["be"] is None or b > h["be"][0]):
                h["be"] = (b, where, a["w"], ((a["crn"] or {}).get("breakeven_water_usd_per_gal")))
    return H


def headline_md(P, H):
    M = ["\n## Headline per fuel (lowest cost per mile at equal-or-better power, any regime / mode)\n",
         f"Water priced at retail distilled ({P['prices']['water_distilled']['usd']} USD/gal). 'w = 0' = no water amount "
         "lowers cost at that price. Break-even = the highest water price at which some equal-or-better-power step still "
         "lowers cost per mile (M03 / CRN at that step).\n",
         "| fuel | best cost per mile: where, w | **cost per mile %** (M03 / CRN) | power % (M03 / CRN) | verdict | "
         "biggest fuel saving (eff-opt): where, w | fuel per unit work % (M03 / CRN) | cost per mile % there (M03 / CRN) | "
         "same, water free % (M03 / CRN) | power % there (M03 / CRN) | break-even water price USD/gal (M03 / CRN), where, w |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for fuel, h in H.items():
        v, where, w, cc = h["cost"]
        e = h["eff"]
        be = h["be"]
        bes = f"{be[0]:.2f} / {_p(be[3], '%.2f')}, {be[1]}, {be[2]:.3f}" if be else "-"
        M.append(f"| {fuel} | {where}, {w:.3f} | {_two(cc, 'cost_per_mile_pct')} | {_two(cc, 'power_change_pct')} | "
                 f"{C.verdict(cc)} | {e[1]}, {e[2]:.3f} | {_two(e[3], 'fuel_volume_per_work_pct')} | "
                 f"{_two(e[3], 'cost_per_mile_pct')} | {_two(e[3], 'cost_per_mile_water_free_pct')} | "
                 f"{_two(e[3], 'power_change_pct')} | {bes} |")
    return M


def write_track_b(P, out_md=TB / "COST.md"):
    res, L = track_b(P)
    H = headline(res)
    M = [f"# Water Engine - Track B cost metric\n\nGenerated {time.strftime('%Y-%m-%d %H:%M %Z')} by `python -m sims.cost.report` "
         "(also run by `python -m sims.track_b.report`). " + BANNER + "\n",
         "Rule (James, 2026-10-25 06:53 PDT): gains are judged on cost too. If adding water keeps power (horsepower) the "
         "same or better, the fuel it saves per unit work is a cost-per-mile (MPG) gain. Existing result files only - "
         "no new combustion runs.\n", method_md(), prices_md(P)]
    M += headline_md(P, H)
    M += ["\n## Every chain (both engines side by side)\n", HDR] + L
    M.append("\n" + CAVEATS)
    out_md.write_text("\n".join(M) + "\n")
    js = {"|".join(k): dict(eff_w=c["eff_row"].get("w"), eff=c["eff"], cost_w=c["cost_row"].get("w"), cost=c["cost"],
                            last_step=c["last_step"], stopped=c["stopped"]) for k, c in res.items()}
    (TB / "cost_trackb.json").write_text(json.dumps(js, indent=1, default=float))
    return res, H


# ------------------------------------------------------------------ Track A
def dry_refs():
    """Best eligible dry point per (fuel, regime): Track B dry sweep, else the H1 low-CR hot sweep."""
    refs = {}
    for p, tag in ((TB / "dry_sweep.json", "Track B dry sweep CR 9-24"), (TB / "h1_hot" / "dry_low_cr.json", "H1 low-CR CR 6-8")):
        if not p.exists():
            continue
        for r in json.loads(p.read_text()):
            if not _ok(r) or r.get("w", 0) != 0:
                continue
            k = (r["fuel"], r["regime"])
            if k in refs and refs[k][1] != tag:
                continue
            if k not in refs or r["gross_indicated_efficiency"] > refs[k][0]["gross_indicated_efficiency"]:
                refs[k] = (r, tag)
    return refs


def write_track_a(P, reopt=None):
    TA.mkdir(parents=True, exist_ok=True)
    refs = dry_refs()
    grid = TB / "trackA_humid_grid.json"
    g = [r for r in json.loads(grid.read_text()) if _ok(r)] if grid.exists() else []
    M = [f"# Water Engine - Track A cost metric\n\nGenerated {time.strftime('%Y-%m-%d %H:%M %Z')} by `python -m sims.cost.report`. "
         + BANNER + "\n",
         "Track A = water-majority work (w = 0.5-0.8). Source: `results/track_b/trackA_humid_grid.json` (Module 03 "
         "dual-regime rerun, 3 water modes, CR 12-24; **single engine - no M03-CRN values saved**, so every verdict is "
         "labelled 1 engine). Dry reference = best eligible dry point of the same fuel and regime (Track B continuous "
         "spark optimiser; hot CH3OH has none in CR 9-24, so the H1 low-CR hot baseline is used). Wet and dry points "
         "are at their own best CR (best-dry-engine vs best-wet-engine, as Track A has always been compared).\n",
         method_md(), prices_md(P), "\n## Track A grid (Module 03)\n",
         "| fuel | regime | mode | point | CR / T_intake / w | d_eta pp (M03) | power % | fuel volume per unit work % | "
         "**cost per mile %** | cost/mile if water free % | verdict | dry reference |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    js = {}
    for fuel in ("CH3OH", "C2H5OH", "CH4"):
        for reg in ("normal", "hot"):
            ref = refs.get((fuel, reg))
            for mode in MODES:
                pts = [r for r in g if r["fuel"] == fuel and r["regime"] == reg and r.get("water_mode") == mode]
                if not ref or not pts:
                    M.append(f"| {fuel} | {reg} | {mode} | - | no eligible {'dry reference' if not ref else 'wet point'} | | | | | | | |")
                    continue
                dry, tag = ref
                eff = max(pts, key=lambda r: r["gross_indicated_efficiency"])
                cb, cc = C.best_cost(pts, dry, P)
                for lab, row, c in (("eff-opt", eff, C.compare(eff, dry, P)), ("cost-opt", cb, cc)):
                    m = c["m03"]
                    M.append(f"| {fuel} | {reg} | {mode} | {lab} | {row['CR']:.0f} / {row['T_intake_K']:.0f} / {row.get('w', 0):.2f} | "
                             f"{m['d_eta_pp']:+.3f} | {m['power_change_pct']:+.2f} | {m['fuel_volume_per_work_pct']:+.2f} | "
                             f"{m['cost_per_mile_pct']:+.2f} | {m['cost_per_mile_water_free_pct']:+.2f} | {C.verdict(c)} | "
                             f"{tag}: CR {dry['CR']:.0f}, eta {dry['gross_indicated_efficiency']:.4f} |")
                    js[f"{fuel}|{reg}|{mode}|{lab}"] = dict(CR=row["CR"], T=row["T_intake_K"], w=row.get("w"), cost=c)
    if reopt and Path(reopt).exists():
        rows = read_jsonl(reopt)
        dry_rows = [r for r in rows if r.get("kind") == "dry" and _ok(r)]
        wet = [r for r in rows if r.get("kind") != "dry" and _ok(r)]
        M += ["\n## Track A wet re-optimisation (hot C2H5OH, water-majority, both engines)\n",
              f"Source: `{reopt}` (Track A re-opt branch, not yet committed here). Dry reference = best eligible dry "
              "point in the same file.\n", HDR]
        if dry_rows and wet:
            dry = max(dry_rows, key=lambda r: r["gross_indicated_efficiency"])
            eff = max(wet, key=lambda r: r["gross_indicated_efficiency"])
            cb, cc = C.best_cost(wet, dry, P)
            M.append(line("C2H5OH", "hot", "coupled", f"eff-opt CR {eff['CR']:.0f}", eff, C.compare(eff, dry, P)))
            M.append(line("C2H5OH", "hot", "coupled", f"cost-opt CR {cb['CR']:.0f}", cb, cc))
    M.append("\n" + CAVEATS.replace("* **Lower bounds at w = 0.10", "* (Track B only) **Lower bounds at w = 0.10"))
    (TA / "COST_TRACK_A.md").write_text("\n".join(M) + "\n")
    (TA / "cost_tracka.json").write_text(json.dumps(js, indent=1, default=float))
    return js


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--track-a-reopt", default="/workspace/we-trackA-reopt/results/track_a/wet_reopt/points_hot_eth_us.jsonl")
    a = ap.parse_args(argv)
    P = C.load_prices()
    write_track_b(P)
    write_track_a(P, a.track_a_reopt)
    print("wrote", TB / "COST.md", TA / "COST_TRACK_A.md")


if __name__ == "__main__":
    main()
