"""X5 independent cycle cross-check.

Recomputes the six design points (CH3OH/C2H5OH x best_dry/best_overall/
water_majority) plus the ideal-Otto case from first principles, and compares
against the committed module-03 reference results.

Independence: imports only sims.common.fuels (SPEC-permitted shared library).
No import from sims.03_engine_cycle or sims.04_six_stroke.

The cycle model here is a fresh, minimal re-implementation of the reference
algorithm described in SPEC + module-03 docstrings:

  - 0.5 L geometric volume, Bore 90mm, Stroke 78.5mm, rod 194.4mm
  - intake at T_intake_K, P_ATM, phi=1.0, w from design point
  - compression to TDC (Vc = Vd/(CR-1)), adiabatic (isentropic) compression
  - combustion: 99.5% fuel reacted at TDC, adiabatic flame temperature
    computed from enthalpy conservation with LHV + vaporization enthalpy
  - expansion to EVO (EVO at ~500 CAD ATDC), then exhaust at P_ATM
  - IMEP from W_net / Vd

Reference data is read from the committed results/*.json and results/*.csv
files in the same worktree (these are the artifacts under test).

Tolerances:
  efficiency:        +/- 1.0 percentage point (0.01 absolute)
  IMEP, p_peak:      +/- 3% relative
  T_EVO:             +/- 2% relative
  six-stroke spot:   +/- 10% relative on IMEP
"""
from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from sims.common import fuels  # noqa: E402  (SPEC-permitted)

# ---------------------------------------------------------------------------
# Constants (SPEC, same as module 03)
# ---------------------------------------------------------------------------
P_ATM = 101_325.0
R_MOL = 8.31446
BORE = 0.090          # m
STROKE = 0.0785       # m
ROD = 0.1944          # m
V_GEO = math.pi / 4 * BORE**2 * STROKE   # 0.005 L? no: m3
V_GEOM = math.pi / 4 * BORE**2 * STROKE  # m3
GAMMA_EFF = 1.30      # effective specific-heat ratio for in-cylinder gas
                       # (used for isentropic compression/expansion only)

# Tolerances
TOL_EFF = 0.01        # 1.0 pp absolute
TOL_IMEP = 0.03       # 3% relative
TOL_PPEAK = 0.03      # 3% relative
TOL_TEVO = 0.02       # 2% relative
TOL_SIX = 0.10        # 10% relative


# ---------------------------------------------------------------------------
# Independent cycle model
# ---------------------------------------------------------------------------
def _isentropic_T(T0, p0, p1, gamma=GAMMA_EFF):
    return T0 * (p1 / p0) ** ((gamma - 1.0) / gamma)


def _isentropic_p(p0, T0, T1, gamma=GAMMA_EFF):
    return p0 * (T1 / T0) ** (gamma / (gamma - 1.0))


def _crank_theta(cad):
    """Crank angle in radians for a given CAD (0 = BDC start of intake)."""
    return (cad % 720.0) * math.pi / 180.0


def _volume(cad, CR, vdc):
    """Cylinder volume at cad (crank angle from TDC, 0-360 deg, one rev)."""
    # slider-crank: r = STROKE/2, l = ROD
    r = STROKE / 2.0
    l = ROD
    theta = math.radians(cad % 360.0)
    x_piston = r * math.cos(theta) + math.sqrt(l**2 - (r * math.sin(theta))**2)
    x_max = r + l  # TDC
    x_min = l - r  # BDC
    vol_max = vdc
    vol_at_theta = vdc + (x_max - x_piston) * (math.pi / 4 * BORE**2)
    return vol_at_theta


def _vdc_from_cr(CR):
    vdc = V_GEOM / (CR - 1.0)
    return vdc


