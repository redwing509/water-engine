"""Track B FIT EDGE (Claude review Oct 26 2026, item 3): the E10 hot humid_evap symmetric-DEI chain stopped at the
Cantera S_L fit edge w 0.300 while still gaining (both engines). Here, for E10 HOT ONLY (Claude's explicit ask;
the normal regime chain is not extended), the same flame method (sims/track_b/flame_w030.py: Cantera FreeFlame,
CRECK TPRF_HT_ALC_254_7568, phi 1, water vapour, hot IVC state) is extended to w 0.45: existing w 0..0.25 points are
reused, w 0.30 is solved fresh (consistency vs the existing 0.30 point), then 0.35/0.40/0.45 by continuation. Same
cubic fit over w 0..0.45, RMS reported. The chain continues from step 300 (w 0.300 recomputed with the new fit =
consistency row, used as prev) with the same rule (0.1-pp steps, spark re-optimised, M03 gain > 3.3e-5 AND
M03-CRN gain > 0), cap 450 (w 0.45 = new fit edge). Both engines. Cost metric (sims/cost) vs the fair dry-evap
(DEI w 0) baseline: $0.10/gal water headline, $0 secondary.
Tags: Track B; hot regime only (by request); executed (2 engines); NOT validated.
    python -m sims.track_b.fitedge_w045 flames      # ~1-1.3 h, 1 core
    python -m sims.track_b.fitedge_w045 chain N
    python -m sims.track_b.fitedge_w045 report
"""
import json, os, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from sims.track_b import run as R

OUT = R.OUT / "fitedge_w045"
FLD = OUT / "cantera_flames"
SYM = Path(os.environ.get("FE_SYM", "/workspace/we-tbmail/results/track_b/symmetric_dei"))
OLD = R.OUT / "w030" / "cantera_flames" / "E10_hot.json"
MECH = os.environ.get("FE_MECH", "/workspace/boxwork0700/tprf/tprf_ht_alc.yaml")  # sha256 47fde27a... (= rig1jobs copy)
WMAX, CAP, START = 0.45, 450, 300
ENV = dict(W030_FL_DIR=str(FLD), W030_WMAX=str(WMAX), W030_FIT_ONLY="E10/hot")


def flames():
    FLD.mkdir(parents=True, exist_ok=True)
    new = FLD / "E10_hot_new.json"
    if not new.exists():
        env = dict(os.environ, FL_WS="0.30,0.35,0.40,0.45")
        subprocess.run([sys.executable, "sims/track_b/flame_w030.py", MECH, "E10", "hot", str(new)], check=True, env=env)
    old = json.loads(OLD.read_text()); nw = json.loads(new.read_text())
    rows = [r for r in old if r["w"] < 0.30 - 1e-9] + nw
    (FLD / "E10_hot.json").write_text(json.dumps(rows, indent=1))
    fit_md()


def fit_md():
    rows = json.loads((FLD / "E10_hot.json").read_text()); old = json.loads(OLD.read_text())
    ws = np.array([r["w"] for r in rows]); sl = np.array([r["S_L_m_s"] for r in rows])
    c = np.polyfit(ws, sl, 3); rms = float(np.sqrt(np.mean((np.polyval(c, ws) - sl) ** 2)))
    wo = np.array([r["w"] for r in old]); so = np.array([r["S_L_m_s"] for r in old]); co = np.polyfit(wo, so, 3)
    rms_o = float(np.sqrt(np.mean((np.polyval(co, wo) - so) ** 2)))
    o30 = next(r["S_L_m_s"] for r in old if abs(r["w"] - 0.30) < 1e-9)
    n30 = next(r["S_L_m_s"] for r in rows if abs(r["w"] - 0.30) < 1e-9)
    d = dict(coefficients_highest_first=c.tolist(), rms_m_s=rms, rms_old_0_030=rms_o, n_points=len(rows),
             S_L_030_existing=o30, S_L_030_fresh=n30, fit_030_new=float(np.polyval(c, 0.30)),
             fit_030_old=float(np.polyval(co, 0.30)), points=[(r["w"], r["S_L_m_s"]) for r in rows])
    (OUT / "fit_w045.json").write_text(json.dumps(d, indent=1))
    return d


def chain(n):
    from sims.track_b import chains_sym as CS
    os.environ.update(ENV)          # inherited by the spawn workers (chains_w030.use_fits reads it)
    OUT.mkdir(parents=True, exist_ok=True)
    for f in ("dei_hardware.json", "w0_rows.json"):
        if not (OUT / f).exists():
            shutil.copy(SYM / f, OUT / f)
    CS.OUT, CS.CAP = OUT, CAP
    CS.chains(n, f"E10/hot/humid_evap/{START}")


