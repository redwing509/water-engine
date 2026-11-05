"""Module 09 at the Module 03 design points (relay job water-engine-20261023-103500).

For CH3OH and C2H5OH at Module 03's best_dry, best_overall and water_majority
points and all 7 atomisers, runs the Module 09 chain
  atomiser -> runner -> bend (Pui) -> induction -> IVC -> compression -> spark
with the Module 03 inputs (CR, w, T_intake, rpm, trapped air / alcohol / water
masses) and, during compression, Module 03's own pre-spark cylinder pressure
p(theta) imposed in the "pt" mode of model.Spray (regenerated here with
sims/03_engine_cycle integrate_cycle(keep_trace=True); the design-point
efficiency and peak pressure are reproduced and checked).

Spark timing = CA50 - (0-50 % burn angle). Module 03 does not report a 0-50 %
angle, so the Module 03 Wiebe function (a = 5, m = 2) is used: the 0 % point of
the Wiebe with Module 03's 10-90 % duration, theta_spark = CA50 - dtheta z(0.5),
dtheta = burn_10_90 / (z(0.9) - z(0.1)), z(x) = (-ln(1-x)/a)^(1/(m+1)).

Two variants per case:
  nominal     : the Module 09 model as derived (transfer multiplier k = 1). It
                is NOT tuned to CFD; its bias vs the OpenFOAM phase-A cases
                (A1 evaporated 1.5-2.5x CFD, A2 +1 to +12 pp) is a known limitation.
  cfd_matched : a labelled SENSITIVITY BOUND, not a validated model. One
                droplet-gas transfer multiplier per CFD condition (applied to both
                mass and heat transfer, i.e. a Sh/Nu multiplier), least-squares
                fitted to the A1-BLEND (1 bar, 360 K) and A2-BLEND (20 bar, 700 K)
                evaporated-% histories. k_A1 is used in runner and induction; during
                compression k is interpolated in ln p between the two chamber
                pressures and held constant outside them. The same k is used for
                ethanol (no ethanol CFD exists; flagged).

Status labels: all outputs are EXECUTED model runs; tests VERIFY numerics;
nothing is experimentally VALIDATED.
"""

from dataclasses import replace
import argparse
import csv
import importlib
import json
import math
import os
from pathlib import Path
import time
from concurrent.futures import ProcessPoolExecutor

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar

from . import atomisers as A
from . import model as M
from . import properties as P
from . import run as R

ROOT = Path(__file__).resolve().parents[2]
FUELS = ("CH3OH", "C2H5OH")
POINTS = ("best_dry", "best_overall", "water_majority")
VARIANTS = ("nominal", "cfd_matched")
FIT_CASES = ("A1-BLEND", "A2-BLEND")
OUT_SUB = "design_points"


def m03():
    return importlib.import_module("sims.03_engine_cycle.run")


# ---------------------------------------------------------------- spark timing
def wiebe_z(x, a=5.0, m=2.0):
    return (-math.log1p(-x) / a) ** (1.0 / (m + 1.0))


def spark_angle_deg(ca50_deg, burn_10_90_deg, a=5.0, m=2.0):
    """(theta_spark [deg aTDC], Wiebe total duration dtheta, 0-50 % burn angle)."""
    dth = burn_10_90_deg / (wiebe_z(0.9, a, m) - wiebe_z(0.1, a, m))
    b050 = dth * wiebe_z(0.5, a, m)
    return ca50_deg - b050, dth, b050


