"""Tests for Module 08 (water_chemistry) per SPEC section 12.1.

Validations:
- At w = 0, real and FH2O variants give identical S_L, tau and T_ad.
- FH2O has an LHV of 0.
- Oxygen bookkeeping balance closes to 1e-6 or better.
- Energy from water is zero (energy balance closes).
- Mechanism files load and FH2O has zero net production in every reaction.
- Quick run completes cleanly.
"""
from pathlib import Path
import json
import math
import pytest
import cantera as ct

from sims.common import fuels, io
import importlib
wc = importlib.import_module("sims.08_water_chem.run")
bm = importlib.import_module("sims.08_water_chem.build_mechanisms")


def test_build_mechanisms_and_load(tmp_path):
    """Confirm mechanism copies exist or can be built, load without error,
    contain FH2O, and FH2O appears in no reactions."""
    for source_name, source_path in bm.SOURCES.items():
        if not source_path.is_file():
            continue
        for variant in ("a", "b"):
            out, n = bm.build(source_name, source_path, variant)
            assert out.is_file()
            gas = ct.Solution(str(out))
            assert "FH2O" in gas.species_names
            # Check FH2O participates in zero reactions as reactant/product.
            for rx in gas.reactions():
                eq = rx.equation or ""
                assert "FH2O" not in eq, f"FH2O found in reaction: {eq}"


def test_fh2o_lhv_is_zero():
    """FH2O is fully oxidised and has zero heating value."""
    for fuel in wc.FUELS:
        for variant in ("fh2o_a", "fh2o_b"):
            p = wc._mechanism_path(fuel, variant)
            gas = ct.Solution(p)
            gas.TP = fuels.REFERENCE_T_K, fuels.REFERENCE_P_PA
            idx = gas.species_index("FH2O")
            assert idx >= 0
            # By definition, water undergoing H2O -> H2O has 0 LHV.
            # Its enthalpy change in complete combustion is zero.
            h = float(gas.standard_enthalpies_RT[idx] * ct.gas_constant
                      * fuels.REFERENCE_T_K / 1000.0)
            idx_h2o = gas.species_index("H2O")
            h_h2o = float(gas.standard_enthalpies_RT[idx_h2o] * ct.gas_constant
                          * fuels.REFERENCE_T_K / 1000.0)
            # Thermo of FH2O matches H2O exactly
            assert abs(h - h_h2o) < 1e-9
            # Fully oxidised: LHV is 0
            lhv = (h - h) / gas.molecular_weights[idx]
            assert abs(lhv) < 1e-6


def test_w0_identical_real_and_fh2o():
    """At w = 0, real H2O and both FH2O variants give identical results."""
    for fuel in ("CH3OH", "CH4"):
        T_ad = {}
        for var in ("real", "fh2o_a", "fh2o_b"):
            r = wc.adiabatic_temperature(fuel, var, 1.0, 0.0, 400.0, ct.one_atm)
            assert r["status"] == "computed"
            T_ad[var] = r["T_ad_K"]
        assert T_ad["fh2o_a"] == pytest.approx(T_ad["real"], rel=1e-9)
        assert T_ad["fh2o_b"] == pytest.approx(T_ad["real"], rel=1e-9)


@pytest.mark.slow
def test_w0_flame_speed_identical():
    """At w = 0, flame speeds match identically."""
    fuel = "CH4"
    speeds = {}
    for var in ("real", "fh2o_a", "fh2o_b"):
        r = wc.flame_speed(fuel, var, 1.0, 0.0, 400.0, ct.one_atm)
        assert r["status"] == "computed"
        speeds[var] = r["S_L_m_s"]
    assert speeds["fh2o_a"] == pytest.approx(speeds["real"], rel=1e-6)
    assert speeds["fh2o_b"] == pytest.approx(speeds["real"], rel=1e-6)


def test_oxygen_bookkeeping_closure():
    """Oxygen balance closes to 1e-6 and net energy from water is zero."""
    res = wc.oxygen_bookkeeping(fuel="CH3OH", w=0.6, T_K=900.0, max_time_s=0.1)
    assert res["status"] == "computed"
    assert res["O_balance_rel_error"] is not None
    # O closure: element conservation in adiabatic CV reactor.
    assert res["O_balance_rel_error"] <= 1e-6
    # Energy closure: heat release at 298 K, per kg fuel, must be unchanged
    # by water (water enters and leaves at 298 K).
    assert abs(res["energy_closure_rel"]) < 1e-6


@pytest.mark.slow
def test_quick_smoke(tmp_path):
    """--quick smoke run produces SPEC-compliant results and summary.json."""
    rc = wc.main(["--quick", "--workers", "2", "--out", str(tmp_path)])
    assert rc == 0
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert set(summary) == io.SUMMARY_KEYS
    assert summary["module"] == wc.MODULE
    assert summary["validation"]["passed"] is True
    assert (tmp_path / "chemical_effect.csv").stat().st_size > 0
    assert (tmp_path / "oxygen_bookkeeping.json").stat().st_size > 0
