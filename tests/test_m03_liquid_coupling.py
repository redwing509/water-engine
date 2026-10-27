"""Module 03 retained-liquid / wall-film coupling (item B, 2026-10-24).

Required checks (Claude's coupling-takeover job):
  1. 0 % liquid at spark reproduces the current (legacy) model exactly;
  2. increasing liquid at spark changes efficiency monotonically;
  3. water adds no energy (release = eta_c m_f LHV dx_b only; the liquid
     sink is a debit; energy closes).
"""
import math

import pytest

ct = pytest.importorskip("cantera")
pytest.importorskip("CoolProp")


@pytest.fixture(scope="module")
def m():
    from conftest import load_sims_module
    return load_sims_module("sims.03_engine_cycle.run")


@pytest.fixture(scope="module")
def ep():
    from conftest import load_sims_module
    return load_sims_module("sims.03_engine_cycle.evap_profile")


@pytest.fixture(scope="module")
def fits(m):
    from conftest import REPO_ROOT
    ign, fl, _ = m.read_fits(REPO_ROOT / "results" / "02_flame_chem", "full")
    return ign, fl


KEYS = ("gross_indicated_efficiency", "peak_pressure_Pa", "peak_temperature_K", "NO_mol_per_J_fuel",
        "knock_integral_at_xb90", "ca50_used_deg", "energy_closure_error_fraction", "EVO_T_K",
        "wall_heat_J", "T_IVC_K", "f_evap_intake_effective")


def _pt(m, fits, fuel, cr, w, T, **kw):
    ign, fl = fits
    return m.run_point(fuel, cr, w, T, ign[fuel], fl[fuel], m.DEFAULTS, "full", **kw)["point"]


def test_zero_liquid_dry_point_bit_exact(m, fits):
    a = _pt(m, fits, "CH3OH", 16, 0.0, 320.0)
    b = _pt(m, fits, "CH3OH", 16, 0.0, 320.0, coupling=dict(liquid_sink=True))
    assert a["status"] == b["status"] == "computed"
    for k in KEYS:
        assert a[k] == b[k], k


def test_zero_liquid_wet_point_bit_exact(m, fits):
    """Default schedule finishes evaporating before the flame: sink inactive, legacy reproduced."""
    a = _pt(m, fits, "CH3OH", 23, 0.3, 320.0)
    b = _pt(m, fits, "CH3OH", 23, 0.3, 320.0, coupling=dict(liquid_sink=True))
    assert b["liquid_fraction_spark"] == 0.0
    assert b["liquid_sink_J"] == 0.0
    for k in KEYS:
        assert a[k] == b[k], k


def _cycle(m, ep, fits, f_evap, fuel="CH3OH", cr=23, w=0.3, T=320.0):
    ign, fl = fits
    par = m.DEFAULTS
    sl, ref = m.check_fits(ign[fuel], fl[fuel], w, "full")
    dur = m.burn_duration(sl, ref, par)
    prof = ep.SyntheticProfile(f_evap, spark_deg=-30.0)
    ch = m.Charge(fuel, cr, w, T, par, evap_profile=prof,
                  coupling=dict(liquid_sink=True, intake_cap_frac=f_evap))
    return ch, m.integrate_cycle(ch, par.ca50_rad, dur, ign[fuel])


@pytest.fixture(scope="module")
def sweep(m, ep, fits):
    return [(f,) + _cycle(m, ep, fits, f) for f in (1.0, 0.75, 0.5, 0.25, 0.0)]


def test_liquid_monotonic_efficiency(sweep):
    liq = [r["liquid_fraction_spark"] for _, _, r in sweep]
    eta = [r["gross_indicated_efficiency"] for _, _, r in sweep]
    assert all(b > a for a, b in zip(liq, liq[1:])), liq
    d = [b - a for a, b in zip(eta, eta[1:])]
    assert all(x < 0 for x in d) or all(x > 0 for x in d), eta
    assert abs(eta[0] - eta[-1]) > 1e-3  # the coupling is not a no-op


def test_water_adds_no_energy(sweep):
    for f, ch, r in sweep:
        # Release is the Wiebe fuel energy only, independent of the water.
        assert r["released_energy_J"] <= ch.Q_avail * (1 + 1e-12)
        assert r["released_energy_J"] == pytest.approx(ch.Q_avail * r["xb_EVO"], rel=1e-9)
        assert r["liquid_sink_J"] >= 0.0
        liq_kg = ch.water_mass * r["liquid_fraction_spark"]
        # Sink >= latent u_fg of the liquid (plus sensible), and zero without liquid.
        if liq_kg == 0.0:
            assert r["liquid_sink_J"] == 0.0
        else:
            assert r["liquid_sink_J"] >= 0.9 * liq_kg * ch.h_latent
        assert abs(r["energy_closure_error_fraction"]) < 2e-3
        assert abs(r["integrator_identity_error_fraction"]) < 1e-9
        assert r["indicated_work_J"] < r["released_energy_J"]
    # Release per unit fuel energy is identical in every case: the water only
    # ever debits (the trapped fuel mass itself varies with T_IVC).
    rel = [r["released_energy_J"] / ch.Q_avail for _, ch, r in sweep]
    assert max(rel) - min(rel) < 1e-9
