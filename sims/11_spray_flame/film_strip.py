"""Module 11 SENSITIVITY, bound (ii): Module 09 wall film stripped back into the cylinder as large drops.

Question (Claude review of ad50959): airborne liquid at spark is small (0-3.8 % of the injected liquid), but
54-99 % of it is deposited as wall film in Module 09. If that film is sheared/stripped off and re-enters the
charge as large drops before spark, does the Ballal-Lefebvre spray flame misfire?

Liquid at spark (per species, per design point x atomiser x Module 09 variant):
    m_liq,s = m_airborne,s (Module 09 spray_at_spark.json)  +  X_strip * m_film,s
    m_film,s = m_injected,s * (1 - f_evap,s(spark)) - m_airborne,s
with f_evap,s from Module 09 evap_profiles.json (f_evap_alcohol, f_evap_water at the spark crank angle) and
m_injected,s from Module 03 design_point.json. The species balance closes against Module 09 wall_impinged_pct
to machine precision (checked in tests). X_strip = 1 is the bound (all film airborne at spark); the smallest
X_strip that gives MIE > 50 mJ and > 100 mJ is also reported.

Drop size: the repository has no wall-film strip-off SMD model (film dynamics are Module 13), so the SMD of
the whole liquid at spark is swept over SMD_STRIP_um = 200, 350, 500 um (film-stripping/sheet-breakup drops
are typically O(100-1000) um). The airborne Module 09 droplets are lumped into the same SMD (conservative: they
are 7-60 um, so the true mass-weighted d^2 is slightly smaller).

Conservative choices (all push toward misfire, so "no misfire" would be robust, "misfire" is an upper bound):
  * film is not re-evaporated between deposition and spark (Module 09 has no film evaporation);
  * the film has its deposited composition (no preferential alcohol evaporation from the film);
  * liquid water is a heat sink evaporated in the preheat zone (Module 11 model);
  * MIE is compared directly with the spark energy (no transfer-efficiency credit either way).
Same spark state (T, p from Module 09), same Ballal-Lefebvre/MIE model and verdict thresholds as run.py.

Status: EXECUTED model runs; numerics VERIFIED by tests/test_spray_flame_film_strip.py; NOT VALIDATED. B-L is
EXTRAPOLATED (fitted for SMD ~20-200 um at 0.1-1 atm; here 200-500 um at 25-35 bar).
"""

import json
from pathlib import Path
import time

from sims.common import io

from . import model as M
from . import run as R

MODULE = "11_spray_flame"
SUBDIR = "bound_ii_film_strip"
VERSION = "1.0.0"
EP_PATH = R.ROOT / "results" / "09_spray_evaporation" / "evap_profiles.json"
SMD_STRIP_um = (200.0, 350.0, 500.0)


def verdict(mie_J: float, p: M.Params = M.DEF) -> str:
    return ("MISFIRE (MIE > 100 mJ)" if mie_J > p.E_SPARK_HIGH_J else
            "MARGINAL (50 < MIE <= 100 mJ)" if mie_J > p.E_SPARK_LOW_J else "IGNITES (MIE <= 50 mJ)")


def film_masses(s: dict, prof: dict, ms: dict) -> dict:
    """Wall-film alcohol and water masses [kg] at spark from Module 09 species evaporated fractions."""
    fa, fw = prof["f_evap_alcohol"][-1], prof["f_evap_water"][-1]
    film_a = max(0.0, ms["m_fuel"] * (1.0 - fa) - s["liquid_alcohol_spark_kg"])
    film_w = max(0.0, ms["m_water"] * (1.0 - fw) - s["liquid_water_spark_kg"])
    return dict(film_alcohol_kg=film_a, film_water_kg=film_w,
                film_pct=100.0 * (film_a + film_w) / (ms["m_fuel"] + ms["m_water"]))


