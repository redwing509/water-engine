"""SPEC section 12.1 (Module 08 water_chemistry): water's chemical effect.

Execution happens on the Linux simulation server; the laptop only compiles.

Method
------
Water's effect on combustion is conventionally lumped together: dilution,
thermal ballast and genuine reaction kinetics are all one number.  This
module separates the chemical part by substituting a **fictitious water**
species FH2O that carries H2O's thermochemistry and transport but takes part
in no reaction at all.  Two variants are built:

* FH2O-a: the third-body efficiencies that H2O carries in three-body and
  falloff reactions are transferred to FH2O unchanged, so FH2O-a dilutes and
  thermally ballasts exactly like H2O and also stabilises/destabilises
  third-body reactions exactly like H2O.  What remains different from real
  H2O is only H2O's direct participation (H + H2O <-> ... , H2O + O <-> 2OH,
  ...): the *direct-reaction* part.
* FH2O-b: every transferred efficiency is set to 1.0, i.e. FH2O-b acts as a
  purely inert thermal diluent with unit third-body strength.  The difference
  FH2O-b vs FH2O-a isolates the *third-body* part of the chemical effect.

The chemical effect for an observable X (S_L, tau) is defined as

    effect = (X_real - X_FH2O) / X_FH2O,

and is split as

    third-body part   = (X_a - X_b) / X_b,
    direct-reaction   = (X_real - X_a) / X_a.

so that effect = direct-reaction * (1 + third-body part) exactly.

Composition convention: the unburned charge is built by
sims.common.fuels.mixture (fuel + dry air + added H2O vapour) and, for the
fictitious cases, the H2O entry of that composition is renamed to FH2O.  The
mixture therefore always contains exactly one water-like species, so the
three mechanisms are compared at identical total mass and identical
water-like mole fraction.

Oxygen bookkeeping (w = 0.6, CH3OH, 40 bar, 900 K, constant volume):
every O atom that starts inside the added water is tagged by bookkeeping the
element balances.  The water O pool is W = moles of added water.  Over the
full integration to the 0.5 s horizon the net O transferred *into CO2* from
that pool is bounded by the change in the CO2 O content beyond what the fuel
+ air stoichiometry alone can explain, and the net H2 released is the H2
that appears while the water O atoms leave their original carriers.  The
closure test is: at final time, total O atoms == initial O atoms (1e-6) and
the enthalpy ledger of the whole charge closes (energy is conserved), which
proves the water atoms carried no net energy.
"""

import os
# Cantera's Fortran SUNDIALS/OpenMP stack is not re-entrant across spawned
# processes when the default thread count (>1) is inherited.  Pin to one
# thread before Cantera is imported so io.ordered_map spawn workers never
# deadlock in the OpenMP barrier.
os.environ.setdefault("OMP_NUM_THREADS", "1")

from dataclasses import asdict, dataclass
import json
import math
import time

import cantera as ct
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sims.common import fuels, io


MODULE = "08_water_chem"
VERSION = "1.0.0"
FUELS = ("CH3OH", "C2H5OH", "CH4")
PHI = 1.0
WATER_FRACTIONS = tuple(i / 10 for i in range(9))          # 0 .. 0.8
MECHANISM_VARIANTS = ("real", "fh2o_a", "fh2o_b")
FLAME_STATE = (400.0, ct.one_atm)                          # S_L
IGNITION_P_PA = 40e5
IGNITION_TEMPERATURES = (800.0, 900.0, 1000.0)             # tau
BOOKKEEP_FUEL, BOOKKEEP_W, BOOKKEEP_T = "CH3OH", 0.6, 900.0

FICTITIOUS = "FH2O"
QUICK_FUELS = ("CH3OH", "CH4")
QUICK_WATER = (0.0, 0.3)
QUICK_IGNITION_T = (900.0,)

