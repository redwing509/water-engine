"""Reproducible first-pass carburetor sizing; no engine-module imports.

All calculations use SI. Mean engine demand is converted to an intake-event
flow before sizing the venturi and jets. This is a rectangular-pulse model,
not a prediction of the pressure waveform or a calibrated carburetor map.
See README.md for equations, sources, and the distinction between the
Module 03 pre-water-mixing temperature and a fully vaporized 360 K charge.
"""

from dataclasses import asdict, dataclass
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import re
import time

from sims.common import io

MODULE = "06_carburetor"
VERSION = "1.0.0"
G = 9.80665
R_AIR = 287.05
GAMMA = 1.4
MW = {"N2": 28.014, "O2": 31.998, "H2O": 18.015, "CO2": 44.009,
      "CH3OH": 32.042}
SOURCES = {
    "compressible_flow": "https://www.grc.nasa.gov/www/k-12/airplane/mflchk.html",
    "blend_properties": "https://trc.nist.gov/ThermoML/10.1016/j.jct.2007.05.004.html",
    "atomization": "https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=91016WNN.TXT",
    "evaporation": "https://ntrs.nasa.gov/citations/20040084641",
    "methanol_latent_heat": "https://webbook.nist.gov/cgi/cbook.cgi?ID=C67561&Mask=4",
    "water_properties": "https://iapws.org/relguide/IAPWS95-2018.pdf",
}


@dataclass(frozen=True)
class Parameters:
    displacement_m3: float = 500e-6
    rpm_min: float = 1000.0
    rpm_max: float = 4000.0
    ambient_Pa: float = 101325.0
    tank_T_K: float = 300.0
    intake_event_duty: float = 0.25  # 180 CAD of each 720 CAD four-stroke cycle
    throat_max_mach: float = 0.30
    venturi_Cd: float = 0.95
    jet_Cd_inviscid: float = 0.75
    jet_length_m: float = 0.001
    fuel_float_drop_m: float = 0.006
    idle_map_ratio: float = 0.30
    idle_taper_signal_Pa: float = 700.0
    cruise_WFR: float = 0.50
    valve_fully_open_vacuum_Pa: float = 15000.0
    valve_closed_vacuum_Pa: float = 25000.0
    needle_supply_gauge_Pa: float = 20000.0
    needle_capacity_margin: float = 1.50
    inlet_throat_ratio: float = 1.45
    throttle_throat_ratio: float = 1.30
    drill_increment_m: float = 0.00001  # nominal 0.01 mm, verify by flow testing
    hx_effectiveness: float = 0.60
    exhaust_minimum_T_K: float = 360.0
    water_latent_300K_J_kg: float = 2437000.0
    methanol_latent_300K_J_kg: float = 1169000.0
    plenum_volume_m3: float = 0.001
    droplet_surface_T_K: float = 310.0
    gas_conductivity_W_m_K: float = 0.030
    gas_cp_J_kg_K: float = 1050.0


DEFAULTS = Parameters()
# Rounded preliminary values near 300 K. Blend properties are engineering
# estimates informed by Gonzalez et al. (2007), not an extracted fitted table.
# Surface tensions are screening assumptions. Sweep uncertainty before machining.
LIQUIDS = {
    "blend": dict(density_kg_m3=930.0, viscosity_Pa_s=0.00160, surface_tension_N_m=0.035),
    "fuel": dict(density_kg_m3=785.0, viscosity_Pa_s=0.00055, surface_tension_N_m=0.022),
    "water": dict(density_kg_m3=996.5, viscosity_Pa_s=0.000855, surface_tension_N_m=0.0717),
}


def area(d):
    return math.pi * d*d / 4


