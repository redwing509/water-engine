#!/usr/bin/env python3
"""X5 independent cross-check: faithful re-implementation of the 0-D
closed-cycle SI model (SPEC section 6). Independent of module 03/04 code.
Only sims.common.fuels is imported from the project (SPEC-permitted).
Outputs a single JSON object to stdout: per-case computed values.
"""
import json, math, sys
from pathlib import Path

import cantera as ct
import numpy as np
from CoolProp.CoolProp import PropsSI
from scipy.optimize import brentq

REPO = Path(sys.argv[1] if len(sys.argv) > 1 else "/opt/water-engine")
sys.path.insert(0, str(REPO / "code"))
from sims.common import fuels  # noqa: E402  (only permitted import)

RAD = math.pi / 180.0
R_MOL = ct.gas_constant / 1000.0
T_REF = fuels.REFERENCE_T_K
T_TRIPLE = float(PropsSI("Ttriple", "Water"))
T_CRIT_W = float(PropsSI("Tcrit", "Water"))

B, S, L = 0.086, 0.086, 0.145
RPM = 2000.0
OMEGA = RPM * 2.0 * math.pi / 60.0
IVC = -math.pi
EVO = 140.0 * RAD
R_RESID = 0.05
P_IVC = 1.0e5
PHI = 1.0
WIEBE_A, WIEBE_M = 5.0, 2.0
ETA_C = 0.98
DUR_REF, DUR_CAP = 25.0 * RAD, 80.0 * RAD
FS_EXP = 0.5
CA50 = 8.0 * RAD
KNOCK_XB = 0.9
RETARD_STEP, RETARD_LIMIT = 2.0 * RAD, 30.0 * RAD
ANCHOR_XB = 1.0e-3
WALL_T = 450.0
WOS_C, WOS_C1, WOS_C2 = 3.26, 2.28, 3.24e-3
F_EVAP_INTAKE = 0.5
EVAP_END = -30.0 * RAD
WATER_T = 300.0
STEP = 0.5 * RAD
EQ_MIN_T = 1000.0
RTOL_U, RTOL_P = 1e-8, 1e-8
DISPL = math.pi * B**2 / 4.0 * S


def volume(theta, cr):
    a = S / 2.0
    s = a * math.cos(theta) + math.sqrt(L**2 - (a * math.sin(theta))**2)
    return DISPL / (cr - 1.0) + math.pi * B**2 / 4.0 * (L + a - s)


def wall_area(V):
    return 2.0 * math.pi * B**2 / 4.0 + 4.0 * V / B


def psat_w(T):
    if T >= T_CRIT_W:
        return math.inf
    if T < T_TRIPLE:
        return 0.0
    return float(PropsSI("P", "T", T, "Q", 1, "Water"))


def _z(x):
    return (-math.log1p(-x) / WIEBE_A) ** (1.0 / (WIEBE_M + 1.0))


def wiebe(theta, ca50, dur):
    scale = dur / (_z(0.9) - _z(0.1))
    start = ca50 - scale * _z(0.5)
    return -math.expm1(-WIEBE_A * max(0.0, (theta - start) / scale) ** (WIEBE_M + 1.0))


def burn_angle(f, ca50, dur):
    return ca50 + dur * (_z(f) - _z(0.5)) / (_z(0.9) - _z(0.1))


