"""SPEC section 12.2 (Module 09 spray_evaporation): intake atomisation and
evaporation of water, methanol and premixed wet-methanol blends.

Chain per case (one cylinder charge, closed mass balance, see model.py):
  atomiser -> runner (constant p, gas at U_runner for L/U)
  -> 90 deg bend (Stokes-number wall impingement, Pui et al. 1987)
  -> induction (constant p, mean in-cylinder residence before IVC)
  -> IVC -> isentropic compression (slider-crank V(theta)) -> spark.
Outputs % evaporated at IVC and spark, % wall-impinged, remaining liquid
SMD at spark, spray_at_spark.json (Module 11 input), the recommended
atomiser for Module 06, and a chamber-mode cross-check against the
OpenFOAM phase-A cases A1/A2 (Module 12, branch wme1-cfd).

Status labels (SPEC 0.3): results are EXECUTED model runs. The d2-law,
saturation and mass-conservation tests VERIFY the numerics. Nothing here is
experimentally VALIDATED; the CFD cross-check is model-vs-model.

Module 03 p(theta) and Module 06 airflow are not available at b00342f, so
the SPEC fallbacks are used: isentropic compression and a 30 m/s venturi
throat speed (recorded in summary.json assumptions).
"""

from dataclasses import dataclass, asdict
import csv
import importlib
import json
import math
from pathlib import Path
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sims.common import fuels, io

from . import atomisers as A
from . import model as M
from . import properties as P

MODULE = "09_spray_evaporation"
VERSION = "1.0.0"


@dataclass(frozen=True)
class Defaults:
    bore_m: float = 0.086              # SPEC 6 default test engine
    stroke_m: float = 0.086
    rod_m: float = 0.145
    rpm: float = 2000.0
    CR: float = 12.0                   # placeholder: Module 03 design point not on this branch
    p_plenum_Pa: float = 1.0e5         # SPEC 6: WOT, p_IVC = 1 bar
    eta_v: float = 1.0                 # trapped air = plenum density x displacement
    phi: float = 1.0
    T_liquid_K: float = 300.0          # tank temperature (SPEC 7 uses 300 K liquid)
    spark_CAD_bTDC: float = 25.0       # CA50 8 aTDC (SPEC 6) minus ~33 CAD ignition-to-CA50 (rationale)
    induction_fraction: float = 0.5    # mean residence = half the 180 CAD intake stroke before IVC (BDC)
    runner_diameter_m: float = 0.035   # rationale: ~35 mm runner for a 0.5 L cylinder
    venturi_throat_U_m_s: float = 30.0 # SPEC 12.2 fallback (Module 06 not yet available)
    psi_injection_s: float = 0.010     # port-injector pulse width for the Lefebvre mass flow (rationale)
    psi_velocity_coeff: float = 0.6    # droplet exit speed = c sqrt(2 dP / rho) (rationale)
    rr_q: float = A.RR_SPREAD_Q
    rr_classes: int = A.RR_CLASSES
    activity: str = "wilson"


DEF = Defaults()
ATOMISERS = ("carb_venturi", "psi_3bar", "psi_5bar", "air_assist_20um", "air_assist_30um",
             "ultrasonic_40kHz", "ultrasonic_120kHz")
FULL_W = (0.0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8)
FULL_T = (320.0, 340.0, 360.0, 380.0, 400.0, 420.0)
FULL_U = (10.0, 20.0, 30.0, 40.0)
FULL_L = (0.1, 0.2, 0.3, 0.4)
REFERENCE = dict(T_plenum_K=360.0, U_runner_m_s=30.0, L_runner_m=0.2)
QUICK_W = (0.0, 0.6)

# OpenFOAM phase-A chamber (aachenBomb box 20 x 100 x 20 mm, cfd/README.md)
CFD_CHAMBER_V_m3 = 0.02 * 0.1 * 0.02
CFD_RR_Q = 3.0              # sprayCloudProperties RosinRammler n
CFD_T_LIQUID_K = 300.0
CROSSCHECK_CASES = ("A1-H2O", "A1-CH3OH", "A1-BLEND", "A2-H2O", "A2-CH3OH", "A2-BLEND")
LIQUID_YM = {"H2O": 0.0, "CH3OH": 1.0, "BLEND": 0.4}


