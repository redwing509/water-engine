"""Module 11 film sensitivity map (box-queue J4): budget sanity checks + closed form of the boiling branch."""
import csv
import importlib
import math
from pathlib import Path

import pytest

P = importlib.import_module("sims.dual_temp.port_film_wall_T")
FM = importlib.import_module("sims.11_spray_flame.film_map")
ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "results" / "11_spray_flame" / "film_map" / "film_map_boundary.csv"

FILM = (2.0e-6, 3.0e-6, "CH3OH")  # kg alcohol, kg water per cycle (Module 09 order of magnitude)


def test_regime_points_are_on_the_grid():
    for T in (363.15, 388.15, 420.0):
        assert T in FM.T_WALL
    assert FM.L_WET[0] == 0.02 and FM.L_WET[-1] == 0.10


@pytest.mark.parametrize("Tw", [355.0, 375.0, 400.0, 430.0])
def test_capacity_non_decreasing_in_h_and_length(Tw):
    ma, mw, alc = FILM
    prev = -1.0
    for h in FM.H_FILM:
        c = sum(P.capacity(ma, mw, alc, Tw, 360.0, 0.05, h)[:2])
        assert c >= prev - 1e-15
        prev = c
    prev = -1.0
    for L in FM.L_WET:
        c = sum(P.capacity(ma, mw, alc, Tw, 360.0, L, 2e4)[:2])
        assert c >= prev - 1e-15
        prev = c


def test_boiling_branch_matches_closed_form():
    ma, mw, alc = FILM
    n_a, n_w = ma / P.MW[alc], mw / P.MW["H2O"]
    x = {alc: n_a / (n_a + n_w), "H2O": n_w / (n_a + n_w)}
    Tb = P.bubble_T(x, alc)
    Tw, h, L = Tb + 30.0, 2e4, 0.06
    ca, cw, reg = P.capacity(ma, mw, alc, Tw, 360.0, L, h)
    assert reg.startswith("boiling")
    wa, ww = ma / (ma + mw), mw / (ma + mw)
    Lmix = wa * P.hfg(alc, Tb) + ww * P.hfg("H2O", Tb)
    expect = min(P.CHF, h * 30.0) * math.pi * P.D_RUN * L * (120.0 / P.RPM) / Lmix
    assert ca + cw == pytest.approx(expect, rel=1e-12)
    assert ca / (ca + cw) == pytest.approx(wa, rel=1e-12)


@pytest.mark.skipif(not BOUNDARY.exists(), reason="film_map not run")
def test_map_reach_counts_fall_with_wall_T_and_heat_supply():
    rows = list(csv.DictReader(BOUNDARY.open()))
    assert len(rows) == 3 * 2 * 9 * 5 * 3
    for r in rows:
        n = [int(v) for v in r["n_reach_vs_T"].split()]
        assert len(n) == len(FM.T_WALL)
        assert all(0 <= v <= int(r["n_cases"]) for v in n)
        # boiling heat-limited budget grows with T_wall -> at most one-sided wiggle at the bubble point
        i363, i420 = FM.T_WALL.index(363.15), FM.T_WALL.index(420.0)
        assert n[i420] <= n[i363]
