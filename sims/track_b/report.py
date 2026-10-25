"""Build TRACKS.md (Track A vs Track B best results per fuel, humid-intake comparison) from results/.

Run:  python -m sims.track_b.report [--out TRACKS.md]
Robust to partial results: chains still running are reported as 'in progress' with the last step.
"""
import argparse
import glob
import json
import os
import time
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "results" / "track_b"
GAIN_THRESHOLD = 1.0e-4

# Track A references (existing water-majority work); copied from committed results, see 'source'.
TRACK_A = {
    "CH3OH": dict(legacy_best="CR 23, w 0.30, 320 K: 0.4543", legacy_wmaj="CR 24, w 0.60, 360 K: 0.4310",
                  legacy_dry="CR 16: 0.4207", coupled_normal="wet 0.4543 (CR 23, w 0.3) vs dry 0.4207",
                  coupled_hot="wet 0.4488 (CR 23, w 0.3); no eligible hot dry point"),
    "C2H5OH": dict(legacy_best="CR 23, w 0.40: 0.4529", legacy_wmaj="w >= 0.5: 0.4378",
                   legacy_dry="CR 24: 0.4455", coupled_normal="wet 0.4529 vs dry 0.4455",
                   coupled_hot="wet 0.4493 (CR 23, w 0.4) vs dry 0.3837 (CR 11)"),
    "CH4": dict(legacy_best="CR 23, w 0.50: 0.4484", legacy_wmaj="CR 23, w 0.60: 0.4463",
                legacy_dry="CR 22: 0.4327", coupled_normal="not in coupled set", coupled_hot="not in coupled set"),
}
TRACK_A_SRC = "results/03_engine_cycle/design_point.json (legacy) and results/03_engine_cycle/coupled_points.csv (PR 8 coupled)"


def load_chain(path):
    rows = {}
    for line in open(path):
        r = json.loads(line)
        rows[(r["kind"], r["w"])] = r
    return rows


def f(x, fmt="%.4f"):
    return "-" if x is None else fmt % x


def chain_summary(rows):
    base = next((r for k, r in rows.items() if k[0] == "dry_baseline"), None)
    steps = sorted((r for k, r in rows.items() if k[0] == "step"), key=lambda r: r["w"])
    probes = sorted((r for k, r in rows.items() if k[0].startswith("exploratory")), key=lambda r: r["w"])
    best, prev, stop = base, base, None
    for s in steps:
        ok = s["status"] == "computed" and s["eligible"]
        g = (s["gross_indicated_efficiency"] - prev["gross_indicated_efficiency"]) if ok else None
        gc = (s["crn_efficiency"] - prev["crn_efficiency"]) if ok and s.get("crn_efficiency") else None
        s["_gain"], s["_crn_gain"] = g, gc
        if ok and g > GAIN_THRESHOLD and (gc or 0) > 0:
            best = prev = s
        else:
            stop = ("not eligible/failed" if not ok else f"gain {g:.2e} <= threshold {GAIN_THRESHOLD:.0e}"
                    if g <= GAIN_THRESHOLD else f"CRN gain {gc}")
            break
    return base, steps, probes, best, stop


def row(r, base):
    d = r["gross_indicated_efficiency"] - base["gross_indicated_efficiency"]
    dc = (r["crn_efficiency"] - base["crn_efficiency"]) if r.get("crn_efficiency") else None
    q = r.get("specific_humidity_kg_per_kg_dry_air")
    return (f"| {r['kind'].replace('exploratory_probe_not_a_track_b_step', 'probe*')} | {r['w']:.3f} | "
            f"{f(r['gross_indicated_efficiency'], '%.5f')} | {f(r.get('crn_efficiency'), '%.5f')} | "
            f"{d * 100:+.3f} | {f(dc * 100 if dc is not None else None, '%+.3f')} | {f(r.get('d_eta_pp'), '%+.3f')} | "
            f"{r['knock_margin']:.4f} | {r['ca50_used_deg']:.2f} ({r['spark_limited_by']}) | "
            f"{r['peak_pressure_Pa'] / 1e5:.1f} / {f((r.get('crn_p_max_Pa') or 0) / 1e5, '%.1f')} | "
            f"{r['NO_mol_per_J_fuel']:.2e} | {f(q * 1000 if q else None, '%.2f')} | {r.get('c1_pass')} |")