# ---------------------------------------------------------------- geometry
def cyl_volume(theta_deg, par=DEF):
    a = par.stroke_m / 2.0
    Ap = math.pi * par.bore_m**2 / 4.0
    Vd = Ap * par.stroke_m
    Vc = Vd / (par.CR - 1.0)
    th = math.radians(theta_deg)
    s = par.rod_m + a - a * math.cos(th) - math.sqrt(par.rod_m**2 - (a * math.sin(th))**2)
    return Vc + Ap * s


def cyl_dVdtheta(theta_deg, par=DEF):
    h = 1e-4
    return (cyl_volume(theta_deg + h, par) - cyl_volume(theta_deg - h, par)) / (2 * h)


def displacement(par=DEF):
    return math.pi * par.bore_m**2 / 4.0 * par.stroke_m


# ---------------------------------------------------------------- charge
def charge(w, T_pl, par=DEF):
    """Air, methanol and water mass per cycle [kg] at phi = 1 on fuel+air."""
    tab = P.tables()
    R_air = P.R_U / tab.M_g[0]
    m_air = par.eta_v * par.p_plenum_Pa * displacement(par) / (R_air * T_pl)
    m_f = m_air / (fuels.stoich_air_fuel_ratio("CH3OH") / par.phi)
    m_w = m_f * w / (1.0 - w)
    return m_air, m_f, m_w


def atomiser_smd(name, w, T_pl, U_runner, par=DEF):
    """Returns (SMD [m], initial droplet velocity [m/s], note)."""
    tab = P.tables()
    m_air, m_f, m_w = charge(w, T_pl, par)
    Y_m = 1.0 - w
    liq = P.blend_physical(tab, Y_m, par.T_liquid_K)
    rho_a = par.p_plenum_Pa * tab.M_g[0] / (P.R_U * T_pl)
    m_l = m_f + m_w
    if name == "carb_venturi":
        q = (m_l / liq["rho"]) / (m_air / rho_a)
        return A.nukiyama_tanasawa(par.venturi_throat_U_m_s, liq["sigma"], liq["rho"], liq["mu"], q), 0.0, "Nukiyama-Tanasawa, 30 m/s throat"
    if name.startswith("psi_"):
        dP = float(name[4]) * 1e5
        mdot = m_l / par.psi_injection_s
        u0 = par.psi_velocity_coeff * math.sqrt(2.0 * dP / liq["rho"])
        return A.lefebvre_pressure_swirl(liq["sigma"], liq["mu"], mdot, dP, rho_a), u0, f"Lefebvre simplex, dP {dP/1e5:g} bar"
    if name.startswith("air_assist_"):
        return float(name.split("_")[2][:-2]) * 1e-6, U_runner, "SPEC 20-30 um"
    if name.startswith("ultrasonic_"):
        f = float(name.split("_")[1][:-3]) * 1e3
        return A.lang_ultrasonic(liq["sigma"], liq["rho"], f), 0.0, f"Lang (1962), {f/1e3:g} kHz"
    raise ValueError(name)


def pui_bend_efficiency(d, rho_l, U, mu_g, D_tube):
    """90-degree bend inertial deposition, turbulent flow: Pui, Romay-Novas &
    Liu (1987), Aerosol Sci. Technol. 7:301, eta = 1 - 10^(-0.963 St),
    St = rho_p d^2 U / (9 mu D) (Cunningham slip = 1 for d > 1 um)."""
    St = rho_l * d**2 * U / (9.0 * mu_g * D_tube)
    return 1.0 - 10.0**(-0.963 * St), St


def _energy(sp):
    return sp.enthalpy()


