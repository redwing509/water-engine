"""Atomiser SMD correlations and Rosin-Rammler discretisation (SI units).

* Nukiyama & Tanasawa (1939), Trans. Soc. Mech. Eng. Japan 5:68, as given in
  Lefebvre (1989), Atomization and Sprays, eq. 6.1 (CGS units inside):
  SMD[um] = 585/U * sqrt(sigma/rho) + 597 (mu/sqrt(sigma rho))^0.45 (1000 Ql/Qa)^1.5
  with U [m/s], sigma [dyn/cm], rho [g/cm3], mu [P].
* Lefebvre (1987) pressure-swirl (simplex) correlation, Lefebvre (1989)
  eq. 6.47: SMD = 2.25 sigma^0.25 mu^0.25 mdot^0.25 dP^-0.5 rho_A^-0.25 (SI).
* Lang (1962), J. Acoust. Soc. Am. 34:6: d = 0.34 (8 pi sigma/(rho f^2))^(1/3).
  Lang's d is a median drop size; it is used here as the SMD (stated).
* Air-assisted nozzle: SPEC section 12.2 prescribes SMD 20-30 um.
* Rosin-Rammler (mass) distribution 1 - Q = exp(-(d/X)^q); SMD = X/Gamma(1-1/q).
"""

import math

import numpy as np
from scipy import integrate, special

RR_SPREAD_Q = 3.0   # Rosin-Rammler spread; 3 is the aachenBomb/CFD value and mid-range of Lefebvre's 2-4
RR_CLASSES = 12


def nukiyama_tanasawa(U_rel, sigma, rho_l, mu_l, Ql_over_Qa):
    s = sigma * 1e3; r = rho_l * 1e-3; m = mu_l * 10.0
    smd_um = 585.0 / U_rel * math.sqrt(s / r) + 597.0 * (m / math.sqrt(s * r))**0.45 * (1000.0 * Ql_over_Qa)**1.5
    return smd_um * 1e-6


def lefebvre_pressure_swirl(sigma, mu_l, mdot_l, dP, rho_a):
    return 2.25 * sigma**0.25 * mu_l**0.25 * mdot_l**0.25 * dP**-0.5 * rho_a**-0.25


def lang_ultrasonic(sigma, rho_l, f_Hz):
    return 0.34 * (8.0 * math.pi * sigma / (rho_l * f_Hz**2))**(1.0 / 3.0)


def rosin_rammler_classes(smd, q=RR_SPREAD_Q, n=RR_CLASSES):
    """Equal-mass classes; each class diameter is the mass-weighted harmonic
    mean of its bin, so the discrete SMD equals the continuous SMD exactly.
    Returns (d [n], mass_fraction [n])."""
    X = smd * special.gamma(1.0 - 1.0 / q)
    edges = np.linspace(0.0, 1.0, n + 1)
    d = np.empty(n)
    for i in range(n):
        a, b = edges[i], edges[i + 1]
        # integrate 1/d(Q) dQ with d(Q) = X (-ln(1-Q))^(1/q); substitute s = -ln(1-Q)
        sa = -math.log1p(-a); sb = math.inf if b >= 1.0 else -math.log1p(-b)
        f = lambda s: math.exp(-s) * s**(-1.0 / q) / X
        val, _ = integrate.quad(f, sa, sb, limit=200)
        d[i] = (b - a) / val
    return d, np.full(n, 1.0 / n)


def smd_of(d, mass_frac):
    return float(np.sum(mass_frac) / np.sum(mass_frac / d))