# ---------------------------------------------------------------- Module 03 p(theta)
def design_inputs(dp_path):
    dp = json.loads(Path(dp_path).read_text())
    out = {}
    for f in FUELS:
        for pt in POINTS:
            r = dp["per_fuel"][f][pt]
            out[(f, pt)] = dict(fuel=f, point=pt, key=r["key"], CR=float(r["CR"]), w=float(r["w"]),
                                T_intake_K=float(r["T_intake_K"]), rpm=float(r["rpm"]),
                                ca50_deg=float(r["ca50_used_deg"]), burn_10_90_deg=float(r["burn_10_90_deg"]),
                                m_air_kg=float(r["air_mass_kg"]), m_alcohol_kg=float(r["fuel_mass_kg"]),
                                m_water_kg=float(r["water_mass_kg"]), m_residual_kg=float(r["residual_mass_kg"]),
                                eta_m03=float(r["gross_indicated_efficiency"]), p_peak_m03=float(r["peak_pressure_Pa"]),
                                T_IVC_m03=float(r["T_IVC_K"]))
    return out, dp


def m03_trace(inp):
    """Regenerate the Module 03 cycle at a design point; returns the pre-spark trace."""
    mod = m03()
    par = mod.DEFAULTS
    assert abs(par.wiebe_a - 5.0) < 1e-12 and abs(par.wiebe_m - 2.0) < 1e-12
    th_s, dth, b050 = spark_angle_deg(inp["ca50_deg"], inp["burn_10_90_deg"], par.wiebe_a, par.wiebe_m)
    ch = mod.Charge(inp["fuel"], inp["CR"], inp["w"], inp["T_intake_K"])
    res = mod.integrate_cycle(ch, math.radians(inp["ca50_deg"]), math.radians(inp["burn_10_90_deg"]),
                              None, keep_trace=True, track_no=False)
    tr = res["_trace"]
    th = np.asarray(tr["theta_deg"], float)
    keep = th <= th_s + 2.0
    check = dict(eta_regen=float(res["gross_indicated_efficiency"]), eta_design=inp["eta_m03"],
                 p_peak_regen=float(res["peak_pressure_Pa"]), p_peak_design=inp["p_peak_m03"])
    check["reproduced"] = bool(abs(check["eta_regen"] - check["eta_design"]) < 1e-6
                               and abs(check["p_peak_regen"] / check["p_peak_design"] - 1) < 1e-6)
    xb = np.asarray(tr["xb"], float)[keep]
    return dict(theta_deg=th[keep], p_Pa=np.asarray(tr["p_Pa"], float)[keep],
                T_K=np.asarray(tr["T_K"], float)[keep], V_m3=np.asarray(tr["V_m3"], float)[keep],
                water_evaporated=np.asarray(tr["evaporated"], float)[keep], xb_max_pre_spark=float(xb[th[keep] <= th_s].max()),
                theta_spark_deg=th_s, wiebe_dtheta_deg=dth, burn_0_50_deg=b050, check=check,
                geometry=dict(bore_m=par.bore_m, stroke_m=par.stroke_m, rod_m=par.rod_m, rpm=par.rpm,
                              ivc_deg=math.degrees(par.ivc_rad)))


# ---------------------------------------------------------------- cfd_matched fit
def fit_rate_scale(cfd, case, step_s=1e-4):
    meta = cfd[case]["meta"]; smd = cfd[case]["summary"]["SMD_eoi_um"] * 1e-6
    t_cfd, e_cfd = cfd[case]["t"], cfd[case]["evap"]
    t_end = float(t_cfd[-1])
    grid = np.arange(step_s, t_end + 1e-12, step_s)
    ecfd = np.interp(grid, t_cfd, e_cfd)
    evals = []

    def rms(lnk):
        sn = R.chamber_run(meta, smd, t_end, "wilson", rate_scale=math.exp(lnk))
        tb = np.array([x["t_s"] for x in sn]); eb = np.array([100 * x["evaporated_frac"] for x in sn])
        e09 = np.interp(grid, tb, eb)
        v = float(np.sqrt(np.mean((e09 - ecfd)**2)))
        evals.append((math.exp(lnk), v, float(e09[-1])))
        return v

    r0 = rms(0.0)
    opt = minimize_scalar(rms, bounds=(math.log(0.05), math.log(2.0)), method="bounded", options=dict(xatol=2e-3))
    k = math.exp(opt.x)
    best = min(evals, key=lambda e: abs(e[0] - k))
    return dict(case=case, k=k, rms_pp_fitted=float(opt.fun), rms_pp_nominal=r0, p_Pa=meta["p"], T_K=meta["T"],
                cfd_end_pct=float(ecfd[-1]), m09_end_pct_fitted=best[2], t_end_ms=t_end * 1e3,
                n_evals=len(evals), SMD_matched_um=smd * 1e6, objective="RMS of evaporated % on a 0.1 ms grid")