class Ph:
    def __init__(self, fuel):
        self.gas = fuels.load_mechanism(fuel)
        self.eq = fuels.load_mechanism(fuel)
        self.eg = fuels.load_mechanism(fuel)
        self.flame = fuels.load_mechanism(fuel)
        g = self.gas
        self.MW = np.array(g.molecular_weights, dtype=float)
        self.inv = 1.0 / self.MW
        self.i = {n: g.species_index(fuels.species_name(g, n))
                  for n in ("O2", "N2", "H2O", "CO2")}
        self.i_fuel = g.species_index(fuels.species_name(g, fuel))
        self.lhv = fuels.lhv(fuel)
        self.h_ref = None
        self._T = None

    def _set(self, T):
        if T != self._T:
            self.gas.TP = T, ct.one_atm
            self._u = (np.array(self.gas.standard_enthalpies_RT) - 1.0) * ct.gas_constant * T * self.inv
            self._cv = (np.array(self.gas.standard_cp_R) - 1.0) * ct.gas_constant * self.inv
            self._T = T

    def u(self, T):
        self._set(T)
        return self._u

    def cv(self, T):
        self._set(T)
        return self._cv

    def h(self, T):
        self._set(T)
        return np.array(self.gas.standard_enthalpies_RT) * ct.gas_constant * T * self.inv

    def species_h(self, T):
        return self.h(T)

    def eq_masses(self, masses, T, p):
        m = self.eq
        m.TPY = T, p, masses / masses.sum()
        m.equilibrate("TP")
        return np.array(m.Y) * masses.sum()


_PH = {}


def ph(fuel):
    if fuel not in _PH:
        _PH[fuel] = Ph(fuel)
    return _PH[fuel]


