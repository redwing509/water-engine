"""Shared Water Engine cost metric (James, 2026-10-25 06:53 PDT).

Rule: a water result is judged on cost too. If adding water keeps power (IMEP; horsepower at fixed speed and
displacement) the same or better, the fuel it saves per unit work is a cost-per-mile (MPG) gain.

Definitions (checked against sims/03_engine_cycle/run.py, Charge.__init__ and the result block):
* w = m_water / (m_water + m_fuel) (mass), so water per kg fuel is r = w / (1 - w).
* The charge is built at fixed equivalence ratio on the FUEL (phi = 1): water is ADDED to a stoichiometric
  fuel-air charge, it does not replace fuel inside the stoichiometric mixture. At fixed p_IVC the trapped
  mass changes (evaporative cooling raises it, vapour displaces air) and fuel_mass_kg follows.
* gross_indicated_efficiency eta = W_ind(IVC-EVO) / (m_fuel * LHV_fuel). Water has zero heating value and is
  NOT in the denominator. So fuel energy per unit work = 1/eta and fuel mass (and fuel volume) per unit
  work = 1/(eta * LHV): % change vs dry = eta_dry/eta - 1 (same fuel, same LHV, same density).
* The liquid that has to be carried (fuel + water) per unit work is (1 + r)/(eta*LHV) kg - reported too.
* IMEP_Pa = W_ind / V_displacement (Module 03). M03-CRN reports only efficiency at the same fuel mass, so its
  IMEP is derived: IMEP_CRN = IMEP_M03 * eta_CRN / eta_M03 (same m_fuel, same displacement, same LHV).
* Brake power is NOT modelled (no friction / pumping model). At equal speed and FMEP, brake power changes
  by the same absolute amount as IMEP (larger in %), so the IMEP sign test also holds for brake power.
* Cost per kWh of indicated work: C = (p_fuel + p_water * r) / (eta * LHV / 3.6e6), with p in USD/kg.
  % vs dry = (1 + r * p_water/p_fuel) * eta_dry/eta - 1; independent of the vehicle assumption.
* Break-even water price: the water price at which the cost change is exactly zero,
  p_w* = p_fuel * (eta/eta_dry - 1) / r (reported in USD per US gallon of water; negative = never pays).
* Water price: headline = James's test-case cost 0.10 USD/gal (2026-10-25 07:32 PDT); 0 USD/gal (free tap water,
  paid via the utility bill - James 07:31 PDT) is the secondary comparison; retail distilled is a footnote.
* Per mile: a fixed reference vehicle needing WORK_KWH_PER_MILE of indicated work per mile (documented
  assumption below). MPG(fuel gallons only) and cost/mile scale with it; their % changes do not.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRICES_FILE = HERE / "prices_20261025.json"
US_GAL_M3 = 3.785411784e-3
LB_KG = 0.45359237

# LHV (J/kg, registered phase, H2O(g) products, 298.15 K) and liquid density (kg/m3) from sims.common.fuels
# (+ sims.track_b.fuels_b.register()) at commit 041a10e; test_cost checks them against the live functions.
FUEL_PROPS = {
    "PRF87": dict(lhv=44.3701694e6, rho=690.288),
    "PRF91": dict(lhv=44.3617566e6, rho=690.784),
    "PRF97": dict(lhv=44.3491600e6, rho=691.528),
    "E10": dict(lhv=42.3848046e6, rho=700.6356),
    "E85": dict(lhv=29.1606001e6, rho=774.5226),
    "CH3OH": dict(lhv=19.9306581e6, rho=786.3267),
    "C2H5OH": dict(lhv=26.8029399e6, rho=785.1333),
    "CH4": dict(lhv=50.0253959e6, rho=None),
}
WATER_RHO = 998.2  # kg/m3, 20 C

# Reference vehicle (assumption, stated): 0.40 kWh of INDICATED work per mile. Derivation: a 30 mpg
# gasoline car uses 33.7 kWh/gal (EPA MPGe convention) / 30 = 1.12 kWh fuel per mile; at a typical
# drive-cycle indicated efficiency of ~0.35 that is ~0.39 kWh indicated work per mile. Only absolute
# $/mile and MPG depend on it; every % change is independent of it.
WORK_KWH_PER_MILE = 0.40

# Tolerances ("equal within noise"): the Track B efficiency noise level is 3.3e-5 absolute (James 19:01 PDT
# rule) = ~1e-4 relative at eta 0.33-0.45. IMEP at fixed fuel mass inherits the same relative noise.
POWER_TOL_REL = 1.0e-4
COST_TOL_REL = 1.0e-4


def load_prices(path=PRICES_FILE):
    return json.loads(Path(path).read_text())


# Water price cases (prices file 'water_cases'): 'headline' = James's test-case cost 0.10 USD/gal (default,
# 2026-10-25 07:32 PDT); 'free' = 0 USD/gal (07:31 PDT: water is paid through the utility bill, no extra cost to
# fill a tank); 'retail_sensitivity' = retail distilled water (footnote only).
HEADLINE_WATER = "headline"


def usd_per_kg(fuel, prices=None, water=HEADLINE_WATER):
    """Price of the fuel (or 'water', for the given water case) in USD/kg, from the dated prices file."""
    P = prices or load_prices()
    if fuel == "water":
        p = P["prices"][P["water_cases"][water]]
        return p["usd"] / (US_GAL_M3 * WATER_RHO)
    key = P["fuel_to_price"][fuel]
    p = P["prices"][key]
    if p["unit"] == "USD/US gal":
        return p["usd"] / (US_GAL_M3 * FUEL_PROPS[fuel]["rho"])
    if p["unit"] == "USD/metric ton":
        return p["usd"] / 1000.0
    if p["unit"] == "USD/GGE":
        return p["usd"] / (p["gge_lb"] * LB_KG)
    raise ValueError(p["unit"])


def water_per_fuel(row):
    """r = m_water/m_fuel; from the saved masses when present (checked against w), else from w."""
    w = float(row.get("w") or 0.0)
    r_w = w / (1.0 - w)
    mf, mw = row.get("fuel_mass_kg"), row.get("water_mass_kg")
    if mf and mw is not None:
        r = mw / mf
        if not math.isclose(r, r_w, rel_tol=1e-6, abs_tol=1e-12):
            raise ValueError(f"water/fuel mass {r} inconsistent with w={w}")
        return r
    return r_w


def cost_per_kwh(fuel, eta, r, prices=None, water=HEADLINE_WATER):
    """USD per kWh of indicated work (fuel + water at the given water price case)."""
    pf = usd_per_kg(fuel, prices)
    pw = usd_per_kg("water", prices, water)
    return (pf + pw * r) / (eta * FUEL_PROPS[fuel]["lhv"] / 3.6e6)


def mpg(fuel, eta):
    """Miles per US gallon of FUEL (water not counted) for the reference vehicle; None for gaseous fuel."""
    rho = FUEL_PROPS[fuel]["rho"]
    if rho is None:
        return None
    return eta * FUEL_PROPS[fuel]["lhv"] * rho * US_GAL_M3 / 3.6e6 / WORK_KWH_PER_MILE


def _engine(row, dry, eng):
    """(eta, IMEP_Pa, eta_dry, IMEP_dry) for engine 'm03' or 'crn'; None if not available."""
    e, ed = row.get("gross_indicated_efficiency"), dry.get("gross_indicated_efficiency")
    p, pd = row.get("IMEP_Pa"), dry.get("IMEP_Pa")
    if eng == "m03":
        return (e, p, ed, pd) if None not in (e, p, ed, pd) else None
    c, cd = row.get("crn_efficiency"), dry.get("crn_efficiency")
    if None in (e, p, ed, pd, c, cd) or row.get("crn_status") not in (None, "ok") or dry.get("crn_status") not in (None, "ok"):
        return None
    return (c, p * c / e, cd, pd * cd / ed)


def compare(row, dry, prices=None, water=HEADLINE_WATER):
    """Cost metric of one result vs its fuel's dry baseline (same fuel, same regime). Both engines.
    cost_* = the selected water case (default: headline 0.10 USD/gal); *_water_free_pct = 0 USD/gal;
    *_retail_water_pct = retail distilled (footnote sensitivity)."""
    fuel = row["fuel"]
    if dry["fuel"] != fuel:
        raise ValueError("dry baseline must be the same fuel")
    r = water_per_fuel(row)
    pf, pw = usd_per_kg(fuel, prices), usd_per_kg("water", prices, water)
    out = dict(fuel=fuel, w=float(row.get("w") or 0.0), water_per_fuel=r, price_fuel_usd_kg=pf, water_case=water,
               price_water_usd_kg=pw, water_to_fuel_price_ratio=pw / pf)
    for eng in ("m03", "crn"):
        v = _engine(row, dry, eng)
        if v is None:
            out[eng] = None
            continue
        eta, imep, eta_d, imep_d = v
        fuel_rel = eta_d / eta - 1.0
        c, cd = cost_per_kwh(fuel, eta, r, prices, water), cost_per_kwh(fuel, eta_d, 0.0, prices, water)
        cf = cost_per_kwh(fuel, eta, r, prices, "free")
        cr = cost_per_kwh(fuel, eta, r, prices, "retail_sensitivity")
        dp = imep / imep_d - 1.0
        dc = c / cd - 1.0
        power_ok = dp >= -POWER_TOL_REL
        out[eng] = dict(
            eta=eta, eta_dry=eta_d, d_eta_pp=100 * (eta - eta_d), imep_Pa=imep, imep_dry_Pa=imep_d,
            power_change_pct=100 * dp, power_drop=not power_ok,
            fuel_energy_per_work_pct=100 * fuel_rel, fuel_mass_per_work_pct=100 * fuel_rel,
            fuel_volume_per_work_pct=100 * fuel_rel,
            liquid_mass_per_work_pct=100 * ((1 + r) * eta_d / eta - 1.0),
            cost_usd_per_kwh=c, cost_usd_per_kwh_dry=cd, cost_per_kwh_pct=100 * dc,
            cost_per_mile_usd=c * WORK_KWH_PER_MILE, cost_per_mile_dry_usd=cd * WORK_KWH_PER_MILE,
            cost_per_mile_pct=100 * dc, cost_per_mile_water_free_pct=100 * (cf / cd - 1.0),
            cost_per_mile_retail_water_pct=100 * (cr / cd - 1.0),
            mpg_fuel=mpg(fuel, eta), mpg_fuel_dry=mpg(fuel, eta_d),
            mpg_pct=100 * (eta / eta_d - 1.0),
            breakeven_water_usd_per_gal=(pf * (eta / eta_d - 1.0) / r * US_GAL_M3 * WATER_RHO) if r > 0 else None,
            cost_gain=bool(power_ok and dc < -COST_TOL_REL))
    engines = [out[e] for e in ("m03", "crn") if out[e]]
    out["engines"] = len(engines)
    out["cost_gain_all_engines"] = bool(engines) and all(e["cost_gain"] for e in engines)
    out["power_ok_all_engines"] = bool(engines) and all(not e["power_drop"] for e in engines)
    return out


def verdict(c):
    if not c["engines"]:
        return "no data"
    tag = "" if c["engines"] == 2 else " (1 engine)"
    if c["cost_gain_all_engines"]:
        return "COST GAIN" + tag
    if not c["power_ok_all_engines"]:
        return "power loss" + tag
    if all((c[e] or {}).get("cost_per_mile_water_free_pct", 1) < -100 * COST_TOL_REL for e in ("m03", "crn") if c[e]):
        return "fuel saved, but water cost eats it" + tag
    return "no cost gain" + tag


def best_cost(rows, dry, prices=None, water=HEADLINE_WATER):
    """Lowest M03 cost per mile among rows with equal-or-better power in every engine the dry baseline has (a row
    missing an engine the baseline has, e.g. an M03-CRN integrator failure, is not a candidate). The dry point is
    always a candidate, so 'w = 0' means water never pays. Returns (row, compare)."""
    best = (dry, compare(dry, dry, prices, water))
    need = best[1]["engines"]
    for r in rows:
        c = compare(r, dry, prices, water)
        if not c["m03"] or c["engines"] < need or not c["power_ok_all_engines"]:
            continue
        if c["m03"]["cost_per_mile_pct"] < best[1]["m03"]["cost_per_mile_pct"]:
            best = (r, c)
    return best


def best_efficiency(rows, dry):
    el = [r for r in rows if r.get("gross_indicated_efficiency") is not None] + [dry]
    return max(el, key=lambda r: r["gross_indicated_efficiency"])
