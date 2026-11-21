"""Fast checks for the independent module-03 engine (engines/m03_cantera, ACCEPTANCE.md).

Full verification (rtol GCI, all design points) is engines/m03_cantera/verify.py.
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
ct = pytest.importorskip("cantera")
from engines.m03_cantera import engine as E, points as P  # noqa: E402


def test_ideal_otto_cr16():
    r = E.ideal_otto(16, d1090_deg=0.5)
    assert abs(r["error"]) <= 1e-3
    assert abs(r["eta_energy"] - r["eta_trapezoid"]) <= 1e-6


def test_lhv_methanol_matches_module03_convention():
    gas = E.build_gas(kinetics=False)
    assert E.lhv_liquid("CH3OH", gas) == pytest.approx(19.9307e6, rel=5e-3)


@pytest.mark.parametrize("regime", ["normal", "hot"])
def test_energy_closure_design_point(regime):
    d = P.load_rows()
    key = next(k.split("|", 1)[1] for k in d["rows"] if k.startswith(regime + "|"))
    c = P.case_from_row(d["rows"][f"{regime}|{key}"], regime, heat_transfer="woschni", rtol=1e-8)
    r = E.run_case(c)
    assert abs(r["energy_closure"]) <= 1e-5
    assert 0.2 < r["efficiency"] < 0.75