class Charge:
    ideal = False

    def __init__(self, fuel, cr, w, T_intake):
        self.fuel, self.cr, self.w = fuel, float(cr), float(w)
        self.T_intake = float(T_intake)
        P = self.ph = ph(fuel)
        j = self.j = P.i["H2O"]
        nf = 1.0 / P.MW[P.i_fuel]
        o2 = fuels.oxygen_demand(fuel) * nf / PHI
        fresh = np.zeros(P.gas.n_species)
        fresh[P.i_fuel] = 1.0
        fresh[P.i["O2"]] = o2 * P.MW[P.i["O2"]]
        fresh[P.i["N2"]] = fuels.AIR_N2_O2 * o2 * P.MW[P.i["N2"]]
        c, h, _o = fuels.FUELS[fuel].atoms
        complete = np.zeros(P.gas.n_species)
        if c:
            complete[P.i["CO2"]] = c * nf * P.MW[P.i["CO2"]]
        complete[j] = h / 2.0 * nf * P.MW[j]
        complete[P.i["N2"]] = fresh[P.i["N2"]]
        complete[P.i["O2"]] = (o2 - fuels.oxygen_demand(fuel) * nf / PHI) * P.MW[P.i["O2"]]
        self.dry = fresh + complete * R_RESID / (1.0 - R_RESID)
        self.burned_ref = complete + complete * R_RESID / (1.0 - R_RESID)
        self.water = np.zeros(P.gas.n_species)
        self.water[j] = w / (1.0 - w)
        P._set(WATER_T)
        self.h_ref = np.array(P.gas.standard_enthalpies_RT) * ct.gas_constant * T_REF * P.inv
        hfg = PropsSI("Hmass", "T", WATER_T, "Q", 1, "Water") - PropsSI("Hmass", "T", WATER_T, "Q", 0, "Water")
        ufg = PropsSI("Umass", "T", WATER_T, "Q", 1, "Water") - PropsSI("Umass", "T", WATER_T, "Q", 0, "Water")
        self.h_lat = hfg - float(self.ph.h(WATER_T)[j] - self.h_ref[j])
        self.u_lat = ufg - float(self.ph.u(WATER_T)[j] - self.h_ref[j])
        self.m_water_basis = float(self.burned_ref[self.j])  # H2O kg per kg fuel in burned basis
        self._intake()
        vec = self.dry + self.e_intake * self.water
        self.V_ivc = volume(IVC, self.cr)
        n = P_IVC * self.V_ivc / (ct.gas_constant * self.T_ivc)
        self.scale = n / float(vec @ self.ph.inv)
        self.fuel_mass = self.scale
        self.water_mass = self.scale * float(self.water.sum())
        self.Q_fuel = self.scale * self.ph.lhv
        self.Q_avail = ETA_C * self.Q_fuel
        self.L_cyl = self.water_mass * self.u_lat
        self.u_ref = self.u_ref_arr = self.h_ref
        self.U_ivc = self.scale * float(vec @ (self.ph.u(self.T_ivc) - self.h_ref))

    def _H(self, vec, T):
        return float(vec @ (self.ph.h(T) - self.h_ref))

    def _xw(self, vec):
        moles = vec * self.ph.inv
        return float(moles[self.j] / moles.sum())

    def _T_ivc(self, e):
        if e <= 0.0:
            return self.T_intake
        target = self._H(self.dry, self.T_intake) - e * self.water.sum() * self.h_lat
        vec = self.dry + e * self.water
        f = lambda T: self._H(vec, T) - target
        if f(150.0) >= 0.0:
            return None
        return brentq(f, 150.0, self.T_intake, xtol=1e-10)

    def _intake(self):
        f = F_EVAP_INTAKE

        def excess(e):
            T = self._T_ivc(e)
            if T is None or T < T_TRIPLE:
                return P_IVC
            return self._xw(self.dry + e * self.water) * P_IVC - psat_w(T)

        if self.w == 0.0 or f <= 0.0:
            e = 0.0
        elif excess(f) <= 0.0:
            e = f
        else:
            e = brentq(excess, 0.0, f, xtol=1e-12)
        self.e_intake = float(e)
        self.T_ivc = float(self._T_ivc(e))

    def masses(self, xb, e):
        un = self.scale * (1.0 - xb) * (self.dry + e * self.water)
        bn = self.scale * xb * (self.burned_ref + e * self.water)
        return un, bn

    def evaluate(self, T, p, xb, e):
        mu, mb = self.masses(xb, e)
        mb_eq = mb
        if xb > 0.0 and T > EQ_MIN_T:
            mb_eq = self.ph.eq_masses(mb, T, p)
        tot = mu + mb_eq
        U = float(tot @ self.ph.u(T) - (mu + mb) @ self.h_ref)
        return U, float(tot @ self.ph.inv), tot

    def state(self, U, V, xb, e, guess):
        T, p = float(guess[0]), float(guess[1])
        tol = RTOL_U * self.Q_fuel
        T_old = F_old = None
        for _ in range(120):
            Us, n, mas = self.evaluate(T, p, xb, e)
            p_new = n * ct.gas_constant * T / V
            F = Us - U
            if abs(F) <= tol and abs(p_new - p) <= RTOL_P * p_new:
                return dict(T=T, p=p_new, U=Us, V=V, n=n, masses=mas,
                            mass=float(mas.sum()), xb=xb, e=e)
            p = p_new
            slope = (F - F_old) / (T - T_old) if (T_old is not None and T != T_old) else 0.0
            if not slope > 0.0:
                slope = float(mas @ self.ph.cv(T))
            T_old, F_old = T, F
            T = min(6000.0, max(150.0, T - F / slope))
        raise RuntimeError("state inversion did not converge")

    def sched(self, theta):
        if self.water_mass <= 0.0:
            return 0.0
        fr = min(1.0, max(0.0, (theta - IVC) / (EVAP_END - IVC)))
        return self.e_intake + (1.0 - self.e_intake) * fr

    def evaporate(self, e_left, theta, left, V):
        target = self.sched(theta)
        if target <= e_left:
            return e_left
        T_l = left["T"]
        cv = float(left["masses"] @ self.ph.cv(T_l))
        gamma = 1.0 + left["n"] * ct.gas_constant / cv
        T_est = T_l * (left["V"] / V) ** (gamma - 1.0)
        if T_est >= T_CRIT_W:
            return target
        cool = self.L_cyl / cv
        n0 = float(left["masses"][self.j] / self.ph.MW[self.j])
        dn = self.water_mass / self.ph.MW[self.j]

        def excess(de):
            T = T_est - cool * de
            if T < T_TRIPLE:
                return 1e30
            return (n0 + dn * de) * ct.gas_constant * T / V - psat_w(T)

        span = target - e_left
        if excess(0.0) >= 0.0:
            return e_left
        if excess(span) <= 0.0:
            return target
        return e_left + brentq(excess, 0.0, span, xtol=1e-13)

    def saturation_ratio(self, st):
        ps = psat_w(st["T"])
        if math.isinf(ps):
            return 0.0
        x = float(st["masses"][self.j] / self.ph.MW[self.j]) / st["n"]
        return math.inf if ps == 0.0 else x * st["p"] / ps

    def endgas_anchor(self, st):
        eg = self.ph.eg
        Y = self.dry + st["e"] * self.water
        eg.TPY = st["T"], st["p"], Y / Y.sum()
        return dict(s=float(eg.entropy_mass), gamma=float(eg.cp_mass / eg.cv_mass),
                    p=st["p"], V=st["V"], T=st["T"], e=st["e"])

    def endgas_T(self, anchor, p):
        eg = self.ph.eg
        eg.SP = anchor["s"], p
        return float(eg.T)

    def reanchor(self, anchor, p, e_bulk, mass):
        e0 = anchor["e"]
        if e_bulk <= e0:
            return anchor
        eg = self.ph.eg
        T_iso = self.endgas_T(anchor, p)
        cooling = self.L_cyl / (mass * float(eg.cv_mass))
        inv = self.ph.inv

        def excess(e):
            T = T_iso - cooling * (e - e0)
            if T < T_TRIPLE:
                return 1e30
            moles = (self.dry + e * self.water) * inv
            return float(moles[self.j] / moles.sum()) * p - psat_w(T)

        if excess(e_bulk) <= 0.0:
            e_new = e_bulk
        elif excess(e0) >= 0.0:
            e_new = e0
        else:
            e_new = brentq(excess, e0, e_bulk, xtol=1e-13)
        Y = self.dry + e_new * self.water
        eg.TPY = T_iso - cooling * (e_new - e0), p, Y / Y.sum()
        return dict(anchor, s=float(eg.entropy_mass), e=float(e_new))

    def flame_T(self, anchor, T_u, p):
        ph_ = self.ph
        e = anchor["e"]
        Yu = self.dry + e * self.water
        Yc = self.burned_ref + self.water
        mass = float(Yc.sum())
        H = (float(Yc @ ph.h_ref) + float(Yu @ (self.ph.species_h(T_u) - self.h_ref))
             + self.Q_avail - (1.0 - e) * self.m_water_basis * self.h_lat)
        fl = ph_.flame
        fl.HPY = H / mass, p, Yc / mass
        fl.equilibrate("HP")
        return float(fl.T)

    def species_h(self, T):
        return self.h(T)


