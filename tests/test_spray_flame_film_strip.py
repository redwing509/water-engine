"""Module 11 sensitivity bound (ii): wall film stripped into the cylinder as large drops."""

import csv
import importlib
import json

import pytest

M = importlib.import_module("sims.11_spray_flame.model")
R = importlib.import_module("sims.11_spray_flame.run")
F = importlib.import_module("sims.11_spray_flame.film_strip")


@pytest.fixture(scope="module")
def inputs():
    fits, sas, dp = R.load_inputs()
    ep = json.loads(F.EP_PATH.read_text())
    return fits, sas, dp, ep


def _iter(sas, dp, ep):
    for key, c in sas["cases"].items():
        ms = R.masses(dp["per_fuel"][c["fuel"]][c["point"]], c["fuel"])
        for an, a in c["atomisers"].items():
            for v in R.VARIANTS:
                yield key, c, an, v, a[v], ep[f"{key}/{an}/{v}"], ms


def test_film_mass_balance_closes_with_module09(inputs):
    _, sas, dp, ep = inputs
    n = 0
    for key, c, an, v, s, prof, ms in _iter(sas, dp, ep):
        film = F.film_masses(s, prof, ms)
        assert film["film_pct"] == pytest.approx(s["wall_impinged_pct"], abs=0.02), (key, an, v)
        f_fuel, Y_wl, liq = F.liquid_state(s, film, ms, 1.0)
        assert liq == pytest.approx(s["liquid_spark_pct"] + s["wall_impinged_pct"], abs=0.02)
        assert 0.0 <= f_fuel <= 1.0 and Y_wl >= 0.0
        n += 1
    assert n == 84   # 6 design points x 7 atomisers x 2 variants


def test_zero_strip_reproduces_module11_baseline(inputs):
    fits, sas, dp, ep = inputs
    base = {(r["case"], r["atomiser"], r["variant"]): r
            for r in csv.DictReader(open(R.ROOT / "results" / "11_spray_flame" / "design_points.csv"))}
    for key, c, an, v, s, prof, ms in list(_iter(sas, dp, ep))[::9]:
        film = F.film_masses(s, prof, ms)
        f_fuel, Y_wl, _ = F.liquid_state(s, film, ms, 0.0)
        st = R.make_state(c["fuel"], float(c["w"]), s["T_spark_m09_K"], s["p_spark_Pa"], M.poly_SL(fits[c["fuel"]], float(c["w"])))
        r = M.spray_point(st, f_fuel, Y_wl, s["SMD_spark_um"] * 1e-6)
        b = base[(key, an, v)]
        assert r["MIE_J"] == pytest.approx(float(b["MIE_J"]), rel=1e-9)
        assert r["S_eff_m_s"] == pytest.approx(float(b["S_eff_m_s"]), rel=1e-9)


@pytest.fixture(scope="module")
def wm_case(inputs):
    fits, sas, dp, ep = inputs
    key, an, v = "CH3OH/water_majority", "ultrasonic_120kHz", "nominal"
    c = sas["cases"][key]; s = c["atomisers"][an][v]
    ms = R.masses(dp["per_fuel"][c["fuel"]][c["point"]], c["fuel"])
    film = F.film_masses(s, ep[f"{key}/{an}/{v}"], ms)
    st = R.make_state(c["fuel"], float(c["w"]), s["T_spark_m09_K"], s["p_spark_Pa"], M.poly_SL(fits[c["fuel"]], float(c["w"])))
    return st, s, film, ms


def test_mie_monotonic_in_strip_fraction_and_smd(wm_case):
    st, s, film, ms = wm_case
    xs = [i / 10 for i in range(11)]
    for D in (200e-6, 350e-6, 500e-6):
        e = [M.spray_point(st, *F.liquid_state(s, film, ms, x)[:2], D)["MIE_J"] for x in xs]
        assert all(b > a for a, b in zip(e, e[1:]))
    e = [M.spray_point(st, *F.liquid_state(s, film, ms, 1.0)[:2], d * 1e-6)["MIE_J"] for d in F.SMD_STRIP_um]
    assert all(b > a for a, b in zip(e, e[1:]))


def test_critical_strip_fraction_hits_threshold(wm_case):
    st, s, film, ms = wm_case
    for E in (M.DEF.E_SPARK_LOW_J, M.DEF.E_SPARK_HIGH_J):
        x = F.critical_strip(st, s, film, ms, 350e-6, E)
        assert x is not None and 0.0 < x < 1.0
        mie = M.spray_point(st, *F.liquid_state(s, film, ms, x)[:2], 350e-6)["MIE_J"]
        assert mie == pytest.approx(E, rel=1e-6)
    # tiny drops never reach 100 mJ for this case
    assert F.critical_strip(st, s, film, ms, 5e-6, M.DEF.E_SPARK_HIGH_J) is None


def test_verdict_thresholds():
    assert F.verdict(0.0499).startswith("IGNITES")
    assert F.verdict(0.0501).startswith("MARGINAL")
    assert F.verdict(0.1001).startswith("MISFIRE")
