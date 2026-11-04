"""Module 08 water chemical effect, normal vs hot regime (box-queue 20261024-1230 J2, module 08 part).

Runs Module 08's own functions (this commit includes the a6da0e8 stoichiometry fix and the f55d15d
Q_dry/Q_wet bookkeeping fix) at the two regimes used by J2 (xcheck/chem 95d537e):
  normal T_u = 360 K, hot T_u = 400 K; p = 1 atm for S_L and T_ad; phi = 1; w = 0, 0.3, 0.6;
  tau_ig at J2's TDC-equivalent states (frozen isentropic compression from T_u, 1 bar, CR 16 and 24;
  copied to results/08_water_chem_dualT/j2_tdc_states_sandiego.json).
Variants: real H2O, FH2O-a (inert, H2O third-body efficiencies), FH2O-b (inert, unit efficiencies).

Consistency check stated before the run: Module 08 'real' T_ad and tau_ig must reproduce J2's San Diego values
(same mechanism, same states) within 0.1 % (T_ad) and 2 % (tau_ig: Module 08 horizon 0.5 s vs J2 50 ms, same
max dT/dt definition). This is a code-consistency check, not an independent second engine.
Status: EXECUTED only (single engine).
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
OUT = ROOT / "results" / "08_water_chem_dualT"
REGIMES = {"normal": 360.0, "hot": 400.0}
FUELS = ("CH3OH", "C2H5OH")
W = (0.0, 0.3, 0.6)
VARIANTS = m08.MECHANISM_VARIANTS


def _task(t):
    kind, args = t
    if kind == "tad":
        return kind, m08.adiabatic_temperature(*args)
    if kind == "flame":
        return kind, m08.flame_speed(*args)
    return kind, m08.ignition_delay(*args)


def main(workers=2):
    from multiprocessing import get_context
    t0 = time.time()
    tdc = json.loads((OUT / "j2_tdc_states_sandiego.json").read_text())["rows"]
    tasks = []
    for fuel in FUELS:
        for w in W:
            for v in VARIANTS:
                for reg, Tu in REGIMES.items():
                    tasks.append(("tad", (fuel, v, 1.0, w, Tu, 101325.0)))
                    tasks.append(("flame", (fuel, v, 1.0, w, Tu, 101325.0)))
                for r in tdc:
                    if r["fuel"] == fuel and abs(r["w"] - w) < 1e-9:
                        tasks.append(("ign", (fuel, v, 1.0, w, r["T_TDC_K"], r["p_TDC_bar"] * 1e5, 0.5)))
    with get_context("spawn").Pool(workers) as pool:
        res = pool.map(_task, tasks, chunksize=1)
    rows = {"tad": [], "flame": [], "ign": []}
    for k, r in res:
        rows[k].append(r)
    # attach regime / CR labels
    def reg_of(T):
        return next(k for k, v in REGIMES.items() if abs(v - T) < 1e-9)
    for r in rows["tad"] + rows["flame"]:
        r["regime"] = reg_of(r["T_K"])
    for r in rows["ign"]:
        m = next(x for x in tdc if x["fuel"] == r["fuel"] and abs(x["w"] - r["w"]) < 1e-9 and abs(x["T_TDC_K"] - r["T_K"]) < 1e-9)
        r["regime"], r["CR"], r["j2_tau_s"] = m["regime"], m["CR"], m["tau_ig_s"]
    eff = []
    for fuel in FUELS:
        for w in W:
            for reg, Tu in REGIMES.items():
                e = dict(fuel=fuel, w=w, regime=reg, T_u_K=Tu)
                f = {r["variant"]: r["S_L_m_s"] for r in rows["flame"] if r["fuel"] == fuel and r["w"] == w and r["regime"] == reg}
                if all(f.get(v) for v in VARIANTS):
                    e.update(S_L_real=f["real"], S_L_chem_effect=(f["real"] - f["fh2o_b"]) / f["fh2o_b"],
                             S_L_third_body=(f["fh2o_a"] - f["fh2o_b"]) / f["fh2o_b"],
                             S_L_direct=(f["real"] - f["fh2o_a"]) / f["fh2o_a"])
                for cr in (16.0, 24.0):
                    g = {r["variant"]: r["tau_s"] for r in rows["ign"] if r["fuel"] == fuel and r["w"] == w and r["regime"] == reg and r["CR"] == cr}
                    if all(g.get(v) for v in VARIANTS):
                        e[f"tau_CR{cr:g}_real"] = g["real"]
                        e[f"tau_CR{cr:g}_chem_effect"] = (g["real"] - g["fh2o_b"]) / g["fh2o_b"]
                        e[f"tau_CR{cr:g}_third_body"] = (g["fh2o_a"] - g["fh2o_b"]) / g["fh2o_b"]
                        e[f"tau_CR{cr:g}_direct"] = (g["real"] - g["fh2o_a"]) / g["fh2o_a"]
                eff.append(e)
    j2 = {(r["fuel"], r["w"], r["regime"]): r for r in tdc if r["CR"] == 16.0}
    cons = []
    for r in rows["tad"]:
        if r["variant"] == "real" and r["T_ad_K"]:
            ref = j2[(r["fuel"], r["w"], r["regime"])]["T_ad_1atm_K"]
            cons.append(dict(q="T_ad", fuel=r["fuel"], w=r["w"], regime=r["regime"], m08=r["T_ad_K"], j2=ref, rel=r["T_ad_K"] / ref - 1, ok=abs(r["T_ad_K"] / ref - 1) <= 1e-3))
    for r in rows["ign"]:
        if r["variant"] == "real" and r["tau_s"] and r["j2_tau_s"]:
            cons.append(dict(q="tau", fuel=r["fuel"], w=r["w"], regime=r["regime"], CR=r["CR"], m08=r["tau_s"], j2=r["j2_tau_s"], rel=r["tau_s"] / r["j2_tau_s"] - 1, ok=abs(r["tau_s"] / r["j2_tau_s"] - 1) <= 0.02))
    out = dict(status="EXECUTED (single engine)", regimes=REGIMES, chemical_effect=eff, consistency_vs_J2=cons,
               consistency_pass=all(c["ok"] for c in cons), rows=rows, runtime_s=time.time() - t0)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "dual_temp.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps(dict(consistency_pass=out["consistency_pass"], n=len(cons), runtime_s=out["runtime_s"]), indent=1))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
