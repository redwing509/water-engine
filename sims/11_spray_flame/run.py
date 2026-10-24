"""SPEC 12.3 Module 11 spray_flame: how much liquid the flame front tolerates at spark.

Inputs (files only, SPEC 3):
  results/02_flame_chem/flame_speed_fits.json   gas-phase S_L(w), Module 02 (wme1-dev 4420273)
  results/09_spray_evaporation/spray_at_spark.json   liquid at spark, SMD, T and p at spark (Module 09)
  results/03_engine_cycle/design_point.json     trapped fuel and water masses per design point

Outputs (results/11_spray_flame/): sweep.csv (S and MIE vs liquid fraction and SMD per design point),
design_points.csv (per atomiser and Module 09 variant), max_smd.csv, spray_flame.json, summary.json, PNGs.

Status (SPEC 0.3): EXECUTED model runs; tests VERIFY limits and monotonic trends; NOT VALIDATED, and the
Ballal-Lefebvre correlations are EXTRAPOLATED far beyond their atmospheric quiescent-mist range.
"""

import json
import math
from pathlib import Path
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import cantera as ct
from CoolProp.CoolProp import PropsSI

from sims.common import fuels, io

from . import model as M

MODULE = "11_spray_flame"
VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parents[2]
FIT_PATH = ROOT / "results" / "02_flame_chem" / "flame_speed_fits.json"
SAS_PATH = ROOT / "results" / "09_spray_evaporation" / "spray_at_spark.json"
DP_PATH = ROOT / "results" / "03_engine_cycle" / "design_point.json"

F_LIQ_FULL = (0.0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0)
F_LIQ_QUICK = (0.0, 0.01, 0.1)
D_FULL_um = (1, 2, 5, 10, 15, 20, 30, 40, 60, 80, 100, 150, 200)
D_QUICK_um = (5, 20, 60)
VARIANTS = ("nominal", "cfd_matched")

_GAS = {}


def _gas(fuel):
    if fuel not in _GAS:
        _GAS[fuel] = fuels.load_mechanism(fuel)
    return _GAS[fuel]


def make_state(fuel: str, w: float, T: float, p: float, SL0: float, prm: M.Params = M.DEF) -> M.State:
    """Unburned charge at spark (fully vaporised fuel + air + water vapour) and liquid properties."""
    gas = _gas(fuel)
    gas.TPX = T, p, fuels.mixture(fuel, prm.phi, w)
    rho, cp = gas.density, gas.cp_mass
    gas.equilibrate("HP")
    T_ad = gas.T
    k_air = PropsSI("conductivity", "T", T, "P", p, "Air")    # rationale: N2/O2 dominate the charge
    alpha = k_air / (rho * cp)
    name = fuels.FUELS[fuel].coolprop_name
    if p < PropsSI("pcrit", name):
        Tb = PropsSI("T", "P", p, "Q", 0, name)
        L = PropsSI("H", "P", p, "Q", 1, name) - PropsSI("H", "P", p, "Q", 0, name)
    else:   # supercritical: no latent heat; fall back to the near-critical bound
        Tb, L = PropsSI("Tcrit", name) - 1.0, 1e5
    B = max(cp * (T - Tb) / L, 1e-6)
    hfg_w = fuels.FUELS["H2O"].h_fg
    return M.State(T_K=T, p_Pa=p, rho_g=rho, cp_g=cp, alpha=alpha, T_ad_K=T_ad,
                   rho_F=fuels.FUELS[fuel].liquid_density, B=B, h_fg_w=hfg_w,
                   SL_gas=M.SL_at_state(SL0, T, p, prm))


def masses(dp_case: dict, fuel: str, prm: M.Params = M.DEF) -> dict:
    mf, mw = dp_case["fuel_mass_kg"], dp_case["water_mass_kg"]
    ma = mf * fuels.stoich_air_fuel_ratio(fuel) / prm.phi
    return dict(m_fuel=mf, m_water=mw, m_air=ma, m_charge=mf + mw + ma)


def load_inputs():
    fits = json.loads(FIT_PATH.read_text())
    sas = json.loads(SAS_PATH.read_text())
    dp = json.loads(DP_PATH.read_text())
    return fits, sas, dp