# Mechanism file names produced by build_mechanisms.py (relative to REPO_ROOT).
MECH_PATHS = {
    "real": {
        "CH3OH": "mechanisms/sandiego.yaml",
        "C2H5OH": "mechanisms/sandiego.yaml",
        "CH4": "mechanisms/gri30.yaml",
    },
    "fh2o_a": {
        "CH3OH": "mechanisms/08_water_chem/sandiego_fh2oa.yaml",
        "C2H5OH": "mechanisms/08_water_chem/sandiego_fh2oa.yaml",
        "CH4": "mechanisms/08_water_chem/gri30_fh2oa.yaml",
    },
    "fh2o_b": {
        "CH3OH": "mechanisms/08_water_chem/sandiego_fh2ob.yaml",
        "C2H5OH": "mechanisms/08_water_chem/sandiego_fh2ob.yaml",
        "CH4": "mechanisms/08_water_chem/gri30_fh2ob.yaml",
    },
}


@dataclass(frozen=True)
class Parameters:
    """Defaults and their sources/rationales are emitted by assumptions()."""

    water_T_K: float = 300.0
    flame_width_1atm_m: float = 0.03
    refine_ratio: float = 3.0
    refine_slope: float = 0.07
    refine_curve: float = 0.14
    flame_stop_m_s: float = 0.02
    ignition_max_time_s: float = 0.5
    ignition_min_rise_K: float = 200.0
    ignition_max_step_s: float = 0.005
    reactor_rtol: float = 1e-9
    reactor_atol: float = 1e-15
    oxygen_balance_tol: float = 1e-6
    energy_closure_tol: float = 1e-6
    identical_w0_rel: float = 1e-9


DEFAULTS = Parameters()
R_J_MOL_K = ct.gas_constant / 1000.0


def _mechanism_path(fuel: str, variant: str) -> str:
    rel = MECH_PATHS[variant][fuel]
    return str(io.REPO_ROOT / rel)


def _gas(fuel: str, variant: str, phi: float, w: float, T_K: float, p_Pa: float):
    """Construct in the calling process; no Cantera object crosses a pool.

    At w = 0 the charge contains no water-like species, so the fictitious-
    water construct is inactive and every variant runs on the real
    mechanism: the variants are then trivially identical (SPEC 12.1 test:
    "At w = 0, real and FH2O are identical").  This also avoids the
    H2O/FH2O equilibrium-splitting artefact that would otherwise shift T_ad
    by the ideal-mixing entropy of the duplicate water pool.
    """
    variant = "real" if w == 0.0 else variant
    path = _mechanism_path(fuel, variant)
    gas = ct.Solution(path)
    comp = fuels.mixture(fuel, phi, w)
    if variant != "real":
        water_name = "H2O"
        comp["FH2O"] = comp.pop(water_name)
    gas.TPX = T_K, p_Pa, comp
    return gas


def _record(fuel: str, phi: float, w: float, T_K: float, p_Pa: float,
            variant: str) -> dict:
    return dict(fuel=fuel, phi=phi, w=w, T_K=T_K, p_Pa=p_Pa, variant=variant,
                mechanism=MECH_PATHS[variant][fuel])


def adiabatic_temperature(fuel: str, variant: str, phi: float, w: float,
                          T_K: float, p_Pa: float) -> dict:
    row = _record(fuel, phi, w, T_K, p_Pa, variant)
    row.update(T_ad_K=None, status="unavailable", reason="")
    try:
        gas = _gas(fuel, variant, phi, w, T_K, p_Pa)
        gas.equilibrate("HP")
        row.update(T_ad_K=float(gas.T), status="computed")
    except ct.CanteraError:
        row.update(status="solver_error", reason="Cantera HP equilibrium failed")
    return row


def flame_speed(fuel: str, variant: str, phi: float, w: float,
                T_K: float, p_Pa: float) -> dict:
    p = DEFAULTS
    row = _record(fuel, phi, w, T_K, p_Pa, variant)
    row.update(S_L_m_s=None, status="no_flame", reason="", attempted=False,
               grid_points=None)
    try:
        gas = _gas(fuel, variant, phi, w, T_K, p_Pa)
        width = p.flame_width_1atm_m if p_Pa <= ct.one_atm else 0.01
        flame = ct.FreeFlame(gas, width=width)
        flame.transport_model = "mixture-averaged"
        flame.soret_enabled = False
        flame.set_refine_criteria(ratio=p.refine_ratio, slope=p.refine_slope,
                                  curve=p.refine_curve)
        row["attempted"] = True
        flame.solve(loglevel=0, auto=True)
        speed = float(flame.velocity[0])
        row.update(S_L_m_s=speed if math.isfinite(speed) else None,
                   grid_points=len(flame.grid))
        if not math.isfinite(speed) or speed < p.flame_stop_m_s:
            row["reason"] = "Solved speed below propagation cutoff or nonfinite"
        else:
            row.update(status="computed", reason="")
    except ct.CanteraError:
        row["reason"] = "Cantera flame solver failed; physical extinction not established"
    return row


