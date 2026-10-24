"""Lagrangian droplet ensemble in a closed-mass-balance gas parcel.

Physics (SPEC section 12.2):
* Droplet classes: each class i holds N_i identical droplets (well-mixed
  liquid, uniform temperature: the infinite-conductivity / rapid-mixing
  limit). Liquid = water + methanol; pure liquids are the end members.
* Evaporation: Abramzon & Sirignano (1989), Int. J. Heat Mass Transfer
  32:1605, film model with the 1/3 reference rule (Hubbard, Denny & Mills
  1975), F(B) = (1+B)^0.7 ln(1+B)/B, Nu* = 2 + (Nu0-2)/F(B_T),
  Sh* = 2 + (Sh0-2)/F(B_M), B_T = (1+B_M)^phi - 1. Nu0/Sh0 are the
  Ranz & Marshall (1952) correlations 2 + 0.6 Re^1/2 Pr^1/3 (Sc^1/3).
* Multicomponent: total rate from B_M = (sum Ys - sum Yinf)/(1 - sum Ys),
  species split m_k = m Ys_k + (m/B_M)(Ys_k - Yinf_k) (equal diffusivities,
  Sirignano 2010, Fluid Dynamics and Transport of Droplets and Sprays).
  Surface vapour: modified Raoult x_s,k = gamma_k x_l,k p_sat,k(T_d)/p with
  Wilson gamma (properties.py) or gamma = 1 when activity="ideal".
* Closed mass balance: the gas parcel holds the air plus all vapour
  produced; vapour is never removed. Y_inf therefore rises, B_M falls to 0
  at saturation, and the model condenses (B_M < 0) if the gas is
  supersaturated with respect to the droplet surface. Saturation is a
  thermodynamic limit of the same equations, not an extra clip.
* Gas energy: constant pressure (plenum / runner / induction),
  prescribed volume V(t) (compression, constant-volume chamber), or
  prescribed pressure p(t) ("pt": an imposed cylinder pressure trace, e.g.
  Module 03's motored p(theta); m cp dT = V dp/dt + droplet terms).
* Optional transfer multiplier k (rate_scale / rate_scale_fun(p)) applied
  to both the droplet mass and heat transfer (a Sh/Nu multiplier). k = 1 is
  the nominal model; k != 1 is used ONLY for the labelled cfd_matched
  sensitivity bound, never for nominal results.
  Vapour enters the gas at the droplet temperature; heat conducted to the
  droplets leaves the gas. Wall heat transfer is neglected (adiabatic).
* Drag: Schiller & Naumann (1933) on the slip velocity in 1-D.
* Wall impingement is applied between segments by the caller.

Conservation: the vapour masses are ODE states whose rates are exactly
minus the sum of droplet mass rates, so linear multistep integration keeps
total mass to round-off; tests check this to 1e-8.

Regularisation: droplets below R_FLOOR of their initial mass have every
flux scaled by (relative mass / R_FLOOR) so the vanishing-droplet
singularity is Lipschitz; the liquid left in such droplets is still
counted as liquid (never silently evaporated).
"""

from dataclasses import dataclass, field
import math

import numpy as np
from scipy.integrate import solve_ivp

from . import properties as P

R_FLOOR = 1e-3          # relative droplet mass below which fluxes are scaled
SUM_XS_CAP = 0.99       # surface vapour mole-fraction cap (boiling guard)
RM_A, RM_B = 0.6, 0.5   # Ranz-Marshall coefficient and Re exponent


def _lg(B):
    """ln(1+B)/B, safe at B -> 0."""
    B = np.asarray(B, float)
    small = np.abs(B) < 1e-6
    Bs = np.where(small, 1.0, B)
    return np.where(small, 1.0 - B / 2.0 + B * B / 3.0, np.log1p(Bs) / Bs)


def _F(B):
    return (1.0 + B)**0.7 * _lg(B)