# ---------------------------------------------------------------- engine case
def run_case(case, par=DEF, keep_trace=False):
    """One sweep point -> row dict."""
    start = time.perf_counter()
    w, T_pl, U, L, atom = case["w"], case["T_plenum_K"], case["U_runner_m_s"], case["L_runner_m"], case["atomiser"]
    tab = P.tables()
    m_air, m_f, m_w = charge(w, T_pl, par)
    m_l = m_f + m_w
    Y_m = m_f / m_l
    smd0, u0, note = atomiser_smd(atom, w, T_pl, U, par)
    d, frac = A.rosin_rammler_classes(smd0, par.rr_q, par.rr_classes)
    sp = M.Spray(m_air=m_air, T_gas=T_pl, p=par.p_plenum_Pa, m_ref=m_l, activity=par.activity)
    rho0 = sp.liquid_density(np.full(d.size, par.T_liquid_K), np.full(d.size, Y_m))
    sp.add_classes(d, m_l * frac / (rho0 * math.pi * d**3 / 6.0), Y_m, par.T_liquid_K, u0)
    closure = []
    trace = []
    # 1) runner
    H0 = sp.enthalpy()
    snaps = sp.run(L / U, mode="p", u_g=U, n_out=10); trace += snaps
    closure.append((sp.enthalpy() - H0))
    evap_runner = snaps[-1]["evaporated_frac"]
    # 2) bend
    mw, mm, Td, ud, Tg, mv = sp.split()
    mu_g = float(np.interp(Tg, tab.TG, tab.mu_g[0]))
    dd = sp.droplet_diameters()
    rho_now = sp.liquid_density(Td, np.where(mw + mm > 0, mm / np.maximum(mw + mm, 1e-300), 0))
    eta, St = pui_bend_efficiency(dd, rho_now, U, mu_g, par.runner_diameter_m)
    if not case.get("bend_impingement", True):
        eta = np.zeros_like(eta)
    sp.impinge(eta)
    # 3) induction to IVC
    t_cycle_deg = 1.0 / (6.0 * par.rpm)   # s per CAD
    t_ind = par.induction_fraction * 180.0 * t_cycle_deg
    H0 = sp.enthalpy()
    snaps = sp.run(t_ind, mode="p", u_g=0.0, n_out=10); trace += snaps
    closure.append((sp.enthalpy() - H0))
    ivc = snaps[-1]
    # 4) compression IVC (BDC, -180) -> spark
    V_ivc = ivc["V_m3"]
    V_bdc = cyl_volume(-180.0, par)
    t_ivc = sp.t
    def Vfun(tt):
        th = -180.0 + (tt - t_ivc) / t_cycle_deg
        return V_ivc * cyl_volume(th, par) / V_bdc, V_ivc * cyl_dVdtheta(th, par) / V_bdc / t_cycle_deg
    U0 = sp.internal_energy(); W0 = sp.work
    snaps = sp.run((180.0 - par.spark_CAD_bTDC) * t_cycle_deg, mode="V", Vfun=Vfun, n_out=40); trace += snaps
    closure.append((sp.internal_energy() - U0) + (sp.work - W0))
    spk = snaps[-1]
    latent_scale = m_w * 2.4e6 + m_f * 1.17e6
    mk, Q, ex = sp.fluxes(sp.y, spk["p_Pa"], 0.0)
    mw, mm, Td, ud, Tg, mv = sp.split()
    wt = sp.N * (np.maximum(mw, 0) + np.maximum(mm, 0)) * sp.m0
    sat_ratio = float(np.sum(wt * ex["Yinf"].sum()) / np.sum(wt * ex["Ys"].sum(axis=1))) if wt.sum() > 0 else float("nan")
    liq_w = float(np.sum(sp.N * np.maximum(mw, 0) * sp.m0)); liq_m = float(np.sum(sp.N * np.maximum(mm, 0) * sp.m0))
    m_charge = m_air + m_l - spk["wall_kg"]
    row = dict(atomiser=atom, bend_impingement=bool(case.get("bend_impingement", True)), w=w, T_plenum_K=T_pl, U_runner_m_s=U, L_runner_m=L,
               SMD_initial_um=smd0 * 1e6, atomiser_note=note,
               m_air_kg=m_air, m_methanol_kg=m_f, m_water_kg=m_w,
               evaporated_runner_pct=100 * evap_runner,
               wall_impinged_pct=100 * spk["wall_kg"] / m_l,
               evaporated_IVC_pct=100 * ivc["evaporated_frac"], T_IVC_K=ivc["T_gas_K"],
               evaporated_spark_pct=100 * spk["evaporated_frac"],
               airborne_liquid_spark_pct=100 * spk["liquid_kg"] / m_l,
               SMD_spark_um=spk["SMD_m"] * 1e6, T_spark_K=spk["T_gas_K"], p_spark_Pa=spk["p_Pa"],
               liquid_water_spark_kg=liq_w, liquid_methanol_spark_kg=liq_m,
               liquid_mass_fraction_of_charge_spark=(liq_w + liq_m) / m_charge,
               S_water_spark=spk["S_water"], S_methanol_spark=spk["S_methanol"],
               S_water_IVC=ivc["S_water"], S_methanol_IVC=ivc["S_methanol"],
               surface_saturation_ratio_spark=sat_ratio,
               saturation_limited_spark=bool(spk["liquid_kg"] > 0.01 * m_l and sat_ratio > 0.9),
               max_mass_error_rel=max(s["mass_error_rel"] for s in trace),
               max_S_pure=max(max(s["S_water"], s["S_methanol"]) for s in trace),
               max_energy_closure_rel=max(abs(c) for c in closure) / latent_scale,
               boiling_cap_hits=sp.cap_hits, runtime_s=time.perf_counter() - start)
    if keep_trace:
        return row, trace
    return row


