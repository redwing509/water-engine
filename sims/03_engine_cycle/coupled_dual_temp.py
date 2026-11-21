"""Item B: coupled retained-liquid / wall-film design-point runs at both temperatures.

Run:  python -m sims.03_engine_cycle.coupled_dual_temp [--workers 4]

For CH3OH and C2H5OH, at the Module 03 design points (best_dry, best_overall,
water_majority) x atomiser (carb_venturi, ultrasonic_120kHz) x Module 09
variant (nominal, cfd_matched) x wall-film bound x regime:

  bound (ii) "film-carried": all water not evaporated by spark (airborne
      droplets + wall film, Module 09) is liquid at spark: excluded from the
      unburned gas, vaporised into the burned zone at the burn rate.
      Module 11 caveat: film entering as 200-500 um drops makes nearly every
      case misfire (wme1-spray11 220e3ac) - not modelled by this cycle.
  bound (ii) is also the airborne-liquid treatment in bound (i).
  bound (i) "port-evaporated": the wall film evaporates off the port wall
      before IVC, capped by (a) the Module 06 exhaust-heat surplus after the
      air + fuel intake heating it already pays for (Module 06 heat_balance
      definition, fuel-specific latent heat), (b) the port-wall film
      capacity (wme1-hiT results/dual_temp/port_film_wall_T, L_wet 0.05 m,
      h_film 3e4 W/m2K) and (c) saturation at T_intake. Excess -> bound (ii).
      Fixed point on the EVO state (<= 4 iterations, |df| < 0.002).

Regimes (wme1-hiT sims/dual_temp/regimes.py; docs/DUAL_TEMPERATURE_RULE.md,
PR #5; sources MAHLE/VW SSP 222, SAE 960271, Heywood 1988 ch. 12):
  normal: coolant 363.15 K, chamber wall 450 K, port wall 363.15 K,
          T_intake = design point value (320 / 360 K; Module 09 keyed there)
  hot:    coolant 388.15 K, chamber wall 520 K, port wall 388.15 K,
          T_intake 400 K (Module 09 fractions of the design point reused:
          Module 09 not rerun at 400 K - conservative for evaporation)

Status: executed (and cross-checked by M03-CRN where stated); NOT validated
against experiment.
"""
import argparse
import csv
import json
import math
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from multiprocessing import get_context
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "results" / "03_engine_cycle" / "coupled"
FILM_CSV = REPO / "results" / "03_engine_cycle" / "inputs" / "port_film_wall_T.csv"
FUELS = ("CH3OH", "C2H5OH")
POINTS = ("best_dry", "best_overall", "water_majority")
ATOMISERS = ("carb_venturi", "ultrasonic_120kHz")
VARIANTS = ("nominal", "cfd_matched")
REGIMES = {
    "normal": dict(coolant_K=363.15, chamber_wall_K=450.0, port_wall_K=363.15, T_intake_K=None,
                   dry_T_intake=(320.0, 360.0)),
    "hot": dict(coolant_K=388.15, chamber_wall_K=520.0, port_wall_K=388.15, T_intake_K=400.0,
                dry_T_intake=(400.0,)),
}
HX_EFF, T_TANK, T_EXH_MIN = 0.60, 300.0, 360.0   # Module 06 DEFAULTS
FILM_L_WET, FILM_H = 0.05, 30000.0
M11_CAVEAT = "M11: film entering as 200-500 um drops -> nearly every case misfires (not in this cycle)"
KEEP = ("status reason fuel CR w T_intake_K gross_indicated_efficiency IMEP_Pa peak_pressure_Pa "
        "peak_pressure_angle_deg peak_temperature_K peak_burned_temperature_K peak_flame_temperature_K "
        "low_flame_temperature ca50_used_deg burn_10_90_deg S_L_m_s knock knock_limited "
        "knock_integral_at_xb90 wall_heat_J fuel_energy_J NO_mol_per_J_fuel EVO_T_K T_IVC_K "
        "f_evap_intake_effective intake_saturation_limited energy_closure_error_fraction "
        "integrator_identity_error_fraction liquid_sink_J evaporated_fraction_spark liquid_fraction_spark "
        "liquid_freeze_deg port_evap_fraction port_wall_heat_J port_evap_saturation_limited "
        "fuel_mass_kg air_mass_kg residual_mass_kg water_mass_kg released_energy_J").split()


