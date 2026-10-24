"""Evaporation profile for Module 03 coupled evaporation.

Derived from Module 09 (branch wme1-spray09, commit e32288e) outputs
(results/09_spray_evaporation/spray_at_spark.json and
design_points/design_point_sweep.csv), which give the fraction of water
evaporated at IVC and at spark for the six Module 03 design points
(CH3OH/C2H5OH x best_dry/best_overall/water_majority) and two atomiser
variants (carb_venturi, ultrasonic_120kHz) under both the nominal and
cfd_matched sensitivity bound.

The profile is interpolated linearly in crank angle between IVC
(-180 deg aTDC) and spark (spark_deg_aTDC from the sweep).  Beyond spark
the profile is held at its spark value; the Module 03 evaporation
schedule (IVC -> evap_end = -30 CAD, saturation-capped) remains the
governing physics and this profile only supplies the *target* schedule
shape when --evap-profile is passed.

Limitations (documented):
  * This is NOT Grok Bot's evap_profiles.json.  That file was never
    produced.  The values come from a different model (Module 09 spray
    evaporation, itself unvalidated against experiment and known to
    over-evaporate vs the OpenFOAM CFD phase A by 1.5-2.5x at 1 bar).
  * The IVC/spark interpolation is a straight line; the real in-cylinder
    evaporation history is not linear in crank angle.
  * Only the six design points above are covered.  Other CR/w/T_intake
    combinations fall back to the default f_evap_intake schedule.
  * The cfd_matched variant is a sensitivity bound, not a validated model.
"""

import json
import math
from pathlib import Path

# Crank angle [deg aTDC] at IVC (Module 03 parameter ivc_rad = -pi).
IVC_DEG = -180.0

# Atomiser variants consumed by the profile.  Any other name falls back
# to the default schedule and is reported in summary.json.
ATOMISERS = ("carb_venturi", "ultrasonic_120kHz")
VARIANTS = ("nominal", "cfd_matched")


def _build():
    """Return {(fuel, point, atomiser, variant): (spark_deg, frac_ivc, frac_spark)}."""
    import csv
    here = Path(__file__).resolve().parent
    # Prefer the committed copy in results/03_engine_cycle/inputs; fall
    # back to the source on the wme1-spray09 branch at runtime.
    src = here.parent / "results" / "03_engine_cycle" / "inputs" / "spray_at_spark.json"
    if not src.exists():
        import subprocess
        out = subprocess.run(
            ["git", "show", "wme1-spray09:results/09_spray_evaporation/spray_at_spark.json"],
            capture_output=True, cwd=here.parent.parent, text=True)
        if out.returncode != 0:
            raise FileNotFoundError("spray_at_spark.json not found locally or on wme1-spray09")
        data = json.loads(out.stdout)
    else:
        data = json.loads(src.read_text())

    cases = data["cases"]
    table = {}
    for case_key, case in cases.items():
        fuel, point = case_key.split("/")
        for atomiser in ATOMISERS:
            for variant in VARIANTS:
                entry = case["atomisers"][atomiser][variant]
                spark_deg = float(case["spark_deg_aTDC"])
                frac_ivc = float(entry["evaporated_IVC_pct"]) / 100.0
                frac_spark = float(entry["evaporated_spark_pct"]) / 100.0
                table[(fuel, point, atomiser, variant)] = (spark_deg, frac_ivc, frac_spark)
    return table


_TABLE = _build()


def lookup(fuel, point, atomiser, variant):
    """Return (spark_deg_aTDC, frac_ivc, frac_spark) or None if not covered."""
    return _TABLE.get((fuel, point, atomiser, variant))


def profile_at(fuel, point, atomiser, variant, theta_deg):
    """Fraction of water evaporated at crank angle theta_deg [aTDC].

    Linear interpolation between IVC and spark; clamped to [0, 1] and
    held at the spark value above spark.  Returns None when this
    (fuel, point, atomiser, variant) combination is not in the table.
    """
    hit = lookup(fuel, point, atomiser, variant)
    if hit is None:
        return None
    spark_deg, frac_ivc, frac_spark = hit
    if theta_deg <= IVC_DEG:
        return frac_ivc
    if theta_deg >= spark_deg:
        return frac_spark
    span = spark_deg - IVC_DEG
    if span <= 0.0:
        return frac_spark
    return frac_ivc + (frac_spark - frac_ivc) * (theta_deg - IVC_DEG) / span


def source_label():
    return "derived from module 09 e32288e (IVC/spark interpolation)"


# Reverse map from (fuel, CR, w, T_intake) -> point name, built from the
# cases in spray_at_spark.json (each case carries module03_key).
def _build_point_index():
    import json
    here = Path(__file__).resolve().parent
    src = here.parent / "results" / "03_engine_cycle" / "inputs" / "spray_at_spark.json"
    if not src.exists():
        import subprocess
        out = subprocess.run(
            ["git", "show", "wme1-spray09:results/09_spray_evaporation/spray_at_spark.json"],
            capture_output=True, cwd=here.parent.parent, text=True)
        if out.returncode != 0:
            return {}
        data = json.loads(out.stdout)
    else:
        data = json.loads(src.read_text())
    index = {}
    for case_key, case in data["cases"].items():
        fuel, point = case_key.split("/")
        key = case.get("module03_key", "")
        # module03_key looks like "CH3OH/CR=16/w=0/T_intake=320"
        parts = dict(kv.split("=") for kv in key.split("/")[1:])
        cr, w, T = float(parts["CR"]), float(parts["w"]), float(parts["T_intake"])
        index[(fuel, cr, w, T)] = point
    return index


_POINT_INDEX = _build_point_index()


def point_name(fuel, cr, w, T_intake):
    """Map a Module 03 sweep point to its Module 09 case name, or None."""
    return _POINT_INDEX.get((fuel, float(cr), float(w), float(T_intake)))


class Profile:
    """A single atomiser/variant evaporation profile for Module 03."""

    def __init__(self, atomiser, variant):
        if atomiser not in ATOMISERS:
            raise ValueError(f"unknown atomiser {atomiser!r}; known: {ATOMISERS}")
        if variant not in VARIANTS:
            raise ValueError(f"unknown variant {variant!r}; known: {VARIANTS}")
        self.atomiser = atomiser
        self.variant = variant

    def target(self, fuel, cr, w, T_intake, theta_deg):
        """Evaporated fraction of the water charge at theta_deg [aTDC].

        Returns None when this (fuel, point) combination is not covered,
        in which case the caller falls back to the default schedule.
        """
        name = point_name(fuel, cr, w, T_intake)
        if name is None:
            return None
        return profile_at(fuel, name, self.atomiser, self.variant, theta_deg)

    def source_label(self):
        return source_label()

    def __repr__(self):
        return f"Profile({self.atomiser!r}, {self.variant!r})"


def profile_for(atomiser, variant):
    return Profile(atomiser, variant)