def _task(case):
    try:
        return run_case(case)
    except Exception as exc:  # recorded, never hidden
        return dict(case, status="failed", reason=repr(exc))


def sweep(mode):
    ws = QUICK_W if mode == "quick" else FULL_W
    Ts = (REFERENCE["T_plenum_K"],) if mode == "quick" else FULL_T
    Us = (REFERENCE["U_runner_m_s"],) if mode == "quick" else FULL_U
    Ls = (REFERENCE["L_runner_m"],) if mode == "quick" else FULL_L
    main_cases = [dict(atomiser=a, w=w, T_plenum_K=T, U_runner_m_s=U, L_runner_m=L)
                  for a in ATOMISERS for w in ws for T in Ts for U in Us for L in Ls]
    # sensitivity: no wall impingement at the bend, reference condition only
    sens = [dict(REFERENCE, atomiser=a, w=w, bend_impingement=False) for a in ATOMISERS for w in ws]
    return main_cases + sens


# ---------------------------------------------------------------- chamber mode
def read_cfd(cfd_dir):
    cfd_dir = Path(cfd_dir)
    summ = json.loads((cfd_dir / "summary.json").read_text())
    out = {}
    for c in CROSSCHECK_CASES:
        if c not in summ or not summ[c].get("complete") or not (cfd_dir / summ[c]["csv"]).is_file():
            continue
        with open(cfd_dir / summ[c]["csv"]) as fh:
            rows = list(csv.DictReader(fh))
        out[c] = dict(meta=summ[c]["meta"], summary=summ[c],
                      t=np.array([float(r["t_ms"]) for r in rows]) * 1e-3,
                      evap=np.array([float(r["evaporated_pct"]) for r in rows]),
                      smd=np.array([float(r["SMD_um"]) for r in rows]),
                      pen=np.array([float(r["penetration_mm"]) for r in rows]))
    return out


def chamber_run(meta, smd, t_end, activity="wilson", packets=10, classes=8):
    """Constant-volume chamber reproducing an OpenFOAM phase-A case."""
    tab = P.tables()
    Y_m = float(meta["composition"].get("CH3OH", 0.0))
    p, T = meta["p"], meta["T"]
    m_inj = meta["massTotal_kg"]; dur = meta["dur"]; U = meta["U_bernoulli_m_s"]
    m_air = p * CFD_CHAMBER_V_m3 * tab.M_g[0] / (P.R_U * T)
    sp = M.Spray(m_air=m_air, T_gas=T, p=p, m_ref=m_inj, activity=activity)
    Vf = lambda tt: (CFD_CHAMBER_V_m3, 0.0)
    d, frac = A.rosin_rammler_classes(smd, CFD_RR_Q, classes)
    rho = sp.liquid_density(np.full(d.size, CFD_T_LIQUID_K), np.full(d.size, Y_m))
    snaps = [sp.snapshot(0.0, sp.y, "V", Vf)]
    for k in range(packets):
        tk = (k + 0.5) * dur / packets
        if tk > sp.t:
            snaps += sp.run(tk - sp.t, mode="V", Vfun=Vf, n_out=8)[1:]
        sp.add_classes(d, m_inj / packets * frac / (rho * math.pi * d**3 / 6.0), Y_m, CFD_T_LIQUID_K, U)
        snaps.append(sp.snapshot(sp.t, sp.y, "V", Vf))
    snaps += sp.run(t_end - sp.t, mode="V", Vfun=Vf, n_out=40)[1:]
    return snaps


