"""Track B B3 (R-WE-08/09): stopping points as water/fuel ratio and all routes vs TOTAL in-cylinder water.

Total in-cylinder water here = added water (any route) / trapped charge mass (air+fuel+water+residual);
residual-gas water from combustion is not separated out by Module 03 and is excluded (same for all routes).
Literature: WE-27 (+1.5 % thermal efficiency only with spark advance, optimum ~30 % water/gasoline vol),
WE-28 (knock-free above 10 % water/fuel), WE-25/26 (knock relief tracks total in-cylinder water).
Labels: executed, 2-engine, literature-compared (not validated).
"""
import glob, json, os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RHO = {"PRF87": 692.0, "PRF91": 692.0, "PRF97": 692.0, "E10": 745.0, "E85": 785.0,
       "CH3OH": 791.0, "C2H5OH": 789.0, "CH4": None}  # kg/m3 liquid at ~20 C; CH4 is gaseous
RHO_W = 998.0
OUT = Path("results/track_b")


def load():
    chains = {}
    for f in sorted(glob.glob("results/track_b/steps_*__noise.jsonl")):
        recs = [json.loads(l) for l in open(f) if l.strip()]
        recs = [r for r in recs if r.get("status") == "computed" and r.get("kind") in ("dry_baseline", "step")
                and r.get("eligible")]
        if recs:
            chains[Path(f).stem.replace("steps_", "").replace("__noise", "")] = recs
    return chains


def tot_water(r):
    m = r["air_mass_kg"] + r["fuel_mass_kg"] + r["water_mass_kg"] + (r.get("residual_mass_kg") or 0)
    return r["water_mass_kg"] / m


def main():
    chains = load()
    rows = []
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    for name, recs in chains.items():
        dry = recs[0]
        best = max(recs, key=lambda r: r["gross_indicated_efficiency"])
        mode = "humid_evap" if name.endswith("humid_evap") else "humid_ambient" if name.endswith("humid_ambient") else "liquid"
        fuel = best["fuel"]
        wf_mass = best["water_mass_kg"] / best["fuel_mass_kg"]
        wf_vol = (wf_mass * RHO[fuel] / RHO_W) if RHO[fuel] else None
        rows.append(dict(chain=name, fuel=fuel, regime=best["regime"], mode=mode, w_best=best["w"],
                         water_fuel_mass_pct=100 * wf_mass,
                         water_fuel_vol_pct=None if wf_vol is None else 100 * wf_vol,
                         total_incyl_water_pct=100 * tot_water(best),
                         d_eta_pp_m03=100 * (best["gross_indicated_efficiency"] - dry["gross_indicated_efficiency"]),
                         d_eta_pp_crn=100 * (best["crn_efficiency"] - dry["crn_efficiency"]),
                         in_WE27_window_10_30pct=None if wf_vol is None else bool(0.10 <= wf_vol <= 0.30)))
        x = [100 * tot_water(r) for r in recs]
        y = [100 * (r["gross_indicated_efficiency"] - dry["gross_indicated_efficiency"]) for r in recs]
        k = [r.get("knock_margin") or 0 for r in recs]
        st = {"liquid": "-", "humid_evap": "--", "humid_ambient": ":"}[mode]
        ax[0].plot(x, y, st, label=f"{fuel} {best['regime']} {mode}")
        ax[1].plot(x, [r["ca50_used_deg"] for r in recs], st)
    ax[0].axhline(1.5, color="k", lw=0.8)
    ax[0].text(0.02, 1.52, "WE-27 +1.5 % (with spark advance, ~30 % vol water/gasoline)", fontsize=7)
    ax[0].set_xlabel("total added in-cylinder water, % of trapped mass"); ax[0].set_ylabel("d eta vs dry, pp (Module 03)")
    ax[1].set_xlabel("total added in-cylinder water, % of trapped mass"); ax[1].set_ylabel("CA50 used, deg aTDC")
    ax[0].legend(fontsize=5, ncol=2)
    fig.suptitle("Track B: all water routes vs total in-cylinder water (executed, 2-engine; literature-compared)")
    fig.tight_layout(); fig.savefig(OUT / os.environ.get("LIT_PNG", "lit_compare.png"), dpi=130)
    (OUT / os.environ.get("LIT_JSON", "lit_compare.json")).write_text(json.dumps(rows, indent=1))
    hdr = "| chain | w best | water/fuel mass % | water/fuel vol % | total in-cyl water % | d_eta M03 / CRN pp | in WE-27 10-30 % vol window |"
    lines = [hdr, "|" + "---|" * 7]
    for r in rows:
        v = "n/a (gas)" if r["water_fuel_vol_pct"] is None else f"{r['water_fuel_vol_pct']:.1f}"
        lines.append(f"| {r['chain']} | {r['w_best']:.3f} | {r['water_fuel_mass_pct']:.1f} | {v} | "
                     f"{r['total_incyl_water_pct']:.2f} | {r['d_eta_pp_m03']:+.3f} / {r['d_eta_pp_crn']:+.3f} | "
                     f"{r['in_WE27_window_10_30pct']} |")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
