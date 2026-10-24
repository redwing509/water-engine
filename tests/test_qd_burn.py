"""Focused tests for Module 10 Tabaczynski turbulent entrainment model.

Validates:
1. Reproduce Module 03 w=0 CA10-90 at CR 10 within ±30% (target: 25 CAD).
2. Water contributes zero fuel energy (LHV assertion).
3. No net energy from water appears.
"""

import math
import pytest
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[1]


def _load_qd_burn():
    """Load sims/10_qd_burn/run.py (package name starts with a digit)."""
    from conftest import load_sims_module
    return load_sims_module("sims.10_qd_burn.run")


qd = _load_qd_burn()
(
    mean_piston_speed,
    clearance_height,
    turbulent_intensity,
    integral_length_scale,
    taylor_microscale,
    entrainment_rate,
    burn_up_time,
    flame_area,
    estimate_burn_duration,
    validate_water_energy_assertion,
    check_no_net_energy_from_water,
    C_T,
    C_L,
    C_LAM,
    DEFAULTS,
) = (
    qd.mean_piston_speed,
    qd.clearance_height,
    qd.turbulent_intensity,
    qd.integral_length_scale,
    qd.taylor_microscale,
    qd.entrainment_rate,
    qd.burn_up_time,
    qd.flame_area,
    qd.estimate_burn_duration,
    qd.validate_water_energy_assertion,
    qd.check_no_net_energy_from_water,
    qd.C_T,
    qd.C_L,
    qd.C_LAM,
    qd.DEFAULTS,
)


def test_constants_defined():
    """Verify Tabaczynski model constants are defined."""
    assert C_T == 2.0
    assert C_L == 0.1
    assert C_LAM == 1.0


def test_mean_piston_speed():
    """Mean piston speed = 2 * stroke * rpm / 60."""
    # DEFAULTS: stroke=0.086m, rpm=2000
    expected = 2.0 * 0.086 * 2000.0 / 60.0
    assert mean_piston_speed() == pytest.approx(expected)


def test_clearance_height_at_tdc():
    """Clearance height at TDC (theta=0) for CR=10."""
    cr = 10.0
    theta = 0.0
    h = clearance_height(theta, cr)
    # V_tdc = displacement / (cr - 1)
    # h = V_tdc / bore_area
    bore_area = math.pi * DEFAULTS.bore_m**2 / 4.0
    v_tdc = DEFAULTS.stroke_m * bore_area / (cr - 1.0)
    expected_h = v_tdc / bore_area
    assert h == pytest.approx(expected_h)


def test_turbulent_intensity():
    """u' = C_T * mean_piston_speed."""
    u_prime = turbulent_intensity()
    expected = C_T * mean_piston_speed()
    assert u_prime == pytest.approx(expected)


def test_integral_length_scale():
    """L_i = c_L * clearance_height."""
    cr = 10.0
    theta = -math.pi / 2.0  # -90 CAD
    L_i = integral_length_scale(theta, cr)
    h = clearance_height(theta, cr)
    assert L_i == pytest.approx(C_L * h)


def test_taylor_microscale():
    """lambda = c_lam * sqrt(nu * L_i / u')."""
    cr = 10.0
    theta = -math.pi / 2.0
    nu = 1.5e-5
    u_prime = turbulent_intensity()
    L_i = integral_length_scale(theta, cr)
    lambda_m = taylor_microscale(theta, cr, nu=nu, u_prime=u_prime)
    expected = C_LAM * math.sqrt(nu * L_i / u_prime)
    assert lambda_m == pytest.approx(expected)


def test_entrainment_rate():
    """dm_e/dt = rho_u * A_f * (u' + S_L)."""
    rho_u = 1.0
    A_f = 0.01
    u_prime = 10.0
    S_L = 0.7
    rate = entrainment_rate(rho_u, A_f, u_prime, S_L)
    expected = rho_u * A_f * (u_prime + S_L)
    assert rate == pytest.approx(expected)


def test_burn_up_time():
    """tau_b = lambda / S_L."""
    lambda_m = 1e-4
    S_L = 0.7
    tau = burn_up_time(lambda_m, S_L)
    expected = lambda_m / S_L
    assert tau == pytest.approx(expected)


def test_burn_up_time_zero_sl():
    """tau_b = inf when S_L = 0."""
    assert burn_up_time(1e-4, 0.0) == float('inf')


def test_flame_area():
    """Flame area scales with xb^(2/3)."""
    A_0 = flame_area(0, 10, xb=0.01)
    A_1 = flame_area(0, 10, xb=0.5)
    assert A_1 > A_0


def test_water_contributes_zero_fuel_energy():
    """Assert water LHV = 0 J/kg."""
    assert validate_water_energy_assertion() is True


def test_no_net_energy_from_water():
    """Verify no net energy appears from water alone."""
    # Water alone (m_fuel=0) should release 0 energy
    assert check_no_net_energy_from_water(0.001, 0.0) is True
    # Energy cannot be negative
    assert check_no_net_energy_from_water(0.001, -100) is False
    assert check_no_net_energy_from_water(0.001, 100) is True


def test_burn_duration_cr10_w0_validation():
    """Module 10 must reproduce Module 03 CA10-90 at CR=10, w=0 within ±30%.
    
    Module 03 target: 25.0 CAD (from cycle_points.csv, CH3OH/CR10/w0/T320).
    Tolerance: 25.0 * (1 ± 0.3) = [17.5, 32.5] CAD.
    """
    cr = 10.0
    S_L = 0.7209888530581408  # Module 03 value for CH3OH at w=0
    duration = estimate_burn_duration(cr, S_L)
    
    target = 25.0
    tolerance = 0.30
    lower = target * (1.0 - tolerance)
    upper = target * (1.0 + tolerance)
    
    assert lower <= duration <= upper, (
        f"Burn duration {duration:.2f} CAD outside [{lower:.2f}, {upper:.2f}] CAD "
        f"(target {target:.2f} ±{tolerance*100:.0f}%)"
    )


def test_burn_duration_scales_with_cr():
    """Burn duration should decrease with increasing CR (higher turbulence)."""
    S_L = 0.72
    d_cr10 = estimate_burn_duration(10.0, S_L)
    d_cr20 = estimate_burn_duration(20.0, S_L)
    assert d_cr20 < d_cr10, "Higher CR should give shorter burn duration"