def crosscheck(cfd, cases, step_s=1e-4):
    rows, summary = [], {}
    for c in cases:
        if c not in cfd:
            summary[c] = "not run: CFD CSV not available (case not complete)"
            continue
        meta = cfd[c]["meta"]; s = cfd[c]["summary"]
        smd = s["SMD_eoi_um"] * 1e-6
        t_end = float(cfd[c]["t"][-1])
        base = chamber_run(meta, smd, t_end, "wilson")
        ideal = chamber_run(meta, smd, t_end, "ideal") if meta["composition"].get("CH3OH", 0) not in (0.0, 1.0) else None
        tb = np.array([x["t_s"] for x in base]); eb = np.array([100 * x["evaporated_frac"] for x in base])
        sb = np.array([x["SMD_m"] * 1e6 for x in base])
        grid = np.arange(step_s, t_end + 1e-12, step_s)
        for tt in grid:
            # model evaporated % at tt: last snapshot at or before tt (injection is discrete)
            j = np.searchsorted(tb, tt, side="right") - 1
            e09 = float(eb[j] if abs(tb[j] - tt) < 1e-12 else np.interp(tt, tb[j:j + 2], eb[j:j + 2]))
            ecfd = float(np.interp(tt, cfd[c]["t"], cfd[c]["evap"]))
            r = dict(case=c, t_ms=round(tt * 1e3, 4), evaporated_cfd_pct=ecfd, evaporated_m09_pct=e09,
                     diff_m09_minus_cfd_pp=e09 - ecfd,
                     ratio_m09_over_cfd=e09 / ecfd if ecfd > 0 else float("nan"),
                     SMD_cfd_um=float(np.interp(tt, cfd[c]["t"], cfd[c]["smd"])),
                     SMD_m09_um=float(np.interp(tt, tb, sb)),
                     penetration_cfd_mm=float(np.interp(tt, cfd[c]["t"], cfd[c]["pen"])))
            if ideal is not None:
                ti = np.array([x["t_s"] for x in ideal]); ei = np.array([100 * x["evaporated_frac"] for x in ideal])
                r["evaporated_m09_ideal_raoult_pct"] = float(np.interp(tt, ti, ei))
            else:
                r["evaporated_m09_ideal_raoult_pct"] = float("nan")
            rows.append(r)
        cr = [r for r in rows if r["case"] == c]
        eoi = min(cr, key=lambda r: abs(r["t_ms"] - meta["dur"] * 1e3))
        end = cr[-1]
        summary[c] = dict(SMD_matched_um=smd * 1e6, eoi_ms=meta["dur"] * 1e3,
                          cfd_eoi_pct=eoi["evaporated_cfd_pct"], m09_eoi_pct=eoi["evaporated_m09_pct"],
                          diff_eoi_pp=eoi["diff_m09_minus_cfd_pp"], ratio_eoi=eoi["ratio_m09_over_cfd"],
                          end_ms=end["t_ms"], cfd_end_pct=end["evaporated_cfd_pct"], m09_end_pct=end["evaporated_m09_pct"],
                          diff_end_pp=end["diff_m09_minus_cfd_pp"], ratio_end=end["ratio_m09_over_cfd"],
                          max_abs_diff_pp=max(abs(r["diff_m09_minus_cfd_pp"]) for r in cr),
                          m09_ideal_raoult_end_pct=end["evaporated_m09_ideal_raoult_pct"])
    return rows, summary


# ---------------------------------------------------------------- validation
def d2_law_check():
    """Constant-property single water droplet vs analytic d2-law (Sh = 2)."""
    c = M.ConstProps()
    sp = M.Spray(m_air=1.0, T_gas=350.0, p=1e5, m_ref=1e-12, const=c, fixed_Td=True, infinite_gas=True)
    d0 = 50e-6
    sp.add_classes([d0], [1.0], 0.0, 300.0, 0.0)
    K = 8.0 * c.rho_g * c.D * math.log1p((c.Ys - c.Yinf) / (1.0 - c.Ys)) / c.rho_l
    t_life = d0**2 / K
    snaps = sp.run(0.9 * t_life, n_out=9, rtol=1e-9)
    errs = []
    for s in snaps[1:]:
        d2_model = sp_d2(sp, s)
        d2_exact = d0**2 - K * s["t_s"]
        errs.append(abs(d2_model - d2_exact) / d2_exact)
    return dict(K_m2_s=K, lifetime_s=t_life, max_rel_err_d2=max(errs))


def sp_d2(sp, snap):
    m = snap["liquid_kg"]
    return (6.0 * m / (math.pi * sp.const.rho_l))**(2.0 / 3.0)