def _load():
    import importlib
    import sys
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    m = importlib.import_module("sims.03_engine_cycle.run")
    ep = importlib.import_module("sims.03_engine_cycle.evap_profile")
    return m, ep


_FITS = {}


def _fits(m):
    if not _FITS:
        ign, fl, prov = m.read_fits(REPO / "results" / "02_flame_chem", "full")
        _FITS.update(ign=ign, fl=fl)
    return _FITS["ign"], _FITS["fl"]


def regime_par(m, regime):
    return replace(m.DEFAULTS, wall_T_K=REGIMES[regime]["chamber_wall_K"])


def design_points(ep):
    out = {}
    for (fuel, cr, w, T), name in ep._POINT_INDEX.items():
        out[(fuel, name)] = (int(cr), float(w), float(T))
    return out


def film_capacity_kg(fuel, point, atomiser, variant, regime):
    with open(FILM_CSV) as fh:
        for r in csv.DictReader(fh):
            if (r["case"] == f"{fuel}/{point}" and r["atomiser"] == atomiser and r["variant"] == variant
                    and r["regime"] == regime and abs(float(r["L_wet_m"]) - FILM_L_WET) < 1e-12
                    and abs(float(r["h_film_W_m2K"]) - FILM_H) < 1e-6):
                return float(r["film_capacity_mg"]) * 1e-6
    raise KeyError((fuel, point, atomiser, variant, regime))


def heat_budget(m, fuel, point_row, evo):
    """Per-cycle Module 06 exhaust-heat budget [J] (heat_balance definition).

    recovered = 0.6 * (m_air + m_fuel + m_water) * [h(T_EVO) - h(360 K)] (frozen EVO composition)
    need      = air 300 K -> T_intake + fuel latent(300 K) + fuel vapour sensible 300 K -> T_intake
    water_per_frac = m_water * [h_fg(300 K) + vapour sensible 300 K -> T_intake]
    """
    import CoolProp.CoolProp as CP
    ph = m.phases(fuel)
    g = ph.gas
    T1 = float(point_row["T_intake_K"])
    ma, mf, mw = (float(point_row[k]) for k in ("air_mass_kg", "fuel_mass_kg", "water_mass_kg"))

    def dh(species, t0, t1):
        h = lambda T: float(ph.species_h(T)[g.species_index(m.fuels.species_name(g, species))])
        return h(t1) - h(t0)
    yo2 = 32.0 / (32.0 + 3.76 * 28.0134)
    air = ma * (yo2 * dh("O2", T_TANK, T1) + (1 - yo2) * dh("N2", T_TANK, T1))
    cp_name = {"CH3OH": "Methanol", "C2H5OH": "Ethanol"}[fuel]
    hfg = lambda f: CP.PropsSI("H", "T", T_TANK, "Q", 1, f) - CP.PropsSI("H", "T", T_TANK, "Q", 0, f)
    fuel_h = mf * (hfg(cp_name) + dh(fuel, T_TANK, T1))
    water_per_frac = mw * (hfg("Water") + dh("H2O", T_TANK, T1))
    names = g.species_names
    Y = [0.0] * len(names)
    for s, y in evo["composition"].items():
        Y[names.index(s)] = y
    g.TPY = evo["T_K"], 1e5, Y
    h1 = g.enthalpy_mass
    g.TPY = T_EXH_MIN, 1e5, Y
    h0 = g.enthalpy_mass
    rec = HX_EFF * (ma + mf + mw) * max(0.0, h1 - h0)
    ph._T = None  # phases cache shares the gas object
    return dict(recovered_J=rec, need_air_J=air, need_fuel_J=fuel_h, surplus_J=rec - air - fuel_h,
                water_per_frac_J=water_per_frac)