def bisect(function, low, high):
    fl, fh = function(low), function(high)
    if fl * fh > 0:
        raise ValueError("Root is not bracketed")
    for _ in range(75):
        mid = (low + high) / 2
        fm = function(mid)
        if fm * fl > 0:
            low, fl = mid, fm
        else:
            high = mid
    return (low + high) / 2


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_inputs(directory):
    directory = Path(directory)
    paths = [directory / "design_point.json", directory / "evo_states.json"]
    design, states = [json.loads(p.read_text(encoding="utf-8-sig")) for p in paths]
    if (design.get("use_for_design") is not True or design.get("validation_passed") is not True
            or design.get("synthetic_fits") is not False):
        raise ValueError("Module 03 must provide a validated, nonsynthetic design")
    point = design["per_fuel"]["CH3OH"]["water_majority"]
    for key, expected in (("CR", 24), ("w", 0.6), ("T_intake_K", 360), ("phi", 1)):
        if not math.isclose(point[key], expected, rel_tol=1e-8):
            raise ValueError(f"Requested CH3OH design point mismatch: {key}")
    evo = states[point["evo_state_key"]]
    if evo.get("synthetic_fits") is not False or evo["composition_basis"] != "mass_fraction":
        raise ValueError("EVO must be real simulation output with mass fractions")
    for key in ("fuel", "CR", "w", "T_intake_K"):
        if evo[key] != point[key]:
            raise ValueError(f"EVO identity mismatch: {key}")
    if not math.isclose(evo["T_K"], point["EVO_T_K"], rel_tol=1e-8):
        raise ValueError("EVO temperature mismatch")
    if not math.isclose(sum(evo["composition"].values()), 1.0, abs_tol=1e-6):
        raise ValueError("EVO composition is not normalized")
    if evo["liquid_water_kg"] != 0:
        raise ValueError("This sensible-exhaust model requires fully gaseous EVO")
    for key in ("air_mass_kg", "fuel_mass_kg", "water_mass_kg", "rpm"):
        if not math.isfinite(point[key]) or point[key] <= 0:
            raise ValueError(f"Invalid Module 03 quantity: {key}")
    if not math.isclose(point["water_mass_kg"] / point["fuel_mass_kg"], 1.5, rel_tol=1e-6):
        raise ValueError("Module 03 water and fuel masses disagree with w")
    provenance = {p.name: sha256(p) for p in paths}
    return point, evo, design["engine"], provenance


def mass_flux(mach, par=DEFAULTS):
    """Isentropic air nozzle flux, kg/m2/s; Mach capped at sonic capacity."""
    if not 0 <= mach <= 1:
        raise ValueError("Mach must be between zero and one")
    return (par.venturi_Cd * par.ambient_Pa / math.sqrt(par.tank_T_K)
            * math.sqrt(GAMMA / R_AIR) * mach
            * (1 + (GAMMA-1)*mach*mach/2)**(-(GAMMA+1)/(2*(GAMMA-1))))


def venturi_state(mdot_event, diameter, par=DEFAULTS):
    capacity = area(diameter) * mass_flux(1, par)
    if mdot_event < 0 or mdot_event > capacity*(1+1e-12):
        raise ValueError("Requested air flow exceeds sonic venturi capacity")
    mach = (1.0 if math.isclose(mdot_event, capacity, rel_tol=1e-12) else
            bisect(lambda m: area(diameter)*mass_flux(m, par)-mdot_event, 0, 1))
    factor = 1 + (GAMMA-1)*mach*mach/2
    T = par.tank_T_K / factor
    pressure = par.ambient_Pa * factor**(-GAMMA/(GAMMA-1))
    return dict(mach=mach, pressure_Pa=pressure,
                signal_Pa=par.ambient_Pa-pressure,
                velocity_m_s=mach*math.sqrt(GAMMA*R_AIR*T),
                density_kg_m3=pressure/(R_AIR*T))


def jet_flow(diameter, signal_Pa, liquid, float_drop_m=0, par=DEFAULTS):
    """kg/s from quadratic orifice + laminar bore loss, resisting float lift.

    dp = mdot^2/(2*rho*Cd^2*A^2) + 128*mu*L*mdot/(pi*rho*d^4).
    The additive viscous term is a short-bore engineering correction, not an
    experimentally fitted carburetor Cd(Re) relation.
    """
    if diameter <= 0:
        raise ValueError("Jet diameter must be positive")
    rho, mu = liquid["density_kg_m3"], liquid["viscosity_Pa_s"]
    dp = max(0, signal_Pa-rho*G*float_drop_m)
    a = 1/(2*rho*par.jet_Cd_inviscid**2*area(diameter)**2)
    b = 128*mu*par.jet_length_m/(math.pi*rho*diameter**4)
    return 0.0 if dp == 0 else 2*dp/(b+math.sqrt(b*b+4*a*dp))


def effective_cd(diameter, signal, liquid, head, par=DEFAULTS):
    dp = signal-liquid["density_kg_m3"]*G*head
    if dp <= 0:
        return 0.0
    return jet_flow(diameter, signal, liquid, head, par)/(area(diameter)*math.sqrt(2*liquid["density_kg_m3"]*dp))


def size_jet(mdot, signal, liquid, head, par=DEFAULTS):
    d = bisect(lambda d: jet_flow(d, signal, liquid, head, par)-mdot, 1e-5, 0.02)
    return round(d/par.drill_increment_m)*par.drill_increment_m


def valve_opening(vacuum_Pa, par=DEFAULTS):
    return min(1, max(0, (par.valve_closed_vacuum_Pa-vacuum_Pa) /
                         (par.valve_closed_vacuum_Pa-par.valve_fully_open_vacuum_Pa)))