# ---------------------------------------------------------------- outputs
def write_plots(out, rows, xrows, mode):
    ok = [r for r in rows if r.get("status") != "failed"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for a in ATOMISERS:
        pts = [r for r in ok if r["atomiser"] == a and r["w"] == 0.6
               and r["U_runner_m_s"] == REFERENCE["U_runner_m_s"] and r["L_runner_m"] == REFERENCE["L_runner_m"]]
        pts.sort(key=lambda r: r["T_plenum_K"])
        if pts:
            ax.plot([r["T_plenum_K"] for r in pts], [r["evaporated_spark_pct"] for r in pts], "o-", label=a)
    ax.set_xlabel("Plenum temperature [K]"); ax.set_ylabel("Evaporated at spark [%]")
    ax.set_title("w = 0.6, U = 30 m/s, L = 0.2 m"); ax.legend(fontsize=7); ax.grid(alpha=0.3)
    io.save_fig(fig, out / "evaporated_at_spark_w06.png"); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for a in ATOMISERS:
        pts = [r for r in ok if r["atomiser"] == a and r["T_plenum_K"] == REFERENCE["T_plenum_K"]
               and r["U_runner_m_s"] == REFERENCE["U_runner_m_s"] and r["L_runner_m"] == REFERENCE["L_runner_m"]]
        pts.sort(key=lambda r: r["w"])
        if pts:
            ax.plot([r["w"] for r in pts], [r["evaporated_spark_pct"] for r in pts], "o-", label=a)
    ax.set_xlabel("Water fraction of liquid w [-]"); ax.set_ylabel("Evaporated at spark [%]")
    ax.set_title("T_plenum 360 K, U 30 m/s, L 0.2 m"); ax.legend(fontsize=7); ax.grid(alpha=0.3)
    io.save_fig(fig, out / "evaporated_at_spark_vs_w.png"); plt.close(fig)
    if xrows:
        cases = sorted({r["case"] for r in xrows})
        fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))
        for c in cases:
            cr = [r for r in xrows if r["case"] == c]
            ax = axs[0] if c.startswith("A1") else axs[1]
            l, = ax.plot([r["t_ms"] for r in cr], [r["evaporated_cfd_pct"] for r in cr], "-", label=f"{c} CFD")
            ax.plot([r["t_ms"] for r in cr], [r["evaporated_m09_pct"] for r in cr], "--", color=l.get_color(), label=f"{c} m09")
        for ax, ttl in zip(axs, ("A1: 1 bar, 360 K", "A2: 20 bar, 700 K")):
            ax.set_xlabel("Time after SOI [ms]"); ax.set_ylabel("Evaporated [% of injected]")
            ax.set_title(ttl); ax.grid(alpha=0.3)
            if ax.get_legend_handles_labels()[0]:
                ax.legend(fontsize=7)
        io.save_fig(fig, out / "cfd_crosscheck.png"); plt.close(fig)


def recommend(rows):
    ok = [r for r in rows if r.get("status") != "failed" and r["w"] == 0.6]
    score = {}
    for a in ATOMISERS:
        v = [r["evaporated_spark_pct"] for r in ok if r["atomiser"] == a]
        wl = [r["wall_impinged_pct"] for r in ok if r["atomiser"] == a]
        if v:
            score[a] = dict(mean_evaporated_spark_pct=float(np.mean(v)), median_evaporated_spark_pct=float(np.median(v)),
                            mean_wall_impinged_pct=float(np.mean(wl)), n=len(v))
    best = max(score, key=lambda a: score[a]["mean_evaporated_spark_pct"]) if score else None
    return best, score


