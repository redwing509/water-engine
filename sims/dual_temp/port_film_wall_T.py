"""Dual-temperature check of Module 11 bound (ii): does a hotter intake-port wall evaporate the Module 09 wall film?

STATUS: executed estimate only -- NOT verified by a second engine and NOT validated against experiment.
This is a first-order steady-state film budget, a stand-in until Module 13 (port film dynamics) exists.

Per bound-(ii) case (Module 09 design point x atomiser x variant), per cycle:
  deposit_s  = Module 11 film_strip film mass of species s (alcohol, water) [kg/cycle]
  capacity_s = film evaporation the port wall can sustain in one cycle [kg/cycle]
  f_film_evap = min(1, capacity/deposit) per species;  X_strip_max = 1 - f_film_evap (what is left to strip)
Bound (ii) misfire is still reachable only if X_strip_max >= Module 11's critical strip fraction x_crit(100 mJ).

Capacity, two limits, the smaller wins:
 (a) gas-side mass transfer (film below its bubble point): film at the wall temperature (thin film, wall-controlled:
     upper bound), Raoult's law at the deposited liquid mole fractions (ideal solution), Spalding B_M,
     m'' = rho_g h_m ln(1+B_M), h_m from Gilliland-Sherwood Sh = 0.023 Re^0.83 Sc^0.44, active only while
     the intake valve is open (duty = 230/720).
 (b) wall heat supply (any regime): q'' = h_film (T_wall - T_bubble or T_wet) capped at a critical heat flux,
     whole cycle; h_film and CHF are sensitivity parameters (nucleate boiling / thin-film evaporation order).
     If the deposited mixture's bubble point is above the wall temperature only (a) applies.
Wetted area: pi D_runner L_wet, L_wet in {0.02, 0.05, 0.10} m (sensitivity; bend deposition patch).
"""
import csv, json, math, sys
from pathlib import Path
import numpy as np
from CoolProp.CoolProp import PropsSI
from scipy.optimize import brentq

from sims.dual_temp.regimes import NORMAL, HOT

ROOT = Path(__file__).resolve().parents[2]
BOUND = ROOT / "results" / "11_spray_flame" / "bound_ii_film_strip" / "design_points.csv"
OUT = ROOT / "results" / "dual_temp" / "port_film_wall_T"
CP_NAME = {"CH3OH": "Methanol", "C2H5OH": "Ethanol", "H2O": "Water"}
MW = {"CH3OH": 0.03204, "C2H5OH": 0.04607, "H2O": 0.018015}
D_AIR_300 = {"CH3OH": 1.6e-5, "C2H5OH": 1.2e-5, "H2O": 2.5e-5}   # binary diffusivity in air at 300 K, 1 atm [m2/s]
RPM, P_PORT, D_RUN, U_RUN = 2000.0, 1.0e5, 0.035, 30.0           # Module 03 / Module 09 reference values
DUTY = 230.0 / 720.0
L_WET = (0.02, 0.05, 0.10)
H_FILM = (1.0e4, 3.0e4)          # W/m2K
CHF = 1.0e6                      # W/m2, Zuber-order for water at 1 bar (lower for alcohols -> optimistic)
WALLS = [("normal", NORMAL["port_wall_K"], 360.0), ("hot", HOT["port_wall_K"], 400.0),
         ("hot+heated_port", HOT["heated_port_wall_K"], 400.0)]

def psat(sp, T):
    Tc = PropsSI("Tcrit", CP_NAME[sp])
    return PropsSI("P", "T", min(T, Tc - 1), "Q", 0, CP_NAME[sp])

def hfg(sp, T):
    n = CP_NAME[sp]
    T = min(T, PropsSI("Tcrit", n) - 5)
    return PropsSI("H", "T", T, "Q", 1, n) - PropsSI("H", "T", T, "Q", 0, n)

def bubble_T(x, alc):
    f = lambda T: x[alc] * psat(alc, T) + x["H2O"] * psat("H2O", T) - P_PORT
    return brentq(f, 250.0, 600.0)

def capacity(m_a, m_w, alc, T_wall, T_gas, L_wet, h_film):
    """kg/cycle (alcohol, water) the wetted patch can evaporate; regime label."""
    A = math.pi * D_RUN * L_wet
    t_cyc = 120.0 / RPM
    n_a, n_w = m_a / MW[alc], m_w / MW["H2O"]
    if n_a + n_w <= 0:
        return 0.0, 0.0, "no_film"
    x = {alc: n_a / (n_a + n_w), "H2O": n_w / (n_a + n_w)}
    Tb = bubble_T(x, alc)
    wa, ww = m_a / (m_a + m_w), m_w / (m_a + m_w)
    L_mix = wa * hfg(alc, min(T_wall, Tb)) + ww * hfg("H2O", min(T_wall, Tb))
    # (b) heat supply: superheat over bubble point if boiling, else drive to wet-bulb ~ keep 5 K minimum
    dT = max(T_wall - Tb, 5.0)
    q = min(CHF, h_film * dT)
    m_heat = q * A * t_cyc / L_mix
    if T_wall >= Tb:
        regime, m_tot = "boiling (heat-limited)", m_heat
    else:
        T_f = 0.5 * (T_wall + T_gas)
        rho = P_PORT / (287.0 * T_f)
        mu = PropsSI("V", "T", T_f, "P", P_PORT, "Air")
        p_a, p_w = x[alc] * psat(alc, T_wall), x["H2O"] * psat("H2O", T_wall)
        Mv = (p_a * MW[alc] + p_w * MW["H2O"]) / (p_a + p_w)
        Xv = (p_a + p_w) / P_PORT
        Ys = Xv * Mv / (Xv * Mv + (1 - Xv) * 0.02897)
        B = Ys / (1.0 - Ys)
        D = (wa * D_AIR_300[alc] + ww * D_AIR_300["H2O"]) * (T_f / 300.0) ** 1.75
        Re, Sc = rho * U_RUN * D_RUN / mu, mu / (rho * D)
        h_m = 0.023 * Re ** 0.83 * Sc ** 0.44 * D / D_RUN
        m_gas = rho * h_m * math.log1p(B) * A * t_cyc * DUTY
        regime = "gas-side mass transfer" if m_gas < m_heat else "heat-limited"
        m_tot = min(m_gas, m_heat)
    # split: deposited composition (methanol-first preference ignored -> conservative for the alcohol)
    return m_tot * wa, m_tot * ww, regime