def run(mode: str):
    fits, sas, dp = load_inputs()
    f_grid = F_LIQ_QUICK if mode == "quick" else F_LIQ_FULL
    d_grid = D_QUICK_um if mode == "quick" else D_FULL_um
    sweep, dprows, maxrows, cases_out = [], [], [], {}
    for key, c in sas["cases"].items():
        fuel, point, w = c["fuel"], c["point"], float(c["w"])
        dpc = dp["per_fuel"][fuel][point]
        ms = masses(dpc, fuel)
        SL0 = M.poly_SL(fits[fuel], w)
        nom = [a["nominal"] for a in c["atomisers"].values()]
        T_ref = sum(n["T_spark_m09_K"] for n in nom) / len(nom)
        p_ref = nom[0]["p_spark_Pa"]
        st = make_state(fuel, w, T_ref, p_ref, SL0)
        base = dict(case=key, fuel=fuel, point=point, w=w, T_spark_K=T_ref, p_spark_Pa=p_ref)
        # (1) sweep: liquid fraction of the intake liquid (alcohol and water at intake ratio) x SMD
        for f in f_grid:
            Y_wl = f * ms["m_water"] / ms["m_charge"]
            for d in d_grid:
                r = M.spray_point(st, f, Y_wl, d * 1e-6)
                sweep.append(base | dict(f_liquid=f, SMD_um=d, **r))
            mx = M.max_smd(st, f, Y_wl)
            maxrows.append(base | dict(f_liquid=f) | {k[:-2] + "_um": v * 1e6 for k, v in mx.items()})
        # (2) design points: Module 09 liquid composition and SMD per atomiser and variant
        per_atom = {}
        for an, a in c["atomisers"].items():
            for v in VARIANTS:
                s = a[v]
                sta = make_state(fuel, w, s["T_spark_m09_K"], s["p_spark_Pa"], SL0)
                f_fuel = min(1.0, s["liquid_alcohol_spark_kg"] / ms["m_fuel"])
                Y_wl = s["liquid_water_spark_kg"] / ms["m_charge"]
                D = s["SMD_spark_um"] * 1e-6
                r = M.spray_point(sta, f_fuel, Y_wl, D)
                mx = M.max_smd(sta, f_fuel, Y_wl)
                verdict = ("MISFIRE (MIE > 100 mJ)" if r["MIE_J"] > M.DEF.E_SPARK_HIGH_J else
                           "MARGINAL (50 < MIE <= 100 mJ)" if r["MIE_J"] > M.DEF.E_SPARK_LOW_J else "IGNITES (MIE <= 50 mJ)")
                row = base | dict(atomiser=an, variant=v, T_spark_K=s["T_spark_m09_K"], liquid_spark_pct=s["liquid_spark_pct"],
                                  f_liquid_alcohol=f_fuel, Y_liquid_water=Y_wl, SMD_spark_um=s["SMD_spark_um"],
                                  verdict=verdict, **r, **{k[:-2] + "_um": val * 1e6 for k, val in mx.items()})
                dprows.append(row)
                per_atom.setdefault(an, {})[v] = {k: row[k] for k in (
                    "liquid_spark_pct", "f_liquid_alcohol", "SMD_spark_um", "S_L_gas_m_s", "S_BL_m_s", "S_eff_m_s",
                    "S_BL_over_SL", "S_eff_over_SL", "MIE_J", "verdict", "D_max_MIE_50mJ_um", "D_max_SBL_ratio_um",
                    "D_max_Seff_ratio_um")}
        cases_out[key] = dict(fuel=fuel, point=point, w=w, S_L0_400K_1atm_m_s=SL0, state_at_spark={
            k: getattr(st, k) for k in ("T_K", "p_Pa", "rho_g", "cp_g", "alpha", "T_ad_K", "rho_F", "B", "SL_gas")},
            atomisers=per_atom)
    return sweep, dprows, maxrows, cases_out


def recommended_max_smd(maxrows, dprows):
    """Per w: max SMD at spark at the WORST Module 09 liquid fraction among atomisers (nominal), by criterion."""
    out = {}
    for r in dprows:
        if r["variant"] != "nominal":
            continue
        k = r["case"]
        cur = out.get(k)
        if cur is None or r["f_liquid_alcohol"] > cur["f_liquid_alcohol_worst"]:
            out[k] = dict(w=r["w"], f_liquid_alcohol_worst=r["f_liquid_alcohol"], worst_atomiser=r["atomiser"],
                          D_max_MIE_50mJ_um=r["D_max_MIE_50mJ_um"], D_max_MIE_100mJ_um=r["D_max_MIE_100mJ_um"],
                          D_max_SBL_10pct_um=r["D_max_SBL_ratio_um"], D_max_Seff_10pct_um=r["D_max_Seff_ratio_um"])
    return out


def write_plots(out, sweep, case="CH3OH/water_majority"):
    rows = [r for r in sweep if r["case"] == case]
    fs = sorted({r["f_liquid"] for r in rows})
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for f in fs:
        rr = sorted((r for r in rows if r["f_liquid"] == f), key=lambda r: r["SMD_um"])
        x = [r["SMD_um"] for r in rr]
        l, = ax[0].plot(x, [r["S_BL_over_SL"] for r in rr], label=f"liquid {f:g}")
        ax[0].plot(x, [r["S_eff_over_SL"] for r in rr], ls="--", color=l.get_color())
        ax[1].loglog(x, [r["MIE_J"] * 1e3 for r in rr], color=l.get_color(), label=f"liquid {f:g}")
    ax[0].set_xscale("log"); ax[0].set_xlabel("SMD at spark [um]"); ax[0].set_ylabel("S_spray / S_L,gas [-]")
    ax[0].set_title(f"{case}: solid B-L, dashed with vapour-flame floor", fontsize=9); ax[0].legend(fontsize=7)
    for e in (50, 100):
        ax[1].axhline(e, color="k", ls=":")
    ax[1].set_xlabel("SMD at spark [um]"); ax[1].set_ylabel("Minimum ignition energy [mJ]")
    ax[1].set_title("Ballal-Lefebvre MIE (dotted: 50/100 mJ spark)", fontsize=9)
    io.save_fig(fig, out / "spray_flame_CH3OH_water_majority.png"); plt.close(fig)