class IdealCharge:
    ideal = True

    def __init__(self, cr, gamma=1.4):
        self.cr, self.gamma, self.w = float(cr), gamma, 0.0
        self.e_intake, self.water_mass, self.L_cyl = 0.0, 0.0, 0.0
        self.R, T0 = 287.0, 300.0
        self.cv = self.R / (gamma - 1.0)
        self.T_ivc = T0
        self.V_ivc = volume(IVC, cr)
        self.mass = P_IVC * self.V_ivc / (self.R * T0)
        self.Q_fuel = self.Q_avail = self.mass * 1.5e6
        self.U_ivc = 0.0

    def state(self, U, V, xb, e, guess):
        T = self.T_ivc + U / (self.mass * self.cv)
        return dict(T=T, p=self.mass * self.R * T / V, U=U, V=V, n=None,
                    masses=None, mass=self.mass, xb=xb, e=e)

    def evaporate(self, e_left, theta, left, V):
        return e_left


def wall_heat(st, ch, anchor):
    if ch.ideal:
        return 0.0
    speed = WOS_C1 * 2.0 * S * RPM / 60.0
    if anchor is not None:
        p_mot = anchor["p"] * (anchor["V"] / st["V"]) ** anchor["gamma"]
        speed += (WOS_C2 * DISPL * ch.T_ivc / (P_IVC * ch.V_ivc) * max(0.0, st["p"] - p_mot))
    h = WOS_C * B ** -0.2 * (st["p"] / 1000.0) ** 0.8 * st["T"] ** -0.55 * speed ** 0.8
    return h * wall_area(st["V"]) * (st["T"] - WALL_T)