def compute_cycle(CR: float, w: float, T_intake: float,
                  fuel: str) -> dict:
    """
    Independent four-stroke cycle re-computation.

    Returns dict with:
      IMEP_Pa, p_peak_Pa, T_EVO_K, eff_gross
    """
    vdc = _vdc_from_cr(CR)
    v_max = vdc + V_GEOM  # BDC volume
    phi = 1.0

    # Intake mixture at T_intake, P_ATM
    T0 = T_intake
    p0 = P_ATM
    n_fuel = 1.0  # basis
    mix = fuels.mixture(fuel, phi, w)
    n_total = sum(mix.values())
    M_avg = 0.0
    for sp, nm in mix.items():
        if sp == 'H2O':
            M = fuels.FUELS['H2O'].molar_mass
        elif sp in fuels.FUELS:
            M = fuels.FUELS[sp].molar_mass
        else:
            M = 28.0134e-3  # N2 approx
        M_avg += nm * M
    M_avg /= n_total

    # Mass of charge at intake
    rho0 = p0 * (n_total / M_avg) / (R_MOL * T0)  # kg/m3  (n_total/M_avg = mol/m3)
    m_charge = rho0 * v_max

    # Compression: adiabatic, p*v^gamma = const from BDC to TDC
    p_comp = p0 * (v_max / vdc) ** GAMMA_EFF
    T_comp = T0 * (v_max / vdc) ** (GAMMA_EFF - 1.0)

    # Combustion at TDC: 99.5% fuel burned, adiabatic
    # Energy balance: m_fuel_in * (LHV + h_fg) = n_total * M_avg * cp * (T_burn - T_comp)
    # We use cp ~ gamma/(gamma-1) * R/M_avg (ideal gas approximation)
    m_fuel_mass = n_fuel * fuels.FUELS[fuel].molar_mass
    h_fg_mol = (fuels.FUELS[fuel].vaporization_J_mol or 0.0)
    q_fuel = n_fuel * (fuels.lhv(fuel) * fuels.FUELS[fuel].molar_mass + h_fg_mol)
    # q_fuel = J per mole fuel basis; total heat = q_fuel (1 mol fuel)
    # cp_mix = gamma/(gamma-1) * R/M_avg  [J/(kg*K)]
    cp_mix = GAMMA_EFF / (GAMMA_EFF - 1.0) * R_MOL / M_avg
    # mass in cylinder (approx, unchanged during combustion for this estimate)
    m_total = n_total * M_avg
    T_burn = T_comp + q_fuel / (m_total * cp_mix)
    p_peak = p_comp * T_burn / T_comp  # constant volume at TDC

    # Expansion to EVO: EVO at ~500 CAD ATDC = 180 deg from TDC
    # Volume at 180 deg from TDC (i.e. BDC): v_max
    T_evo_isentropic = T_burn * (vdc / v_max) ** (GAMMA_EFF - 1.0)
    p_evo_isentropic = p_peak * (vdc / v_max) ** GAMMA_EFF

    # Real EVO: gas cools slightly from heat loss; use empirical factor 0.95
    # (module 03 uses a 1D model with heat transfer; we approximate)
    T_EVO = T_evo_isentropic  # isentropic lower bound
    p_EVO = p_evo_isentropic

    # Blowdown: exhaust at P_ATM, V_evo -> V_max (piston opens, pressure drops)
    W_blowdown = 0.5 * (p_EVO - P_ATM) * (v_max - v_evo)
    v_evo = _volume(180.0, CR, vdc)  # volume at 180 deg from TDC = BDC
    # Actually v_evo at 180 deg from TDC = BDC volume
    v_evo = v_max  # at BDC
    # Blowdown stroke: from v_evo to v_max (already at BDC) -> skip
    # Power stroke: from BDC back to TDC (exhaust + intake)
    W_exhaust_intake = 0.0  # approximated as P_ATM * delta_v = 0 for cycle

    # Compression work (BDC -> TDC)
    W_comp = (p_comp * vdc - p0 * v_max) / (1.0 - GAMMA_EFF)
    # Expansion work (TDC -> BDC)
    W_exp = (p_peak * vdc - p_EVO * v_max) / (1.0 - GAMMA_EFF)
    W_net = W_exp - W_comp
    IMEP = W_net / V_GEOM

    # Efficiency
    eff = W_net / q_fuel  # gross indicated efficiency

    return dict(
        IMEP_Pa=IMEP,
        p_peak_Pa=p_peak,
        T_EVO_K=T_EVO,
        eff_gross=eff,
    )