class KofP:
    """Transfer multiplier vs pressure: ln-p interpolation between two fits, clamped."""

    def __init__(self, p1, k1, p2, k2):
        self.p1, self.k1, self.p2, self.k2 = p1, k1, p2, k2

    def __call__(self, p):
        s = (math.log(max(p, 1.0)) - math.log(self.p1)) / (math.log(self.p2) - math.log(self.p1))
        s = min(max(s, 0.0), 1.0)
        return self.k1 + s * (self.k2 - self.k1)


# ---------------------------------------------------------------- one case
def run_design_case(task):
    start = time.perf_counter()
    inp, atom, variant, trace, kfit = task["inp"], task["atomiser"], task["variant"], task["trace"], task["kfit"]
    fuel = inp["fuel"]
    tab = P.tables(fuel)
    par = replace(R.DEF, CR=inp["CR"], rpm=inp["rpm"], spark_CAD_bTDC=-trace["theta_spark_deg"])
    T_pl, U, L = inp["T_intake_K"], R.REFERENCE["U_runner_m_s"], R.REFERENCE["L_runner_m"]
    m_air, m_f, m_w = inp["m_air_kg"], inp["m_alcohol_kg"], inp["m_water_kg"]
    m_l = m_f + m_w
    Y_m = m_f / m_l
    smd0, u0, note = R.atomiser_smd(atom, inp["w"], T_pl, U, par, fuel=fuel, masses=(m_air, m_f, m_w))
    d, frac = A.rosin_rammler_classes(smd0, par.rr_q, par.rr_classes)
    kfun = None
    k_low = 1.0
    if variant == "cfd_matched":
        kfun = KofP(kfit["A1"]["p_Pa"], kfit["A1"]["k"], kfit["A2"]["p_Pa"], kfit["A2"]["k"])
        k_low = kfun(par.p_plenum_Pa)
    sp = M.Spray(m_air=m_air, T_gas=T_pl, p=par.p_plenum_Pa, m_ref=m_l, activity=par.activity,
                 fuel=fuel, rate_scale=k_low)
    rho0 = sp.liquid_density(np.full(d.size, par.T_liquid_K), np.full(d.size, Y_m))
    sp.add_classes(d, m_l * frac / (rho0 * math.pi * d**3 / 6.0), Y_m, par.T_liquid_K, u0)
    closure, allsn = [], []
    H0 = sp.enthalpy()
    snaps = sp.run(L / U, mode="p", u_g=U, n_out=10); allsn += snaps
    closure.append(sp.enthalpy() - H0)
    evap_runner = snaps[-1]["evaporated_frac"]
    mw, mm, Td, ud, Tg, mv = sp.split()
    mu_g = float(np.interp(Tg, tab.TG, tab.mu_g[0]))
    dd = sp.droplet_diameters()
    rho_now = sp.liquid_density(Td, np.where(mw + mm > 0, mm / np.maximum(mw + mm, 1e-300), 0))
    eta, St = R.pui_bend_efficiency(dd, rho_now, U, mu_g, par.runner_diameter_m)
    sp.impinge(eta)
    t_deg = 1.0 / (6.0 * par.rpm)
    H0 = sp.enthalpy()
    snaps = sp.run(par.induction_fraction * 180.0 * t_deg, mode="p", u_g=0.0, n_out=10); allsn += snaps
    closure.append(sp.enthalpy() - H0)
    ivc = snaps[-1]
    # compression with the imposed Module 03 p(theta), IVC (-180) -> spark
    th, pp = trace["theta_deg"], trace["p_Pa"]
    spl = CubicSpline(th, pp); dspl = spl.derivative()
    t_ivc = sp.t
    th_ivc = float(th[0])
    p_ivc_m03 = float(spl(th_ivc))

    def pfun(tt):
        a = th_ivc + (tt - t_ivc) / t_deg
        return float(spl(a)), float(dspl(a)) / t_deg

    if kfun is not None:
        sp.rate_scale_fun = kfun
    H0 = sp.enthalpy(); vdp0 = sp.vdp
    snaps = sp.run((trace["theta_spark_deg"] - th_ivc) * t_deg, mode="pt", Vfun=pfun, n_out=240); allsn += snaps
    closure.append((sp.enthalpy() - H0) - (sp.vdp - vdp0))
    spk = snaps[-1]
    # evaporated fraction vs crank angle, IVC -> spark (evap_profiles.json, Module 03 --evap-profile input)
    profile = dict(theta_deg=[th_ivc + (s["t_s"] - t_ivc) / t_deg for s in snaps],
                   f_evap=[s["evaporated_frac"] for s in snaps],
                   f_evap_water=[s["vapour_water_kg"] / m_w if m_w > 0 else 0.0 for s in snaps],
                   f_evap_alcohol=[s["vapour_methanol_kg"] / m_f if m_f > 0 else 0.0 for s in snaps],
                   f_liquid=[s["liquid_kg"] / m_l for s in snaps], f_wall=[s["wall_kg"] / m_l for s in snaps],
                   T_gas_K=[s["T_gas_K"] for s in snaps])
    mw, mm, Td, ud, Tg, mv = sp.split()
    liq_w = float(np.sum(sp.N * np.maximum(mw, 0) * sp.m0)); liq_m = float(np.sum(sp.N * np.maximum(mm, 0) * sp.m0))
    V_geom = R.cyl_volume(trace["theta_spark_deg"], par)
    T_m03_spark = float(np.interp(trace["theta_spark_deg"], th, trace["T_K"]))
    latent = m_w * 2.4e6 + m_f * 1.0e6
    return dict(fuel=fuel, point=inp["point"], key=inp["key"], atomiser=atom, variant=variant,
                CR=inp["CR"], w=inp["w"], T_intake_K=T_pl, rpm=inp["rpm"],
                spark_deg_aTDC=trace["theta_spark_deg"], spark_CAD_bTDC=-trace["theta_spark_deg"],
                SMD_initial_um=smd0 * 1e6, atomiser_note=note,
                m_air_kg=m_air, m_alcohol_kg=m_f, m_water_kg=m_w,
                k_runner_induction=k_low,
                k_spark=(kfun(spk["p_Pa"]) if kfun is not None else 1.0),
                evaporated_runner_pct=100 * evap_runner,
                wall_impinged_pct=100 * spk["wall_kg"] / m_l,
                evaporated_IVC_pct=100 * ivc["evaporated_frac"],
                evaporated_spark_pct=100 * spk["evaporated_frac"],
                liquid_spark_pct=100 * spk["liquid_kg"] / m_l,
                SMD_spark_um=spk["SMD_m"] * 1e6,
                liquid_water_spark_kg=liq_w, liquid_alcohol_spark_kg=liq_m,
                T_IVC_m09_K=ivc["T_gas_K"], T_IVC_m03_K=inp["T_IVC_m03"],
                p_spark_Pa=spk["p_Pa"], T_spark_m09_K=spk["T_gas_K"], T_spark_m03_K=T_m03_spark,
                V_implied_over_geometric_spark=spk["V_m3"] / V_geom,
                p_ivc_m03_Pa=p_ivc_m03,
                S_water_spark=spk["S_water"], S_alcohol_spark=spk["S_methanol"],
                max_mass_error_rel=max(s["mass_error_rel"] for s in allsn),
                max_energy_closure_rel=max(abs(c) for c in closure) / latent,
                boiling_cap_hits=sp.cap_hits, runtime_s=time.perf_counter() - start, profile=profile)


