"""X5: Independent Cantera-based 0-D cycle cross-check of Module 03/04.

Independent implementation on Cantera ReactorNet. Does NOT reuse module 03 code;
may reuse only sims/common/fuels.py (for mixtures, LHV, mechanism loading).

Approach:
  - IdealGasReactor with a moving piston wall (slider-crank volume law).
  - Prescribed Wiebe heat release imposed as a heat-flux sink on the wall
    (positive heat_flux in Cantera 3.2 leaves the reactor, so combustion is
    added with a negative sign).
  - Woschni convection via wall.heat_transfer_coeff to a wall reservoir.
  - CoolProp water evaporation as a latent-heat energy sink on the same
    evaporation schedule (IVC -> -30 CAD), saturation-capped like Module 03.
  - Constant-volume, adiabatic ideal-Otto check against the analytic formula.

All Wiebe / Woschni / geometry formulas are re-derived here (SPEC 0/6/10),
NOT imported from module 03.
"""

import json
import math
import time
from pathlib import Path

import cantera as ct
import numpy as np
from CoolProp.CoolProp import PropsSI

from sims.common import fuels

# ---------------------------------------------------------------- geometry
BORE = 0.086          # m  (SPEC: Module 03 engine, identical to cross-check)
STROKE = 0.086        # m
ROD = 0.145           # m
RPM = 2000.0
OMEGA = RPM * 2.0 * math.pi / 60.0
RAD = math.pi / 180.0
RESIDUAL_FRACTION = 0.05
P_IVC = 1.0e5
PHI = 1.0
WATER_MAJORITY_W = 0.6
WATER_MAJORITY_T_INTAKE = 360.0
WOSCHNI_C = 3.26
WOSCHNI_C1 = 2.28
WOSCHNI_C2 = 3.24e-3
WALL_T = 450.0
WIEBE_A = 5.0
WIEBE_M = 2.0
COMBUSTION_EFFICIENCY = 0.88
# Water evaporation schedule
EVAP_END_RAD = -30.0 * RAD
F_EVAP_INTAKE = 0.5

WATER_T_TRIPLE = float(PropsSI("Ttriple", "Water"))
WATER_T_CRIT = float(PropsSI("Tcrit", "Water"))


def displacement():
    return math.pi * BORE**2 / 4.0 * STROKE


def volume(theta_rad, cr):
    """Slider-crank volume [m3], theta after TDC fire."""
    a = STROKE / 2.0
    V_swept = displacement()
    V_clearance = V_swept / (cr - 1.0)
    s = a * math.cos(theta_rad) + math.sqrt(ROD**2 - (a * math.sin(theta_rad))**2)
    dist = ROD + a - s
    return V_clearance + (math.pi * BORE**2 / 4.0 * dist)


def wall_area(V):
    return 2.0 * math.pi * BORE**2 / 4.0 + 4.0 * V / BORE


def piston_speed(theta_rad):
    """dV/dt in m3/s at crank angle theta."""
    a = STROKE / 2.0
    A_p = math.pi * BORE**2 / 4.0
    dV_dtheta = A_p * a * math.sin(theta_rad) * (
        1.0 + (a * math.cos(theta_rad)) / math.sqrt(ROD**2 - (a * math.sin(theta_rad))**2))
    return dV_dtheta * OMEGA


def wiebe_fraction(theta_rad, ca50_rad, duration_rad):
    a, m = WIEBE_A, WIEBE_M
    z = lambda x: (-math.log1p(-x) / a) ** (1.0 / (m + 1.0))
    scale = duration_rad / (z(0.9) - z(0.1))
    start = ca50_rad - scale * z(0.5)
    progress = max(0.0, (theta_rad - start) / scale)
    if progress >= 1.0:
        return 1.0
    return -math.expm1(-a * progress ** (m + 1.0))


def water_p_sat(T):
    if T >= WATER_T_CRIT:
        return math.inf
    if T < WATER_T_TRIPLE:
        return 0.0
    return float(PropsSI("P", "T", T, "Q", 1, "Water"))


def wiebe_ca50_from_deg(ca50_deg):
    return ca50_deg * RAD


def wiebe_duration_from_deg(duration_deg):
    return duration_deg * RAD


def flame_speed_to_duration(sl, sl_ref):
    """Module 03: 10-90 % duration = ref * (S_L,ref / S_L)^0.5, capped at 80 deg."""
    cap = 80.0 * RAD
    ref_dur = 25.0 * RAD
    return min(cap, ref_dur * (sl_ref / sl) ** 0.5)


# ------------------------------------------------------------------- case
def design_points_from_module03():
    """Read the design points that Module 03 reported, re-derived from its
    design_point.json so this cross-check re-runs exactly those conditions."""
    path = Path("results/03_engine_cycle/design_point.json")
    with open(path) as f:
        dp = json.load(f)
    out = {}
    for fuel in ("CH3OH", "C2H5OH"):
        for cat in ("best_dry", "best_overall", "best_water_majority"):
            seg = dp["per_fuel"][fuel][cat]
            if seg is None:
                continue
            key = f"{fuel}/{cat}"
            out[key] = dict(
                fuel=fuel, CR=seg["CR"], w=seg["w"], T_intake_K=seg["T_intake_K"],
                ca50_deg=seg["ca50_used_deg"], burn_10_90_deg=seg["burn_10_90_deg"],
                gross_efficiency=seg["gross_indicated_efficiency"],
                IMEP_Pa=seg["IMEP_Pa"],
                peak_pressure_Pa=seg["peak_pressure_Pa"],
                EVO_T_K=seg["EVO_T_K"],
                EVO_p_Pa=seg["EVO_p_Pa"],
                peak_T_K=seg["peak_temperature_K"],
                S_L_m_s=seg["S_L_m_s"],
            )
    return out


def sixstroke_reference():
    """One six-stroke spot check point from Module 04."""
    path = Path("results/04_six_stroke/summary.json")
    with open(path) as f:
        s4 = json.load(f)
    fr = s4["key_results"]["four_stroke"]
    return fr  # contains efficiency, IMEP, EVO_T_K for the four-stroke base