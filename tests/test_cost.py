"""Tests for the shared Water Engine cost metric (sims/cost)."""
import warnings
import math

import pytest

from sims.cost import cost as C


def row(fuel="PRF87", w=0.0, eta=0.40, imep=1.0e6, crn=None, mf=1.0e-5):
    r = dict(fuel=fuel, w=w, gross_indicated_efficiency=eta, IMEP_Pa=imep, fuel_mass_kg=mf,
             water_mass_kg=mf * w / (1 - w), crn_status="ok")
    if crn is not None:
        r["crn_efficiency"] = crn
    return r


def test_no_water_is_zero():
    d = row(crn=0.39)
    c = C.compare(d, d)
    for e in ("m03", "crn"):
        for k in ("power_change_pct", "fuel_volume_per_work_pct", "cost_per_kwh_pct", "cost_per_mile_pct",
                  "cost_per_mile_water_free_pct", "d_eta_pp", "mpg_pct"):
            assert c[e][k] == pytest.approx(0.0, abs=1e-12), (e, k)
        assert not c[e]["cost_gain"] and not c[e]["power_drop"]
    assert C.verdict(c) == "no cost gain"


def test_fuel_per_work_definition():
    d, r = row(eta=0.40), row(w=0.05, eta=0.42)
    c = C.compare(r, d)["m03"]
    assert c["fuel_volume_per_work_pct"] == pytest.approx(100 * (0.40 / 0.42 - 1))
    assert c["fuel_energy_per_work_pct"] == c["fuel_mass_per_work_pct"] == c["fuel_volume_per_work_pct"]
    assert c["liquid_mass_per_work_pct"] == pytest.approx(100 * ((1 + 0.05 / 0.95) * 0.40 / 0.42 - 1))


def test_cost_formula_and_water_price():
    P = C.load_prices()
    d, r = row(eta=0.40), row(w=0.10, eta=0.41)
    c = C.compare(r, d, P)["m03"]
    ratio = C.usd_per_kg("water", P) / C.usd_per_kg("PRF87", P)
    assert c["cost_per_mile_pct"] == pytest.approx(100 * ((1 + ratio / 9) * 0.40 / 0.41 - 1))
    assert c["cost_per_mile_water_free_pct"] == pytest.approx(100 * (0.40 / 0.41 - 1))
    # break-even water price makes the cost change exactly zero
    pw = c["breakeven_water_usd_per_gal"] / (C.US_GAL_M3 * C.WATER_RHO)
    assert (C.usd_per_kg("PRF87", P) + pw / 9) / 0.41 == pytest.approx(C.usd_per_kg("PRF87", P) / 0.40)
    # absolute cost per kWh: fuel price / (eta * LHV in kWh/kg)
    assert c["cost_usd_per_kwh_dry"] == pytest.approx(C.usd_per_kg("PRF87", P) / (0.40 * C.FUEL_PROPS["PRF87"]["lhv"] / 3.6e6))
    assert c["cost_per_mile_dry_usd"] == pytest.approx(c["cost_usd_per_kwh_dry"] * C.WORK_KWH_PER_MILE)


def test_verdicts():
    d = row(eta=0.40, crn=0.39)
    gain = C.compare(row(w=0.001, eta=0.41, imep=1.02e6, crn=0.40), d)
    assert C.verdict(gain) == "COST GAIN"
    loss = C.compare(row(w=0.001, eta=0.41, imep=0.95e6, crn=0.40), d)
    assert C.verdict(loss) == "power loss" and loss["m03"]["power_drop"]
    eaten = C.compare(row(w=0.2, eta=0.401, imep=1.01e6, crn=0.391), d)
    assert C.verdict(eaten).startswith("fuel saved, but water cost eats it")
    one = C.compare(row(w=0.001, eta=0.41, imep=1.02e6), row(eta=0.40))
    assert one["crn"] is None and C.verdict(one) == "COST GAIN (1 engine)"
    # power equal within noise counts as equal
    eq = C.compare(row(w=0.001, eta=0.41, imep=1.0e6 * (1 - 0.5 * C.POWER_TOL_REL)), row(eta=0.40))
    assert not eq["m03"]["power_drop"]