def _task(task):
    try:
        return run_design_case(task)
    except Exception as exc:  # recorded, never hidden
        return dict(fuel=task["inp"]["fuel"], point=task["inp"]["point"], atomiser=task["atomiser"],
                    variant=task["variant"], status="failed", reason=repr(exc))


# ---------------------------------------------------------------- outputs
SPARK_FIELDS = ("evaporated_IVC_pct", "evaporated_spark_pct", "liquid_spark_pct", "wall_impinged_pct", "SMD_spark_um",
                "liquid_water_spark_kg", "liquid_alcohol_spark_kg", "T_spark_m09_K", "p_spark_Pa")


def plot(rows, path):
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharey=True)
    atoms = list(R.ATOMISERS)
    x = np.arange(len(atoms))
    for i, f in enumerate(FUELS):
        for j, pt in enumerate(POINTS):
            ax = axes[i, j]
            for o, (v, c) in enumerate((("nominal", "C0"), ("cfd_matched", "C3"))):
                sel = {r["atomiser"]: r for r in rows if r["fuel"] == f and r["point"] == pt and r["variant"] == v and "status" not in r}
                liq = [sel[a]["liquid_spark_pct"] if a in sel else np.nan for a in atoms]
                wall = [sel[a]["wall_impinged_pct"] if a in sel else np.nan for a in atoms]
                ax.bar(x + (o - 0.5) * 0.38, liq, 0.38, color=c, label=f"liquid at spark ({v})")
                ax.bar(x + (o - 0.5) * 0.38, wall, 0.38, bottom=liq, color=c, alpha=0.35, hatch="//", label=f"wall ({v})")
            ax.set_title(f"{f} {pt}")
            ax.set_xticks(x, [a.replace("_", "\n") for a in atoms], fontsize=7)
            if j == 0:
                ax.set_ylabel("% of injected liquid")
    axes[0, 0].legend(fontsize=7)
    fig.suptitle("Module 09 at Module 03 design points: liquid at spark + wall-impinged (EXECUTED; cfd_matched = sensitivity bound)")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def _sig(x, n=6):
    return float(f"{x:.{n}g}")