def ignition_rate(T, p, w, fit):
    log_rate = (-math.log(fit["A"]) + fit["n"] * math.log(p)
                - fit["E_J_per_mol"] / (R_MOL * T) - math.log1p(fit["c"] * w))
    return math.exp(min(700.0, max(-700.0, log_rate)))


def integrate(ch, ca50, dur, ignition, evo=None, step=STEP, wall=True):
    evo = EVO if evo is None else evo
    omega = OMEGA
    th90 = burn_angle(KNOCK_XB, ca50, dur)
    th_a = burn_angle(ANCHOR_XB, ca50, dur)  # anchor on a node (verification item 1)
    nodes = list(np.linspace(IVC, evo, max(2, math.ceil((evo - IVC) / step)) + 1))
    nodes += [a for a in (EVAP_END, th90, th_a) if IVC < a < evo]
    grid = np.unique(np.array(nodes, dtype=float))
    Qa, Lc = ch.Q_avail, ch.L_cyl
    xb = x_ivc = wiebe(grid[0], ca50, dur)
    e = ch.e_intake
    st = ch.state(ch.U_ivc, volume(grid[0], ch.cr), xb, e, (ch.T_ivc, P_IVC))
    U = ch.U_ivc
    anchor = None
    W = Qw = Qe = W_trap = Qw_trap = 0.0
    LW = LW90 = None
    peak = dict(p=st["p"], T=st["T"])
    q_left = wall_heat(st, ch, anchor) if wall else 0.0
    for left, right in zip(grid[:-1], grid[1:]):
        mid = 0.5 * (left + right)
        dt = (right - left) / omega
        Vm, Vr = volume(mid, ch.cr), volume(right, ch.cr)
        xm, xr = wiebe(mid, ca50, dur), wiebe(right, ca50, dur)
        em = ch.evaporate(e, mid, st, Vm)
        if em > e:  # cap on the no-evaporation predictor state at mid (verification item 1)
            s0 = ch.state(U - st["p"] * (Vm - st["V"]) + Qa * (xm - xb) - 0.5 * q_left * dt, Vm, xm, e,
                          (st["T"], st["p"]))
            em = ch.evaporate(e, mid, s0, Vm)
        er = max(em, ch.evaporate(e, right, st, Vr))
        Um = U - st["p"] * (Vm - st["V"]) + Qa * (xm - xb) - Lc * (em - e) - 0.5 * q_left * dt
        sm = ch.state(Um, Vm, xm, em, (st["T"], st["p"]))
        if anchor is None and not ch.ideal and left >= th_a - 1e-12:
            anchor = ch.endgas_anchor(st)
        q_mid = wall_heat(sm, ch, anchor) if wall else 0.0
        work = sm["p"] * (Vr - st["V"])
        de = Lc * (er - e)
        U += -work + Qa * (xr - xb) - de - q_mid * dt
        if er > e:  # corrector: cap on the no-evaporation right state
            s0 = ch.state(U + de, Vr, xr, e, (sm["T"], sm["p"]))
            er2 = max(em, ch.evaporate(e, right, s0, Vr))
            U -= Lc * (er2 - er)
            er, de = er2, Lc * (er2 - e)
        W += work
        Qw += q_mid * dt
        Qe += de
        endgas = anchor is not None and xm < 0.999
        if ignition is not None and mid < th90:
            Tu = ch.endgas_T(anchor, sm["p"]) if endgas else sm["T"]
            LW = min(1e6, (LW or 0.0) + ignition_rate(Tu, sm["p"], ch.w, ignition) * dt)
        sr = ch.state(U, Vr, xr, er, (sm["T"], sm["p"]))
        if anchor is not None and xr < 0.999 and er > anchor["e"]:
            anchor = ch.reanchor(anchor, sr["p"], er, sr["mass"])
        q_right = wall_heat(sr, ch, anchor) if wall else 0.0
        W_trap += 0.5 * (st["p"] + sr["p"]) * (Vr - st["V"])
        Qw_trap += 0.5 * (q_left + q_right) * dt
        if abs(right - th90) < 1e-12:
            LW90 = LW
        for s in (sm, sr):
            if s["p"] > peak["p"]:
                peak["p"] = s["p"]
            peak["T"] = max(peak["T"], s["T"])
        st, xb, e, q_left = sr, xr, er, q_right
    if LW90 is None:
        LW90 = LW or 0.0
    released = Qa * (xb - x_ivc)
    dU = st["U"] - ch.U_ivc
    closure = released - (W_trap + Qw_trap + Qe + dU)
    return dict(W=W, IMEP=W / DISPL, eff=W / ch.Q_fuel, pmax=peak["p"],
                Tpeak=peak["T"], TEVO=st["T"], PEVO=st["p"],
                closure=closure / ch.Q_fuel, knock=bool(LW90 >= 1.0), LW=LW90,
                xb_evo=xb)