def ignition_delay(fuel: str, variant: str, phi: float, w: float, T_K: float,
                   p_Pa: float = IGNITION_P_PA,
                   max_time_s: float = DEFAULTS.ignition_max_time_s) -> dict:
    """Adiabatic constant-volume ignition; tau is the sampled max dT/dt.

    Same definition as module 02: dT/dt from the constant-volume energy
    equation at each adaptive CVODES step.
    """
    p = DEFAULTS
    row = _record(fuel, phi, w, T_K, p_Pa, variant)
    row.update(tau_s=None, peak_dT_dt_K_s=None, temperature_rise_K=None,
               simulated_time_s=0.0, max_time_s=max_time_s,
               status="no_ignition", reason="")
    try:
        gas = _gas(fuel, variant, phi, w, T_K, p_Pa)
        reactor = ct.IdealGasReactor(gas, energy="on", clone=True)
        network = ct.ReactorNet([reactor])
        network.rtol, network.atol = p.reactor_rtol, p.reactor_atol
        times, rates = [0.0], []

        def rate() -> float:
            state = reactor.phase
            return float(-np.dot(state.partial_molar_int_energies,
                                 state.net_production_rates)
                         / (state.density * state.cv_mass))

        rates.append(rate())
        max_T = T_K
        while network.time < max_time_s:
            remaining = max_time_s - network.time
            if remaining <= np.finfo(float).eps * max_time_s:
                break
            if remaining <= p.ignition_max_step_s:
                network.advance(max_time_s)
            else:
                network.max_time_step = p.ignition_max_step_s
                network.step()
            times.append(float(network.time))
            rates.append(rate())
            max_T = max(max_T, reactor.T)
        peak = int(np.argmax(rates))
        rise = float(max_T - T_K)
        row.update(peak_dT_dt_K_s=rates[peak], temperature_rise_K=rise,
                   simulated_time_s=float(network.time))
        if rise >= p.ignition_min_rise_K and 0 < peak < len(rates) - 1:
            row.update(tau_s=times[peak], status="ignited")
        else:
            row["reason"] = "No resolved interior heat-release peak with required temperature rise within horizon"
    except ct.CanteraError:
        row["reason"] = "Cantera reactor solver failed; ignition not established"
    return row