def liquid_state(s: dict, film: dict, ms: dict, x_strip: float) -> tuple[float, float, float]:
    """(f_liq_fuel, Y_liquid_water, liquid_at_spark_pct) with fraction x_strip of the film airborne."""
    la = s["liquid_alcohol_spark_kg"] + x_strip * film["film_alcohol_kg"]
    lw = s["liquid_water_spark_kg"] + x_strip * film["film_water_kg"]
    return (min(1.0, la / ms["m_fuel"]), lw / ms["m_charge"], 100.0 * (la + lw) / (ms["m_fuel"] + ms["m_water"]))


def critical_strip(st, s, film, ms, D, E_J, p: M.Params = M.DEF) -> float | None:
    """Smallest film fraction x in [0, 1] with MIE > E_J (MIE is monotonic in x); None if never."""
    mie = lambda x: M.spray_point(st, *liquid_state(s, film, ms, x)[:2], D, p)["MIE_J"]
    if mie(1.0) <= E_J:
        return None
    if mie(0.0) > E_J:
        return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (lo, mid) if mie(mid) > E_J else (mid, hi)
    return hi


def run(smds=SMD_STRIP_um):
    fits, sas, dp = R.load_inputs()
    ep = json.loads(EP_PATH.read_text())
    rows = []
    for key, c in sas["cases"].items():
        fuel, point, w = c["fuel"], c["point"], float(c["w"])
        ms = R.masses(dp["per_fuel"][fuel][point], fuel)
        SL0 = M.poly_SL(fits[fuel], w)
        for an, a in c["atomisers"].items():
            for v in R.VARIANTS:
                s = a[v]
                film = film_masses(s, ep[f"{key}/{an}/{v}"], ms)
                st = R.make_state(fuel, w, s["T_spark_m09_K"], s["p_spark_Pa"], SL0)
                f_fuel, Y_wl, liq_pct = liquid_state(s, film, ms, 1.0)
                for d in smds:
                    D = d * 1e-6
                    r = M.spray_point(st, f_fuel, Y_wl, D)
                    x50 = critical_strip(st, s, film, ms, D, M.DEF.E_SPARK_LOW_J)
                    x100 = critical_strip(st, s, film, ms, D, M.DEF.E_SPARK_HIGH_J)
                    rows.append(dict(case=key, fuel=fuel, point=point, w=w, atomiser=an, variant=v,
                                     T_spark_K=s["T_spark_m09_K"], p_spark_Pa=s["p_spark_Pa"],
                                     airborne_spark_pct=s["liquid_spark_pct"], film_pct=film["film_pct"],
                                     wall_impinged_pct_m09=s["wall_impinged_pct"], liquid_at_spark_pct=liq_pct,
                                     f_liquid_alcohol=f_fuel, Y_liquid_water=Y_wl, SMD_um=d,
                                     verdict=verdict(r["MIE_J"]),
                                     x_strip_for_MIE_50mJ=("never" if x50 is None else x50),
                                     x_strip_for_MIE_100mJ=("never" if x100 is None else x100), **r))
    return rows


