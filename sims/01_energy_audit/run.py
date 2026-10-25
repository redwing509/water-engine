"""SPEC §4 energy audit. All calculations use kg, mol, s, W and J/kg."""

from dataclasses import asdict, dataclass
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sims.common.fuels import (
    FUELS, SAN_DIEGO_PATH, fuel_assumptions, lhv, select_mechanism,
)
from sims.common.io import argument_parser, ordered_map, save_fig, write_csv, write_summary


MODULE = "01_energy_audit"
VERSION = "1.0.0"
# NIST CODATA (2022), Faraday constant, rounded as required by the contract.
# https://physics.nist.gov/cgi-bin/cuu/Value?f
FARADAY_C_MOL = 96485.33212
ELECTRONS_PER_H2 = 2  # Balanced cathode half-reaction: 2H+ + 2e- -> H2.
# All efficiency ranges, sampling defaults and validation targets: SPEC §§4,10.
ENGINE_RANGE = (0.20, 0.45)
ALTERNATOR_RANGE = (0.50, 0.75)
ELECTROLYSER_RANGE = (0.40, 0.80)
FULL_SAMPLES = 200_000
QUICK_SAMPLES = 20_000
RANDOM_SEED = 42
HISTOGRAM_BINS = 100  # Display resolution, not a physical assumption.
LHV_TARGETS_J_KG = {"H2": 120.0e6, "CH4": 50.0e6,
                    "CH3OH": 19.9e6, "C2H5OH": 26.8e6}
LHV_REL_TOL = 0.02
WATER_ABS_TOL_J_KG = 1.0  # SPEC: 1e-6 MJ/kg, expressed in SI.


@dataclass(frozen=True)
class KitParameters:
    """Illustrative kit defaults: current A, voltage V, shaft cruise power W."""

    current_A: float = 20.0
    voltage_V: float = 13.8
    faradaic_efficiency: float = 1.0
    eta_engine: float = sum(ENGINE_RANGE) / 2.0
    eta_alternator: float = sum(ALTERNATOR_RANGE) / 2.0
    cruise_shaft_power_W: float = 15000.0