def _clean(o):
    """Replace non-finite floats by None so JSON stays strict (allow_nan=False)."""
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (float, np.floating)):
        return float(o) if math.isfinite(o) else None
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def assumptions(mode, workers):
    d = {k: {"value": v} for k, v in asdict(DEF).items()}
    d["spark_CAD_bTDC"]["rationale"] = "MBT proxy: CA50 8 CAD aTDC (SPEC 6) with ~33 CAD from spark to CA50"
    d["CR"]["rationale"] = "Module 03 design point not available on b00342f; mid-range of SPEC 6 sweep"
    d["induction_fraction"]["rationale"] = "mean in-cylinder residence before IVC of charge inducted uniformly over the intake stroke"
    d["runner_diameter_m"]["rationale"] = "typical runner for 0.5 L cylinder; sets Stokes number at the bend"
    d["psi_injection_s"]["rationale"] = "port-injection pulse at WOT 2000 rpm; sets Lefebvre mass flow only"
    d["venturi_throat_U_m_s"]["source"] = "SPEC 12.2 fallback, Module 06 not available"
    d.update(P.property_assumptions())
    d.update({
        "evaporation_model": {"value": "Abramzon-Sirignano (1989) film model, Ranz-Marshall Nu0/Sh0, 1/3 rule"},
        "drop_internal": {"value": "rapid mixing, uniform temperature and composition (infinite conductivity)"},
        "size_distribution": {"value": f"Rosin-Rammler q={DEF.rr_q}, {DEF.rr_classes} equal-mass classes, discrete SMD exact"},
        "secondary_breakup": {"value": "none", "rationale": "intake We is low for SMD < 150 um at 10-40 m/s slip; CFD A2 shows breakup at 100 bar dP, so chamber cross-check matches SMD at EOI"},
        "wall_impingement": {"value": "Pui, Romay-Novas & Liu (1987) turbulent 90 deg bend: eta = 1 - 10^(-0.963 St)", "caveat": "fit range St < ~1.5; larger St extrapolated (eta -> 1). Wall film is not re-evaporated (conservative for % evaporated)"},
        "wall_heat_transfer": {"value": "none (adiabatic gas)", "rationale": "plenum temperature represents intake heating; conservative for evaporation"},
        "in_cylinder_slip": {"value": "gas velocity 0 after the bend; turbulence enhancement neglected", "rationale": "conservative"},
        "compression": {"value": "slider-crank volume, adiabatic, real cp(T); Module 03 p(theta) not available", "source": "SPEC 12.2 fallback"},
        "residual_gas": {"value": "neglected", "rationale": "hot residuals would raise evaporation; conservative"},
        "closed_mass_balance": {"value": "vapour accumulates in the parcel; no vapour removed; saturation limit emerges from B_M -> 0"},
        "regularisation": {"value": f"fluxes scaled below {M.R_FLOOR:g} of initial droplet mass", "rationale": "Lipschitz vanishing-droplet limit; residual liquid kept as liquid"},
        "boiling_guard": {"value": f"sum of surface vapour mole fractions capped at {M.SUM_XS_CAP}", "count_reported": True},
        "cfd_crosscheck": {"value": "constant-volume 20x100x20 mm chamber, 0-D well mixed, same p, T, liquid, injected mass and top-hat duration as OpenFOAM phase A; SMD = CFD SMD at EOI; RR q = 3; 10 injection packets; no breakup; droplet slip from U_bernoulli relaxing in quiescent gas"},
        "workers": {"value": workers}, "mode": {"value": mode},
    })
    return d


