"""Module 09 spray evaporation: numerical verification tests (SPEC 12.2)."""

import importlib
import json
import math

import numpy as np
import pytest

run = importlib.import_module("sims.09_spray_evaporation.run")
model = importlib.import_module("sims.09_spray_evaporation.model")
props = importlib.import_module("sims.09_spray_evaporation.properties")
atom = importlib.import_module("sims.09_spray_evaporation.atomisers")


def test_single_water_droplet_matches_d2_law_within_2pct():
    res = run.d2_law_check()
    assert res["max_rel_err_d2"] < 0.02


def test_d2_law_lifetime_scales_with_d0_squared():
    c = model.ConstProps()
    lifetimes = []
    for d0 in (30e-6, 60e-6):
        sp = model.Spray(m_air=1.0, T_gas=350.0, p=1e5, m_ref=1e-12, const=c, fixed_Td=True, infinite_gas=True)
        sp.add_classes([d0], [1.0], 0.0, 300.0, 0.0)
        snaps = sp.run(0.05, n_out=5, rtol=1e-9)
        d2 = [run.sp_d2(sp, s) for s in snaps]
        slope = -np.polyfit([s["t_s"] for s in snaps], d2, 1)[0]
        lifetimes.append(d0**2 / slope)
    assert lifetimes[1] / lifetimes[0] == pytest.approx(4.0, rel=0.02)


def _closed_box(Y_m, T=330.0, V=1e-5, excess=20.0):
    tab = props.tables()
    m_air = 1e5 * V * tab.M_g[0] / (props.R_U * T)
    j = 1 if Y_m == 0.0 else 2
    ps = np.interp(T, tab.TL, tab.psat[j - 1])
    m_sat = ps * V * tab.M_g[j] / (props.R_U * T)
    m_liq = excess * m_sat
    sp = model.Spray(m_air=m_air, T_gas=T, p=1e5, m_ref=m_liq, activity="wilson")
    d, f = atom.rosin_rammler_classes(20e-6, n=6)
    rho = sp.liquid_density(np.full(d.size, T), np.full(d.size, Y_m))
    sp.add_classes(d, m_liq * f / (rho * math.pi * d**3 / 6.0), Y_m, T, 0.0)
    Vf = lambda t: (V, 0.0)
    return sp.run(2.0, mode="V", Vfun=Vf, n_out=40)


@pytest.mark.parametrize("Y_m,key", [(0.0, "S_water"), (1.0, "S_methanol")])
def test_evaporation_never_exceeds_saturation(Y_m, key):
    snaps = _closed_box(Y_m)
    S = np.array([s[key] for s in snaps])
    assert S.max() <= 1.0 + 1e-6
    assert S[-1] > 0.98          # excess liquid: the closed parcel reaches saturation
    assert snaps[-1]["liquid_kg"] > 0.5 * snaps[0]["injected_kg"]


def test_mass_conserved_to_1e8_blend_case_with_impingement():
    for atomiser in ("carb_venturi", "ultrasonic_120kHz"):
        row = run.run_case(dict(atomiser=atomiser, w=0.6, T_plenum_K=360.0, U_runner_m_s=30.0, L_runner_m=0.2))
        assert row["max_mass_error_rel"] < 1e-8
        assert row["wall_impinged_pct"] > 0.0
        total = row["evaporated_spark_pct"] + row["wall_impinged_pct"] + row["airborne_liquid_spark_pct"]
        assert total == pytest.approx(100.0, abs=1e-6)
        assert row["max_S_pure"] <= 1.0 + 1e-6
        assert row["max_energy_closure_rel"] < 0.01


def test_wilson_and_nrtl_agree():
    # Two independent DECHEMA fits; worst spread is water at infinite dilution, 300 K (~11%).
    x = np.linspace(0.0, 1.0, 11)
    for T in (300.0, 340.0):
        gw, gm = props.wilson_gamma(x, np.full_like(x, T))
        nw, nm = props.nrtl_gamma(x, np.full_like(x, T))
        assert np.allclose(gw, nw, rtol=0.12) and np.allclose(gm, nm, rtol=0.12)
    gw, gm = props.wilson_gamma(np.array([0.0, 1.0]), np.full(2, 340.0))
    assert gw[0] == pytest.approx(1.0) and gm[1] == pytest.approx(1.0)


def test_rosin_rammler_classes_reproduce_smd():
    for smd in (10e-6, 50e-6, 150e-6):
        d, f = atom.rosin_rammler_classes(smd)
        assert atom.smd_of(d, f) == pytest.approx(smd, rel=1e-9)
        assert np.all(np.diff(d) > 0) and f.sum() == pytest.approx(1.0)


def test_bend_efficiency_limits():
    eta, St = run.pui_bend_efficiency(np.array([1e-7, 5e-6, 1e-3]), 1000.0, 30.0, 1.8e-5, 0.035)
    assert eta[0] < 1e-3 and eta[2] == pytest.approx(1.0) and np.all(np.diff(eta) > 0)


def test_atomiser_correlations_trend():
    assert atom.lang_ultrasonic(0.072, 997.0, 120e3) < atom.lang_ultrasonic(0.072, 997.0, 40e3)
    s3, _, _ = run.atomiser_smd("psi_3bar", 0.6, 360.0, 30.0)
    s5, _, _ = run.atomiser_smd("psi_5bar", 0.6, 360.0, 30.0)
    assert s5 < s3


def test_quick_smoke(tmp_path):
    assert run.main(["--quick", "--out", tmp_path, "--cfd-dir", tmp_path / "none"]) == 0
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert summary["mode"] == "quick" and summary["validation"]["passed"]
    assert set(summary) == {"module", "version", "git_sha", "mode", "assumptions", "key_results", "validation", "runtime_s"}
    spark = json.loads((tmp_path / "spray_at_spark.json").read_text())
    assert spark["recommended_atomiser_for_module06"] in run.ATOMISERS
    assert (tmp_path / "sweep.csv").is_file()