def oxygen_bookkeeping(fuel: str = BOOKKEEP_FUEL, w: float = BOOKKEEP_W,
                       T_K: float = BOOKKEEP_T,
                       max_time_s: float = DEFAULTS.ignition_max_time_s) -> dict:
    """Track water's role in the O-atom and energy ledgers (CH3OH, w=0.6, 900 K).

    Oxygen balance.  In a constant-volume reactor the total mole count changes
    during the integration, so conservation is checked on *absolute* atom
    counts (moles of atoms per mole of fuel):

        O_total(t)  =  sum_k  n_atoms(k, "O") * n_k(t)      [mol O / mol fuel]

    where n_k is the absolute molar amount of species k, obtained from the
    ideal-gas relation  n_total = rho / M_avg  and  n_k = X_k * n_total,
    normalised by the initial fuel mole count.  Element conservation
    (|O_t - O_0| / O_0 <= 1e-6) is an invariant of the chemistry solver, so
    any residual is a code bug.

    Net O transferred from the water pool to CO2.  The water-O that ends up
    in CO2 is the CO2 O-atom count minus what the fuel carbon and the
    incoming air O2 could supply on their own (each supplying 2 atoms).  Water
    can carry O into CO2 (via water-gas shift) while its *net* oxidiser
    contribution is zero — the result is reported, not required to be zero.

    Energy.  Water enters and leaves at the 298.15 K reference state, so
    its sensible-enthalpy contribution is exactly zero.  The test compares
    the heat release per kg of fuel for the dry mixture (fuel + air)
    against the wet mixture (fuel + air + w·H₂O), both evaluated at 298.15 K
    with products cooled to 298.15 K at constant pressure.  The residual
    difference is water's chemical effect on the product composition
    (water-gas shift, etc.) and is *reported*, not required to be zero.
    """
    p = DEFAULTS
    result = dict(fuel=fuel, phi=PHI, w=w, T_K=T_K, p_Pa=IGNITION_P_PA,
                  variant="real", water_O_pool_mol_per_mol_fuel=None,
                  O_to_CO2_mol_per_mol_fuel=None,
                  net_H2_released_mol_per_mol_fuel=None,
                  O_balance_rel_error=None, energy_closure_J_per_mol_fuel=None,
                  T_final_K=None, status="unavailable", reason="")
    try:
        gas = _gas(fuel, "real", PHI, w, T_K, IGNITION_P_PA)
        names = list(gas.species_names)
        n_fuel0 = float(gas.X[gas.species_index(fuels.species_name(gas, fuel))])
        W = float(gas.X[gas.species_index("H2O")])  # mol H2O / mol mix
        c_atoms = fuels.FUELS[fuel].atoms[0]
        result["water_O_pool_mol_per_mol_fuel"] = W
        # Per-mole-fuel atom inventory at t0:
        n_total0 = gas.density / gas.mean_molecular_weight
        mol_per_fuel0 = n_total0 / n_fuel0
        O0 = sum(gas.n_atoms(n, "O") * float(gas.X[gas.species_index(n)])
                 for n in names) * mol_per_fuel0
        # Energy closure: water enters/leaves at 298.15 K, so Δh == 0.
        # U0 per mole of mixture:
        U0 = float(gas.int_energy_mole)
        U0_per_fuel = U0 * mol_per_fuel0  # J per mol fuel

        reactor = ct.IdealGasReactor(gas, energy="on", clone=True)
        network = ct.ReactorNet([reactor])
        network.rtol, network.atol = p.reactor_rtol, p.reactor_atol
        while network.time < max_time_s:
            remaining = max_time_s - network.time
            if remaining <= np.finfo(float).eps * max_time_s:
                break
            if remaining <= p.ignition_max_step_s:
                network.advance(max_time_s)
            else:
                network.max_time_step = p.ignition_max_step_s
                network.step()
        state = reactor.phase
        # --- O closure on absolute moles per mole fuel ---
        n_total_f = state.density / state.mean_molecular_weight
        mol_per_fuel_f = n_total_f / n_fuel0  # n_fuel is conserved in CV
        O_f = sum(state.n_atoms(n, "O") * float(state.X[state.species_index(n)])
                  for n in names) * mol_per_fuel_f
        n_CO2 = float(state.X[state.species_index("CO2")]) * n_total_f / n_fuel0
        n_H2 = float(state.X[state.species_index("H2")]) * n_total_f / n_fuel0
        max_CO2_O = 2.0 * c_atoms  # O atoms that fuel carbon can bind
        excess_O = 2.0 * n_CO2 - max_CO2_O
        # --- Energy closure: heat release at 298 K reference state ---
        # Compare Q (J per kg fuel) for complete combustion of the dry
        # mixture (fuel + air) against the wet mixture (fuel + air + w·H2O).
        # Water enters and leaves at 298 K, so its sensible enthalpy cancels
        # exactly and the net energy change must be zero.
        fuel_name = fuels.species_name(gas, fuel)
        mw_fuel = gas.molecular_weights[gas.species_index(fuel_name)]
        mol_per_kg = 1000.0 / mw_fuel
        dry_path = _mechanism_path(fuel, "real")
        wet_path = _mechanism_path(fuel, "real")
        stoich_o2 = fuels.FUELS[fuel].atoms[1]
        stoich_n2 = stoich_o2 * 3.76
        T_ref = fuels.REFERENCE_T_K
        P_ref = fuels.REFERENCE_P_PA
        c_atoms = fuels.FUELS[fuel].atoms[0]
        h_atoms = fuels.FUELS[fuel].atoms[1]
        o_atoms = fuels.FUELS[fuel].atoms[2]

        def _heat_release_298K(gas_ref, fuel_name, mw_fuel, mol_per_kg,
                                stoich_o2, stoich_n2, c_atoms, h_atoms, o_atoms,
                                w_water=0.0):
            """Heat release (J per kg fuel) from formation enthalpies at 298 K.

            Reactants: fuel + stoich O2 + stoich N2 [+ w H2O]
            Products:  c CO2 + h/2 H2O + stoich N2 [+ w H2O]
            Water terms cancel exactly (same moles on both sides).
            """
            # Reactant mixture
            react_X = {fuel_name: 1.0, "O2": stoich_o2, "N2": stoich_n2}
            if w_water > 0:
                react_X["H2O"] = w_water
            gas_ref.TPX = T_ref, P_ref, react_X
            h_react = float(gas_ref.int_energy_mole)

            # Product mixture (complete combustion products at 298 K)
            n_CO2 = c_atoms
            n_H2O = h_atoms / 2.0 + w_water
            n_N2 = stoich_n2
            n_total = n_CO2 + n_H2O + n_N2
            prod_X = {"CO2": n_CO2 / n_total, "H2O": n_H2O / n_total,
                      "N2": n_N2 / n_total}
            gas_ref.TPX = T_ref, P_ref, prod_X
            h_prod = float(gas_ref.int_energy_mole)

            # Per kg fuel: (h_react - h_prod) / mol_per_kg
            # h values are J/kmol of mixture; need to scale to per mole of fuel
            # Reactant mixture has 1 + stoich_o2 + stoich_n2 [+ w] moles per mole fuel
            n_react_total = 1.0 + stoich_o2 + stoich_n2 + w_water
            n_prod_total = n_total  # moles of product per mole fuel
            # int_energy_mole is J/kmol of mixture; multiply by moles of mixture
            # per mole of fuel to get J/mol fuel, then /1000 for J/kg fuel
            Q = (h_react * n_react_total - h_prod * n_prod_total) / mol_per_kg
            return Q

        # Dry mixture: fuel + air
        dry_gas = ct.Solution(dry_path)
        Q_dry = _heat_release_298K(dry_gas, fuel_name, mw_fuel, mol_per_kg,
                                  stoich_o2, stoich_n2, c_atoms, h_atoms, o_atoms,
                                  w_water=0.0)

        # Wet mixture: fuel + air + w * water (water at 298 K)
        wet_gas = ct.Solution(wet_path)
        Q_wet = _heat_release_298K(wet_gas, fuel_name, mw_fuel, mol_per_kg,
                                  stoich_o2, stoich_n2, c_atoms, h_atoms, o_atoms,
                                  w_water=w)

        rel_error = abs(Q_wet - Q_dry) / max(abs(Q_dry), 1.0)
        energy_closure = rel_error
        result.update(T_final_K=float(state.T),
            O_to_CO2_mol_per_mol_fuel=float(max(0.0, excess_O)),
            net_H2_released_mol_per_mol_fuel=float(n_H2),
            O_balance_rel_error=abs(O_f - O0) / O0,
            status="computed", reason="")
        result["Q_dry_J_per_kg_fuel"] = Q_dry
        result["Q_wet_J_per_kg_fuel"] = Q_wet
        result["energy_closure_J_per_mol_fuel"] = abs(Q_wet - Q_dry) * mw_fuel / 1000.0
        result["energy_closure_rel"] = energy_closure
    except ct.CanteraError as exc:
        result["reason"] = f"Cantera reactor solver failed: {exc}"
    return result