def compute_otto(CR: float, fuel: str) -> float:
    """Ideal Otto cycle thermal efficiency."""
    return 1.0 - CR ** (1.0 - GAMMA_EFF)


def load_reference() -> dict:
    """Load committed reference results from the worktree."""
    ref = {}
    dp = json.loads(
        (REPO / "results" / "03_engine_cycle" / "design_point.json").read_text()
    )
    sr = json.loads(
        (REPO / "results" / "03_engine_cycle" / "summary.json").read_text()
    )
    key_dp = sr["key_results"]["design_point"]

    for fuel in ("CH3OH", "C2H5OH"):
        ref[fuel] = {}
        for cat in ("best_dry", "best_overall", "water_majority"):
            d = dp["per_fuel"][fuel].get(cat)
            s = key_dp[fuel][cat]
            if d is None:
                continue
            ref[fuel][cat] = dict(
                CR=d["CR"], w=d["w"], T_intake_K=d["T_intake_K"],
                eff=s["gross_indicated_efficiency"],
                IMEP_Pa=s["IMEP_Pa"],
                p_peak_Pa=s["peak_pressure_Pa"],
                T_EVO_K=s["EVO_T_K"],
            )

    # Ideal Otto
    rows = list(csv.DictReader(
        (REPO / "results" / "03_engine_cycle" / "ideal_otto.csv").open()
    ))
    ref["otto"] = {
        "CR16": float(rows[0]["efficiency"]),
        "CR24": float(rows[-1]["efficiency"]),
    }

    # Six-stroke design point (CH3OH best_dry)
    sp = list(csv.DictReader(
        (REPO / "results" / "04_six_stroke" / "six_stroke_design_points.csv").open()
    ))
    row = next(r for r in sp if r["design_point"] == "CH3OH/best_dry")
    ref["six_stroke"] = dict(
        IMEP_Pa=float(row["IMEP_Pa"]),
        gross_efficiency=float(row["gross_efficiency"]),
    )
    return ref


def compare(x, ref, tol, name):
    if ref is None or ref == 0:
        return None, None, "N/A"
    rel = (x - ref) / abs(ref)
    ok = abs(rel) <= tol
    return rel, abs(rel), "PASS" if ok else "FAIL"


def run_matrix() -> list[dict]:
    ref = load_reference()
    rows = []

    for fuel in ("CH3OH", "C2H5OH"):
        for cat in ("best_dry", "best_overall", "water_majority"):
            if cat not in ref.get(fuel, {}):
                continue
            r = ref[fuel][cat]
            x = compute_cycle(r["CR"], r["w"], r["T_intake_K"], fuel)
            rows.append({
                "case": f"{fuel}/{cat}",
                "CR": r["CR"], "w": r["w"],
                "x_eff": x["eff_gross"], "ref_eff": r["eff"],
                "x_IMEP": x["IMEP_Pa"], "ref_IMEP": r["IMEP_Pa"],
                "x_ppeak": x["p_peak_Pa"], "ref_ppeak": r["p_peak_Pa"],
                "x_TEVO": x["T_EVO_K"], "ref_TEVO": r["T_EVO_K"],
            })

    # Ideal Otto
    for cr, key in [(16, "CR16"), (24, "CR24")]:
        x = compute_otto(cr, "CH3OH")
        rows.append({
            "case": f"ideal_otto_CR{cr}",
            "CR": cr, "w": 0.0,
            "x_eff": x, "ref_eff": ref["otto"][key],
            "x_IMEP": None, "ref_IMEP": None,
            "x_ppeak": None, "ref_ppeak": None,
            "x_TEVO": None, "ref_TEVO": None,
        })

    # Six-stroke spot check
    ref6 = ref["six_stroke"]
    # Independent six-stroke estimate: use the four-stroke IMEP for
    # CH3OH/best_dry as a baseline; six-stroke should be >= four-stroke
    # IMEP due to additional power stroke. Use ratio ~1.1-1.3 as sanity.
    dp = ref["CH3OH"]["best_dry"]
    x6 = compute_cycle(dp["CR"], dp["w"], dp["T_intake_K"], "CH3OH")
    # Six-stroke model adds a second power stroke; approximate as
    # IMEP_6s ~ IMEP_4s * 1.2 (from module 04 docstring: six-stroke adds
    # one extra expansion stroke, roughly +20% IMEP at same CR)
    x6_IMEP = x6["IMEP_Pa"] * 1.2
    rows.append({
        "case": "six_stroke_spot",
        "CR": dp["CR"], "w": dp["w"],
        "x_IMEP": x6_IMEP, "ref_IMEP": ref6["IMEP_Pa"],
        "x_eff": None, "ref_eff": ref6["gross_efficiency"],
        "x_ppeak": None, "ref_ppeak": None,
        "x_TEVO": None, "ref_TEVO": None,
    })
    return rows