def wfr_area_formula(fuel_d, water_jets, signal, fuel_head, water_head, par=DEFAULTS):
    """General unequal-head formula; reduces to Cd*A*sqrt(rho) at equal dp.

    water_jets is a list of (diameter, open fraction), i.e. parallel paths.
    Effective Cd includes viscosity at this operating point.
    """
    f, w = LIQUIDS["fuel"], LIQUIDS["water"]
    dp_f = max(0, signal-f["density_kg_m3"]*G*fuel_head)
    dp_w = max(0, signal-w["density_kg_m3"]*G*water_head)
    cf = effective_cd(fuel_d, signal, f, fuel_head, par)
    if dp_f <= 0 or cf == 0:
        return None
    wa = sum(opened*effective_cd(d, signal, w, water_head, par)*area(d)
             for d, opened in water_jets)
    return wa/(cf*area(fuel_d))*math.sqrt(w["density_kg_m3"]*dp_w/(f["density_kg_m3"]*dp_f))


@lru_cache(maxsize=8)
def thermo_data(mechanism):
    """Read only the NASA7 numeric blocks needed from checked-in Cantera YAML.

    This deliberately narrow reader fails closed for other schemas. It avoids
    requiring a kinetics solver for polynomial sensible-enthalpy integration.
    """
    text = Path(mechanism).read_text(encoding="utf-8")
    result = {}
    species_text = text.split("\nspecies:\n", 1)[1].split("\nreactions:", 1)[0]
    for block in re.split(r"(?m)^- name: ", species_text)[1:]:
        name = block.splitlines()[0].strip()
        if name not in MW:
            continue
        if "model: NASA7" not in block:
            raise ValueError("Expected NASA7 thermodynamics")
        ranges = json.loads(re.search(r"temperature-ranges: (\[[^]]+\])", block)[1])
        data = block.split("data:", 1)[1]
        coefficients = [json.loads(s) for s in re.findall(r"- (\[[^]]+\])", data)[:2]]
        if len(ranges) != 3 or len(coefficients) != 2 or any(len(a) != 7 for a in coefficients):
            raise ValueError("Invalid NASA7 block")
        result[name] = (ranges, coefficients)
    return result


def sensible_h(species, t0, t1, mechanism):
    """Integrate NASA7 cp exactly, returning J/kg (formation h cancels)."""
    if t1 < t0:
        return -sensible_h(species, t1, t0, mechanism)
    ranges, coefficients = thermo_data(str(mechanism))[species]
    if t0 < ranges[0] or t1 > ranges[-1]:
        raise ValueError("Temperature outside checked-in NASA polynomial range")
    nodes = [t0] + ([ranges[1]] if t0 < ranges[1] < t1 else []) + [t1]
    integral = 0
    for lo, hi in zip(nodes, nodes[1:]):
        a = coefficients[int((lo+hi)/2 >= ranges[1])]
        integral += sum(a[i]*(hi**(i+1)-lo**(i+1))/(i+1) for i in range(5))
    return 8314.462618/MW[species]*integral


def heat_balance(point, evo, engine, par=DEFAULTS):
    mechanism = io.REPO_ROOT / evo["mechanism"]
    scale = par.displacement_m3/engine["displacement_m3"]
    cycles_s = point["rpm"]/120
    mf, mw, ma = [point[k]*scale for k in ("fuel_mass_kg", "water_mass_kg", "air_mass_kg")]
    t0, t1 = par.tank_T_K, point["T_intake_K"]
    air_o2 = MW["O2"]/(MW["O2"]+3.76*MW["N2"])
    air_heat = ma*(air_o2*sensible_h("O2", t0, t1, mechanism)
                   +(1-air_o2)*sensible_h("N2", t0, t1, mechanism))
    fuel_heat = mf*(par.methanol_latent_300K_J_kg+sensible_h("CH3OH", t0, t1, mechanism))
    water_heat = mw*(par.water_latent_300K_J_kg+sensible_h("H2O", t0, t1, mechanism))
    # Residual gas is recirculating mass; net exhaust per cycle is fresh intake.
    fresh_exhaust = ma+mf+mw
    dh = sum(y*sensible_h(s, par.exhaust_minimum_T_K, evo["T_K"], mechanism)
             for s, y in evo["composition"].items())
    available = max(0, fresh_exhaust*dh)*par.hx_effectiveness
    full = air_heat+fuel_heat+water_heat
    upstream = air_heat+fuel_heat  # Water enters cold, as in Module 03.
    return dict(
        basis="2000 rpm WOT; fresh exhaust mass; frozen EVO composition; no condensation credit",
        EVO_T_K=evo["T_K"], exhaust_minimum_T_K=par.exhaust_minimum_T_K,
        hx_effectiveness=par.hx_effectiveness,
        effectiveness_definition="0.6 times hot-side sensible availability down to 360 K; screening heat-recovery factor, not a solved two-stream HX",
        fresh_exhaust_mass_flow_kg_s=fresh_exhaust*cycles_s,
        exhaust_sensible_available_kW=fresh_exhaust*dh*cycles_s/1000,
        recovered_exhaust_heat_kW=available*cycles_s/1000,
        intake_heating_needed_kW=full*cycles_s/1000,
        air_sensible_kW=air_heat*cycles_s/1000,
        methanol_vaporization_and_sensible_kW=fuel_heat*cycles_s/1000,
        water_vaporization_and_sensible_kW=water_heat*cycles_s/1000,
        margin_kW=(available-full)*cycles_s/1000,
        passed=available >= full, status="PASS" if available >= full else "FAIL",
        pass_fail="PASS" if available >= full else "FAIL",
        module03_compatible=dict(
            description="Energy budget for Module 03 idealization: air and methanol vapour initially at 360 K, water at 300 K; subsequent mixing cools the charge. Not a selective vaporization prediction for the premix",
            intake_heating_needed_kW=upstream*cycles_s/1000,
            passed=available >= upstream, T_IVC_K=point["T_IVC_K"],
            water_evaporated_fraction=point["f_evap_intake_effective"]),
        limitations=["EVO temperature is an optimistic HX inlet proxy; exhaust blowdown and pipe losses are not resolved.",
                     "Full vaporization at 360 K changes trapped density and the Module 03 cycle; rerun Module 03 for that configuration.",
                     "Heat of mixing, wall films and cold-start heat supply are not included; water has zero fuel heating value."],
        mechanism_sha256=sha256(mechanism))