def write_evap_profiles(path, good, profiles):
    """evap_profiles.json, schema {case: {fuel, point, atomiser, variant, theta_deg[], f_evap[]}} (Claude's reply to the
    103500 follow-ups). f_evap = evaporated (vapour) mass / injected liquid mass (alcohol + water), from the start of
    compression (Module 03 IVC, -180 deg aTDC) to spark; 241 points. Extra per-case keys are informational:
    f_evap_water / f_evap_alcohol (vapour / injected mass of that species), f_liquid (airborne liquid), f_wall
    (bend-deposited, constant after the bend), T_gas_K (Module 09 parcel), spark_deg_aTDC, f_evap_runner_end."""
    out = {}
    for r in good:
        key = f"{r['fuel']}/{r['point']}/{r['atomiser']}/{r['variant']}"
        pr = profiles[key]
        c = dict(fuel=r["fuel"], point=r["point"], atomiser=r["atomiser"], variant=r["variant"],
                 theta_deg=[round(t, 4) for t in pr["theta_deg"]], f_evap=[_sig(v) for v in pr["f_evap"]])
        c.update({k: [_sig(v) for v in pr[k]] for k in ("f_evap_water", "f_evap_alcohol", "f_liquid", "f_wall", "T_gas_K")})
        c.update(spark_deg_aTDC=r["spark_deg_aTDC"], f_evap_runner_end=r["evaporated_runner_pct"] / 100.0)
        out[key] = c
    Path(path).write_text(json.dumps(out, indent=1))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--design-point", default=str(ROOT / "results" / "03_engine_cycle" / "design_point.json"))
    ap.add_argument("--cfd-dir", default=str(ROOT / "cfd" / "results"))
    ap.add_argument("--cfd-ref", default="", help="git ref/sha of the CFD results (recorded only)")
    ap.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    ap.add_argument("--out", default=str(ROOT / "results" / R.MODULE))
    args = ap.parse_args(argv)
    t0 = time.perf_counter()
    out = Path(args.out); sub = out / OUT_SUB
    sub.mkdir(parents=True, exist_ok=True)
    inputs, dp = design_inputs(args.design_point)
    # 1) Module 03 traces
    traces = {kk: m03_trace(v) for kk, v in inputs.items()}
    with open(sub / "m03_pre_spark_p_theta.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["fuel", "point", "theta_deg_aTDC", "p_Pa", "T_m03_K", "V_m3", "m03_water_evaporated_frac"])
        for (f, pt), tr in traces.items():
            for i in range(tr["theta_deg"].size):
                wr.writerow([f, pt, f"{tr['theta_deg'][i]:.3f}", f"{tr['p_Pa'][i]:.2f}", f"{tr['T_K'][i]:.3f}",
                             f"{tr['V_m3'][i]:.6e}", f"{tr['water_evaporated'][i]:.6f}"])
    # 2) cfd_matched fit
    cfd = R.read_cfd(args.cfd_dir)
    missing = [c for c in FIT_CASES if c not in cfd]
    if missing:
        raise SystemExit(f"CFD cases missing for the cfd_matched fit: {missing}")
    fits = {c: fit_rate_scale(cfd, c) for c in FIT_CASES}
    kfit = {"A1": fits["A1-BLEND"], "A2": fits["A2-BLEND"]}
    # 3) cases
    tasks = []
    for kk, inp in inputs.items():
        tr = {k: v for k, v in traces[kk].items() if k in ("theta_deg", "p_Pa", "T_K", "theta_spark_deg")}
        for a in R.ATOMISERS:
            for v in VARIANTS:
                tasks.append(dict(inp=inp, atomiser=a, variant=v, trace=tr, kfit=kfit))
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        rows = list(ex.map(_task, tasks))
    profiles = {f"{r['fuel']}/{r['point']}/{r['atomiser']}/{r['variant']}": r.pop("profile") for r in rows if "profile" in r}
    failed = [r for r in rows if r.get("status") == "failed"]
    good = [r for r in rows if "status" not in r]
    fields = list(good[0].keys()) if good else ["fuel"]
    with open(sub / "design_point_sweep.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=fields + ["status", "reason"], extrasaction="ignore")
        wr.writeheader()
        for r in rows:
            wr.writerow(r)
    plot(rows, sub / "design_point_liquid_wall.png")
    # spray_at_spark.json (Module 11 input)
    cases = {}
    for r in good:
        c = cases.setdefault(f"{r['fuel']}/{r['point']}", dict(
            fuel=r["fuel"], point=r["point"], module03_key=r["key"], CR=r["CR"], w=r["w"], T_intake_K=r["T_intake_K"],
            rpm=r["rpm"], spark_deg_aTDC=r["spark_deg_aTDC"], atomisers={}))
        c["atomisers"].setdefault(r["atomiser"], {})[r["variant"]] = {k: r[k] for k in SPARK_FIELDS}
    spark_info = {f"{f}/{pt}": dict(theta_spark_deg_aTDC=traces[(f, pt)]["theta_spark_deg"],
                                    wiebe_total_duration_deg=traces[(f, pt)]["wiebe_dtheta_deg"],
                                    burn_0_50_deg=traces[(f, pt)]["burn_0_50_deg"],
                                    m03_xb_max_before_spark=traces[(f, pt)]["xb_max_pre_spark"],
                                    m03_reproduction=traces[(f, pt)]["check"]) for (f, pt) in inputs}
    labels = {
        "status": "EXECUTED (model runs). Numerics VERIFIED by tests/test_spray_evaporation.py. NOT experimentally VALIDATED.",
        "nominal": "Module 09 model as derived, k = 1, NOT tuned to CFD. Known limitation: vs OpenFOAM phase A it evaporates "
                   "1.5-2.5x the CFD value at A1 (1 bar, 360 K) and +1 to +12 pp at A2 (20 bar, 700 K).",
        "cfd_matched": "SENSITIVITY BOUND, not a validated model: one droplet-gas transfer multiplier per CFD condition fitted "
                       "to A1-BLEND / A2-BLEND (model-vs-model; the CFD itself is unvalidated and has wall-bounce, no film). "
                       "Same multiplier applied to ethanol without ethanol CFD.",
    }
    assumptions = {
        "inputs": "Module 03 design_point.json (CR, w, T_intake, rpm, trapped air/alcohol/water masses); residual gas neglected in the Module 09 parcel",
        "pressure_trace": "Module 03 integrate_cycle(keep_trace=True) motored p(theta) with Woschni wall heat and Module 03's own water evaporation schedule, IVC -180 -> spark; imposed in Module 09 'pt' mode (adiabatic Module 09 parcel)",
        "spark_timing": "CA50 - 0-50 % burn angle from Module 03 Wiebe a=5, m=2 (Module 03 reports no 0-50 % angle)",
        "venturi": f"carb_design.json is NOT committed on wme1-dev (an uncommitted copy exists in Hermes's working tree, not used); Nukiyama-Tanasawa at the {R.DEF.venturi_throat_U_m_s:g} m/s SPEC fallback throat speed (FLAGGED)",
        "runner": f"U = {R.REFERENCE['U_runner_m_s']} m/s, L = {R.REFERENCE['L_runner_m']} m, D = {R.DEF.runner_diameter_m} m, plenum T = Module 03 T_intake, 1 bar",
        "wall": "bend deposition only (Pui et al. 1987); deposited liquid leaves the charge (no film re-evaporation; Module 13)",
        "ethanol": "CoolProp Ethanol liquid; San Diego mechanism vapour thermo/transport; DECHEMA/ChemSep Wilson (NRTL cross-check)",
    }
    summary = dict(module=R.MODULE, version=R.VERSION, job="water-engine-20261023-103500", labels=labels,
                   assumptions=assumptions | {"properties": P.property_assumptions(FUELS)},
                   cfd_matched_fit=dict(fits=fits, interpolation="k(p): ln-p interpolation between A1 (1 bar) and A2 (20 bar), clamped; k_A1 in runner/induction",
                                        cfd_dir=str(args.cfd_dir), cfd_ref=args.cfd_ref),
                   spark=spark_info, n_cases=len(rows), n_failed=len(failed), failed=failed,
                   max_mass_error_rel=max((r["max_mass_error_rel"] for r in good), default=None),
                   max_energy_closure_rel=max((r["max_energy_closure_rel"] for r in good), default=None),
                   runtime_s=time.perf_counter() - t0)
    summary["git_sha"] = io.git_sha()
    (sub / "summary.json").write_text(json.dumps(summary, indent=2, default=float))
    sas = dict(module=R.MODULE, version=R.VERSION, source="sims/09_spray_evaporation/design_points.py",
               labels=labels, units=dict(pct="% of injected liquid (alcohol + water)", SMD_spark_um="um, airborne droplets",
                                         kg="per cylinder per cycle"),
               spark=spark_info, cases=cases)
    (out / "spray_at_spark.json").write_text(json.dumps(sas, indent=2, default=float))
    (sub / "spray_at_spark.json").write_text(json.dumps(sas, indent=2, default=float))
    write_evap_profiles(out / "evap_profiles.json", good, profiles)
    print(json.dumps(dict(n_cases=len(rows), n_failed=len(failed), fits={c: round(f["k"], 4) for c, f in fits.items()},
                          runtime_s=round(summary["runtime_s"], 1))))
    return 1 if failed else 0


from sims.common import io  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