def main(argv=None):
    t0 = time.perf_counter()
    args = io.argument_parser(MODULE).parse_args(None if argv is None else list(map(str, argv)))
    out = args.out; out.mkdir(parents=True, exist_ok=True)
    sweep, dprows, maxrows, cases = run(args.mode)
    io.write_csv(out / "sweep.csv", sweep)
    io.write_csv(out / "design_points.csv", dprows)
    io.write_csv(out / "max_smd.csv", maxrows)
    rec = recommended_max_smd(maxrows, dprows)
    write_plots(out, sweep)
    misfire = {f"{r['case']}/{r['atomiser']}/{r['variant']}": r["verdict"] for r in dprows}
    n_mis = sum(v.startswith("MISFIRE") for v in misfire.values())
    labels = {
        "status": "EXECUTED model runs; numerics VERIFIED by tests/test_spray_flame.py (zero-liquid limit, monotonic trends); "
                  "NOT experimentally VALIDATED.",
        "validity": "Ballal-Lefebvre correlations fitted at 0.1-1 atm, ~300 K, quiescent mists, SMD ~20-200 um; applied here at "
                    "25-35 bar and 650-820 K (EXTRAPOLATED). Turbulence and spark-kernel efficiency not modelled.",
        "inputs_bias": "Module 09 nominal over-predicts evaporation vs CFD (1.5-2.5x at A1); cfd_matched variant is a sensitivity bound. "
                       "Module 09 wall-impinged liquid (58-97 %) is NOT in the charge here (film is Module 13's job).",
        "search_cap": "a max-SMD value equal to 1000 um (D_MAX_SEARCH_m) means no limit was found up to 1 mm.",
    }
    payload = dict(module=MODULE, version=VERSION, labels=labels, params=M.params_dict(), cases=cases,
                   recommended_max_smd_um=rec, misfire_verdicts=misfire)
    (out / "spray_flame.json").write_text(json.dumps(payload, indent=1, allow_nan=False, default=float) + "\n")
    assumptions = {
        "flame_speed_source": {"value": "Module 02 flame_speed_fits.json S_L(w) at 400 K, 1 atm, phi 1", "path": str(FIT_PATH.relative_to(ROOT))},
        "SL_state_scaling": {"value": "Metghalchi & Keck (1982) S ~ T^2.18 p^-0.16 at phi = 1", "source": "Combust. Flame 48:191"},
        "spray_flame_speed": {"value": "Ballal & Lefebvre (1981) additive evaporation + reaction time", "source": "18th Symp. Combust. 321-328"},
        "vapour_flame_floor": {"value": "S_eff = max(S_BL, S_L(Omega*phi)), M-K methanol phi-parabola ratio", "rationale": "pre-vaporised mixture propagates independently when flammable"},
        "MIE": {"value": "cp rho dT_ad pi/6 d_q^3, d_q^2 = (1-Omega) rho_F D32^2/(rho_g phi ln(1+B)) + (10 alpha/S_L)^2",
                "source": "Ballal & Lefebvre (1979) Proc. R. Soc. A 364:277; (1975) Proc. R. Soc. A 344:217; Lefebvre (1989) Atomization and Sprays ch. 9"},
        "gas_properties": {"value": "Cantera rho, cp, HP-equilibrium T_ad of the fully vaporised charge; k of air (CoolProp) for alpha"},
        "liquid": {"value": "alcohol rho at 298 K (CoolProp); B = cp (T - T_sat(p)) / h_fg(p) (CoolProp saturation at spark p)"},
        "liquid_water": {"value": "heat sink Y_wl h_fg/cp evaporated in the preheat zone (upper bound), Zeldovich S ~ exp(-Ea/2RT_ad)",
                         "E_a_J_mol": M.DEF.E_A_J_MOL},
        "sweep_liquid_composition": {"value": "liquid at spark has the intake water/alcohol ratio (conservative; Module 09 finds water evaporates first)"},
        "sweep_state": {"value": "T at spark = mean of Module 09 nominal atomiser values per design point; p from Module 09"},
        "spark_energy": {"value": "50-100 mJ compared directly with MIE (spark-to-gas transfer efficiency not applied)"},
        "turbulence": {"value": "not modelled (quiescent correlations)"},
    }
    key = dict(n_cases=len(cases), n_design_rows=len(dprows), n_misfire_rows=n_mis, recommended_max_smd_um=rec,
               ch3oh_water_majority={a: v["nominal"] for a, v in cases.get("CH3OH/water_majority", {}).get("atomisers", {}).items()})
    io.write_summary(out, MODULE, VERSION, args.mode, assumptions, key,
                     {"tests": "tests/test_spray_flame.py", "status": labels["status"]}, time.perf_counter() - t0)
    print(json.dumps(dict(n_misfire_rows=n_mis, recommended=rec), indent=1, default=float))


if __name__ == "__main__":
    main()