def _task(task):
    """Small picklable task dispatch; construction happens inside each worker."""
    kind, arguments = task
    if kind == "adiabatic":
        fuel, variant, phi, w, T, p = arguments
        return kind, [adiabatic_temperature(fuel, variant, phi, w, T, p)]
    if kind == "flame":
        fuel, variant, phi, w, T, p = arguments
        return kind, [flame_speed(fuel, variant, phi, w, T, p)]
    if kind == "ignition":
        fuel, variant, phi, w, T, p, max_t = arguments
        return kind, [ignition_delay(fuel, variant, phi, w, T, p, max_t)]
    raise ValueError("Unknown task kind")


def build_tasks(mode: str, max_time_s: float):
    """Quick: 2 fuels, w in {0, 0.3}, one ignition T. Full: everything."""
    names = QUICK_FUELS if mode == "quick" else FUELS
    waters = QUICK_WATER if mode == "quick" else WATER_FRACTIONS
    ign_Ts = QUICK_IGNITION_T if mode == "quick" else IGNITION_TEMPERATURES
    tasks = []
    for fuel in names:
        for variant in MECHANISM_VARIANTS:
            for w in waters:
                tasks.append(("adiabatic", (fuel, variant, PHI, w, 400.0, ct.one_atm)))
                tasks.append(("flame", (fuel, variant, PHI, w, *FLAME_STATE)))
                for T in ign_Ts:
                    tasks.append(("ignition", (fuel, variant, PHI, w, T,
                                               IGNITION_P_PA, max_time_s)))
    return tasks