def _row(base, res, **extra):
    p = res["point"]
    r = dict(base)
    r.update({k: p.get(k) for k in KEEP})
    r.update(extra)
    return r


def task(spec):
    m, ep = _load()
    ign, fl = _fits(m)
    kind, fuel, regime = spec["kind"], spec["fuel"], spec["regime"]
    par = regime_par(m, regime)
    cr, w, T = spec["CR"], spec["w"], spec["T_intake_K"]
    base = dict(kind=kind, regime=regime, point=spec.get("point", ""), atomiser=spec.get("atomiser", ""),
                variant=spec.get("variant", ""), bound=spec.get("bound", ""), chamber_wall_K=par.wall_T_K,
                port_wall_K=REGIMES[regime]["port_wall_K"], coolant_K=REGIMES[regime]["coolant_K"])
    t0 = time.time()
    if kind in ("dry", "legacy"):
        res = m.run_point(fuel, cr, w, T, ign[fuel], fl[fuel], par, "full")
        return [_row(base, res, runtime_s=time.time() - t0)]
    prof = ep.PointProfile(spec["atomiser"], spec["variant"], spec["point"])
    f_ivc = prof.ivc_fraction(fuel)
    spark_deg, (f_ev, f_air, f_wall) = prof.spark_target(fuel, cr, w, T)
    m09 = dict(m09_spark_deg=spark_deg, m09_frac_ivc=f_ivc, m09_frac_evap_spark=f_ev,
               m09_frac_airborne_spark=f_air, m09_frac_wall_film_spark=f_wall)
    coup = dict(liquid_sink=True, intake_cap_frac=f_ivc)
    rows = []
    res = m.run_point(fuel, cr, w, T, ign[fuel], fl[fuel], par, "full", evap_profile=prof, coupling=coup)
    rows.append(_row(dict(base, bound="ii"), res, iteration=0, caveat=M11_CAVEAT, runtime_s=time.time() - t0,
                     **m09))
    if res["evo"] is None:
        return rows
    cap = film_capacity_kg(fuel, spec["point"], spec["atomiser"], spec["variant"], regime)
    f_pe, it, hist = None, 0, []
    evo, prow = res["evo"], res["point"]
    while it < 4:
        it += 1
        b = heat_budget(m, fuel, prow, evo)
        mw = float(prow["water_mass_kg"])
        f_budget = max(0.0, b["surplus_J"]) / b["water_per_frac_J"] if b["water_per_frac_J"] > 0 else 0.0
        f_cap = cap / mw
        f_new = max(0.0, min(f_wall, f_budget, f_cap))
        limit = min((("wall_film", f_wall), ("module06_heat", f_budget), ("port_wall_capacity", f_cap)),
                    key=lambda kv: kv[1])[0]
        hist.append(dict(iteration=it, f_budget=f_budget, f_cap=f_cap, f_port=f_new, **b))
        if f_pe is not None and abs(f_new - f_pe) < 0.002:
            break
        f_pe = f_new
        r1 = m.run_point(fuel, cr, w, T, ign[fuel], fl[fuel], par, "full", evap_profile=prof,
                         coupling=dict(coup, port_evap_frac=f_pe))
        if r1["evo"] is None:
            rows.append(_row(dict(base, bound="i"), r1, iteration=it, runtime_s=time.time() - t0, **m09))
            return rows
        evo, prow, res1 = r1["evo"], r1["point"], r1
    final = hist[-1]
    rows.append(_row(dict(base, bound="i"), res1, iteration=it, port_evap_request=f_pe,
                     port_limit=limit, film_capacity_mg=cap * 1e6, budget_recovered_J=final["recovered_J"],
                     budget_need_air_J=final["need_air_J"], budget_need_fuel_J=final["need_fuel_J"],
                     budget_surplus_J=final["surplus_J"], budget_water_per_frac_J=final["water_per_frac_J"],
                     f_budget=final["f_budget"], f_cap=final["f_cap"], budget_history=json.dumps(hist),
                     caveat=("excess film -> bound (ii) liquid; " + M11_CAVEAT) if f_pe < f_wall - 1e-9 else "",
                     runtime_s=time.time() - t0, **m09))
    return rows