@dataclass
class ConstProps:
    """Constant-property override for the analytic d2-law test."""

    rho_l: float = 997.0
    cp_l: float = 4180.0
    L: float = 2.4e6
    rho_g: float = 1.0
    D: float = 2.5e-5
    k_g: float = 0.026
    cp_g: float = 1007.0
    Ys: float = 0.05
    Yinf: float = 0.0


@dataclass
class Spray:
    """Gas parcel + droplet classes. Masses kg, temperatures K, SI."""

    m_air: float
    T_gas: float
    p: float
    m_ref: float                       # mass scale: total liquid to be injected
    activity: str = "wilson"           # "wilson" | "ideal"
    const: ConstProps | None = None    # test-only constant properties
    fixed_Td: bool = False             # test-only: hold droplet temperature
    infinite_gas: bool = False         # test-only: Y_inf held constant
    m0: np.ndarray = field(default_factory=lambda: np.zeros(0))
    N: np.ndarray = field(default_factory=lambda: np.zeros(0))
    y: np.ndarray = field(default_factory=lambda: np.zeros(0))
    wall: np.ndarray = field(default_factory=lambda: np.zeros(2))   # kg water, methanol
    wall_H: float = 0.0                 # enthalpy carried to the wall film [J]
    injected: np.ndarray = field(default_factory=lambda: np.zeros(2))
    V: float = float("nan")             # gas volume when in volume mode
    t: float = 0.0
    work: float = 0.0                   # integral p dV done BY the gas [J]
    cap_hits: int = 0
    fuel: str = "CH3OH"                 # alcohol component ("CH3OH" | "C2H5OH")
    rate_scale: float = 1.0             # transfer multiplier (1 = nominal)
    rate_scale_fun: object = None       # optional callable p[Pa] -> multiplier
    vdp: float = 0.0                    # integral V dp in "pt" mode [J]

    def __post_init__(self):
        self.tab = P.tables(self.fuel)
        # y layout: mw[n], mm[n], Td[n], ud[n], Tg, mv_w, mv_m
        self.y = np.array([self.T_gas, 0.0, 0.0])

    # ---------- bookkeeping -------------------------------------------------
    @property
    def n(self):
        return self.m0.size

    def split(self, y=None):
        y = self.y if y is None else y
        n = self.n
        return (y[:n], y[n:2 * n], y[2 * n:3 * n], y[3 * n:4 * n], y[4 * n],
                y[4 * n + 1:4 * n + 3])

    def add_classes(self, d, count, Y_m, T_l, u):
        """Inject classes: diameters d [m], droplet counts, methanol mass fraction."""
        d = np.asarray(d, float); count = np.asarray(count, float)
        rho = self.liquid_density(np.full(d.size, T_l), np.full(d.size, Y_m))
        m0 = rho * math.pi * d**3 / 6.0
        mw, mm, Td, ud, Tg, mv = self.split()
        n_new = d.size
        self.m0 = np.concatenate([self.m0, m0])
        self.N = np.concatenate([self.N, count])
        self.y = np.concatenate([mw, np.full(n_new, 1.0 - Y_m), mm, np.full(n_new, Y_m),
                                 Td, np.full(n_new, T_l), ud, np.full(n_new, u), [Tg], mv])
        self.injected += np.array([1.0 - Y_m, Y_m]) * float(np.sum(count * m0))

    def liquid_density(self, T, Y_m):
        t = self.tab
        if self.const:
            return np.full(np.shape(T), self.const.rho_l)
        return 1.0 / ((1.0 - Y_m) / np.interp(T, t.TL, t.rho_l[0]) + Y_m / np.interp(T, t.TL, t.rho_l[1]))

    def masses(self, y=None):
        """(liquid airborne [2], vapour [2], wall [2]) in kg."""
        mw, mm, Td, ud, Tg, mv = self.split(y)
        liq = np.array([np.sum(self.N * mw * self.m0), np.sum(self.N * mm * self.m0)])
        return liq, mv * self.m_ref, self.wall.copy()

    def gas_masses(self, y=None):
        _, _, _, _, _, mv = self.split(y)
        return np.array([self.m_air, mv[0] * self.m_ref, mv[1] * self.m_ref])

    def gas_pressure(self, Tg, mg, V):
        R = P.R_U / self.tab.M_g
        return float(np.sum(mg * R) * Tg / V)

    def enthalpy(self, y=None):
        """Total enthalpy of gas + airborne liquid + wall film [J]."""
        mw, mm, Td, ud, Tg, mv = self.split(y)
        t = self.tab
        mg = self.gas_masses(y)
        Hg = sum(mg[j] * P.gas_h(t, j, Tg) for j in range(3))
        Hl = np.sum(self.N * self.m0 * (mw * np.interp(Td, t.TL, t.h_l[0]) + mm * np.interp(Td, t.TL, t.h_l[1])))
        return float(Hg + Hl + self.wall_H)

    def internal_energy(self, y=None):
        mw, mm, Td, ud, Tg, mv = self.split(y)
        mg = self.gas_masses(y)
        R = P.R_U / self.tab.M_g
        return self.enthalpy(y) - float(np.sum(mg * R) * Tg)

    # ---------- droplet fluxes ---------------------------------------------
    def fluxes(self, y, p, u_g):
        """Per-droplet mass rates (n,2) [kg/s], gas-side heat Q (n,) [W], extra."""
        t = self.tab
        mw, mm, Td, ud, Tg, mv = self.split(y)
        n = self.n
        mwk = np.maximum(mw, 0.0) * self.m0
        mmk = np.maximum(mm, 0.0) * self.m0
        mt = mwk + mmk
        rel = mt / self.m0
        f_reg = np.clip(rel / R_FLOOR, 0.0, 1.0)
        mt_safe = np.maximum(mt, 1e-300)
        Y_m = np.where(mt > 0, mmk / mt_safe, 0.0)
        rho_l = self.liquid_density(Td, Y_m)
        d = np.cbrt(6.0 * mt / (math.pi * rho_l))
        if self.const is not None:
            c = self.const
            B = (c.Ys - c.Yinf) / (1.0 - c.Ys)
            mdot = 2.0 * math.pi * c.rho_g * c.D * d * math.log1p(B)   # Sh = 2
            mk = np.stack([mdot, np.zeros(n)], axis=1) * f_reg[:, None]
            return mk, np.zeros(n), dict(d=d, rho_l=rho_l, Y_m=Y_m, cp_l=np.full(n, c.cp_l),
                                         L=np.stack([np.full(n, c.L), np.zeros(n)], axis=1),
                                         drag=np.zeros(n), xs_sum=np.full(n, np.nan))
        Mw, Mm, Ma = t.M_g[1], t.M_g[2], t.M_g[0]
        nw = mwk / Mw; nm = mmk / Mm
        x_m = np.where(nw + nm > 0, nm / np.maximum(nw + nm, 1e-300), 0.0)
        if self.activity == "wilson":
            g_w, g_m = P.wilson_gamma(x_m, Td, self.tab.fuel)
        else:
            g_w, g_m = np.ones(n), np.ones(n)
        ps_w = np.interp(Td, t.TL, t.psat[0]); ps_m = np.interp(Td, t.TL, t.psat[1])
        xs = np.stack([g_w * (1.0 - x_m) * ps_w / p, g_m * x_m * ps_m / p], axis=1)
        xs = np.where(mt[:, None] > 0, xs, 0.0)
        xs_sum = xs.sum(axis=1)
        over = xs_sum > SUM_XS_CAP
        if np.any(over):
            self.cap_hits += int(np.sum(over))
            xs[over] *= (SUM_XS_CAP / xs_sum[over])[:, None]
        M_s = xs[:, 0] * Mw + xs[:, 1] * Mm + (1.0 - xs.sum(axis=1)) * Ma
        Ys = np.stack([xs[:, 0] * Mw, xs[:, 1] * Mm], axis=1) / M_s[:, None]
        mg = self.gas_masses(y)
        Yinf = mg[1:] / mg.sum()
        sYs = Ys.sum(axis=1); sYi = Yinf.sum()
        B_M = (sYs - sYi) / (1.0 - sYs)
        B_M = np.maximum(B_M, -0.9)
        # film (1/3 rule)
        Tr = Td + (Tg - Td) / 3.0
        Yr = Ys + (Yinf[None, :] - Ys) / 3.0
        Yr_air = 1.0 - Yr.sum(axis=1)
        Yfull = np.stack([Yr_air, Yr[:, 0], Yr[:, 1]], axis=1)
        Xr = Yfull / t.M_g[None, :]
        Mr = 1.0 / Xr.sum(axis=1)
        Xr = Xr * Mr[:, None]
        rho_f = p * Mr / (P.R_U * Tr)
        cps = np.stack([P.gas_cp(t, j, Tr) for j in range(3)], axis=1)
        cp_f = np.sum(Yfull * cps, axis=1)
        mu_f, k_f = P.film_transport(t, Tr, Xr)
        Dw = P.diffusivity(t, 0, Tr, p); Dm = P.diffusivity(t, 1, Tr, p)
        wv = np.maximum(Yr, 0.0)
        wsum = wv.sum(axis=1)
        D_f = np.where(wsum > 1e-30, (wv[:, 0] * Dw + wv[:, 1] * Dm) / np.maximum(wsum, 1e-30),
                       np.where(Y_m > 0.5, Dm, Dw))
        ysv = np.maximum(Ys, 0.0); ysum = ysv.sum(axis=1)
        cp_v = np.where(ysum > 1e-30, (ysv[:, 0] * cps[:, 1] + ysv[:, 1] * cps[:, 2]) / np.maximum(ysum, 1e-30),
                        np.where(Y_m > 0.5, cps[:, 2], cps[:, 1]))
        slip = u_g - ud
        Re = rho_f * np.abs(slip) * d / mu_f
        Pr = cp_f * mu_f / k_f
        Sc = mu_f / (rho_f * D_f)
        Sh0 = 2.0 + RM_A * Re**RM_B * np.cbrt(Sc)
        Nu0 = 2.0 + RM_A * Re**RM_B * np.cbrt(Pr)
        Sh = 2.0 + (Sh0 - 2.0) / _F(B_M)
        G = math.pi * rho_f * D_f * d * Sh * _lg(B_M)      # = mdot / B_M
        mdot = G * B_M
        Le = k_f / (rho_f * cp_f * D_f)
        Nu = Nu0.copy()
        for _ in range(5):
            phi = (cp_v / cp_f) * (Sh / Nu) / Le
            B_T = (1.0 + B_M)**phi - 1.0
            Nu = 2.0 + (Nu0 - 2.0) / _F(B_T)
        Q = math.pi * d * k_f * Nu * (Tg - Td) * _lg(B_T)
        mk = mdot[:, None] * Ys + G[:, None] * (Ys - Yinf[None, :])
        # a component absent from the liquid cannot leave it
        mk[:, 0] = np.where((mwk <= 0) & (mk[:, 0] > 0), 0.0, mk[:, 0])
        mk[:, 1] = np.where((mmk <= 0) & (mk[:, 1] > 0), 0.0, mk[:, 1])
        kscale = self.rate_scale_fun(p) if self.rate_scale_fun is not None else self.rate_scale
        mk *= (f_reg * kscale)[:, None]
        Q = Q * f_reg * kscale
        cp_l = (1.0 - Y_m) * np.interp(Td, t.TL, t.cp_l[0]) + Y_m * np.interp(Td, t.TL, t.cp_l[1])
        L = np.stack([P.gas_h(t, 1, Td) - np.interp(Td, t.TL, t.h_l[0]),
                      P.gas_h(t, 2, Td) - np.interp(Td, t.TL, t.h_l[1])], axis=1)
        tau = rho_l * d**2 / (18.0 * mu_f)
        drag = slip * (1.0 + 0.15 * Re**0.687) / np.maximum(tau, 1e-300)
        drag = np.where(mt > 0, drag, 0.0)
        return mk, Q, dict(d=d, rho_l=rho_l, Y_m=Y_m, cp_l=cp_l, L=L, drag=drag,
                           xs_sum=xs_sum, Ys=Ys, Yinf=Yinf, B_M=B_M, Re=Re)

    # ---------- ODE ----------------------------------------------------------
    def rhs(self, tt, y, mode, u_g, Vfun):
        t = self.tab
        n = self.n
        mw, mm, Td, ud, Tg, mv = self.split(y)
        mg = self.gas_masses(y)
        R = P.R_U / t.M_g
        if mode == "p":
            p = self.p
        elif mode == "pt":
            p, dp = Vfun(tt)
            V = float(np.sum(mg * R) * Tg / p)
        else:
            V, dV = Vfun(tt)
            p = float(np.sum(mg * R) * Tg / V)
        mk, Q, ex = self.fluxes(y, p, u_g)
        dy = np.zeros_like(y)
        mtot = (np.maximum(mw, 0) + np.maximum(mm, 0)) * self.m0
        dy[:n] = -mk[:, 0] / self.m0
        dy[n:2 * n] = -mk[:, 1] / self.m0
        if not self.fixed_Td:
            heat = Q - mk[:, 0] * ex["L"][:, 0] - mk[:, 1] * ex["L"][:, 1]
            dy[2 * n:3 * n] = np.where(mtot > 0, heat / np.maximum(mtot * ex["cp_l"], 1e-300), 0.0)
        dy[3 * n:4 * n] = ex["drag"]
        flux = (self.N[:, None] * mk).sum(axis=0)
        dy[4 * n + 1:4 * n + 3] = 0.0 if self.infinite_gas else flux / self.m_ref
        if self.const is None and not self.infinite_gas:
            hv = np.stack([P.gas_h(t, 1, Td), P.gas_h(t, 2, Td)], axis=1)
            hg = np.array([P.gas_h(t, 1, Tg), P.gas_h(t, 2, Tg)])
            cps = np.array([P.gas_cp(t, j, Tg) for j in range(3)])
            if mode == "p":
                src = np.sum(self.N * (-Q + np.sum(mk * (hv - hg[None, :]), axis=1)))
                dy[4 * n] = src / np.sum(mg * cps)
            elif mode == "pt":
                src = V * dp + np.sum(self.N * (-Q + np.sum(mk * (hv - hg[None, :]), axis=1)))
                dy[4 * n] = src / np.sum(mg * cps)
            else:
                ug = hg - R[1:] * Tg
                src = -p * dV + np.sum(self.N * (-Q + np.sum(mk * (hv - ug[None, :]), axis=1)))
                dy[4 * n] = src / np.sum(mg * (cps - R))
        return dy

    def run(self, duration, mode="p", u_g=0.0, Vfun=None, n_out=50, rtol=1e-7):
        """Integrate one segment; returns list of snapshot dicts."""
        t0 = self.t
        t_eval = np.linspace(t0, t0 + duration, n_out + 1)
        n = self.n
        atol = np.concatenate([np.full(2 * n, 1e-10), np.full(n, 1e-6), np.full(n, 1e-6),
                               [1e-6], np.full(2, 1e-12)])
        fun = lambda tt, yy: self.rhs(tt, yy, mode, u_g, Vfun)
        sol = solve_ivp(fun, (t0, t0 + duration), self.y, method="BDF", t_eval=t_eval,
                        rtol=rtol, atol=atol)
        if not sol.success:
            raise RuntimeError(f"ODE integration failed: {sol.message}")
        snaps = []
        for j, tt in enumerate(sol.t):
            yy = sol.y[:, j]
            snaps.append(self.snapshot(tt, yy, mode, Vfun))
        if mode == "V":
            # p dV work by trapezoid on the dense output (energy ledger only)
            ps = np.array([s["p_Pa"] for s in snaps]); Vs = np.array([Vfun(tt)[0] for tt in sol.t])
            self.work += float(np.trapezoid(ps, Vs))
        elif mode == "pt":
            ps = np.array([s["p_Pa"] for s in snaps]); Vs = np.array([s["V_m3"] for s in snaps])
            self.vdp += float(np.trapezoid(Vs, ps))
        self.y = sol.y[:, -1].copy()
        self.t = t0 + duration
        return snaps

    def snapshot(self, tt, y, mode, Vfun):
        liq, vap, wall = self.masses(y)
        mw, mm, Td, ud, Tg, mv = self.split(y)
        mg = self.gas_masses(y)
        R = P.R_U / self.tab.M_g
        if mode == "p":
            p = self.p; V = float(np.sum(mg * R) * Tg / p)
        elif mode == "pt":
            p = float(Vfun(tt)[0]); V = float(np.sum(mg * R) * Tg / p)
        else:
            V = Vfun(tt)[0]; p = float(np.sum(mg * R) * Tg / V)
        mtot = (np.maximum(mw, 0) + np.maximum(mm, 0)) * self.m0
        live = (mtot > R_FLOOR * self.m0) & (self.N > 0)
        Ym = np.where(mtot > 0, np.maximum(mm, 0) * self.m0 / np.maximum(mtot, 1e-300), 0.0)
        rho = self.liquid_density(Td, Ym)
        d = np.cbrt(6.0 * mtot / (math.pi * rho))
        smd = float(np.sum(self.N[live] * d[live]**3) / np.sum(self.N[live] * d[live]**2)) if live.any() else 0.0
        inj = float(self.injected.sum())
        # saturation ratio of each vapour w.r.t. its pure liquid at the gas temperature
        x = (mg / self.tab.M_g); x = x / x.sum()
        t = self.tab
        S_w = x[1] * p / P.murphy_koop_psat(Tg) if Tg < P.T_SUBZERO else x[1] * p / np.interp(Tg, t.TL, t.psat[0])
        S_m = x[2] * p / np.interp(min(Tg, t.TL[-1]), t.TL, t.psat[1])
        return dict(t_s=float(tt), T_gas_K=float(Tg), p_Pa=p, V_m3=V,
                    liquid_kg=float(liq.sum()), vapour_kg=float(vap.sum()), wall_kg=float(wall.sum()),
                    vapour_water_kg=float(vap[0]), vapour_methanol_kg=float(vap[1]),
                    injected_kg=inj, evaporated_frac=float(vap.sum() / inj) if inj > 0 else 0.0,
                    mass_error_rel=float(abs(liq.sum() + vap.sum() + wall.sum() - inj) / inj) if inj > 0 else 0.0,
                    SMD_m=smd, Td_mean_K=float(np.sum(self.N * mtot * Td) / max(np.sum(self.N * mtot), 1e-300)),
                    S_water=float(S_w), S_methanol=float(S_m))

    # ---------- events -----------------------------------------------------
    def impinge(self, eta):
        """Remove fraction eta[i] of each class to the wall film."""
        mw, mm, Td, ud, Tg, mv = self.split()
        t = self.tab
        rm = self.N * eta
        mw_k = rm * np.maximum(mw, 0) * self.m0
        mm_k = rm * np.maximum(mm, 0) * self.m0
        self.wall += np.array([mw_k.sum(), mm_k.sum()])
        self.wall_H += float(np.sum(mw_k * np.interp(Td, t.TL, t.h_l[0]) + mm_k * np.interp(Td, t.TL, t.h_l[1])))
        self.N = self.N * (1.0 - eta)

    def droplet_diameters(self):
        mw, mm, Td, ud, Tg, mv = self.split()
        mt = (np.maximum(mw, 0) + np.maximum(mm, 0)) * self.m0
        Ym = np.where(mt > 0, np.maximum(mm, 0) * self.m0 / np.maximum(mt, 1e-300), 0.0)
        return np.cbrt(6.0 * mt / (math.pi * self.liquid_density(Td, Ym)))
