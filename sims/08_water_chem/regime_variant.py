"""Module 08 dated normal + hot regime variant (Grok Bot, 2026-10-24; takeover of Hermes's water-engine-spray r5).

Track A (water-majority, w = 0.6) with the dry (w = 0) and w = 0.3 references. Status: EXECUTED, single engine.

Regimes (James's dual-temperature rule, 2026-10-24; values copied from sims/dual_temp/regimes.py on wme1-hiT):
  normal: coolant 363.15 K, chamber gas-side wall 450 K, port wall 363.15 K, intake charge T_u 320 K and 360 K
  hot:    coolant 388.15 K, chamber gas-side wall 520 K, port wall 388.15 K, intake charge T_u 400 K
  hot heated-port bound: port wall 420 K; used here as an intake-charge upper bound T_u = 420 K (bounding sensitivity,
          a charge that fully equilibrates with a 420 K port; not a nominal operating point)
  Sources: MAHLE "Vehicle cooling" compact knowledge / VW SSP 222 (coolant 85-95 C full load, 95-110 C part load);
  SAE 960271 (110 C part-load coolant); Heywood, Internal Combustion Engine Fundamentals ch. 12 (gas-side wall 400-600 K);
  SPEC section 6 (450 K Woschni wall); Module 03/09 intake sweeps (320/360/400-420 K).

What module 08 can and cannot say: it is a 0-D/1-D chemistry module. Coolant, chamber-wall and port-wall temperatures
enter ONLY through the unburned-charge temperature T_u. It computes T_ad (1 atm, HP equilibrium), S_L (1 atm, freely
propagating flame), tau_ig at TDC-equivalent states (frozen-composition isentropic compression from T_u, 1 bar by the
volume ratio CR = 16 and 24, same construction as xcheck/chem J2), and the water chemical-effect decomposition
(real / FH2O-a / FH2O-b). Efficiency, p_max, CA50, wall heat loss, NOx and MIE are NOT computed here (module 03 / 11).

Checks stated before the run:
  C1  TDC states at T_u = 360/400 K reproduce J2 (j2_tdc_states_sandiego.json) within 0.1 K and 0.1 %.
  C2  'real' T_ad and tau_ig at 360/400 K reproduce dual_temp.json within 1e-6 relative.
  C3  S_L grid sensitivity for the w = 0.3 chemical-effect sign question: real and FH2O-b flames re-solved with tighter
      refinement (ratio 2, slope 0.03, curve 0.06) at T_u = 360 K; the chem effect must keep its sign and move < 1 pp.
"""
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import importlib  # noqa: E402

m08 = importlib.import_module("sims.08_water_chem.run")
OUT = ROOT / "results" / "08_water_chem_regimes"
DATE = "2026-10-24"
REGIMES = {
    "normal": dict(coolant_K=363.15, chamber_wall_K=450.0, port_wall_K=363.15, T_u_K=(320.0, 360.0)),
    "hot": dict(coolant_K=388.15, chamber_wall_K=520.0, port_wall_K=388.15, T_u_K=(400.0,)),
    "hot_heated_port_bound": dict(coolant_K=388.15, chamber_wall_K=520.0, port_wall_K=420.0, T_u_K=(420.0,)),
}
CITATIONS = ["MAHLE 'Vehicle cooling' compact knowledge (VW SSP 222)", "SAE 960271", "SAE 2010-01-0802",
             "Heywood, ICE Fundamentals, ch. 12", "WME-1 SPEC section 6", "sims/dual_temp/regimes.py (wme1-hiT)"]
FUELS = ("CH3OH", "C2H5OH")
W = (0.0, 0.3, 0.6)
CRS = (16.0, 24.0)
P_IVC = 1.0e5
TAU_MAX = 0.5
VARIANTS = m08.MECHANISM_VARIANTS


def points():
    for reg, d in REGIMES.items():
        for Tu in d["T_u_K"]:
            yield reg, Tu


def tdc_state(fuel, w, Tu, cr):
    gas = m08._gas(fuel, "real", 1.0, w, Tu, P_IVC)
    s, v = gas.entropy_mass, 1.0 / gas.density
    gas.SV = s, v / cr
    return float(gas.T), float(gas.P)


def tight_flame(fuel, variant, w, Tu):
    p = m08.DEFAULTS
    saved = (p.refine_ratio, p.refine_slope, p.refine_curve)
    try:
        object.__setattr__(p, "refine_ratio", 2.0)
        object.__setattr__(p, "refine_slope", 0.03)
        object.__setattr__(p, "refine_curve", 0.06)
        return m08.flame_speed(fuel, variant, 1.0, w, Tu, 101325.0)
    finally:
        for k, val in zip(("refine_ratio", "refine_slope", "refine_curve"), saved):
            object.__setattr__(p, k, val)