def module06_check():
    """Reproduce Module 06's CH3OH CR24/w0.6/T360 budget (4.61 kW recovered, 2.02 kW upstream need)."""
    m, ep = _load()
    ign, fl = _fits(m)
    res = m.run_point("CH3OH", 24, 0.6, 360.0, ign["CH3OH"], fl["CH3OH"], m.DEFAULTS, "full")
    b = heat_budget(m, "CH3OH", res["point"], res["evo"])
    cps = m.DEFAULTS.rpm / 120.0
    return dict(EVO_T_K=res["evo"]["T_K"], recovered_kW=b["recovered_J"] * cps / 1e3,
                need_kW=(b["need_air_J"] + b["need_fuel_J"]) * cps / 1e3,
                module06_recovered_kW=4.61, module06_need_kW=2.02)


def specs():
    _, ep = _load()
    dp = design_points(ep)
    out = []
    for regime, R in REGIMES.items():
        for fuel in FUELS:
            for cr in range(9, 25):
                for T in R["dry_T_intake"]:
                    out.append(dict(kind="dry", fuel=fuel, regime=regime, CR=cr, w=0.0, T_intake_K=T))
            for point in POINTS:
                cr, w, T = dp[(fuel, point)]
                T = R["T_intake_K"] or T
                if w == 0:
                    continue
                out.append(dict(kind="legacy", fuel=fuel, regime=regime, point=point, CR=cr, w=w, T_intake_K=T))
                if not any(s["kind"] == "dry" and s["fuel"] == fuel and s["regime"] == regime and s["CR"] == cr
                           and s["T_intake_K"] == T for s in out):
                    out.append(dict(kind="dry", fuel=fuel, regime=regime, CR=cr, w=0.0, T_intake_K=T))
                for a in ATOMISERS:
                    for v in VARIANTS:
                        out.append(dict(kind="coupled", fuel=fuel, regime=regime, point=point, CR=cr, w=w,
                                        T_intake_K=T, atomiser=a, variant=v))
    # longest first
    out.sort(key=lambda s: {"coupled": 0, "legacy": 1, "dry": 2}[s["kind"]])
    return out


def main(workers=4):
    OUT.mkdir(parents=True, exist_ok=True)
    chk = module06_check()
    (OUT / "module06_budget_check.json").write_text(json.dumps(chk, indent=1))
    print("module06 check", chk, flush=True)
    sp = specs()
    rows = []
    with ProcessPoolExecutor(max_workers=workers, mp_context=get_context("spawn")) as ex:
        for i, rr in enumerate(ex.map(task, sp, chunksize=1)):
            rows.extend(rr)
            print(f"{i + 1}/{len(sp)} {sp[i]['kind']} {sp[i]['fuel']} {sp[i]['regime']} "
                  f"{sp[i].get('point', '')} {sp[i].get('atomiser', '')} {sp[i].get('variant', '')} "
                  + " ".join(f"{r.get('bound', '')}:{(r.get('gross_indicated_efficiency') or 0):.4f}"
                             for r in rr), flush=True)
    cols = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    with open(OUT / "coupled_points.csv", "w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=cols)
        wtr.writeheader()
        wtr.writerows(rows)
    print("wrote", OUT / "coupled_points.csv", len(rows), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    main(min(4, ap.parse_args().workers))