def loop_gain_samples(n=FULL_SAMPLES, seed=RANDOM_SEED,
                      engine_range=ENGINE_RANGE, alternator_range=ALTERNATOR_RANGE,
                      electrolyser_range=ELECTROLYSER_RANGE):
    """Return (efficiencies, G), dimensionless, using independent uniforms.

    Each row contains engine, alternator and LHV-basis electrolyser efficiency.
    PCG64 and a fixed seed give the same sample sequence for every worker count.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError("n must be a positive integer")
    ranges = np.asarray([engine_range, alternator_range, electrolyser_range], dtype=float)
    if ranges.shape != (3, 2) or not np.isfinite(ranges).all():
        raise ValueError("Each efficiency range must have two finite endpoints")
    if np.any(ranges[:, 0] < 0) or np.any(ranges[:, 1] > 1) or np.any(ranges[:, 0] > ranges[:, 1]):
        raise ValueError("Efficiency ranges must be ordered and within [0, 1]")
    rng = np.random.Generator(np.random.PCG64(seed))
    efficiencies = rng.uniform(ranges[:, 0], ranges[:, 1], size=(n, 3))
    return efficiencies, np.prod(efficiencies, axis=1)


def loop_gain_statistics(gains) -> dict[str, float]:
    """Dimensionless sample quantiles and gaps to the self-sustaining G=1."""
    maximum = float(np.max(gains))
    p99, p50 = (float(v) for v in np.percentile(gains, [99, 50]))
    theoretical_max = float(np.prod([ENGINE_RANGE[1], ALTERNATOR_RANGE[1],
                                    ELECTROLYSER_RANGE[1]]))
    return {"max": maximum, "p99": p99, "p50": p50,
            "gap_to_one_max": 1.0 - maximum,
            "gap_to_one_p99": 1.0 - p99, "gap_to_one_p50": 1.0 - p50,
            "theoretical_max": theoretical_max,
            "gap_to_one_theoretical_max": 1.0 - theoretical_max}


def hho_kit_ledger(parameters: KitParameters | None = None) -> dict[str, float]:
    """Faraday flow [kg/s], powers [W], and net effect at fixed cruise work.

    Electrical load / alternator efficiency is shaft cost. Hydrogen LHV must
    pass through engine efficiency before it can offset that cost. Additional
    primary fuel power is the remaining shaft deficit / engine efficiency.
    """
    p = parameters or KitParameters()
    if not all(np.isfinite(v) for v in asdict(p).values()):
        raise ValueError("Kit parameters must be finite")
    if p.current_A < 0 or p.voltage_V <= 0 or p.cruise_shaft_power_W <= 0:
        raise ValueError("Current must be nonnegative; voltage and cruise power positive")
    if not 0 <= p.faradaic_efficiency <= 1:
        raise ValueError("Faradaic efficiency must be in [0, 1]")
    if not 0 < p.eta_engine <= 1 or not 0 < p.eta_alternator <= 1:
        raise ValueError("Engine and alternator efficiencies must be in (0, 1]")
    hydrogen_flow = (p.current_A * p.faradaic_efficiency
                     / (ELECTRONS_PER_H2 * FARADAY_C_MOL) * FUELS["H2"].molar_mass)
    electric = p.current_A * p.voltage_V
    hydrogen_power = hydrogen_flow * lhv("H2")
    if hydrogen_power > electric:
        raise ValueError("Kit inputs imply H2 LHV above electrical input; missing energy source")
    shaft_cost = electric / p.eta_alternator
    recovered_shaft = p.eta_engine * hydrogen_power
    net_shaft = recovered_shaft - shaft_cost
    baseline_fuel = p.cruise_shaft_power_W / p.eta_engine
    extra_fuel = -net_shaft / p.eta_engine
    return {
        "hydrogen_mass_flow_kg_s": hydrogen_flow,
        "hydrogen_lhv_J_kg": lhv("H2"),
        "electrical_input_W": electric,
        "hydrogen_lhv_power_W": hydrogen_power,
        "electrolyser_lhv_efficiency": hydrogen_power / electric if electric else 0.0,
        "alternator_shaft_cost_W": shaft_cost,
        "hydrogen_recovered_shaft_W": recovered_shaft,
        "net_shaft_effect_W": net_shaft,
        "cruise_shaft_power_W": p.cruise_shaft_power_W,
        "baseline_fuel_power_W": baseline_fuel,
        "additional_primary_fuel_power_W": extra_fuel,
        "fuel_power_with_kit_W": baseline_fuel + extra_fuel,
        "fuel_power_increase_fraction": extra_fuel / baseline_fuel,
        "hydrogen_fraction_of_baseline_fuel_power": hydrogen_power / baseline_fuel,
    }


def heating_value_record(fuel: str) -> dict:
    """One table row, retaining unavailable ethanol explicitly (no fake zero)."""
    if fuel == "C2H5OH" and not SAN_DIEGO_PATH.is_file():
        return dict(fuel=fuel, state=FUELS[fuel].state, lhv_J_kg=None,
                    mechanism="mechanisms/sandiego.yaml", mechanism_fallback=True,
                    status="unavailable", reason="mechanisms/sandiego.yaml is absent")
    selected = select_mechanism(fuel)
    return dict(fuel=fuel, state=FUELS[fuel].state, lhv_J_kg=lhv(fuel),
                mechanism=selected.name, mechanism_fallback=selected.mechanism_fallback,
                status="computed", reason="")


def heating_value_validation(records: list[dict]) -> dict:
    """Compare computed values to SPEC §10; do not claim skipped values pass."""
    checks = {}
    for row in records:
        fuel, value = row["fuel"], row["lhv_J_kg"]
        if value is None:
            checks[fuel] = {"status": "skipped", "reason": row["reason"]}
        elif fuel == "H2O":
            checks[fuel] = {"status": "passed" if abs(value) < WATER_ABS_TOL_J_KG else "failed",
                            "actual_J_kg": value, "absolute_tolerance_J_kg": WATER_ABS_TOL_J_KG}
        else:
            target = LHV_TARGETS_J_KG[fuel]
            checks[fuel] = {"status": "passed" if abs(value / target - 1) <= LHV_REL_TOL else "failed",
                            "actual_J_kg": value, "target_J_kg": target,
                            "relative_tolerance": LHV_REL_TOL}
    return checks


def write_plots(out, gains, stats, kit):
    """Display dimensionless loop gains and the kit power ledger in watts."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(gains, bins=HISTOGRAM_BINS, color="steelblue")
    ax.axvline(1, color="firebrick", label="Self-sustaining threshold G = 1")
    ax.annotate(f"Gap from sampled maximum: {stats['gap_to_one_max']:.3f}",
                xy=(stats["max"], 0.65), xytext=(0.48, 0.65),
                xycoords=("data", "axes fraction"),
                textcoords=("data", "axes fraction"), arrowprops={"arrowstyle": "->"})
    ax.set(xlim=(0, 1.05), xlabel="Loop gain G [1]", ylabel="Samples [count]",
           title="On-board electrolysis cannot sustain its own input")
    ax.legend()
    save_fig(fig, out / "loop_gain_hist.png")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    names = ["Electrical input", "H2 LHV", "Shaft cost", "Recovered shaft", "Net shaft"]
    values = [kit[k] for k in ("electrical_input_W", "hydrogen_lhv_power_W",
                              "alternator_shaft_cost_W", "hydrogen_recovered_shaft_W",
                              "net_shaft_effect_W")]
    axes[0].barh(names, values, color=["grey", "steelblue", "orange", "seagreen", "firebrick"])
    axes[0].axvline(0, color="black", linewidth=0.7)
    axes[0].set(xlabel="Power [W]", ylabel="Kit ledger category [1]", title="20 A at 13.8 V")
    axes[1].bar(["Cruise fuel", "Added fuel", "H2 LHV"],
                [kit["baseline_fuel_power_W"], kit["additional_primary_fuel_power_W"],
                 kit["hydrogen_lhv_power_W"]])
    axes[1].set(xlabel="Energy stream [1]", ylabel="Power [W]",
                title="Fuel required for 15 kW cruise shaft output")
    fig.tight_layout()
    save_fig(fig, out / "hho_kit_ledger.png")
    plt.close(fig)


