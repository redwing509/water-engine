"""Module 11 spray_flame: zero-liquid limit and monotonic trends (SPEC 12.3)."""

import importlib
import math

import numpy as np
import pytest

M = importlib.import_module("sims.11_spray_flame.model")
R = importlib.import_module("sims.11_spray_flame.run")


@pytest.fixture(scope="module")
def st():
    # CH3OH water-majority-like spark state (w = 0.6, ~31 bar, 700 K)
    return R.make_state("CH3OH", 0.6, 700.0, 3.1e6, 0.323)


def test_zero_liquid_reduces_to_gas_phase_SL(st):
    for d in (1e-6, 20e-6, 200e-6):
        r = M.spray_point(st, 0.0, 0.0, d)
        assert r["S_BL_m_s"] == pytest.approx(st.SL_gas, rel=1e-12)
        assert r["S_eff_m_s"] == pytest.approx(st.SL_gas, rel=1e-12)
        assert r["d_q_m"] == pytest.approx(r["d_q_gas_m"], rel=1e-12)


def test_zero_diameter_reduces_to_gas_phase_SL(st):
    r = M.spray_point(st, 0.5, 0.0, 0.0)
    assert r["S_BL_m_s"] == pytest.approx(st.SL_gas, rel=1e-12)


def test_flame_speed_decreases_with_smd_and_liquid(st):
    ds = np.geomspace(1e-6, 300e-6, 25)
    for f in (0.01, 0.1, 1.0):
        s = [M.spray_point(st, f, 0.0, d)["S_BL_m_s"] for d in ds]
        assert all(b < a for a, b in zip(s, s[1:]))
    fs = np.linspace(0, 1, 21)
    s = [M.spray_point(st, f, 0.0, 30e-6)["S_BL_m_s"] for f in fs]
    assert all(b < a for a, b in zip(s, s[1:]))


def test_mie_increases_with_smd_and_liquid(st):
    ds = np.geomspace(1e-6, 300e-6, 25)
    e = [M.spray_point(st, 0.1, 0.0, d)["MIE_J"] for d in ds]
    assert all(b > a for a, b in zip(e, e[1:]))
    fs = np.linspace(0, 1, 21)
    e = [M.spray_point(st, f, 0.0, 30e-6)["MIE_J"] for f in fs]
    assert all(b > a for a, b in zip(e, e[1:]))


def test_liquid_water_heat_sink_is_monotonic(st):
    ys = np.linspace(0, 0.05, 11)
    s = [M.spray_point(st, 0.0, y, 20e-6)["S_BL_m_s"] for y in ys]
    e = [M.spray_point(st, 0.0, y, 20e-6)["MIE_J"] for y in ys]
    assert all(b < a for a, b in zip(s, s[1:]))
    assert all(b > a for a, b in zip(e, e[1:]))


def test_mie_matches_closed_form(st):
    r = M.spray_point(st, 1.0, 0.0, 50e-6)
    dq = math.sqrt(st.rho_F * (50e-6) ** 2 / (st.rho_g * math.log1p(st.B)) + (10 * st.alpha / st.SL_gas) ** 2)
    mie = st.cp_g * st.rho_g * (st.T_ad_K - st.T_K) * math.pi / 6 * dq ** 3
    assert r["MIE_J"] == pytest.approx(mie, rel=1e-12)


def test_metghalchi_keck_identity_at_reference():
    assert M.SL_at_state(0.4, 400.0, 101325.0) == pytest.approx(0.4)
    assert M.mk_phi_ratio(1.0) == pytest.approx(1.0)


def test_max_smd_consistent_with_criterion(st):
    mx = M.max_smd(st, 1.0, 0.0)
    D = mx["D_max_MIE_50mJ_m"]
    assert 0 < D < M.DEF.D_MAX_SEARCH_m
    assert M.spray_point(st, 1.0, 0.0, D)["MIE_J"] == pytest.approx(0.05, rel=1e-6)


def test_quick_run_writes_outputs(tmp_path):
    R.main(["--quick", "--out", tmp_path])
    for f in ("sweep.csv", "design_points.csv", "max_smd.csv", "spray_flame.json", "summary.json"):
        assert (tmp_path / f).is_file()