def test_crn_imep_derived_at_same_fuel_mass():
    d, r = row(eta=0.40, imep=1.0e6, crn=0.38), row(w=0.01, eta=0.41, imep=1.03e6, crn=0.39)
    c = C.compare(r, d)["crn"]
    assert c["imep_Pa"] == pytest.approx(1.03e6 * 0.39 / 0.41)
    assert c["power_change_pct"] == pytest.approx(100 * ((1.03e6 * 0.39 / 0.41) / (1.0e6 * 0.38 / 0.40) - 1))


def test_best_cost_picks_cheapest_with_power():
    d = row(eta=0.40, crn=0.40)
    rows = [row(w=0.001, eta=0.402, crn=0.402), row(w=0.002, eta=0.405, imep=0.9e6, crn=0.405),
            row(w=0.003, eta=0.403, crn=0.403)]
    br, bc = C.best_cost(rows, d)
    assert br["w"] == 0.003
    assert C.best_cost([row(w=0.2, eta=0.401, crn=0.401)], d)[0] is d  # water never pays -> dry


def test_inconsistent_masses_rejected():
    r = row(w=0.1)
    r["water_mass_kg"] *= 2
    with pytest.raises(ValueError):
        C.water_per_fuel(r)
    with pytest.raises(ValueError):
        C.compare(row(fuel="PRF87"), row(fuel="E10"))


def test_prices_have_source_and_date():
    P = C.load_prices()
    for k, v in P["prices"].items():
        assert v["source"] and len(v["date"]) == 10 and v["usd"] >= 0, k
        if k.startswith("water_") and k != "water_distilled":
            assert v["source"].startswith("James") and v.get("url") is None, k  # owner decision, not a market quote
        else:
            assert v["url"].startswith("https://") and v["usd"] > 0, k
    for f in C.FUEL_PROPS:
        assert C.usd_per_kg(f, P) > 0
    assert C.usd_per_kg("CH3OH", P) == pytest.approx(1.45)
    assert C.usd_per_kg("CH4", P) == pytest.approx(3.10 / (5.660 * 0.45359237))
    # headline water = James's 0.10 USD/gal test case; free = 0; retail distilled = footnote sensitivity
    assert P["water_cases"]["headline"] == "water_test_case" and P["prices"]["water_test_case"]["usd"] == 0.10
    assert C.usd_per_kg("water", P) == pytest.approx(0.10 / 3.785411784 / 0.9982)
    assert C.usd_per_kg("water", P, "free") == 0.0
    assert C.usd_per_kg("water", P, "retail_sensitivity") == pytest.approx(1.54 / 3.785411784 / 0.9982)


def test_free_water_cost_equals_fuel_per_work_and_headline_between():
    d, r = row(eta=0.40, crn=0.39), row(w=0.05, eta=0.41, imep=1.03e6, crn=0.40)
    c = C.compare(r, d)
    for e in ("m03", "crn"):
        x = c[e]
        assert x["cost_per_mile_water_free_pct"] == pytest.approx(x["fuel_mass_per_work_pct"])
        assert x["cost_per_mile_water_free_pct"] < x["cost_per_mile_pct"] < x["cost_per_mile_retail_water_pct"]
    assert C.compare(r, d, water="free")["m03"]["cost_per_mile_pct"] == pytest.approx(c["m03"]["cost_per_mile_water_free_pct"])


def test_best_cost_needs_every_engine_the_dry_has():
    d = row(eta=0.40, crn=0.40)
    assert C.best_cost([row(w=0.003, eta=0.41)], d)[0] is d  # CRN missing on the wet step -> not a candidate


def test_mpg():
    assert C.mpg("CH4", 0.4) is None
    m = C.mpg("PRF87", 0.35)
    assert m == pytest.approx(0.35 * 44.3701694e6 * 690.288 * 3.785411784e-3 / 3.6e6 / 0.40)
    assert 20 < m < 40


def test_fuel_props_match_live_fuel_library():
    pytest.importorskip("cantera")
    import warnings
    warnings.filterwarnings("ignore")
    from sims.common import fuels
    from sims.track_b import fuels_b
    fuels_b.register()
    for f, p in C.FUEL_PROPS.items():
        assert fuels.lhv(f) == pytest.approx(p["lhv"], rel=1e-6), f
        if p["rho"] is not None:
            assert fuels.FUELS[f].liquid_density == pytest.approx(p["rho"], rel=1e-5), f
