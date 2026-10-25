"""Evaporation profile for Module 03 coupled evaporation.

Derived from Module 09 (branch wme1-spray09, commit e32288e) outputs
(results/09_spray_evaporation/spray_at_spark.json), which give three
fractions of the water charge at spark for the six Module 03 design
points (CH3OH/C2H5OH x best_dry/best_overall/water_majority) and two
atomiser variants (carb_venturi, ultrasonic_120kHz) under both the
nominal and cfd_matched sensitivity bound:

  * evaporated at spark      -- fraction that has vaporised by spark
  * airborne liquid at spark -- fraction still as airborne droplets
  * wall film at spark       -- fraction impinged and held as wall film

The three fractions sum to 1.0 (100 %).

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
  * liquid_spark_pct is the *airborne droplet* subset (0-4 %); the bulk of
    the non-evaporated water is wall-impinged film (77-97 % on
    water-majority points).  These two together = 1 - evaporated.
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


def _load_spray_data():
    """Load the raw spray_at_spark.json (cached)."""
    here = Path(__file__).resolve().parent
    src = here.parent.parent / "results" / "03_engine_cycle" / "inputs" / "spray_at_spark.json"
    if not src.exists():
        import subprocess
        out = subprocess.run(
            ["git", "show", "wme1-spray09:results/09_spray_evaporation/spray_at_spark.json"],
            capture_output=True, cwd=here.parent.parent, text=True)
        if out.returncode != 0:
            raise FileNotFoundError("spray_at_spark.json not found locally or on wme1-spray09")
        return json.loads(out.stdout)
    return json.loads(src.read_text())


def _build():
    """Return {(fuel, point, atomiser, variant): row}.

    Each row is a 5-tuple:
      (spark_deg_aTDC, frac_evap_ivc, frac_evap_spark,
       frac_airborne_spark, frac_wall_film)

    where frac_evap_*, frac_airborne_spark and frac_wall_film are fractions
    (0..1) of the water charge at IVC / spark, taken from Module 09's
    spray_at_spark.json.  They sum to 1.0 at spark:
      frac_evap_spark + frac_airborne_spark + frac_wall_film == 1.
    """
    data = _load_spray_data()
    cases = data["cases"]
    table = {}
    for case_key, case in cases.items():
        fuel, point = case_key.split("/")
        for atomiser in ATOMISERS:
            for variant in VARIANTS:
                entry = case["atomisers"][atomiser][variant]
                spark_deg = float(case["spark_deg_aTDC"])
                frac_evap_ivc = float(entry["evaporated_IVC_pct"]) / 100.0
                frac_evap_spark = float(entry["evaporated_spark_pct"]) / 100.0
                frac_airborne = float(entry["liquid_spark_pct"]) / 100.0
                frac_wall = float(entry["wall_impinged_pct"]) / 100.0
                table[(fuel, point, atomiser, variant)] = (
                    spark_deg, frac_evap_ivc, frac_evap_spark,
                    frac_airborne, frac_wall)
    return table


_TABLE = _build()


def lookup(fuel, point, atomiser, variant):
    """Return the 5-tuple row or None if not covered."""
    return _TABLE.get((fuel, point, atomiser, variant))


def profile_at(fuel, point, atomiser, variant, theta_deg):
    """Evaporated fraction of the water charge at crank angle theta_deg [aTDC].

    Linear interpolation between IVC and spark; clamped to [0, 1] and
    held at the spark value above spark.  Returns None when this
    (fuel, point) combination is not in the table.
    """
    hit = lookup(fuel, point, atomiser, variant)
    if hit is None:
        return None
    spark_deg, frac_ivc, frac_spark = hit[0], hit[1], hit[2]
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
    data = _load_spray_data()
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


# --- three-fraction accessors (all fractions 0..1, sum to 1 at spark) ----

def fractions_at_spark(fuel, point, atomiser, variant):
    """Return (frac_evap, frac_airborne, frac_wall_film) at spark, or None.

    All three are fractions of the water charge (0..1) and sum to 1.0.
    """
    hit = lookup(fuel, point, atomiser, variant)
    if hit is None:
        return None
    return (hit[2], hit[3], hit[4])


def frac_spark(fuel, point, atomiser, variant):
    """Fraction of water evaporated by spark (0..1) from the spray table."""
    hit = lookup(fuel, point, atomiser, variant)
    return None if hit is None else hit[2]


def airborne_liquid_at_spark(fuel, point, atomiser, variant):
    """Fraction of the water charge that is *airborne liquid* at spark (0..1).

    This is Module 09's ``liquid_spark_pct`` column.  On the water-majority
    points it reads 0-3.2 % -- the remainder of the non-evaporated water is
    wall-impinged film (see :func:`wall_film_at_spark`), which is NOT airborne.
    """
    hit = lookup(fuel, point, atomiser, variant)
    return None if hit is None else hit[3]


def wall_film_at_spark(fuel, point, atomiser, variant):
    """Fraction of the water charge that is wall-impinged film at spark (0..1).

    On the water-majority points this is 77-97 % of the water charge and is
    the dominant non-evaporated fraction.
    """
    hit = lookup(fuel, point, atomiser, variant)
    return None if hit is None else hit[4]


def liquid_at_spark(fuel, point, atomiser, variant):
    """Fraction of the water charge still non-vapour at spark (0..1).

    This is the *combined* airborne-droplet + wall-film fraction, i.e.
    1 - frac_spark, matching Module 09's total non-evaporated fraction.
    """
    fs = frac_spark(fuel, point, atomiser, variant)
    return None if fs is None else max(0.0, 1.0 - fs)


def spark_target(fuel, cr, w, T_intake, atomiser, variant):
    """Return (spark_deg_aTDC, fractions_at_spark) or None.

    ``fractions_at_spark`` is the 3-tuple
    (frac_evap, frac_airborne, frac_wall_film) from Module 09.
    Used by the Module 03 cycle to cap evaporation at the spark value and
    to debit the retained liquid as a heat sink through combustion.
    """
    name = point_name(fuel, cr, w, T_intake)
    if name is None:
        return None
    hit = lookup(fuel, name, atomiser, variant)
    if hit is None:
        return None
    return hit[0], (hit[2], hit[3], hit[4])


def _m09_field(fuel, point, atomiser, variant, field):
    """Read a raw percentage field from Module 09's spray_at_spark.json."""
    data = _load_spray_data()
    case = data["cases"][f"{fuel}/{point}"]
    sub = case["atomisers"][atomiser][variant]
    return float(sub[field]) / 100.0