HDR = ("| kind | w | eta M03 | eta CRN | d_eta M03 (pp vs dry) | d_eta CRN (pp) | CRN-M03 (pp) | knock margin (1-KI) | "
       "CA50 deg aTDC (limit) | p_max M03 / CRN bar | NO proxy mol/J (M03) | q g/kg dry air | C1 pass |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|---|---|")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO / "results" / "track_b" / "TRACKS.md"))
    a = ap.parse_args()
    L = []
    P = L.append
    P("# Water Engine - Track A / Track B status")
    P(f"\nGenerated {time.strftime('%Y-%m-%d %H:%M %Z')} by `python -m sims.track_b.report` (branch "
      "`track-b/incremental-water-20261024`). **NOT YET PEER-REVIEW VERIFIED** - Module 03 and M03-CRN are "
      "two in-repo engines from the same toolchain; independent engine review (2+ engine rule) still pending.\n")
    P("## Rules (James, 2026-10-24)\n")
    P("* **Two tracks, ~50/50 compute.** Track A = existing water-majority work. Track B = start from normal fuels "
      "(regular/premium gasoline surrogates, E10, E85, methanol, ethanol, methane) dry, then add water in steps "
      "of at most 0.1 percentage point (w = m_water/(m_water+m_fuel) += 0.001), adding more only while efficiency "
      "gains; use data from both tracks to help each other.")
    P("* **Humid intake (6:22 PM rule)**, both tracks: water atomised into the intake air and fully evaporated "
      "before the cylinder (charge = humid air, specific humidity q). Track B: same 0.1-pp steps as humid water. "
      "Track A: humid variant of water-majority cases, capped by intake saturation (excess would condense).")
    P(f"* Gain threshold stated before any step ran: **{GAIN_THRESHOLD:.0e} absolute (0.01 pp)** per step in "
      "Module 03 (~3x the 0.5-CAD step error ~3e-5, ~15x GCI 1.4e-5 relative; verification/x5_m03/RESULTS_FIX.md) "
      "AND a positive M03-CRN gain. Spark re-optimised at every step (golden-section MBT on CA50 0-16 deg, else "
      "knock/p_max-limited bisection to 0.005 deg).")
    P("* **Knock margin, CA50 limit and NO proxy come from Module 03 only** (M03-CRN has no knock or NOx model); "
      "M03-CRN gives an independent efficiency and peak pressure at the same CA50 (Woschni, like-for-like; "
      "C1 pass = |d_eta| <= 1.5 pp and |p_max ratio - 1| <= 5 %).")

    # dry baselines
    P("\n## Track B dry baselines (Module 03, spark at MBT or knock limit; best eligible CR x T_intake)\n")
    dry = json.loads((OUT / "dry_sweep.json").read_text())
    P("| fuel | regime | eligible pts | CR | T_intake K | eta M03 | CA50 (limit) | p_max bar | NO mol/J |\n|---|---|---|---|---|---|---|---|---|")
    fuels = []
    for r in dry:
        if r["fuel"] not in fuels:
            fuels.append(r["fuel"])
    for fu in fuels:
        for g in ("normal", "hot"):
            el = [r for r in dry if r["fuel"] == fu and r["regime"] == g and r.get("eligible")]
            if not el:
                P(f"| {fu} | {g} | 0 | - | - | - | knock-limited CA50 > 15 deg even at CR 9 (no eligible point) | - | - |")
                continue
            b = max(el, key=lambda r: r["gross_indicated_efficiency"])
            P(f"| {fu} | {g} | {len(el)} | {b['CR']:.0f} | {b['T_intake_K']:.0f} | {b['gross_indicated_efficiency']:.4f} | "
              f"{b['ca50_used_deg']:.2f} ({b['spark_limited_by']}) | {b['peak_pressure_Pa'] / 1e5:.1f} | {b['NO_mol_per_J_fuel']:.2e} |")

    # chains
    groups = defaultdict(dict)
    for p in sorted(glob.glob(str(OUT / "steps_*.jsonl"))):
        name = Path(p).stem[6:]
        mode = "liquid"
        for m in ("humid_evap", "humid_ambient"):
            if name.endswith("_" + m):
                mode, name = m, name[: -len(m) - 1]
        groups[name][mode] = load_chain(p)
    P("\n## Track B 0.1-pp water chains\n")
    P("Water modes: **liquid** = water in fuel / port liquid (legacy Module 03: half evaporates in the intake, rest "
      "in-cylinder); **humid_evap** = all water atomised and evaporated in the intake with latent cooling (wet-bulb "
      "limited; humid air, cooled charge); **humid_ambient** = water vapour already in the intake air at T_intake "
      "(no evaporative cooling; pure humidity/dilution effect). p_IVC fixed, so evaporative cooling raises trapped "
      "mass (charge density) and vapour displaces O2 (lower O2 partial pressure) automatically; there is no "
      "gas-exchange model, so volumetric-efficiency effects beyond charge density are NOT modelled.\n")
    P("| fuel/regime | mode | dry eta M03 / CRN | best w (Track B rule) | steps | stop | best eta M03 / CRN | status |\n|---|---|---|---|---|---|---|---|")
    summ = {}
    for name, modes in groups.items():
        for mode, rows in modes.items():
            base, steps, probes, best, stop = chain_summary(rows)
            summ[(name, mode)] = (base, steps, probes, best, stop)
            n = len(steps)
            status = "done" if stop or n >= 100 or probes else f"in progress (step {n})"
            P(f"| {name} | {mode} | {base['gross_indicated_efficiency']:.5f} / {base['crn_efficiency']:.5f} | "
              f"{best['w']:.3f} | {best.get('step', 0)} | {stop or ('cap' if n >= 100 else '-')} | "
              f"{best['gross_indicated_efficiency']:.5f} / {best['crn_efficiency']:.5f} | {status} |")
    P("\n*probe = exploratory point at w = 1/2/5/10 %, same hardware, spark re-optimised; NOT a Track B step "
      "(the 0.1-pp rule stopped earlier). Shown because every gasoline/E-blend chain shows a steady positive "
      "slope just under the per-step threshold.\n")
    for (name, mode), (base, steps, probes, best, stop) in summ.items():
        P(f"\n### {name} - {mode}\n")
        P(HDR)
        P(row(base, base))
        for s in steps:
            if s["status"] == "computed":
                P(row(s, base))
        for s in probes:
            if s["status"] == "computed":
                P(row(s, base))

    # Track A humid grid
    P("\n## Track A humid-intake variant (water-majority cases, w = 0.5-0.8)\n")
    gp = OUT / "trackA_humid_grid.json"
    if gp.exists():
        g = [r for r in json.loads(gp.read_text()) if r.get("status") == "computed"]
        P(f"{len(g)} computed points so far (of 756). Best eligible per fuel x regime x mode (both engines):\n")
        P("| fuel | regime | mode | best CR / T / w | eta M03 | eta CRN | CA50 (limit) | q g/kg | fraction of water evaporated in intake | saturation-limited |\n|---|---|---|---|---|---|---|---|---|---|")
        for fu in ("CH3OH", "C2H5OH", "CH4"):
            for reg in ("normal", "hot"):
                for mode in ("liquid", "humid_evap", "humid_ambient"):
                    el = [r for r in g if r["fuel"] == fu and r["regime"] == reg and r.get("water_mode") == mode and r["eligible"]]
                    if not el:
                        P(f"| {fu} | {reg} | {mode} | none eligible yet | | | | | | |")
                        continue
                    b = max(el, key=lambda r: r["gross_indicated_efficiency"])
                    q = b.get("specific_humidity_kg_per_kg_dry_air")
                    P(f"| {fu} | {reg} | {mode} | {b['CR']:.0f} / {b['T_intake_K']:.0f} / {b['w']:.1f} | "
                      f"{b['gross_indicated_efficiency']:.4f} | {f(b.get('crn_efficiency'))} | {b['ca50_used_deg']:.2f} ({b['spark_limited_by']}) | "
                      f"{f(q * 1000 if q else None, '%.1f')} | {f(b.get('f_evap_intake_effective'), '%.3f')} | "
                      f"{b.get('intake_saturation_limited') or b.get('port_evap_saturation_limited')} |")
    else:
        P("Grid still queued/running (results/track_b/trackA_humid_grid.json not yet written).")
    P("\nSaturation check done by hand (CH3OH, CR 20, 320 K, w = 0.6): with intake evaporative cooling the air "
      "saturates after ~5.4 % of the water (q ~ 12.6 g/kg, T_IVC 296 K); without cooling (vapour at 320 K) ~34 %. "
      "The remaining 66-95 % of water-majority water cannot be carried as vapour - it would condense on the "
      "runners/ports and arrive as liquid film or droplets. A water-majority charge therefore can NOT be a "
      "humid-air charge; Track A humid results are saturation-capped by construction.")

    P("\n## Track A references (existing water-majority work, best per fuel)\n")
    P(f"Source: {TRACK_A_SRC}.\n")
    P("| fuel | legacy best overall | legacy water-majority | legacy dry | coupled normal | coupled hot |\n|---|---|---|---|---|---|")
    for k, v in TRACK_A.items():
        P(f"| {k} | {v['legacy_best']} | {v['legacy_wmaj']} | {v['legacy_dry']} | {v['coupled_normal']} | {v['coupled_hot']} |")
    P("\nNote: Track A legacy points used the 2-CAD retard search; Track B dry baselines use the continuous spark "
      "optimiser, so Track B dry values differ slightly from Track A dry values (e.g. CH3OH dry 0.4238 vs 0.4207).")

    extra = REPO / "results" / "track_b" / "TRACKS_notes.md"
    if extra.exists():
        P("\n" + extra.read_text())
    Path(a.out).write_text("\n".join(L) + "\n")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
