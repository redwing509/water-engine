"""X1 chemistry sweep: AramcoMech 2.0, T_ad and S_L for CH3OH and C2H5OH.

Conditions (task contract):
  T_ad: 300 K and 400 K, 1 atm, phi = 1, w = 0.
  S_L : 400 K, 1 atm, phi = 1, w = 0, 0.3, 0.6.

Uses sims/common/fuels.py for mixture construction (correct stoichiometry,
liquid-alcohol latent heat accounted separately) and mechanisms/aramco20.yaml
as the gas phase.  Output: results/xcheck/chem_x1_*.csv and a summary JSON.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import cantera as ct

from sims.common import fuels, io

REPO_ROOT = Path(__file__).resolve().parents[2]
MECH = REPO_ROOT / "mechanisms" / "aramco20.yaml"
OUT = REPO_ROOT / "results" / "xcheck"

FUELS_X1 = ("CH3OH", "C2H5OH")
T_AD_K = (300.0, 400.0)
P_ATM = ct.one_atm
PHI = 1.0
W_S_L = (0.0, 0.3, 0.6)
T_SL_K = 400.0


def _gas(fuel, phi, w, T_K, p_Pa):
    gas = ct.Solution(str(MECH))
    gas.TPX = T_K, p_Pa, fuels.mixture(fuel, phi, w, mech=str(MECH))
    return gas


def _record(fuel, phi, w, T_K, p_Pa):
    return dict(fuel=fuel, phi=phi, w=w, T_unburned_K=T_K, p_Pa=p_Pa,
                mechanism="mechanisms/aramco20.yaml", mechanism_fallback=False)


def adiabatic_temperature(fuel, phi, w, T_K, p_Pa):
    row = _record(fuel, phi, w, T_K, p_Pa)
    row.update(T_ad_K=None, status="unavailable", reason="")
    try:
        gas = _gas(fuel, phi, w, T_K, p_Pa)
        gas.equilibrate("HP")
        row.update(T_ad_K=float(gas.T), status="computed")
    except ct.CanteraError as exc:
        row.update(status="solver_error", reason=str(exc))
    return row


def flame_speed(fuel, phi, w, T_K, p_Pa):
    row = _record(fuel, phi, w, T_K, p_Pa)
    row.update(S_L_m_s=None, status="no_flame", reason="", attempted=False,
               grid_points=None)
    try:
        gas = _gas(fuel, phi, w, T_K, p_Pa)
        flame = ct.FreeFlame(gas, width=0.03)
        flame.transport_model = "mixture-averaged"
        flame.soret_enabled = False
        flame.set_refine_criteria(ratio=3.0, slope=0.07, curve=0.14)
        flame.solve(loglevel=0, auto=True)
        speed = float(flame.velocity[0])
        row.update(S_L_m_s=speed if math.isfinite(speed) else None,
                   grid_points=len(flame.grid))
        if not math.isfinite(speed) or speed < 0.02:
            row["reason"] = "Solved speed below propagation cutoff or nonfinite"
        else:
            row.update(status="computed", reason="")
    except ct.CanteraError as exc:
        row.update(status="solver_error", reason=str(exc))
    return row


def main():
    start = time.perf_counter()
    adiabatic, flames = [], []
    for fuel in FUELS_X1:
        for T in T_AD_K:
            adiabatic.append(adiabatic_temperature(fuel, PHI, 0.0, T, P_ATM))
        for w in W_S_L:
            flames.append(flame_speed(fuel, PHI, w, T_SL_K, P_ATM))

    io.write_csv(OUT / "chem_x1_adiabatic.csv", adiabatic)
    io.write_csv(OUT / "chem_x1_flame_speed.csv", flames)

    payload = dict(
        mechanism="mechanisms/aramco20.yaml",
        mechanism_sha256="ff445870610f4bc1129f061e1823c0939dc5d44ce15996cb4ee85cd6ff72db33",
        git_sha=io.git_sha(),
        adiabatic=adiabatic,
        flame_speed=flames,
        runtime_s=time.perf_counter() - start,
    )
    (OUT / "chem_x1_run.json").write_text(
        json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    for r in adiabatic:
        print(f"T_ad {r['fuel']} T={r['T_unburned_K']:.0f} w={r['w']} -> "
              f"{r['T_ad_K'] if r['T_ad_K'] is None else round(r['T_ad_K'],2)} K "
              f"{r['status']}")
    for r in flames:
        print(f"S_L  {r['fuel']} w={r['w']} -> "
              f"{r['S_L_m_s'] if r['S_L_m_s'] is None else round(r['S_L_m_s'],5)} m/s "
              f"{r['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())