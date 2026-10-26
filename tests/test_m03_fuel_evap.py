"""Module 03 optional fuel evaporation (dry-evap baseline check, 2026-10-25).

1. fuel_evap_intake = fuel_evap_port = 0 reproduces the legacy model bit-for-bit;
2. intake fuel evaporation cools the charge, is capped at the fuel dew point and closes energy;
3. port fuel evaporation keeps T_IVC = T_intake and only credits the latent heat (release = vapour LHV);
4. M03-CRN latent credit 0 is bit-exact legacy.
"""
import pytest

ct = pytest.importorskip("cantera")
pytest.importorskip("CoolProp")


@pytest.fixture(scope="module")
def m():
    from conftest import load_sims_module
    return load_sims_module("sims.03_engine_cycle.run")


@pytest.fixture(scope="module")
def fits(m):
    from conftest import REPO_ROOT
    ign, fl, _ = m.read_fits(REPO_ROOT / "results" / "02_flame_chem", "full")
    return ign, fl


KEYS = ("gross_indicated_efficiency", "peak_pressure_Pa", "ca50_used_deg", "energy_closure_error_fraction", "T_IVC_K")


def _pt(m, fits, fuel, cr, w, T, **kw):
    ign, fl = fits
    return m.run_point(fuel, cr, w, T, ign[fuel], fl[fuel], m.DEFAULTS, "full", **kw)["point"]


def test_zero_fuel_evap_bit_exact(m, fits):
    a = _pt(m, fits, "CH3OH", 12, 0.0, 400.0)
    b = _pt(m, fits, "CH3OH", 12, 0.0, 400.0, coupling=dict(fuel_evap_intake=0.0, fuel_evap_port=0.0))
    for k in KEYS:
        assert a[k] == b[k], k


def test_intake_fuel_evap_cools_capped_and_closes(m, fits):
    p = _pt(m, fits, "CH3OH", 12, 0.0, 400.0, coupling=dict(fuel_evap_intake=1.0))
    assert p["status"] == "computed"
    assert p["T_IVC_K"] < 330.0
    assert 0.0 < p["fuel_evap_intake_fraction"] <= 1.0
    if p["fuel_evap_saturation_limited"]:
        assert abs(p["fuel_vapour_saturation_ratio_IVC"] - 1.0) < 0.05 or p["fuel_vapour_saturation_ratio_IVC"] <= 1.0
    assert abs(p["energy_closure_error_fraction"]) < 1e-4
    assert abs(p["intake_closure_error_J"]) < 1e-6


def test_port_fuel_evap_credit_only(m, fits):
    from sims.common import fuels
    a = _pt(m, fits, "C2H5OH", 11, 0.0, 400.0)
    b = _pt(m, fits, "C2H5OH", 11, 0.0, 400.0, coupling=dict(fuel_evap_port=1.0))
    assert b["T_IVC_K"] == a["T_IVC_K"] == 400.0
    assert b["released_lhv_J_per_kg"] == pytest.approx(fuels.lhv("C2H5OH") + fuels.FUELS["C2H5OH"].h_fg)
    assert abs(b["energy_closure_error_fraction"]) < 1e-4


def test_crn_zero_credit_bit_exact():
    from engines.m03_cantera import engine as E
    kw = dict(fuel="CH3OH", cr=10.0, T_ivc=400.0, m_fuel=5e-5, m_air=3.2e-4, m_residual=1.5e-5, m_water=0.0,
              e_intake=0.0, ca50_deg=8.0, d1090_deg=25.0, wall_T=450.0, heat_transfer="woschni")
    a = E.run_case(E.Case(**kw))
    b = E.run_case(E.Case(fuel_latent_credit=0.0, **kw))
    c = E.run_case(E.Case(fuel_latent_credit=1.0, **kw))
    assert a["efficiency"] == b["efficiency"]
    assert c["efficiency"] > a["efficiency"]