def main(argv=None):
    start = time.perf_counter()
    parser = io.argument_parser(MODULE)
    parser.add_argument("--cfd-dir", type=Path, default=Path("cfd") / "results",
                        help="OpenFOAM phase-A results dir (summary.json + CSVs), branch wme1-cfd")
    parser.add_argument("--no-crosscheck", action="store_true")
    args = parser.parse_args(None if argv is None else list(map(str, argv)))
    out = args.out; out.mkdir(parents=True, exist_ok=True)
    cases = sweep(args.mode)
    rows = io.ordered_map(_task, cases, args.workers, chunksize=4)
    failed = [r for r in rows if r.get("status") == "failed"]
    ok = [r for r in rows if r.get("status") != "failed"]
    io.write_csv(out / "sweep.csv", ok or rows)
    if failed:
        io.write_csv(out / "failed.csv", failed)
    # cross-check
    xrows, xsum = [], {}
    if not args.no_crosscheck and (args.cfd_dir / "summary.json").is_file():
        cfd = read_cfd(args.cfd_dir)
        cc = ("A1-H2O",) if args.mode == "quick" else CROSSCHECK_CASES
        xrows, xsum = crosscheck(cfd, cc)
        if xrows:
            io.write_csv(out / "cfd_crosscheck.csv", xrows)
    else:
        xsum = {"status": "not run: --cfd-dir has no summary.json" if not args.no_crosscheck else "disabled"}
    sens = [r for r in ok if not r["bend_impingement"]]
    ok = [r for r in ok if r["bend_impingement"]]
    no_bend = {}
    for r in sens:
        no_bend.setdefault(r["atomiser"], {})[f"w={r['w']:g}"] = dict(
            evaporated_IVC_pct=r["evaporated_IVC_pct"], evaporated_spark_pct=r["evaporated_spark_pct"],
            airborne_liquid_spark_pct=r["airborne_liquid_spark_pct"], T_IVC_K=r["T_IVC_K"],
            surface_saturation_ratio_spark=r["surface_saturation_ratio_spark"],
            saturation_limited_spark=r["saturation_limited_spark"])
    best, score = recommend(ok)
    ref = {}
    for r in ok:
        if all(r[k] == v for k, v in REFERENCE.items()):
            ref.setdefault(r["atomiser"], {})[f"w={r['w']:g}"] = dict(
                evaporated_IVC_pct=r["evaporated_IVC_pct"], evaporated_spark_pct=r["evaporated_spark_pct"],
                wall_impinged_pct=r["wall_impinged_pct"], SMD_spark_um=r["SMD_spark_um"], SMD_initial_um=r["SMD_initial_um"],
                saturation_limited_spark=r["saturation_limited_spark"])
    spark = dict(module=MODULE, version=VERSION, git_sha=io.git_sha(), mode=args.mode,
                 description="Liquid remaining at spark per case for Module 11 (Ballal-Lefebvre). Masses per cylinder charge.",
                 reference_condition=REFERENCE, recommended_atomiser_for_module06=best,
                 cases=[{k: r[k] for k in ("atomiser", "w", "T_plenum_K", "U_runner_m_s", "L_runner_m",
                                            "evaporated_spark_pct", "wall_impinged_pct", "airborne_liquid_spark_pct",
                                            "SMD_spark_um", "liquid_water_spark_kg", "liquid_methanol_spark_kg",
                                            "liquid_mass_fraction_of_charge_spark", "T_spark_K", "p_spark_Pa",
                                            "saturation_limited_spark")} for r in ok])
    (out / "spray_at_spark.json").write_text(json.dumps(_clean(spark), indent=1, allow_nan=False) + "\n")
    write_plots(out, ok, xrows, args.mode)
    d2 = d2_law_check()
    checks = dict(
        d2_law=dict(d2, passed=d2["max_rel_err_d2"] < 0.02, tolerance=0.02),
        mass_conservation=dict(max_rel_error=max(r["max_mass_error_rel"] for r in ok + sens), tolerance=1e-8),
        saturation=dict(max_pure_component_saturation_ratio=max(r["max_S_pure"] for r in ok + sens), tolerance=1.0 + 1e-6),
        energy_closure=dict(max_rel_to_latent=max(r["max_energy_closure_rel"] for r in ok + sens), note="diagnostic, segment-wise H (const p) / U+W (volume); trapezoid p dV"),
        failed_cases=len(failed), boiling_cap_hits=sum(r["boiling_cap_hits"] for r in ok),
        status_labels="executed model runs; d2/saturation/mass checks are numerical verification; nothing experimentally validated")
    checks["mass_conservation"]["passed"] = checks["mass_conservation"]["max_rel_error"] < 1e-8
    checks["saturation"]["passed"] = checks["saturation"]["max_pure_component_saturation_ratio"] <= 1.0 + 1e-6
    checks["passed"] = bool(checks["d2_law"]["passed"] and checks["mass_conservation"]["passed"]
                            and checks["saturation"]["passed"] and not failed)
    sat_frac = {f"w={w:g}": float(np.mean([r["saturation_limited_spark"] for r in ok if r["w"] == w]))
                for w in sorted({r["w"] for r in ok})}
    key = dict(cases=len(rows), failed=len(failed), recommended_atomiser_for_module06=best,
               recommendation_basis="highest mean % evaporated at spark at w = 0.6 over the sweep",
               atomiser_scores_w06=score, reference_condition=REFERENCE, reference_results=ref,
               fraction_saturation_limited_at_spark_by_w=sat_frac,
               sensitivity_no_bend_impingement_reference=no_bend,
               cfd_crosscheck=xsum, executed_verified_validated="executed; numerics verified by tests; not validated against experiment")
    io.write_summary(out, MODULE, VERSION, args.mode, _clean(assumptions(args.mode, args.workers)), _clean(key), _clean(checks),
                     time.perf_counter() - start)
    return 0 if checks["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