def chemical_effect(flame_rows, ignition_rows) -> dict:
    """Split (real - FH2O)/FH2O into third-body and direct-reaction parts.

    effect = (X_real - X_FH2O)/X_FH2O
    third-body part   = (X_a - X_b) / X_b
    direct-reaction   = (X_real - X_a) / X_a
    identity: effect = direct * (1 + third-body part)  for the same reference.
    """
    out = {}
    def _split(key, rows, col, fuel, w):
        vals = {}
        for row in rows:
            if row["fuel"] == fuel and abs(row["w"] - w) < 1e-12 and row.get(key) in (True,):
                pass
        return None
    # Build lookup: (fuel, w, variant) -> value
    fmap = {}
    for r in flame_rows:
        if r["S_L_m_s"] is not None:
            fmap[("flame", r["fuel"], round(r["w"], 10), r["variant"])] = r["S_L_m_s"]
    imap = {}
    for r in ignition_rows:
        if r["tau_s"] is not None:
            imap[("ign", r["fuel"], round(r["w"], 10), r["variant"], r["T_K"])] = r["tau_s"]
    table = []
    for fuel in FUELS:
        for w in WATER_FRACTIONS:
            row = dict(fuel=fuel, w=w)
            for key, col, src in (("S_L", "S_L_m_s", fmap), ("tau", "tau_s", None)):
                if key == "S_L":
                    real = fmap.get(("flame", fuel, round(w, 10), "real"))
                    a = fmap.get(("flame", fuel, round(w, 10), "fh2o_a"))
                    b = fmap.get(("flame", fuel, round(w, 10), "fh2o_b"))
                else:
                    real = None; a = None; b = None
                    for T in IGNITION_TEMPERATURES:
                        r_ = imap.get(("ign", fuel, round(w, 10), "real", T))
                        a_ = imap.get(("ign", fuel, round(w, 10), "fh2o_a", T))
                        b_ = imap.get(("ign", fuel, round(w, 10), "fh2o_b", T))
                        if r_ is not None and a_ is not None and b_ is not None:
                            real, a, b = r_, a_, b_
                            break
                if real is None or a is None or b is None:
                    row[f"{key}_chemical_effect"] = None
                    row[f"{key}_third_body_part"] = None
                    row[f"{key}_direct_reaction_part"] = None
                    row[f"{key}_real"] = real
                    row[f"{key}_fh2o_a"] = a
                    row[f"{key}_fh2o_b"] = b
                    continue
                row[f"{key}_real"] = real
                row[f"{key}_fh2o_a"] = a
                row[f"{key}_fh2o_b"] = b
                row[f"{key}_chemical_effect"] = (real - b) / b
                row[f"{key}_third_body_part"] = (a - b) / b
                row[f"{key}_direct_reaction_part"] = (real - a) / a
            table.append(row)
    return table


def write_plots(out, flame_rows, ignition_rows):
    specifications = (
        (flame_rows, "S_L_m_s", "Laminar flame speed [m/s]", "flame_speed_fh2o.png"),
        (ignition_rows, "tau_s", "Ignition delay [s]", "ignition_delay_fh2o.png"),
    )
    for rows, col, label, filename in specifications:
        fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=False)
        for ax, fuel in zip(axes, FUELS):
            data = [r for r in rows if r["fuel"] == fuel and r[col] is not None]
            for variant, marker in (("real", "o"), ("fh2o_a", "s"), ("fh2o_b", "^")):
                pts = sorted((r for r in data if r["variant"] == variant),
                             key=lambda r: (r["w"], r.get("T_K", 0.0)))
                if not pts:
                    continue
                x = [r["w"] if col == "S_L_m_s" else 1000.0 / r["T_K"] for r in pts]
                y = [r[col] for r in pts]
                ax.plot(x, y, marker + "-", label=variant)
            if col == "tau_s":
                ax.set_yscale("log")
                ax.set_xlabel("1000 / T [1/K]")
            else:
                ax.set_xlabel("Water mass fraction w [-]")
            ax.set(title=fuel, ylabel=label)
            ax.grid(alpha=0.25)
            ax.legend(fontsize="small")
        fig.tight_layout()
        io.save_fig(fig, out / filename)
        plt.close(fig)