def report():
    from sims.cost import cost as C, report as REP
    from sims.track_b import chains_sym as CS
    fit = fit_md()
    p = OUT / CS.chain_name("E10", "hot", "humid_evap", START)
    old = REP.chain_cost(SYM / CS.chain_name("E10", "hot", "humid_evap", 0))
    md = ["# Track B fit edge: E10 hot humid_evap chain past w 0.30 (EXECUTED, 2 engines; NOT validated)", "",
          "Claude review Oct 26 2026 item 3. **Hot regime only, by Claude's explicit ask** (the both-regimes rule is "
          "waived for this extension; the E10 normal chain is not extended). Knock label: knock engine 2: ranking "
          "validated, absolute klCR offset +2-2.5 CR vs M03 (gate FAILED); not used for this chain's stop rule.", "",
          "## S_L fit (same method: Cantera FreeFlame CRECK TPRF_HT_ALC, phi 1, water vapour, hot IVC state, cubic)", "",
          f"- w 0..0.45, {fit['n_points']} points: RMS {fit['rms_m_s'] * 100:.3f} cm/s (old w 0..0.30 fit RMS "
          f"{fit['rms_old_0_030'] * 100:.3f} cm/s).",
          f"- w 0.30 consistency: existing point {fit['S_L_030_existing']:.4f} m/s, fresh solve {fit['S_L_030_fresh']:.4f} "
          f"m/s; fit at 0.30 old {fit['fit_030_old']:.4f} vs new {fit['fit_030_new']:.4f} m/s.",
          "- points (w, S_L m/s): " + ", ".join(f"{w:.2f}: {s:.4f}" for w, s in fit["points"]), ""]
    if not p.exists():
        md.append("Chain: NOT RUN / no output.")
    else:
        rows = REP.read_jsonl(p)
        st = [r for r in rows if r.get("kind") == "step"]
        c = REP.chain_cost(p)
        stop = next((r.get("stop_reason") for r in st if r.get("decision") == "stop"), None)
        cons = next((r for r in st if r.get("step") == START), {})
        oldr = next((r for r in REP.read_jsonl(SYM / CS.chain_name("E10", "hot", "humid_evap", 0))
                     if r.get("step") == START), {})
        fails = [f"{r['w']:.3f}:{r.get('status')}/{r.get('crn_status')}" for r in st
                 if r.get("status") != "computed" or r.get("crn_status") != "ok"]
        e = c["eff"]
        md += ["## Chain (continuation from step 300, CR %s, T_intake 400 K, wall 520 K)" % rows[0].get("CR"), "",
               f"- consistency row w 0.300: eta M03 {cons.get('gross_indicated_efficiency')} (old fit "
               f"{oldr.get('gross_indicated_efficiency')}), CRN {cons.get('crn_efficiency')} (old {oldr.get('crn_efficiency')})",
               f"- stop: w {c['eff_row'].get('w'):.3f} (last accepted); reason: {stop or ('cap 450 / incomplete')}",
               f"- d_eta vs DEI dry baseline (pp, M03 / CRN): {REP._two(e, 'd_eta_pp')}  (was at w 0.300: "
               f"{REP._two(old['eff'], 'd_eta_pp') if old else '-'})",
               f"- failed rows: {', '.join(fails) or 'none'}", "",
               "## Cost metric vs the fair dry-evap (DEI w 0) baseline", "", REP.HDR]
        md.append(REP.line("E10", "hot", "humid_evap", "best-eff (last accepted)", c["eff_row"], c["eff"]))
        md.append(REP.line("E10", "hot", "humid_evap", "cost-optimal w ($0.10, within w 0.30..stop)", c["cost_row"], c["cost"]))
        md.append(REP.line("E10", "hot", "humid_evap", "cost-optimal w ($0 water, secondary)", c["free_row"], c["free"]))
        if old:
            md.append(REP.line("E10", "hot", "humid_evap", "previous stop w 0.300 (old fit)", old["eff_row"], old["eff"]))
        md += ["", f"Cost per kWh % at $0.10 (M03 / CRN), best-eff: {REP._two(e, 'cost_per_kwh_pct')}; fuel energy per work "
               f"% (M03 / CRN): {REP._two(e, 'fuel_energy_per_work_pct')}; mpg % (M03 / CRN): {REP._two(e, 'mpg_pct')}.",
               f"Verdict ($0.10/gal): **{C.verdict(e)}**; at $0 water: "
               f"{C.verdict(REP.C.compare(c['eff_row'], c['dry'], None, 'free'))}.", "",
               "Caveats: ignition correlation has no explicit w term (valid_w_range label widened to 0.45, assumption); "
               "S_L at the IVC state, not engine pressure; fit change at w 0.300: steps < 0.300 used the w 0..0.30 fit, steps "
               ">= 0.300 the w 0..0.45 fit (the w 0.300 consistency row above gives the size of the change)."]
        (OUT / "fitedge_table.json").write_text(json.dumps(dict(stop_w=c["eff_row"].get("w"), stop=stop, eff=e,
                                                                cost=c["cost"], free=c["free"], fit=fit), indent=1, default=float))
    (OUT / "FITEDGE.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    c = sys.argv[1]
    {"flames": flames, "report": report}.get(c, lambda: chain(int(sys.argv[2])))()