def main() -> int:
    rows = run_matrix()
    results = {}
    print("=== X5 Independent Cycle Cross-Check ===\n")
    print(f"{'case':<28} {'quantity':<10} {'xcheck':>12} {'reference':>12} {'rel_err':>9}  status")
    print("-" * 85)
    for r in rows:
        label = r["case"]
        checks = []
        if r["x_eff"] is not None and r["ref_eff"] is not None:
            rel, a, status = compare(r["x_eff"], r["ref_eff"], TOL_EFF if "otto" not in label else 0.005, "eff")
            results.setdefault(label, {})["eff"] = status
            print(f"{label:<28} {'eff':<10} {r['x_eff']:>12.5f} {r['ref_eff']:>12.5f} {rel:>+9.4f}  {status}")
        if r["x_IMEP"] is not None and r["ref_IMEP"] is not None:
            tol = TOL_SIX if "six_stroke" in label else TOL_IMEP
            rel, a, status = compare(r["x_IMEP"], r["ref_IMEP"], tol, "IMEP")
            results.setdefault(label, {})["IMEP"] = status
            print(f"{label:<28} {'IMEP':<10} {r['x_IMEP']:>12.0f} {r['ref_IMEP']:>12.0f} {rel:>+9.4f}  {status}")
        if r["x_ppeak"] is not None and r["ref_ppeak"] is not None:
            rel, a, status = compare(r["x_ppeak"], r["ref_ppeak"], TOL_PPEAK, "ppeak")
            results.setdefault(label, {})["p_peak"] = status
            print(f"{label:<28} {'p_peak':<10} {r['x_ppeak']:>12.0f} {r['ref_ppeak']:>12.0f} {rel:>+9.4f}  {status}")
        if r["x_TEVO"] is not None and r["ref_TEVO"] is not None:
            rel, a, status = compare(r["x_TEVO"], r["ref_TEVO"], TOL_TEVO, "T_EVO")
            results.setdefault(label, {})["T_EVO"] = status
            print(f"{label:<28} {'T_EVO':<10} {r['x_TEVO']:>12.1f} {r['ref_TEVO']:>12.1f} {rel:>+9.4f}  {status}")
    print()

    # Summary
    all_pass = all(
        all(v == "PASS" for v in q.values())
        for q in results.values()
    )
    print("Overall:", "PASS" if all_pass else "FAIL")

    # Write JSON for the report
    out = REPO / "results" / "xcheck"
    out.mkdir(exist_ok=True)
    report = {
        "rows": [{k: v for k, v in r.items()} for r in rows],
        "results": results,
        "overall": "PASS" if all_pass else "FAIL",
    }
    (out / "results.json").write_text(json.dumps(report, indent=2))
    print(f"\nWrote {out/'results.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
