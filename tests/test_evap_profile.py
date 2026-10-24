"""Unit tests for sims/03_engine_cycle/evap_profile.py.

The profile is DERIVED from Module 09 outputs on branch wme1-spray09
(commit e32288e); it is NOT Grok Bot's evap_profiles.json, which was
never produced.  These tests verify the interpolation, the point index,
the fallback semantics and the documented source label.
"""

import importlib.util
import sys
import types
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load():
    for n in ("sims", "sims.common"):
        if n not in sys.modules:
            m = types.ModuleType(n)
            m.__path__ = []
            sys.modules[n] = m
    spec = importlib.util.spec_from_file_location(
        "sims.03_engine_cycle.evap_profile",
        REPO / "sims" / "03_engine_cycle" / "evap_profile.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["sims.03_engine_cycle.evap_profile"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def ep():
    return _load()


def test_point_index_covers_six_design_points(ep):
    for fuel, cr, w, T in (("CH3OH", 16, 0.0, 320), ("CH3OH", 23, 0.3, 320),
                           ("CH3OH", 24, 0.6, 360), ("C2H5OH", 24, 0.0, 320),
                           ("C2H5OH", 23, 0.4, 320), ("C2H5OH", 24, 0.6, 360)):
        assert ep.point_name(fuel, cr, w, T) is not None, (fuel, cr, w, T)


def test_point_index_excludes_non_covered_points(ep):
    # CH4 is reference-only in Module 03; no Module 09 case exists.
    assert ep.point_name("CH4", 10, 0.0, 320) is None
    assert ep.point_name("CH3OH", 20, 0.2, 340) is None
    # The internal index is private; verify the public API rejects it.
    assert not hasattr(ep, "POINT_INDEX")


def test_linear_interpolation_ivc_to_spark(ep):
    # CH3OH/water_majority/carb_venturi/nominal: IVC 2.879 %, spark 2.879 %
    # (flat profile because evaporation is already complete at IVC for this
    #  case).  Check the clamping and the linear path with a sloped case.
    f = ep.profile_at("CH3OH", "water_majority", "carb_venturi", "nominal", -180.0)
    assert f == pytest.approx(0.028791177094191135)
    s = ep.profile_at("CH3OH", "water_majority", "carb_venturi", "nominal", -30.965)
    assert s == pytest.approx(0.028791177094191135)
    # ultrasonic_120kHz nominal: IVC 14.419 %, spark 19.780 % -> slope
    ivc = ep.profile_at("CH3OH", "water_majority", "ultrasonic_120kHz", "nominal", -180.0)
    spark = ep.profile_at("CH3OH", "water_majority", "ultrasonic_120kHz", "nominal", -30.965)
    assert ivc == pytest.approx(0.1441933134203222)
    assert spark == pytest.approx(0.19779594741816485)
    mid = ep.profile_at("CH3OH", "water_majority", "ultrasonic_120kHz", "nominal", -105.4825)
    assert mid == pytest.approx((ivc + spark) / 2.0, rel=1e-6)
    # Above spark the value is held.
    assert ep.profile_at("CH3OH", "water_majority", "ultrasonic_120kHz", "nominal", -10.0) == spark
    # Below IVC the value is held.
    assert ep.profile_at("CH3OH", "water_majority", "ultrasonic_120kHz", "nominal", -200.0) == ivc


def test_profile_at_returns_none_for_uncovered(ep):
    # CH4 is reference-only in Module 03; no Module 09 case exists.
    assert ep.profile_at("CH4", "best_dry", "carb_venturi", "nominal", -100.0) is None
    # C2H5OH water_majority ultrasonic cfd_matched IS covered.
    assert ep.profile_at("C2H5OH", "water_majority", "ultrasonic_120kHz",
                         "cfd_matched", -100.0) is not None


def test_profile_object_validation(ep):
    with pytest.raises(ValueError):
        ep.Profile("unknown_atomiser", "nominal")
    with pytest.raises(ValueError):
        ep.Profile("carb_venturi", "unknown_variant")
    p = ep.Profile("ultrasonic_120kHz", "cfd_matched")
    assert p.atomiser == "ultrasonic_120kHz"
    assert p.variant == "cfd_matched"
    assert p.source_label() == "derived from module 09 e32288e (IVC/spark interpolation)"


def test_source_label_is_documented(ep):
    assert "derived from module 09" in ep.source_label()
    assert "e32288e" in ep.source_label()


def test_evaporated_fractions_are_bounded(ep):
    for fuel in ("CH3OH", "C2H5OH"):
        for point in ("best_dry", "best_overall", "water_majority"):
            for atomiser in ep.ATOMISERS:
                for variant in ep.VARIANTS:
                    for theta in (-180.0, -100.0, -31.0, -10.0):
                        v = ep.profile_at(fuel, point, atomiser, variant, theta)
                        if v is not None:
                            assert 0.0 <= v <= 1.0, (fuel, point, atomiser, variant, theta, v)