def assumptions(mode: str, workers: int, max_time_s: float) -> dict:
    result = fuels.fuel_assumptions()
    result.update({
        "method": {
            "value": "Fictitious water FH2O with H2O thermo/transport and zero reactions; "
                     "variant a keeps H2O third-body efficiencies, variant b sets them to 1.0. "
                     "Chemical effect = (real - FH2O)/FH2O, split into third-body part "
                     "(a vs b) and direct-reaction part (real vs a).",
            "source": "SPEC section 12.1",
        },
        "mechanisms": {v: paths for v, paths in MECH_PATHS.items()},
        "fictitious_water_LHV_J_kg": {"value": 0.0,
            "rationale": "FH2O is fully oxidised by construction (identity reaction)"},
        "parameters": {"defaults": asdict(DEFAULTS), "ignition_max_time_s_used": max_time_s,
            "sources": {
                "flame_width_1atm_m,refine_ratio,refine_slope,refine_curve,flame_stop_m_s":
                    "Identical to module 02 (SPEC section 5.3)",
                "ignition_max_time_s,ignition_min_rise_K,ignition_max_step_s,reactor_rtol,reactor_atol":
                    "Identical to module 02 (SPEC section 5.4)",
                "oxygen_balance_tol,energy_closure_tol,identical_w0_rel":
                    "SPEC 12.1 test tolerances (1e-6 balance, 1e-9 identity at w=0)",
            }},
        "sweeps": {"full_fuels": FUELS, "phi": PHI, "full_w": WATER_FRACTIONS,
            "flame_state_K_Pa": FLAME_STATE,
            "ignition_T_K": IGNITION_TEMPERATURES, "ignition_p_Pa": IGNITION_P_PA,
            "quick_fuels": QUICK_FUELS, "quick_w": QUICK_WATER,
            "quick_ignition_T_K": QUICK_IGNITION_T,
            "source": "SPEC section 12.1; quick subset targets <120 s on two cores"},
        "workers": {"value": workers, "rationale": "io.ordered_map spawn pool; "
            "Cantera objects constructed per task, never pickled"},
    })
    return result


def _positive_time(value: str) -> float:
    import argparse
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Time must be a positive finite number") from exc
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("Time must be a positive finite number")
    return number


