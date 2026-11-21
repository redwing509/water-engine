"""Module 03 design-point rows (problem definition + Module 03 outputs) for the two-engine comparison."""
import csv
import json
from pathlib import Path

from .engine import Case

HERE = Path(__file__).resolve().parent
ROWS = HERE / "m03_rows.json"   # frozen copy, provenance inside
REGIME_WALL_K = {"normal": 450.0, "hot": 520.0}
# Regimes: water-engine wme1-hiT sims/dual_temp/regimes.py (MAHLE/VW SSP 222 coolant ranges, SAE 960271,
# Heywood 1988 ch. 12 gas-side wall 400-600 K, WME-1 SPEC section 6 wall 450 K).
REGIMES = {
    "normal": dict(coolant_K=363.15, chamber_wall_K=450.0, port_wall_K=363.15, T_intake_K=[320.0, 360.0]),
    "hot": dict(coolant_K=388.15, chamber_wall_K=520.0, port_wall_K=388.15, T_intake_K=[320.0, 360.0, 400.0]),
}
OUT_COLS = ["gross_indicated_efficiency", "IMEP_Pa", "peak_pressure_Pa", "peak_pressure_angle_deg",
            "peak_temperature_K", "peak_burned_temperature_K", "EVO_T_K", "wall_heat_J", "NO_mol_per_J_fuel",
            "knock_integral_at_xb90", "knock_limited", "fuel_energy_J", "energy_closure_error_fraction",
            "S_L_m_s", "evaporation_cylinder_J"]
IN_COLS = ["fuel", "CR", "w", "T_intake_K", "T_IVC_K", "f_evap_intake_effective", "fuel_mass_kg", "air_mass_kg",
           "residual_mass_kg", "water_mass_kg", "ca50_used_deg", "burn_10_90_deg"]


def key(fuel, cr, w, T):
    return f"{fuel}/CR={int(round(float(cr)))}/w={float(w):.1f}/T_intake={float(T):.0f}"


def freeze(normal_csv, hot_csv, normal_design, hot_design, provenance, out=ROWS):
    """Copy the needed Module 03 rows (both regimes) into m03_rows.json."""
    def load(path):
        rows = {}
        with open(path) as fh:
            for r in csv.DictReader(fh):
                if r.get("status", "ok") not in ("ok", "", None) and not r.get("gross_indicated_efficiency"):
                    continue
                rows[key(r["fuel"], r["CR"], r["w"], r["T_intake_K"])] = r
        return rows
    tables = {"normal": load(normal_csv), "hot": load(hot_csv)}
    designs = {}
    for regime, path in (("normal", normal_design), ("hot", hot_design)):
        d = json.loads(Path(path).read_text())
        for fuel, sel in d["per_fuel"].items():
            if fuel not in ("CH3OH", "C2H5OH"):
                continue
            for name, v in sel.items():
                if isinstance(v, dict) and "CR" in v:
                    designs[f"{regime}:{fuel}:{name}"] = key(fuel, v["CR"], v["w"], v["T_intake_K"])
    keys = sorted(set(designs.values()))
    rows = {}
    for k in keys:
        for regime in ("normal", "hot"):
            r = tables[regime].get(k)
            if r is None or not r.get("gross_indicated_efficiency"):
                continue
            rows[f"{regime}|{k}"] = {c: r.get(c) for c in IN_COLS + OUT_COLS + ["status", "reason"]}
    out.write_text(json.dumps(dict(provenance=provenance, designs=designs, rows=rows), indent=1))
    return out


def load_rows(path=ROWS):
    return json.loads(Path(path).read_text())


def case_from_row(row, regime, **kw):
    f = lambda k: float(row[k])
    return Case(fuel=row["fuel"], cr=f("CR"), T_ivc=f("T_IVC_K"), m_fuel=f("fuel_mass_kg"), m_air=f("air_mass_kg"),
                m_residual=f("residual_mass_kg"), m_water=f("water_mass_kg"),
                e_intake=f("f_evap_intake_effective"), ca50_deg=f("ca50_used_deg"), d1090_deg=f("burn_10_90_deg"),
                wall_T=REGIME_WALL_K[regime], **kw)
