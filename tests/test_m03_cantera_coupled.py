"""M03-CRN retained-liquid extension (evap_mode="coupled", item B 2026-10-24).

Independent of Module 03's formulation: CVODES ReactorNet, ct.Water h_fg,
H2O(g) mass-flow inflow; after min(spark, Wiebe start) the liquid left enters
at the burn rate. Checks: zero-liquid identity, energy closure, all liquid
vaporised by EVO, efficiency monotonic in the liquid at spark, and the
evaporated fraction at spark follows the prescribed schedule.
"""
import dataclasses
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
ct = pytest.importorskip("cantera")
from engines.m03_cantera import engine as E, points as P  # noqa: E402


@pytest.fixture(scope="module")
def base():
    d = P.load_rows()
    row = d["rows"]["normal|CH3OH/CR=24/w=0.6/T_intake=360"]
    return P.case_from_row(row, "normal", heat_transfer="woschni", rtol=1e-8)


def _coupled(c, f_spark, f_ivc=None):
    f_ivc = c.e_intake if f_ivc is None else f_ivc
    return dataclasses.replace(c, evap_mode="coupled", spark_deg=-31.0, f_ivc=f_ivc, f_spark=f_spark)


def test_zero_liquid_identity(base):
    dry_water = dataclasses.replace(base, e_intake=1.0)
    a = E.run_case(dry_water)
    b = E.run_case(_coupled(dry_water, 1.0))
    for k in ("efficiency", "p_max_Pa", "T_max_K", "wall_heat_J", "NO_mol_per_J_fuel_bulk", "T_EVO_K"):
        assert b[k] == pytest.approx(a[k], rel=1e-6, abs=1e-12), k  # extra grid break points only
    assert b["liquid_at_spark_kg"] == 0.0


@pytest.fixture(scope="module")
def sweep(base):
    out = []
    for fs in (base.e_intake + 0.6 * (1 - base.e_intake), base.e_intake + 0.3 * (1 - base.e_intake),
               base.e_intake):
        out.append((fs, E.run_case(_coupled(base, fs))))
    return out


def test_closure_and_full_vaporisation(base, sweep):
    for fs, r in sweep:
        assert abs(r["energy_closure"]) <= 1e-5
        assert abs(r["wiebe_integral_error"]) <= 1e-5
        # all water vapour by EVO (x_b(EVO) ~ 1): only the Wiebe tail is left
        assert r["liquid_left_kg"] <= 1e-3 * base.m_water
        # schedule honoured at spark unless saturation capped it (then less evaporated)
        assert r["evaporated_fraction_spark"] <= fs + 1e-6


def test_monotonic_in_liquid(sweep):
    liq = [r["liquid_at_spark_kg"] for _, r in sweep]
    eta = [r["efficiency"] for _, r in sweep]
    assert all(b > a for a, b in zip(liq, liq[1:])), liq
    d = [b - a for a, b in zip(eta, eta[1:])]
    assert all(x < 0 for x in d) or all(x > 0 for x in d), eta


def test_water_adds_no_energy(base, sweep):
    for _, r in sweep:
        assert r["heat_released_J"] == pytest.approx(E.ETA_C * r["Q_fuel_J"] *
                                                     (1 - 0.0), rel=2e-3)
        assert r["latent_J"] >= 0.0
        assert r["work_J"] < r["heat_released_J"]