def main():
    rows_in = list(csv.DictReader(BOUND.open()))
    import importlib
    FS = importlib.import_module("sims.11_spray_flame.film_strip")
    R = importlib.import_module("sims.11_spray_flame.run")
    fits, sas, dp = R.load_inputs()
    ep = json.loads(FS.EP_PATH.read_text())
    film = {}
    for key, c in sas["cases"].items():
        ms = R.masses(dp["per_fuel"][c["fuel"]][c["point"]], c["fuel"])
        for an, a in c["atomisers"].items():
            for v in R.VARIANTS:
                film[(key, an, v)] = (c["fuel"], FS.film_masses(a[v], ep[f"{key}/{an}/{v}"], ms))
    xcrit = {}
    for r in rows_in:
        k = (r["case"], r["atomiser"], r["variant"])
        xc = r["x_strip_for_MIE_100mJ"]
        xcrit.setdefault(k, {})[r["SMD_um"]] = None if xc == "never" else float(xc)
    out = []
    for k, (alc, fm) in film.items():
        for wname, Tw, Tg in WALLS:
            for L in L_WET:
                for h in H_FILM:
                    ca, cw, reg = capacity(fm["film_alcohol_kg"], fm["film_water_kg"], alc, Tw, Tg, L, h)
                    fa = 1.0 if fm["film_alcohol_kg"] <= 0 else min(1.0, ca / fm["film_alcohol_kg"])
                    fw = 1.0 if fm["film_water_kg"] <= 0 else min(1.0, cw / fm["film_water_kg"])
                    dep = fm["film_alcohol_kg"] + fm["film_water_kg"]
                    f_tot = 1.0 if dep <= 0 else (fa * fm["film_alcohol_kg"] + fw * fm["film_water_kg"]) / dep
                    xmax = 1.0 - f_tot
                    row = dict(case=k[0], atomiser=k[1], variant=k[2], fuel=alc, regime=wname, port_wall_K=Tw,
                               plenum_K=Tg, L_wet_m=L, h_film_W_m2K=h, film_deposit_mg=dep * 1e6,
                               film_capacity_mg=(ca + cw) * 1e6, film_evap_frac=f_tot, X_strip_max=xmax,
                               evap_regime=reg)
                    for smd, xc in sorted(xcrit[k].items()):
                        row[f"misfire_reachable_SMD{float(smd):g}"] = (xc is not None and xmax >= xc)
                    out.append(row)
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "port_film_wall_T.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    summ = {}
    for r in out:
        s = summ.setdefault(f"{r['regime']} (T_port_wall {r['port_wall_K']:.0f} K)", dict(n=0, film_evap_frac=[1, 0],
                     film_deposit_mg=[1e9, 0], film_capacity_mg=[1e9, 0], misfire_reachable={}))
        s["n"] += 1
        for kk in ("film_evap_frac", "film_deposit_mg", "film_capacity_mg"):
            s[kk] = [min(s[kk][0], r[kk]), max(s[kk][1], r[kk])]
        for kk, v in r.items():
            if kk.startswith("misfire_reachable_"):
                s["misfire_reachable"].setdefault(kk[18:], [0, 0])
                s["misfire_reachable"][kk[18:]][0] += int(v); s["misfire_reachable"][kk[18:]][1] += 1
    # nominal-parameter view (L_wet 0.05 m, h 3e4)
    nom = {}
    for r in out:
        if r["L_wet_m"] == 0.05 and r["h_film_W_m2K"] == 3.0e4:
            e = nom.setdefault(r["regime"], dict(cases=0, misfire_reachable_SMD350=0, mean_film_evap_frac=0.0))
            e["cases"] += 1; e["misfire_reachable_SMD350"] += int(r.get("misfire_reachable_SMD350", False))
            e["mean_film_evap_frac"] += r["film_evap_frac"]
    for e in nom.values():
        e["mean_film_evap_frac"] /= e["cases"]
    json.dump(dict(status="executed estimate; not verified (no 2nd engine), not validated",
                   ranges_over_sensitivity=summ, nominal_Lwet_0p05_h_3e4=nom,
                   walls=[dict(regime=a, port_wall_K=b, plenum_K=c) for a, b, c in WALLS],
                   rpm=RPM, p_port_Pa=P_PORT, D_runner_m=D_RUN, U_runner_m_s=U_RUN, duty=DUTY, CHF_W_m2=CHF),
              (OUT / "summary.json").open("w"), indent=2)
    print(json.dumps(nom, indent=1))
    return 0

if __name__ == "__main__":
    sys.exit(main())