def verify_three_fractions(tolerance_pp=1.0):
    """Cross-check this module's three spark fractions against Module 09.

    Returns a list of rows (case, atomiser, variant, frac_evap_derived,
    frac_evap_m09, delta_pp, frac_air_derived, frac_air_m09, delta_pp,
    frac_wall_derived, frac_wall_m09, delta_pp) for every atomiser/variant
    in the spray table.  Each ``delta_pp`` is in percentage points
    (derived*100 - m09*100).
    """
    data = _load_spray_data()
    rows = []
    for case_key, case in data["cases"].items():
        fuel, point = case_key.split("/")
        for atomiser, sub in case["atomisers"].items():
            for variant in sub:
                derived = fractions_at_spark(fuel, point, atomiser, variant)
                if derived is None:
                    continue
                m09_evap = _m09_field(fuel, point, atomiser, variant, "evaporated_spark_pct")
                m09_air = _m09_field(fuel, point, atomiser, variant, "liquid_spark_pct")
                m09_wall = _m09_field(fuel, point, atomiser, variant, "wall_impinged_pct")
                rows.append((
                    case_key, atomiser, variant,
                    derived[0], m09_evap, (derived[0] - m09_evap) * 100.0,
                    derived[1], m09_air, (derived[1] - m09_air) * 100.0,
                    derived[2], m09_wall, (derived[2] - m09_wall) * 100.0,
                ))
    return rows


# --- coupling item B (2026-10-24): fixed-point and synthetic profiles -----

class PointProfile(Profile):
    """Profile pinned to one Module 09 design point, independent of T_intake.

    Used for the dual-temperature HOT regime (T_intake 400 K), where the
    Module 09 table (keyed at 320/360 K) has no entry: the design point's
    fractions are applied unchanged. Caveat recorded by the caller: Module 09
    was not rerun at 400 K (a hotter intake would evaporate more, so this is
    conservative for the wet points).
    """

    def __init__(self, atomiser, variant, point):
        super().__init__(atomiser, variant)
        self.point = point

    def target(self, fuel, cr, w, T_intake, theta_deg):
        return profile_at(fuel, self.point, self.atomiser, self.variant, theta_deg)

    def spark_target(self, fuel, cr, w, T_intake):
        hit = lookup(fuel, self.point, self.atomiser, self.variant)
        if hit is None:
            return None
        return hit[0], (hit[2], hit[3], hit[4])

    def ivc_fraction(self, fuel):
        hit = lookup(fuel, self.point, self.atomiser, self.variant)
        return None if hit is None else hit[1]

    def __repr__(self):
        return f"PointProfile({self.atomiser!r}, {self.variant!r}, {self.point!r})"


class SyntheticProfile:
    """Flat test profile: fraction f_evap evaporated from IVC, spark at spark_deg.

    Not Module 09 data; used by the unit tests to vary the liquid at spark.
    """

    atomiser = "synthetic"
    variant = "synthetic"

    def __init__(self, f_evap, spark_deg=-30.0):
        self.f_evap, self.spark_deg = float(f_evap), float(spark_deg)

    def target(self, fuel, cr, w, T_intake, theta_deg):
        return self.f_evap

    def spark_target(self, fuel, cr, w, T_intake):
        return self.spark_deg, (self.f_evap, 1.0 - self.f_evap, 0.0)