def smd(velocity, liquid, liquid_volume_flow, air_volume_flow):
    """Nukiyama-Tanasawa correlation, explicitly converted from cgs to SI.

    d[um] = 585/u[m/s]*sqrt(sigma[dyn/cm]/rho[g/cm3])
            + 597*(mu[poise]/sqrt(sigma*rho))^.45*(1000*Ql/Qa)^1.5.
    """
    rho, mu, sigma = liquid["density_kg_m3"]/1000, liquid["viscosity_Pa_s"]*10, liquid["surface_tension_N_m"]*1000
    return 1e-6*(585/velocity*math.sqrt(sigma/rho)
                 +597*(mu/math.sqrt(sigma*rho))**0.45*(1000*liquid_volume_flow/air_volume_flow)**1.5)


def evaporation(diameter, liquid, latent, gas_T, par=DEFAULTS):
    # Stagnant isolated-drop, heat-limited d^2 model with Nu=2.
    bt = par.gas_cp_J_kg_K*max(0, gas_T-par.droplet_surface_T_K)/latent
    k = 8*par.gas_conductivity_W_m_K/(liquid["density_kg_m3"]*par.gas_cp_J_kg_K)*math.log1p(bt)
    return dict(d2_constant_m2_s=k, evaporation_time_s=None if k == 0 else diameter**2/k)


def operating_point(design, rpm, map_ratio, par=DEFAULTS):
    if not par.rpm_min <= rpm <= par.rpm_max or not par.idle_map_ratio <= map_ratio <= 1:
        raise ValueError("Operating point outside sized map")
    ref = design["design_point"]
    air = ref["air_mass_flow_kg_s"]*rpm/ref["rpm"]*map_ratio
    event_air = air/par.intake_event_duty
    state = venturi_state(event_air, design["venturi"]["throat_diameter_m"], par)
    vacuum = par.ambient_Pa-map_ratio*ref["p_manifold_Pa"]
    idle_fraction = max(0, 1-state["signal_Pa"]/par.idle_taper_signal_Pa)
    opening = valve_opening(vacuum, par)

    def flows(circuit, liquid):
        head = circuit["float_level_below_throat_m"]
        main = jet_flow(circuit["main_jet_diameter_m"], state["signal_Pa"], liquid, head, par)
        idle = idle_fraction*jet_flow(circuit["idle_jet_diameter_m"], vacuum, liquid, head, par)
        return main*par.intake_event_duty, idle*par.intake_event_duty

    am, ai = flows(design["option_A"], LIQUIDS["blend"])
    bm, bi = flows(design["option_B"]["fuel"], LIQUIDS["fuel"])
    wm, wi = flows(design["option_B"]["water"], LIQUIDS["water"])
    power = opening*par.intake_event_duty*jet_flow(
        design["option_B"]["water_power_valve"]["jet_diameter_m"], state["signal_Pa"],
        LIQUIDS["water"], design["option_B"]["water"]["float_level_below_throat_m"], par)
    fuel_a, water_a = (am+ai)*(1-ref["w"]), (am+ai)*ref["w"]
    fuel_b, water_b = bm+bi, wm+wi+power
    result = []
    for option, fuel, water, main_f, idle_f in (("A", fuel_a, water_a, am*(1-ref["w"]), ai*(1-ref["w"])),
                                               ("B", fuel_b, water_b, bm, bi)):
        afr = air/fuel
        result.append(dict(option=option, rpm=rpm, manifold_ratio=map_ratio,
                           manifold_Pa=map_ratio*ref["p_manifold_Pa"], air_mass_flow_kg_s=air,
                           fuel_mass_flow_kg_s=fuel, water_mass_flow_kg_s=water,
                           main_fuel_mass_flow_kg_s=main_f, idle_fuel_mass_flow_kg_s=idle_f,
                           AFR=afr, phi=ref["stoichiometric_AFR"]/afr, WFR=water/fuel,
                           throat_signal_Pa=state["signal_Pa"], throat_mach=state["mach"],
                           water_power_valve_open_fraction=opening if option == "B" else 0.0,
                           main_water_mass_flow_kg_s=wm if option == "B" else am*ref["w"],
                           power_water_mass_flow_kg_s=power if option == "B" else 0.0))
    return result


