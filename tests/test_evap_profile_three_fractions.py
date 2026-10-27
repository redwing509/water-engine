"""Unit tests for sims/03_engine_cycle/evap_profile.py -- three-fraction semantics.

Step 1 verifies that the three fractions carried from Module 09
(evaporated, airborne liquid, wall film) match spray_at_spark.json within
1 percentage point for every case, and that they sum to 100 %.
"""

import pytest

REPO_ROOT = "C:/Users/spoka/git/water-engine"


def _load():
    from conftest import load_sims_module
    return load_sims_module("sims.03_engine_cycle.evap_profile")


@pytest.fixture(scope="module")
def ep():
    return _load()


def test_three_fractions_match_m09_within_1pp(ep):
    rows = ep.verify_three_fractions(tolerance_pp=1.0)
    assert len(rows) > 0
    for row in rows:
        case, atomiser, variant = row[0], row[1], row[2]
        # row layout: case, atomiser, variant,
        #   frac_evap_derived, frac_evap_m09, delta_pp_evap,
        #   frac_air_derived,  frac_air_m09,  delta_pp_air,
        #   frac_wall_derived, frac_wall_m09, delta_pp_wall
        d_evap, m_evap, dd = row[3], row[4], row[5]
        d_air, m_air, da = row[6], row[7], row[8]
        d_wall, m_wall, dw = row[9], row[10], row[11]
        assert abs(dd) < 1.0, (case, atomiser, variant, "evap", dd)
        assert abs(da) < 1.0, (case, atomiser, variant, "air", da)
        assert abs(dw) < 1.0, (case, atomiser, variant, "wall", dw)


def test_three_fractions_sum_to_100(ep):
    rows = ep.verify_three_fractions(tolerance_pp=1.0)
    assert len(rows) > 0
    for row in rows:
        total = row[3] + row[6] + row[9]  # derived evap + air + wall
        assert total == pytest.approx(1.0, abs=1e-9), (row[0], row[1], row[2], total)


def test_three_fractions_all_six_design_points(ep):
    for fuel in ("CH3OH", "C2H5OH"):
        for point in ("best_dry", "best_overall", "water_majority"):
            for atomiser in ep.ATOMISERS:
                for variant in ep.VARIANTS:
                    fracs = ep.fractions_at_spark(fuel, point, atomiser, variant)
                    assert fracs is not None, (fuel, point, atomiser, variant)
                    assert sum(fracs) == pytest.approx(1.0, abs=1e-9)
                    for f in fracs:
                        assert 0.0 <= f <= 1.0


def test_airborne_liquid_is_small_on_water_majority(ep):
    """CLAUDE CORRECTION: airborne liquid at spark is 0-3.2 % on water_majority."""
    for atomiser in ep.ATOMISERS:
        for variant in ep.VARIANTS:
            fr = ep.fractions_at_spark("CH3OH", "water_majority", atomiser, variant)
            assert fr is not None
            airborne = fr[1] * 100.0
            wall = fr[2] * 100.0
            assert 0.0 <= airborne <= 3.2 + 1.0, (atomiser, variant, airborne)
            assert wall >= 77.0 - 1.0, (atomiser, variant, wall)


def test_spark_target_returns_three_fractions(ep):
    t = ep.spark_target("CH3OH", 24, 0.6, 360.0, "carb_venturi", "nominal")
    assert t is not None
    spark_deg, fracs = t
    assert isinstance(spark_deg, float)
    assert len(fracs) == 3
    assert sum(fracs) == pytest.approx(1.0, abs=1e-9)


def test_liquid_at_spark_is_total_nonvapour(ep):
    """liquid_at_spark == 1 - evap == airborne + wall."""
    for fuel in ("CH3OH", "C2H5OH"):
        for point in ("best_dry", "best_overall", "water_majority"):
            for atomiser in ep.ATOMISERS:
                for variant in ep.VARIANTS:
                    fr = ep.fractions_at_spark(fuel, point, atomiser, variant)
                    if fr is None:
                        continue
                    liq = ep.liquid_at_spark(fuel, point, atomiser, variant)
                    assert liq == pytest.approx(1.0 - fr[0], abs=1e-9)
                    assert liq == pytest.approx(fr[1] + fr[2], abs=1e-9)