def _task(t):
    kind, meta, args = t
    if kind == "tad":
        r = m08.adiabatic_temperature(*args)
    elif kind == "flame":
        r = m08.flame_speed(*args)
    elif kind == "flame_tight":
        r = tight_flame(*args)
    else:
        r = m08.ignition_delay(*args)
    r.update(meta)
    return kind, r


def build():
    tdc, tasks = [], []
    for fuel in FUELS:
        for w in W:
            vs = ("real",) if w == 0.0 else VARIANTS   # w = 0: variants identical by construction (module 08 _gas)
            for reg, Tu in points():
                meta = dict(regime=reg, T_u_K=Tu)
                for v in vs:
                    tasks.append(("tad", meta, (fuel, v, 1.0, w, Tu, 101325.0)))
                    tasks.append(("flame", meta, (fuel, v, 1.0, w, Tu, 101325.0)))
                for cr in CRS:
                    T, p = tdc_state(fuel, w, Tu, cr)
                    tdc.append(dict(fuel=fuel, w=w, regime=reg, T_u_K=Tu, CR=cr, T_TDC_K=T, p_TDC_bar=p / 1e5))
                    for v in vs:
                        tasks.append(("ign", dict(meta, CR=cr), (fuel, v, 1.0, w, T, p, TAU_MAX)))
    for fuel in FUELS:
        for v in ("real", "fh2o_b"):
            tasks.append(("flame_tight", dict(regime="normal", T_u_K=360.0), (fuel, v, 0.3, 360.0)))
    return tdc, tasks


def pick(rows, key, **kw):
    for r in rows:
        if all((abs(r[k] - val) < 1e-9 if isinstance(val, float) else r[k] == val) for k, val in kw.items()):
            return r.get(key)
    return None


def rel(a, b):
    return None if (a is None or b is None) else a / b - 1.0


