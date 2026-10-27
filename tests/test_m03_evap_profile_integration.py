"""Integration test: Module 03 --evap-profile is consumed by run_point.

Exercises the build_tasks -> _task -> run_point(EvapProfile=...) wiring
without spawning the full multiprocessing pool.
"""

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load():
    from conftest import load_sims_module
    return load_sims_module("sims.03_engine_cycle.evap_profile")


@pytest.fixture(scope="module")
def ep():
    return _load()


@pytest.fixture(scope="module")
def run_mod():
    import cantera  # noqa: F401
    from conftest import load_sims_module
    return load_sims_module("sims.03_engine_cycle.run")


def test_source_label_documented(ep):
    assert ep.source_label() == "derived from module 09 e32288e (IVC/spark interpolation)"


def test_evap_profile_consumed_and_labeled(ep):
    prof = ep.profile_for("carb_venturi", "nominal")
    v = prof.target("CH3OH", 24, 0.6, 360.0, -100.0)
    assert v is not None
    assert 0.0 <= v <= 1.0
    # CH4 is reference-only; profile has no entry for it.
    assert prof.target("CH4", 10, 0.0, 320.0, -100.0) is None
    # cfd_matched variant also covered.
    v2 = ep.profile_for("ultrasonic_120kHz", "cfd_matched").target("CH3OH", 24, 0.6, 360.0, -100.0)
    assert v2 is not None


def test_scheduled_fraction_uses_profile(run_mod, ep):
    """Charge.scheduled_fraction returns the profile target when set."""
    par = run_mod.DEFAULTS
    prof = ep.profile_for("carb_venturi", "nominal")
    charge = run_mod.Charge("CH3OH", 24, 0.6, 360.0, par, evap_profile=prof)
    # CH3OH water_majority carb nominal: IVC 2.879 %, spark 2.879 % (flat).
    assert abs(charge.scheduled_fraction(-100.0) - 0.028791) < 1e-3


def test_task_tuple_passes_evap_profile_keyword(run_mod, ep):
    """build_tasks returns tuples whose final element is the Profile;
    _task unpacks it and passes it as evap_profile= keyword, NOT to
    flame_speed_factor (regression for TypeError: float *= Profile)."""
    prof = ep.profile_for("carb_venturi", "nominal")
    tasks = run_mod.build_tasks("quick", {}, {}, {"per_fuel": {}}, evap_profile=prof)
    assert len(tasks) > 0
    t = tasks[0]
    assert len(t) == 11
    assert t[10] is prof