def main(argv=None) -> int:
    """Write the complete audit; return nonzero if an in-run validation fails."""
    start = time.perf_counter()
    args = argument_parser(MODULE).parse_args(None if argv is None else list(map(str, argv)))
    count = QUICK_SAMPLES if args.mode == "quick" else FULL_SAMPLES
    records = ordered_map(heating_value_record, FUELS, args.workers)
    efficiencies, gains = loop_gain_samples(count)
    stats = loop_gain_statistics(gains)
    parameters = KitParameters()
    kit = hho_kit_ledger(parameters)
    write_csv(args.out / "heating_values.csv", records)
    write_csv(args.out / "loop_gain_samples.csv", (
        {"eta_engine": float(e[0]), "eta_alternator": float(e[1]),
         "eta_electrolyser_lhv": float(e[2]), "loop_gain": float(g)}
        for e, g in zip(efficiencies, gains)))
    write_csv(args.out / "loop_gain_statistics.csv", [stats])
    write_csv(args.out / "hho_kit_ledger.csv", [kit])
    write_plots(args.out, gains, stats, kit)
    assumptions = fuel_assumptions()
    assumptions.update({
        "mechanism_fallback": any(r["mechanism_fallback"] for r in records),
        "mechanisms": {r["fuel"]: {"name": r["mechanism"], "status": r["status"]} for r in records},
        "monte_carlo": {"samples": count, "full_samples": FULL_SAMPLES,
                        "quick_samples": QUICK_SAMPLES, "seed": RANDOM_SEED,
                        "generator": "PCG64", "distribution": "independent uniform",
                        "eta_engine_range": ENGINE_RANGE, "eta_alternator_range": ALTERNATOR_RANGE,
                        "eta_electrolyser_lhv_range": ELECTROLYSER_RANGE,
                        "source": "SPEC §4; quick sample count per task contract"},
        "kit": {"parameters": asdict(parameters),
                "source": "SPEC §4 for current, voltage, Faradaic efficiency and cruise power",
                "efficiency_rationale": "Engine and alternator use midpoints of SPEC Monte Carlo ranges; fixed efficiency at cruise",
                "cell_basis": "One Faraday-equivalent cell at stated current, per requested flow formula; no unstated series-cell multiplier",
                "energy_boundary": "Only electrical input powers electrolysis; no external heat or additional chemistry",
                "faraday_C_mol": FARADAY_C_MOL, "faraday_source": "NIST CODATA 2022",
                "electrons_per_H2": ELECTRONS_PER_H2,
                "electron_rationale": "Balanced hydrogen reduction half-reaction"},
        "workers": {"value": args.workers, "rationale": "Parallel independent fuel enthalpy calculations; Monte Carlo generated once in fixed order"},
        "histogram_bins": {"value": HISTOGRAM_BINS, "rationale": "Display resolution"},
    })
    checks = heating_value_validation(records)
    passed = (all(c["status"] != "failed" for c in checks.values())
              and stats["max"] < 1 and stats["theoretical_max"] < 1
              and kit["net_shaft_effect_W"] < 0)
    validation = {"passed": passed, "lhv": checks,
                  "loop_gain_below_one": stats["max"] < 1,
                  "analytic_upper_bound_below_one": stats["theoretical_max"] < 1,
                  "kit_is_net_loss": kit["net_shaft_effect_W"] < 0}
    write_summary(args.out, MODULE, VERSION, args.mode, assumptions,
                  {"heating_values": records, "loop_gain": stats, "hho_kit": kit,
                   "energy_source": "Primary fuel drives the alternator; water supplies zero heating value"},
                  validation, time.perf_counter() - start)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