def build_design(input_dir, par=DEFAULTS):
    point, evo, engine, provenance = read_inputs(input_dir)
    scale = par.displacement_m3/engine["displacement_m3"]
    air, fuel, water = [point[k]*scale*point["rpm"]/120 for k in ("air_mass_kg", "fuel_mass_kg", "water_mass_kg")]
    max_event_air = air*par.rpm_max/point["rpm"]/par.intake_event_duty
    throat = math.sqrt(4*max_event_air/(math.pi*mass_flux(par.throat_max_mach, par)))
    throat = math.ceil(throat/0.0001)*0.0001
    signal = venturi_state(air/par.intake_event_duty, throat, par)["signal_Pa"]
    idle_air = air*par.rpm_min/point["rpm"]*par.idle_map_ratio
    idle_signal = venturi_state(idle_air/par.intake_event_duty, throat, par)["signal_Pa"]
    idle_vacuum = par.ambient_Pa-engine["p_ivc_Pa"]*par.idle_map_ratio
    idle_taper = max(0, 1-idle_signal/par.idle_taper_signal_Pa)
    if idle_taper <= 0:
        raise ValueError("Idle taper suppresses calibration point")
    fuel_head = par.fuel_float_drop_m
    # Equal pressure heads, not equal physical heights: rho_w*h_w = rho_f*h_f.
    water_head = fuel_head*LIQUIDS["fuel"]["density_kg_m3"]/LIQUIDS["water"]["density_kg_m3"]

    def circuit(name, flow, idle_flow, head, max_flow):
        liquid = LIQUIDS[name]
        main_d = size_jet(flow/par.intake_event_duty, signal, liquid, head, par)
        idle_main = jet_flow(main_d, idle_signal, liquid, head, par)*par.intake_event_duty
        idle_d = size_jet(max(0, idle_flow-idle_main)/(par.intake_event_duty*idle_taper),
                          idle_vacuum, liquid, head, par)
        needle = size_jet(max_flow*par.needle_capacity_margin, par.needle_supply_gauge_Pa, liquid, 0, par)
        if jet_flow(needle, par.needle_supply_gauge_Pa, liquid, 0, par) < max_flow*par.needle_capacity_margin:
            needle += par.drill_increment_m
        return dict(main_jet_diameter_m=main_d, idle_jet_diameter_m=idle_d,
                    float_level_below_throat_m=head, needle_seat_diameter_m=needle,
                    jet_length_m=par.jet_length_m, liquid_properties=liquid,
                    main_jet_Cd_effective=effective_cd(main_d, signal, liquid, head, par),
                    needle_capacity_kg_s=jet_flow(needle, par.needle_supply_gauge_Pa, liquid, 0, par),
                    main_jet_reynolds=4*jet_flow(main_d, signal, liquid, head, par)/(math.pi*main_d*liquid["viscosity_Pa_s"]))

    idle_scale = idle_air/air
    max_scale = par.rpm_max/point["rpm"]
    a = circuit("blend", fuel+water, (fuel+water)*idle_scale, fuel_head, (fuel+water)*max_scale)
    bf = circuit("fuel", fuel, fuel*idle_scale, fuel_head, fuel*max_scale)
    bw = circuit("water", fuel*par.cruise_WFR, fuel*idle_scale*par.cruise_WFR, water_head, water*max_scale)
    power_d = size_jet((water-fuel*par.cruise_WFR)/par.intake_event_duty, signal, LIQUIDS["water"], water_head, par)
    design = dict(module=MODULE, version=VERSION, git_sha=io.git_sha(), synthetic_fits=False,
                  design_status="preliminary sizing; flow-bench and engine calibration required",
                  provenance=provenance,
                  design_point=dict(fuel="CH3OH", CR=24, w=0.6, WFR=1.5, T_intake_K=360,
                                    rpm=point["rpm"], displacement_m3=par.displacement_m3,
                                    module03_displacement_m3=engine["displacement_m3"],
                                    p_manifold_Pa=engine["p_ivc_Pa"],
                                    air_mass_flow_kg_s=air, fuel_mass_flow_kg_s=fuel,
                                    water_mass_flow_kg_s=water, stoichiometric_AFR=air/fuel,
                                    evo_state_key=point["evo_state_key"]),
                  venturi=dict(throat_diameter_m=throat, inlet_diameter_m=throat*par.inlet_throat_ratio,
                               throttle_bore_diameter_m=throat*par.throttle_throat_ratio,
                               design_signal_Pa=signal, maximum_event_air_mass_flow_kg_s=max_event_air,
                               maximum_mach=venturi_state(max_event_air, throat, par)["mach"]),
                  option_A=dict(fuel="CH3OH", water_mass_fraction=0.6, **a,
                                circuit="One premix bowl supplies main and idle/progression passages; both meter 40/60 methanol/water by mass"),
                  option_B=dict(fuel=bf, water=bw, cruise_WFR_target=par.cruise_WFR, WOT_WFR_target=1.5,
                                water_power_valve=dict(jet_diameter_m=power_d,
                                    fully_open_below_vacuum_Pa=par.valve_fully_open_vacuum_Pa,
                                    closed_above_vacuum_Pa=par.valve_closed_vacuum_Pa,
                                    topology="Parallel water enrichment jet at the same throat signal; manifold vacuum closes the diaphragm valve",
                                    interlock="Normally closed liquid shutoff linked to engine-running and warm-intake permissives; vacuum alone opens at engine stop",
                                    model="Linear effective-area opening between thresholds; no transient/hysteresis prediction"),
                                WFR_formula="sum(Cd_w*A_w*opening)*sqrt(rho_w*dp_w)/(Cd_f*A_f*sqrt(rho_f*dp_f))",
                                equal_head_formula="sum(Cd_w*A_w*opening)*sqrt(rho_w)/(Cd_f*A_f*sqrt(rho_f))",
                                float_head_note="Water float set for equal hydrostatic pressure lift, not equal geometric float height"),
                  assumptions=dict(parameters=asdict(par), sources=SOURCES,
                      liquid_properties_basis="Rounded estimates near 300 K; blend viscosity/density informed by Gonzalez 2007; no exact data fit claimed",
                      air_demand="Module 03 fresh charge scaled by 500 cc / source displacement, rpm and manifold pressure ratio; constant trapped-temperature/VE proxy",
                      metering="Quasi-steady rectangular intake pulses; atmosphere-vented bowls; main at throat, idle downstream of throttle",
                      idle_progression="Idle effective port area tapers linearly to zero at 700 Pa venturi signal; empirical layout assumption requiring bench calibration",
                      throttle="Map coordinate is manifold pressure ratio, not butterfly angle; no throttle-angle torque model",
                      heat_model="Frozen NASA7 enthalpy from source mechanism; 300 K liquids; additive pure-component vaporization; no water fuel energy",
                      viscosity="Quadratic orifice pressure drop plus laminar bore loss; Cd_inviscid 0.75; effective Cd is reported",
                      drill_sizes="Rounded to 0.01 mm; geometric diameters, not commercial jet-number labels"))
    design["heat_balance"] = heat_balance(point, evo, engine, par)
    rows = operating_point(design, point["rpm"], 1.0, par)
    actual_fuel = rows[1]["main_fuel_mass_flow_kg_s"]
    actual_water = rows[1]["main_water_mass_flow_kg_s"]+rows[1]["power_water_mass_flow_kg_s"]
    formula = wfr_area_formula(bf["main_jet_diameter_m"], [(bw["main_jet_diameter_m"], 1), (power_d, 1)], signal, fuel_head, water_head, par)
    errors = {r["option"]: abs(r["AFR"]/(air/fuel)-1) for r in rows}
    validation = dict(design_AFR_relative_error=errors, AFR_tolerance=0.03,
                      AFR_passed=all(e <= 0.03 for e in errors.values()),
                      option_B_WFR_from_flow=actual_water/actual_fuel,
                      option_B_WFR_from_jet_area_formula=formula,
                      option_B_formula_relative_error=abs(formula/(actual_water/actual_fuel)-1),
                      option_B_formula_passed=math.isclose(formula, actual_water/actual_fuel, rel_tol=1e-10),
                      option_B_WFR_target_passed=abs(rows[1]["WFR"]/1.5-1) <= 0.03,
                      heat_balance_passed=design["heat_balance"]["passed"])
    validation["sizing_passed"] = validation["AFR_passed"] and validation["option_B_formula_passed"] and validation["option_B_WFR_target_passed"]
    design.update(validation=validation, validation_passed=validation["sizing_passed"],
                  use_for_design=validation["sizing_passed"],
                  use_for_design_scope="Concept CAD dimensions only; thermal/full-map feasibility is reported separately",
                  design_point_metering=rows)
    design["design_table"] = [dict(circuit=label, **{k: c[k] for k in (
        "main_jet_diameter_m", "idle_jet_diameter_m", "float_level_below_throat_m", "needle_seat_diameter_m")},
        **{k: design["venturi"][k] for k in ("throat_diameter_m", "inlet_diameter_m", "throttle_bore_diameter_m")})
        for label, c in (("option_A_premix", a), ("option_B_fuel", bf), ("option_B_water", bw))]
    # Atomization at the design point; primary nozzle signal, not idle sprays.
    state = venturi_state(air/par.intake_event_duty, throat, par)
    qair = air/par.intake_event_duty/state["density_kg_m3"]
    # Mean residence includes all vapour volume, conservatively assuming full vaporization.
    molar_flow = air/28.85 + fuel/MW["CH3OH"] + water/MW["H2O"]
    residence = par.plenum_volume_m3/(molar_flow*8314.462618*360/engine["p_ivc_Pa"])
    sprays = {}
    for name, flow, latent in (("blend", fuel+water, 0.4*par.methanol_latent_300K_J_kg+0.6*par.water_latent_300K_J_kg),
                               ("fuel", fuel, par.methanol_latent_300K_J_kg), ("water", water, par.water_latent_300K_J_kg)):
        liquid = LIQUIDS[name]
        d = smd(state["velocity_m_s"], liquid, flow/par.intake_event_duty/liquid["density_kg_m3"], qair)
        ev = evaporation(d, liquid, latent, 360, par)
        sprays[name] = dict(SMD_m=d, **ev, residence_time_s=residence,
                            evaporation_within_residence=ev["evaporation_time_s"] is not None and ev["evaporation_time_s"] <= residence)
    design["atomization"] = dict(design_point=sprays, model="Nukiyama-Tanasawa SMD + isolated-droplet heat-limited d2 law",
        limitation="Screening only: low throat velocity extrapolates the correlation; blend preferential evaporation, spray humidity and wall films unresolved. SMD factor-two uncertainty means evaporation-time factor four.")
    # Stable SI contract consumed by Module 07; keep the enrichment passage
    # explicit instead of disguising it as an enlarged baseline water jet.
    def cad_circuit(c, liquid, water_valve=False):
        return dict(liquid=liquid, main_jet_diameter_m=c["main_jet_diameter_m"],
                    idle_jet_diameter_m=c["idle_jet_diameter_m"],
                    needle_seat_diameter_m=c["needle_seat_diameter_m"],
                    float_level_m=-c["float_level_below_throat_m"],
                    jet_length_m=c["jet_length_m"], vacuum_power_valve=water_valve)
    common = dict(venturi_throat_diameter_m=throat,
                  venturi_inlet_diameter_m=design["venturi"]["inlet_diameter_m"],
                  throttle_bore_diameter_m=design["venturi"]["throttle_bore_diameter_m"])
    design["schema_version"] = 1
    design["options"] = dict(A=dict(common, circuits=[cad_circuit(a, "wet_methanol_w0.6")]),
                             B=dict(common, circuits=[cad_circuit(bf, "methanol"),
                                                      cad_circuit(bw, "water", True)],
                                    water_power_jet_diameter_m=power_d,
                                    water_power_jet_topology="Parallel to baseline water main jet"))
    design["assumptions"]["parameters"].update(
        power_valve_starts_vacuum_Pa=par.valve_closed_vacuum_Pa,
        power_valve_full_vacuum_Pa=par.valve_fully_open_vacuum_Pa)
    design["design_table"].append(dict(circuit="option_B_water_power", main_jet_diameter_m=power_d,
        idle_jet_diameter_m=0.0, float_level_below_throat_m=water_head,
        needle_seat_diameter_m=bw["needle_seat_diameter_m"],
        **{k: design["venturi"][k] for k in ("throat_diameter_m", "inlet_diameter_m", "throttle_bore_diameter_m")}))
    return design