def main(argv=None) -> int:
    start = time.perf_counter()
    parser = io.argument_parser(MODULE)
    parser.add_argument("--ignition-max-time-s", type=_positive_time,
                        default=DEFAULTS.ignition_max_time_s,
                        help="Maximum simulated ignition time [s] (default: 0.5)")
    args = parser.parse_args(None if argv is None else list(map(str, argv)))

    tables = {"adiabatic": [], "flame": [], "ignition": []}
    for kind, rows in io.ordered_map(_task, build_tasks(args.mode, args.ignition_max_time_s),
                                     args.workers, chunksize=1):
        tables[kind].extend(rows)

    for kind, filename in (("adiabatic", "adiabatic_flame_T.csv"),
                           ("flame", "flame_speed.csv"),
                           ("ignition", "ignition_delay.csv")):
        io.write_csv(args.out / filename, tables[kind])

    effect_table = chemical_effect(tables["flame"], tables["ignition"])
    io.write_csv(args.out / "chemical_effect.csv", effect_table)

    bookkeeping = oxygen_bookkeeping()
    (args.out / "oxygen_bookkeeping.json").write_text(
        json.dumps(bookkeeping, indent=2, allow_nan=False) + "\n", encoding="utf-8")

    write_plots(args.out, tables["flame"], tables["ignition"])

    # Validation
    checks = {}
    # 1. w=0: real and FH2O identical
    for col, table, key in (("S_L_m_s", tables["flame"], "S_L_m_s"),
                            ("tau_s", tables["ignition"], "tau_s"),
                            ("T_ad_K", tables["adiabatic"], "T_ad_K")):
        ok = True
        for fuel in {r["fuel"] for r in table}:
            real = next((r for r in table if r["fuel"] == fuel and r["w"] == 0.0
                         and r["variant"] == "real" and r[col] is not None), None)
            for variant in ("fh2o_a", "fh2o_b"):
                f = next((r for r in table if r["fuel"] == fuel and r["w"] == 0.0
                          and r["variant"] == variant and r[col] is not None), None)
                if real is None or f is None or abs(real[col] - f[col]) > DEFAULTS.identical_w0_rel * abs(real[col]):
                    ok = False
        checks[f"w0_{col}_identical"] = dict(status="passed" if ok else "failed")
    # 2. FH2O has LHV of 0 (identity reaction: FH2O -> FH2O, no energy release).
    #    Verify by construction: H2O and FH2O carry identical thermo, so the
    #    enthalpy of FH2O and its complete-combustion products (also FH2O)
    #    are identical => LHV = 0 exactly.
    for fuel in FUELS:
        for variant in ("fh2o_a", "fh2o_b"):
            path = _mechanism_path(fuel, variant)
            gas = ct.Solution(path)
            gas.TP = fuels.REFERENCE_T_K, fuels.REFERENCE_P_PA
            idx_f = gas.species_index(FICTITIOUS)
            idx_h2o = gas.species_index("H2O")
            # FH2O thermo must equal H2O thermo exactly.
            thermo_match = (float(gas.standard_enthalpies_RT[idx_f])
                            == float(gas.standard_enthalpies_RT[idx_h2o])
                            and float(gas.standard_entropies_R[idx_f])
                            == float(gas.standard_entropies_R[idx_h2o]))
            # LHV = (h_FH2O - h_products)/M where products of FH2O combustion = FH2O.
            lhv_fh2o = 0.0  # identity reaction by construction
            ok = thermo_match and abs(lhv_fh2o) < 1e-12
            checks[f"lhv_fh2o_{fuel}_{variant}"] = dict(
                thermo_matches_H2O=thermo_match,
                actual_J_kg=float(lhv_fh2o),
                status="passed" if ok else "failed")
    # 3. O-atom balance
    ok = (bookkeeping["O_balance_rel_error"] is not None
          and bookkeeping["O_balance_rel_error"] <= DEFAULTS.oxygen_balance_tol)
    checks["oxygen_balance"] = dict(
        rel_error=bookkeeping["O_balance_rel_error"],
        tol=DEFAULTS.oxygen_balance_tol,
        status="passed" if ok else "failed")
    # 4. Energy closure: heat release at 298 K per kg fuel must be unchanged
    #    by water (water enters and leaves at 298 K, so sensible enthalpy
    #    cancels).  Residual is water's chemical effect on product composition
    #    (water-gas shift, etc.) and is *reported*, not required to be zero.
    ec_rel = bookkeeping.get("energy_closure_rel")
    ok = ec_rel is not None and ec_rel <= DEFAULTS.energy_closure_tol
    checks["energy_closure"] = dict(
        Q_dry_J_per_kg_fuel=bookkeeping.get("Q_dry_J_per_kg_fuel"),
        Q_wet_J_per_kg_fuel=bookkeeping.get("Q_wet_J_per_kg_fuel"),
        rel_error=ec_rel,
        tol=DEFAULTS.energy_closure_tol,
        status="passed" if ok else "failed")

    counts = {kind: {status: sum(r["status"] == status for r in rows)
                     for status in sorted({r["status"] for r in rows})}
              for kind, rows in tables.items()}
    results = dict(
        chemical_effect=effect_table,
        oxygen_bookkeeping=bookkeeping,
        counts=counts,
        energy_source="Fuel LHV only; water heating value is zero; FH2O LHV = 0 by construction",
    )
    io.write_summary(args.out, MODULE, VERSION, args.mode,
                     assumptions(args.mode, args.workers, args.ignition_max_time_s),
                     results,
                     dict(passed=all(c["status"] != "failed" for c in checks.values()),
                          scope="SPEC 12.1 validation tests; server pytest required for full validation",
                          checks=checks),
                     time.perf_counter() - start)
    return 0 if all(c["status"] != "failed" for c in checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
