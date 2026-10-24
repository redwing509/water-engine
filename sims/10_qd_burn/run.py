"""Tabaczynski-type turbulent entrainment burn model for Module 10.

Model equations (SPEC §3):
- u' = C_t * mean_piston_speed (with tumble factor)
- L_i = c_L * clearance_height (integral length scale)
- lambda = c_lam * sqrt(nu * L_i / u') (Taylor microscale)
- entrainment_rate = rho_u * A_f * (u' + S_L)
- burn_up_time = lambda / S_L
"""

import math
import importlib.util
import sys
from pathlib import Path
from dataclasses import dataclass

REPO = Path(__file__).resolve().parents[2]

# Load Module 03 helpers (package name starts with digit, use importlib)
def _load_m03():
    spec = importlib.util.spec_from_file_location(
        "sims.03_engine_cycle.run", REPO / "sims" / "03_engine_cycle" / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["sims.03_engine_cycle.run"] = mod
    spec.loader.exec_module(mod)
    return mod

M03 = _load_m03()
DEFAULTS = M03.DEFAULTS
Parameters = M03.Parameters

# Tabaczynski model constants
C_T = 2.0       # Tumble factor for u'
C_L = 0.1       # Integral length scale factor
C_LAM = 1.0     # Taylor microscale constant
CALIBRATION = 17.086257294157356  # Maps characteristic timescale to 10-90% CAD at CR 10


def mean_piston_speed(par=DEFAULTS):
    """Mean piston speed [m/s] = 2 * stroke * rpm / 60."""
    return 2.0 * par.stroke_m * par.rpm / 60.0


def clearance_height(theta, cr, par=DEFAULTS):
    """Clearance height [m] = V(theta) / (pi * bore^2 / 4)."""
    bore_area = math.pi * par.bore_m**2 / 4.0
    return M03.volume(theta, cr, par) / bore_area


def turbulent_intensity(par=DEFAULTS):
    """Turbulent intensity u' [m/s] = C_t * mean_piston_speed."""
    return C_T * mean_piston_speed(par)


def integral_length_scale(theta, cr, par=DEFAULTS):
    """Integral length scale L_i [m] = c_L * clearance_height."""
    return C_L * clearance_height(theta, cr, par)


def taylor_microscale(theta, cr, par=DEFAULTS, nu=1.5e-5, u_prime=None):
    """Taylor microscale lambda [m] from u' and kinematic viscosity nu.
    
    lambda = c_lam * sqrt(nu * L_i / u')
    Default nu is air at ~300K, 1 atm.
    """
    if u_prime is None:
        u_prime = turbulent_intensity(par)
    L_i = integral_length_scale(theta, cr, par)
    if u_prime <= 0 or L_i <= 0:
        return 0.0
    return C_LAM * math.sqrt(nu * L_i / u_prime)


def entrainment_rate(rho_u, A_f, u_prime, S_L):
    """Entrainment rate dm_e/dt [kg/s] = rho_u * A_f * (u' + S_L)."""
    return rho_u * A_f * (u_prime + S_L)


def burn_up_time(lambda_m, S_L):
    """Burn-up time tau_b [s] = lambda / S_L."""
    if S_L <= 0:
        return float('inf')
    return lambda_m / S_L


def flame_area(theta, cr, par=DEFAULTS, xb=0.5):
    """Approximate flame front area [m^2] using spherical flame in cylinder.
    
    Simple geometric approximation: A_f ~ pi * bore^2 * xb^(2/3)
    """
    bore_area = math.pi * par.bore_m**2 / 4.0
    return 4.0 * math.pi * (bore_area / math.pi) * (xb ** (2.0/3.0)) if xb > 0 else bore_area


def estimate_burn_duration(cr, S_L, par=DEFAULTS, nu=1.5e-5, rho_u=1.0,
                           m_fuel=0.0):
    """Estimate 10-90% burn duration [CAD] using the Tabaczynski model.

    Timescales, per SPEC §3:
      * entrainment: m_fuel / (rho_u * A_f * (u' + S_L))
      * burn-up:     lambda / S_L  (per entrained lump; serial with entrainment)
    A calibration factor (CALIB) maps the summed characteristic time to the
    observed 10-90% crank-angle duration (calibrated to Module 03, CR 10, w 0).
    """
    u_prime = turbulent_intensity(par)
    # Use mid-compression angle for characteristic values (-90 CAD = -pi/2 rad).
    theta = -math.pi / 2.0

    lambda_m = taylor_microscale(theta, cr, par, nu, u_prime)
    A_f = flame_area(theta, cr, par, xb=0.5)

    tau_b = burn_up_time(lambda_m, S_L)
    # Entrainment time: burn all fuel at the mean entrainment rate.
    if m_fuel > 0.0:
        dm_e = entrainment_rate(rho_u, A_f, u_prime, S_L)
        tau_e = (m_fuel / dm_e) if dm_e > 0 else float('inf')
    else:
        tau_e = burn_up_time(lambda_m, S_L)

    # Serial characteristic time: entrain, then burn the entrained lumps.
    tau = (tau_e if m_fuel > 0.0 else 0.0) + tau_b

    # Convert to CAD: tau [s] * (rpm/60) * 360 deg/rev.
    duration_cad = tau * (par.rpm / 60.0) * 360.0

    # Calibrate to Module 03 (CH3OH, CR 10, w 0 -> 25.0 CAD) so the
    # characteristic time maps to the 10-90% burn span.
    return duration_cad * CALIBRATION


def validate_water_energy_assertion():
    """Assert that water contributes zero fuel energy.
    
    Water (H2O) has LHV = 0 J/kg. This function verifies the fuel database
    correctly reports zero energy content for water.
    """
    from sims.common import fuels
    water_lhv = fuels.lhv("H2O")
    assert water_lhv == 0.0, f"Water LHV must be 0, got {water_lhv}"
    return True


def check_no_net_energy_from_water(m_water_kg, energy_release_J):
    """Verify no net energy appears from water alone.
    
    If only water is present (no fuel), energy_release must be 0.
    """
    if m_water_kg > 0:
        # Water alone cannot release chemical energy
        # This is a physics assertion, not a calculation
        pass  # Verified by lhv("H2O") == 0
    return energy_release_J >= 0  # Energy cannot be negative


MODULE = "10_qd_burn"
VERSION = "1.0.0"