def write_plots(rows, out):
    """Use standard matplotlib; Pillow fallback supports constrained local runs."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        from PIL import Image, ImageDraw
        for quantity in ("phi", "WFR"):
            img = Image.new("RGB", (1500, 800), "white")
            draw = ImageDraw.Draw(img)
            draw.text((50, 20), f"{quantity} [dimensionless] vs manifold pressure ratio [1]", fill="black")
            draw.text((50, 45), "Model screening map: port taper and intake pulses assumed; not bench calibrated", fill="black")
            ymax = max(2, max(r[quantity] for r in rows)*1.05)
            colors = ["#1f77b4", "#2ca02c", "#d62728", "#9467bd", "#ff7f0e", "#17becf", "#8c564b"]
            for panel, option in enumerate(("A", "B")):
                left, top, width, height = 90+panel*740, 100, 590, 540
                draw.text((left, 75), f"Option {option}", fill="black")
                draw.rectangle((left, top, left+width, top+height), outline="black")
                for j in range(6):
                    y = top+height*(1-j/5)
                    draw.line((left, y, left+width, y), fill="#dddddd")
                    draw.text((left-45, y), f"{ymax*j/5:.2f}", fill="black")
                for ratio in (0.3, 0.5, 0.7, 0.9, 1.0):
                    x = left+(ratio-0.3)/0.7*width
                    draw.text((x-10, top+height+10), str(ratio), fill="black")
                draw.text((left+150, top+height+35), "Manifold pressure ratio [1]", fill="black")
                for j, rpm in enumerate(sorted({r["rpm"] for r in rows})):
                    selected = [r for r in rows if r["option"] == option and r["rpm"] == rpm]
                    coords = [(left+(r["manifold_ratio"]-0.3)/0.7*width, top+height*(1-r[quantity]/ymax)) for r in selected]
                    draw.line(coords, fill=colors[j % len(colors)], width=3)
                    draw.text((left+(j % 4)*145, 710+(j//4)*25), f"{rpm:g} rpm", fill=colors[j % len(colors)])
            img.save(out/f"{quantity}_map.png", dpi=(150, 150))
        return "Pillow fallback (matplotlib unavailable)"
    for quantity in ("phi", "WFR"):
        fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
        for ax, option in zip(axes, ("A", "B")):
            for rpm in sorted({r["rpm"] for r in rows}):
                selected = [r for r in rows if r["option"] == option and r["rpm"] == rpm]
                ax.plot([r["manifold_ratio"] for r in selected], [r[quantity] for r in selected], label=f"{rpm:g} rpm")
            ax.set(xlabel="Manifold pressure ratio [1]", ylabel=f"{quantity} [1]", title=f"Option {option}")
            ax.grid(alpha=0.3)
            ax.legend(fontsize=7)
        io.save_fig(fig, out/f"{quantity}_map.png")
        plt.close(fig)
    return "matplotlib"


def main(argv=None):
    parser = io.argument_parser(MODULE)
    parser.add_argument("--engine-results", type=Path, default=io.REPO_ROOT/"results/03_engine_cycle")
    args = parser.parse_args(argv)
    started = time.perf_counter()
    design = build_design(args.engine_results)
    rpms = (1000, 2000, 3000, 4000) if args.mode == "quick" else tuple(range(1000, 4001, 500))
    ratios = tuple(0.30+0.05*i for i in range(15))
    rows = [row for rpm in rpms for ratio in ratios for row in operating_point(design, rpm, ratio)]
    design["operating_map"] = dict(rpm_range=[1000, 4000], manifold_ratio_range=[0.3, 1.0], rows=len(rows),
        heat_balance_scope="Design point only; no Module 03 part-load EVO sweep is available",
        ranges={option: {q: [min(r[q] for r in rows if r["option"] == option), max(r[q] for r in rows if r["option"] == option)]
                         for q in ("phi", "WFR")} for option in ("A", "B")},
        full_map_AFR_within_3pct=all(abs(r["AFR"]/design["design_point"]["stoichiometric_AFR"]-1) <= 0.03 for r in rows),
        limitation="Fixed main/idle jets and assumed progression do not guarantee target AFR throughout the map; tune air bleed/progression on a flow bench")
    args.out.mkdir(parents=True, exist_ok=True)
    io.write_csv(args.out/"operating_map.csv", rows)
    renderer = write_plots(rows, args.out)
    design["assumptions"].update(plot_renderer=renderer, workers_requested=args.workers,
                                  execution="Serial deterministic algebraic sizing; no benefit from multiprocessing")
    (args.out/"carb_design.json").write_text(json.dumps(design, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    io.write_csv(args.out/"design_table.csv", design["design_table"])
    io.write_summary(args.out, MODULE, VERSION, args.mode, design["assumptions"],
                     {k: design[k] for k in ("design_point", "venturi", "heat_balance", "operating_map")},
                     design["validation"], time.perf_counter()-started)
    print(json.dumps(dict(output=str(args.out/"carb_design.json"), validation=design["validation"],
                          heat_balance=design["heat_balance"]["status"]), indent=2))
    return 0 if design["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
