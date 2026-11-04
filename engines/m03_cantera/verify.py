"""Verification of M03-CRN on its own (ACCEPTANCE.md V-A..V-C). Writes results/engines/m03_cantera/verification.json."""
import json
import math
import sys
import time
import warnings
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engines.m03_cantera import engine as E, points as P  # noqa: E402

OUT = ROOT / "results" / "engines" / "m03_cantera"
QTY = ["efficiency", "IMEP_Pa", "p_max_Pa", "T_max_K", "wall_heat_J", "T_EVO_K"]
RTOLS = [1e-6, 1e-7, 1e-8, 1e-9]


def _run(args):
    key, regime, kw = args
    d = P.load_rows()
    c = P.case_from_row(d["rows"][f"{regime}|{key}"], regime, **kw)
    c.label = f"{regime}|{key}"
    t = time.time()
    r = E.run_case(c)
    r["runtime_s"] = time.time() - t
    return r


def gci(f1, f2, f3, r=10.0, Fs=1.25):
    """f1 finest. Returns (p, GCI_fine relative) or (None, None) if not monotone."""
    e21, e32 = f2 - f1, f3 - f2
    if e21 == 0.0:
        return math.inf, 0.0
    if e32 == 0.0 or e32 / e21 <= 0.0:
        return None, None
    p = math.log(abs(e32 / e21)) / math.log(r)
    if p <= 0:
        return p, None
    return p, Fs * abs(e21 / f1) / (r ** p - 1.0)


def main(workers=6):
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    out = {}
    # V-A ideal Otto
    otto = [E.ideal_otto(cr, d) for cr in (16, 24) for d in (1.0, 0.5)]
    va = all(abs(o["error"]) <= 1e-3 for o in otto)
    shrink = all(abs(otto[2 * i + 1]["error"]) < abs(otto[2 * i]["error"]) for i in range(2))
    out["V-A_ideal_otto"] = dict(cases=otto, pass_=va and shrink, criterion="|err|<=1e-3 and error shrinks 1.0->0.5 CAD")
    d = P.load_rows()
    design_keys = sorted({(k.split(":")[0], v) for k, v in d["designs"].items()})
    tasks = []
    for regime, key in design_keys:
        for ht in ("hohenberg", "woschni"):
            for rt in RTOLS:
                tasks.append((key, regime, dict(heat_transfer=ht, rtol=rt, atol=rt * 1e-8)))
            tasks.append((key, regime, dict(heat_transfer=ht, rtol=1e-9, atol=1e-17, tau_evap_deg=0.025)))
            tasks.append((key, regime, dict(heat_transfer=ht, rtol=1e-9, atol=1e-17, sample_deg=0.025)))
    with Pool(workers) as pool:
        res = pool.map(_run, tasks)
    conv, tau, samp, closures = [], [], [], []
    i = 0
    for regime, key in design_keys:
        for ht in ("hohenberg", "woschni"):
            seq = res[i:i + 4]; rt_tau = res[i + 4]; rt_s = res[i + 5]; i += 6
            row = dict(point=f"{regime}|{key}", heat_transfer=ht)
            for q in QTY:
                f = [s[q] for s in seq]  # rtol 1e-6 .. 1e-9
                p, g = gci(f[3], f[2], f[1])
                row[q] = dict(values=f, rel_change_8_9=abs(f[3] / f[2] - 1.0), p=p, GCI_fine=g)
            conv.append(row)
            tau.append(dict(point=f"{regime}|{key}", heat_transfer=ht,
                            d_eta=rt_tau["efficiency"] - seq[3]["efficiency"]))
            samp.append(dict(point=f"{regime}|{key}", heat_transfer=ht,
                             d_pmax_rel=rt_s["p_max_Pa"] / seq[3]["p_max_Pa"] - 1.0,
                             d_Tmax=rt_s["T_max_K"] - seq[3]["T_max_K"]))
            closures += [abs(s["energy_closure"]) for s in seq[2:] + [rt_tau, rt_s]]
            closures_w = [abs(s["wiebe_integral_error"]) for s in seq[2:]]
    vb_fail = []
    for row in conv:
        for q in QTY:
            c = row[q]
            if c["rel_change_8_9"] > 1e-5:
                vb_fail.append(f"{row['point']} {row['heat_transfer']} {q} rel change {c['rel_change_8_9']:.2e}")
            if c["GCI_fine"] is not None and c["GCI_fine"] > 1e-4:
                vb_fail.append(f"{row['point']} {row['heat_transfer']} {q} GCI {c['GCI_fine']:.2e}")
    tau_fail = [t for t in tau if abs(t["d_eta"]) > 1e-4]
    out["V-B_convergence"] = dict(rows=conv, tau_halved=tau, sample_halved=samp, failures=vb_fail + [str(t) for t in tau_fail],
                                  no_gci_defined=[f"{r['point']} {r['heat_transfer']} {q}" for r in conv for q in QTY if r[q]["GCI_fine"] is None],
                                  pass_=not vb_fail and not tau_fail,
                                  criterion="rel change 1e-8->1e-9 <= 1e-5; GCI_fine <= 1e-4 where defined (monotone triple); tau halved |d eta| <= 1e-4")
    out["V-C_closure"] = dict(max_energy_closure=max(closures), pass_=max(closures) <= 1e-5,
                              criterion="|closure|/Q_fuel <= 1e-5 at rtol <= 1e-8")
    out["V-D_ic_engine"] = dict(status="not applicable", reason=(
        "Cantera's ic_engine.py is a compression-ignition engine with gaseous fuel injection near TDC, finite-rate "
        "chemistry and open valves; it has no Wiebe release, no water and no SI flame, so its efficiency cannot benchmark "
        "this closed SI cycle. Only its pattern (moving ct.Wall with piston velocity, reservoir environment) is reused."))
    out["overall_pass"] = bool(out["V-A_ideal_otto"]["pass_"] and out["V-B_convergence"]["pass_"] and out["V-C_closure"]["pass_"])
    out["cantera_version"] = E.ct.__version__
    out["runtime_s"] = time.time() - t0
    (OUT / "verification.json").write_text(json.dumps(out, indent=1, default=float))
    print(json.dumps({k: (v.get("pass_") if isinstance(v, dict) else v) for k, v in out.items()}, indent=1, default=str))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