def run_case(fuel, cr, w, T, ig_fit, sl):
    dur = min(DUR_CAP, DUR_REF * (sl / sl) ** FS_EXP) if False else None
    # burn duration from flame speed ratio: ref * (sl_ref/sl)^0.5
    return None


def main():
    fits_dir = REPO / "results" / "02_flame_chem"
    ign = json.loads((fits_dir / "ignition_fits.json").read_text())
    fla = json.loads((fits_dir / "flame_speed_fits.json").read_text())

    def sl_w(fuel, w):
        c = fla[fuel]["coefficients_highest_first"]
        return float(np.polyval(c, w))

    def run_case(fuel, cr, w, T):
        sl = sl_w(fuel, w)
        sl_ref = sl_w(fuel, 0.0)
        dur = min(DUR_CAP, DUR_REF * (sl_ref / sl) ** FS_EXP)
        ch = Charge(fuel, cr, w, T)
        fit = ign[fuel]
        ca50, n = CA50, 0
        while True:
            r = integrate(ch, ca50, dur, fit)
            n += 1
            if not r["knock"] or ca50 >= RETARD_LIMIT - 1e-12:
                break
            ca50 = min(RETARD_LIMIT, ca50 + RETARD_STEP)
        r["ca50"] = ca50 / RAD
        r["attempts"] = n
        return r

    cases = {
        "CH3OH/best_dry": ("CH3OH", 16, 0.0, 320.0),
        "CH3OH/best_overall": ("CH3OH", 23, 0.3, 320.0),
        "CH3OH/water_majority": ("CH3OH", 24, 0.5, 360.0),
        "C2H5OH/best_dry": ("C2H5OH", 24, 0.0, 320.0),
        "C2H5OH/best_overall": ("C2H5OH", 23, 0.4, 320.0),
        "C2H5OH/water_majority": ("C2H5OH", 24, 0.5, 360.0),
        "SIXSTROKE_SPOT_C2H5OH_CR18_w0.6_T360": ("C2H5OH", 18, 0.6, 360.0),
    }
    out = {}
    for name, (fuel, cr, w, T) in cases.items():
        r = run_case(fuel, cr, w, T)
        out[name] = {k: (float(v) if isinstance(v, (int, float, np.floating))
                         and not isinstance(v, bool) else v)
                     for k, v in r.items()}

    otto = {}
    for cr in (16, 24):
        ch = IdealCharge(cr)
        r = integrate(ch, 0.0, 1.0 * RAD, None, evo=math.pi, step=0.5 * RAD, wall=False)
        otto[f"CR{cr}"] = dict(eff=r["eff"], analytic=1.0 - cr ** (1.0 - 1.4),
                               closed=r["closure"])
    out["otto"] = otto
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