def analyse(tdc, rows):
    eff = []
    for fuel in FUELS:
        for w in W:
            for reg, Tu in points():
                e = dict(fuel=fuel, w=w, regime=reg, T_u_K=Tu)
                g = lambda kind, key, v, **kw: pick(rows[kind], key, fuel=fuel, w=w, T_u_K=Tu,
                                                    variant=("real" if w == 0.0 else v), **kw)
                e["T_ad_K"] = g("tad", "T_ad_K", "real")
                e["S_L_m_s"] = g("flame", "S_L_m_s", "real")
                if w > 0:
                    r_, a_, b_ = (g("flame", "S_L_m_s", v) for v in VARIANTS)
                    e.update(S_L_chem=rel(r_, b_), S_L_third_body=rel(a_, b_), S_L_direct=rel(r_, a_))
                for cr in CRS:
                    e[f"T_TDC_CR{cr:g}_K"] = pick(tdc, "T_TDC_K", fuel=fuel, w=w, T_u_K=Tu, CR=cr)
                    e[f"tau_CR{cr:g}_s"] = g("ign", "tau_s", "real", CR=cr)
                    if w > 0:
                        r_, a_, b_ = (g("ign", "tau_s", v, CR=cr) for v in VARIANTS)
                        e.update({f"tau_CR{cr:g}_chem": rel(r_, b_), f"tau_CR{cr:g}_third_body": rel(a_, b_),
                                  f"tau_CR{cr:g}_direct": rel(r_, a_)})
                eff.append(e)
    # hot vs normal side by side (reference normal 360 K = J2 normal; also vs 320 K)
    side = []
    for fuel in FUELS:
        for w in W:
            base = {Tu: next(e for e in eff if e["fuel"] == fuel and e["w"] == w and e["T_u_K"] == Tu)
                    for _, Tu in points()}
            for ref in (320.0, 360.0):
                for hot in (400.0, 420.0):
                    b, h = base[ref], base[hot]
                    s = dict(fuel=fuel, w=w, normal_T_u_K=ref, hot_T_u_K=hot,
                             dT_ad_K=None if None in (h["T_ad_K"], b["T_ad_K"]) else h["T_ad_K"] - b["T_ad_K"],
                             S_L_ratio=None if not (h["S_L_m_s"] and b["S_L_m_s"]) else h["S_L_m_s"] / b["S_L_m_s"])
                    for cr in CRS:
                        th, tb = h[f"tau_CR{cr:g}_s"], b[f"tau_CR{cr:g}_s"]
                        s[f"tau_CR{cr:g}_ratio"] = None if not (th and tb) else th / tb
                        if w > 0:
                            ch, cb = h.get(f"tau_CR{cr:g}_chem"), b.get(f"tau_CR{cr:g}_chem")
                            s[f"tau_CR{cr:g}_chem_shift_pp"] = None if None in (ch, cb) else 100 * (ch - cb)
                    if w > 0:
                        ch, cb = h.get("S_L_chem"), b.get("S_L_chem")
                        s["S_L_chem_shift_pp"] = None if None in (ch, cb) else 100 * (ch - cb)
                    side.append(s)
    checks = {}
    j2 = json.loads((ROOT / "results/08_water_chem_dualT/j2_tdc_states_sandiego.json").read_text())["rows"]
    c1 = []
    for r in j2:
        mine = next(t for t in tdc if t["fuel"] == r["fuel"] and abs(t["w"] - r["w"]) < 1e-9
                    and t["T_u_K"] == r["T_u_K"] and t["CR"] == r["CR"])
        c1.append(dict(fuel=r["fuel"], w=r["w"], T_u_K=r["T_u_K"], CR=r["CR"], dT_K=mine["T_TDC_K"] - r["T_TDC_K"],
                       dp_rel=mine["p_TDC_bar"] / r["p_TDC_bar"] - 1))
    checks["C1_tdc_vs_J2"] = dict(n=len(c1), max_dT_K=max(abs(c["dT_K"]) for c in c1),
                                  max_dp_rel=max(abs(c["dp_rel"]) for c in c1),
                                  passed=all(abs(c["dT_K"]) <= 0.1 and abs(c["dp_rel"]) <= 1e-3 for c in c1))
    dt = json.loads((ROOT / "results/08_water_chem_dualT/dual_temp.json").read_text())["rows"]
    c2 = []
    for r in dt["tad"]:
        if r["variant"] == "real" and r["T_ad_K"]:
            m = pick(rows["tad"], "T_ad_K", fuel=r["fuel"], w=r["w"], T_u_K=r["T_K"], variant="real")
            c2.append(rel(m, r["T_ad_K"]))
    for r in dt["ign"]:
        if r["variant"] == "real" and r["tau_s"]:
            m = pick(rows["ign"], "tau_s", fuel=r["fuel"], w=r["w"], T_u_K=REGIMES_J2[r["regime"]], CR=r["CR"], variant="real")
            c2.append(rel(m, r["tau_s"]))
    checks["C2_vs_dual_temp_json"] = dict(n=len(c2), max_rel=max(abs(x) for x in c2 if x is not None),
                                          n_missing=sum(x is None for x in c2),
                                          passed=all(x is not None and abs(x) <= 1e-6 for x in c2))
    c3 = []
    for fuel in FUELS:
        def sl(kind, v):
            return pick(rows[kind], "S_L_m_s", fuel=fuel, w=0.3, T_u_K=360.0, variant=v)
        base_c, tight_c = rel(sl("flame", "real"), sl("flame", "fh2o_b")), rel(sl("flame_tight", "real"), sl("flame_tight", "fh2o_b"))
        c3.append(dict(fuel=fuel, chem_default=base_c, chem_tight=tight_c,
                       S_L_real_default=sl("flame", "real"), S_L_real_tight=sl("flame_tight", "real"),
                       grid_default=pick(rows["flame"], "grid_points", fuel=fuel, w=0.3, T_u_K=360.0, variant="real"),
                       grid_tight=pick(rows["flame_tight"], "grid_points", fuel=fuel, w=0.3, T_u_K=360.0, variant="real")))
    checks["C3_SL_grid_sign"] = dict(rows=c3, passed=all(
        c["chem_default"] is not None and c["chem_tight"] is not None and (c["chem_default"] > 0) == (c["chem_tight"] > 0)
        and abs(c["chem_default"] - c["chem_tight"]) < 0.01 for c in c3))
    return eff, side, checks


REGIMES_J2 = {"normal": 360.0, "hot": 400.0}


def main(workers=2):
    from multiprocessing import get_context
    t0 = time.time()
    tdc, tasks = build()
    with get_context("spawn").Pool(workers) as pool:
        res = pool.map(_task, tasks, chunksize=1)
    rows = {"tad": [], "flame": [], "ign": [], "flame_tight": []}
    for k, r in res:
        rows[k].append(r)
    eff, side, checks = analyse(tdc, rows)
    out = dict(date=DATE, track="A (water-majority w=0.6; w=0 and 0.3 references)",
               status=dict(executed=True, verified="no (single engine; C1-C3 are code/grid self-consistency only)",
                           validated="no (no published alcohol-water flame/ignition data at these states; see /opt/knowledge WE-11)"),
               regimes=REGIMES, citations=CITATIONS, mechanism="mechanisms/sandiego.yaml (+ FH2O-a/b built by build_mechanisms)",
               phi=1.0, p_flame_Pa=101325.0, p_IVC_Pa=P_IVC, CR=CRS, tau_max_s=TAU_MAX,
               effects=eff, hot_vs_normal=side, checks=checks, tdc_states=tdc, rows=rows,
               runtime_s=time.time() - t0, workers=workers)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "regimes.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps(dict(checks={k: v["passed"] for k, v in checks.items()}, runtime_s=out["runtime_s"]), indent=1))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