def summarise(rows):
    def rng(k):
        vals = [r[k] for r in rows]
        return [min(vals), max(vals)]
    worst = max(rows, key=lambda r: r["MIE_J"])
    best = min(rows, key=lambda r: r["MIE_J"])
    counts = {}
    for r in rows:
        counts.setdefault(f"SMD {r['SMD_um']:g} um", {}).setdefault(r["verdict"], 0)
        counts[f"SMD {r['SMD_um']:g} um"][r["verdict"]] += 1
    by_case = {}
    for r in rows:
        e = by_case.setdefault(f"{r['case']} @ {r['SMD_um']:g} um", dict(n=0, misfire=0, marginal=0, ignites=0,
                                                                     MIE_mJ=[1e99, 0.0], S_eff_over_SL=[1e99, 0.0]))
        e["n"] += 1
        e[{"MISFIRE": "misfire", "MARGINAL": "marginal", "IGNITES": "ignites"}[r["verdict"].split()[0]]] += 1
        e["MIE_mJ"] = [min(e["MIE_mJ"][0], r["MIE_J"] * 1e3), max(e["MIE_mJ"][1], r["MIE_J"] * 1e3)]
        e["S_eff_over_SL"] = [min(e["S_eff_over_SL"][0], r["S_eff_over_SL"]), max(e["S_eff_over_SL"][1], r["S_eff_over_SL"])]
    xs = [r["x_strip_for_MIE_100mJ"] for r in rows if r["x_strip_for_MIE_100mJ"] != "never"]
    sel = lambda r: {k: r[k] for k in ("case", "atomiser", "variant", "SMD_um", "liquid_at_spark_pct", "f_liquid_alcohol",
                                        "Y_liquid_water", "MIE_J", "S_BL_over_SL", "S_eff_over_SL", "dT_heat_sink_K", "verdict")}
    return dict(n_rows=len(rows), verdict_counts=counts, by_case_and_smd=by_case,
                liquid_at_spark_pct=rng("liquid_at_spark_pct"), film_pct=rng("film_pct"),
                airborne_spark_pct=rng("airborne_spark_pct"), S_BL_over_SL=rng("S_BL_over_SL"),
                S_eff_over_SL=rng("S_eff_over_SL"), MIE_mJ=[x * 1e3 for x in rng("MIE_J")],
                x_strip_for_MIE_100mJ_range=([min(xs), max(xs)] if xs else None),
                worst=sel(worst), least_severe=sel(best))


def main(argv=None):
    t0 = time.perf_counter()
    args = io.argument_parser(MODULE).parse_args(None if argv is None else list(map(str, argv)))
    out = Path(args.out) / SUBDIR
    out.mkdir(parents=True, exist_ok=True)
    smds = SMD_STRIP_um if args.mode == "full" else (200.0, 500.0)
    rows = run(smds)
    io.write_csv(out / "design_points.csv", rows)
    key = summarise(rows)
    labels = {
        "status": "SENSITIVITY bound (ii). EXECUTED model runs; numerics VERIFIED by tests/test_spray_flame_film_strip.py; "
                  "NOT experimentally VALIDATED.",
        "validity": "Ballal-Lefebvre fitted at 0.1-1 atm, ~300 K, SMD ~20-200 um; applied at 25-35 bar, 650-820 K, 200-500 um "
                    "(EXTRAPOLATED). Upper bound: all film airborne at spark, no film evaporation.",
    }
    assumptions = {
        "liquid_at_spark": {"value": "Module 09 airborne + X_strip * Module 09 wall film, per species; X_strip = 1 (bound)"},
        "film_mass": {"value": "m_inj,s (1 - f_evap,s at spark) - m_airborne,s; f_evap,s from evap_profiles.json; closes with wall_impinged_pct",
                      "path": str(EP_PATH.relative_to(R.ROOT))},
        "smd": {"value": list(smds), "unit": "um", "rationale": "no strip-off SMD model in repo (Module 13); swept 200-500 um, all liquid lumped at that SMD"},
        "film_evaporation": {"value": "none before spark (conservative)"},
        "model": {"value": "unchanged Module 11 Ballal-Lefebvre S and MIE (sims/11_spray_flame/model.py), same thresholds 50/100 mJ"},
    }
    io.write_summary(out, MODULE + "/" + SUBDIR, VERSION, args.mode, assumptions, key | {"labels": labels},
                     {"tests": "tests/test_spray_flame_film_strip.py", "status": labels["status"]}, time.perf_counter() - t0)
    print(json.dumps({k: key[k] for k in ("verdict_counts", "liquid_at_spark_pct", "S_eff_over_SL", "S_BL_over_SL",
                                          "MIE_mJ", "x_strip_for_MIE_100mJ_range", "worst")}, indent=1, default=float))


if __name__ == "__main__":
    main()
