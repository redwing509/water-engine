"""Module 07: dimensioned concept CAD, in millimetres, from carb_design.json.

The sizing input is required; there is no synthetic/default design fallback.
See cad/README.md for the input contract and mechanical simplifications.
"""

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
import time

from sims.common.io import REPO_ROOT, argument_parser, write_summary

VERSION = "1.0.0"
DEFAULT_DESIGN = REPO_ROOT / "results/06_carburetor/carb_design.json"


@dataclass(frozen=True)
class Circuit:
    main_jet_mm: float
    idle_jet_mm: float
    needle_seat_mm: float
    float_head_mm: float
    jet_length_mm: float


@dataclass(frozen=True)
class Design:
    throat_mm: float
    inlet_mm: float
    throttle_mm: float
    wet_methanol: Circuit
    fuel: Circuit
    water: Circuit
    valve_starts_vacuum_Pa: float
    valve_full_vacuum_Pa: float


def dimension(data, key, *, allow_zero=False):
    """Read a dimension with explicit m or mm suffix; never guess units."""
    values = []
    for suffix, scale in (("_m", 1000.0), ("_mm", 1.0)):
        if key + suffix in data:
            raw = data[key + suffix]
            if isinstance(raw, bool) or not isinstance(raw, (int, float)):
                raise ValueError(f"{key + suffix} must be a finite number")
            value = raw * scale
            if not math.isfinite(value) or (value < 0 if allow_zero else value <= 0):
                raise ValueError(f"{key + suffix} must be {'nonnegative' if allow_zero else 'positive'}")
            values.append(value)
    if not values:
        raise ValueError(f"Missing dimension: {key}_m (or {key}_mm)")
    if len(values) == 2 and not math.isclose(*values, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError(f"Conflicting metre/millimetre values for {key}")
    return values[0]


def circuit(data):
    level = data["float_level_m"]
    if isinstance(level, bool) or not isinstance(level, (int, float)) or not math.isfinite(level) or level > 0:
        raise ValueError("float_level_m must be finite and <= 0 (relative to throat)")
    return Circuit(dimension(data, "main_jet_diameter"),
                   dimension(data, "idle_jet_diameter", allow_zero=True),
                   dimension(data, "needle_seat_diameter"), -1000 * level,
                   dimension(data, "jet_length"))


def load_design(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Required sizing input missing: {path}. Run Module 06 first or pass --design PATH.")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    try:
        if data.get("validation_passed") is False or data.get("use_for_design") is False or data.get("validation", {}).get("passed") is False:
            raise ValueError("Sizing input is marked unsuitable for design")
        if data.get("synthetic_fits") is True:
            raise ValueError("Synthetic sizing input cannot generate production CAD outputs")
        if data["schema_version"] != 1:
            raise ValueError("Unsupported carb_design.json schema_version")
        if data["design_point"]["fuel"] != "CH3OH":
            raise ValueError("Option A must explicitly identify fuel as CH3OH (wet methanol)")
        a, b = data["options"]["A"], data["options"]["B"]
        dimensions = ("venturi_throat_diameter", "venturi_inlet_diameter", "throttle_bore_diameter")
        for key in dimensions:
            if not math.isclose(dimension(a, key), dimension(b, key), abs_tol=1e-8):
                raise ValueError("Options A and B must share venturi and throttle dimensions")
        if len(a["circuits"]) != 1 or len(b["circuits"]) != 2:
            raise ValueError("Expected one Option A circuit and two Option B circuits")
        wet = a["circuits"][0]
        if not wet["liquid"].startswith("wet_methanol_"):
            raise ValueError("Option A liquid must be wet methanol")
        liquids = {c["liquid"]: c for c in b["circuits"]}
        fuel, water = liquids["methanol"], liquids["water"]
        if water["vacuum_power_valve"] is not True:
            raise ValueError("Option B requires the water vacuum power valve")
        parameters = data["assumptions"]["parameters"]
        design = Design(*(dimension(a, key) for key in dimensions),
                        circuit(wet), circuit(fuel), circuit(water),
                        parameters["power_valve_starts_vacuum_Pa"],
                        parameters["power_valve_full_vacuum_Pa"])
    except (KeyError, TypeError) as exc:
        raise ValueError(f"Invalid carb_design.json schema: {exc}; see cad/README.md") from exc
    validate_design(design)
    return design


def validate_design(d):
    # Bounds reflect the geometric construction, not carburetor sizing physics.
    if not 8 <= d.throat_mm < min(d.inlet_mm, d.throttle_mm) <= 100:
        raise ValueError("CAD requires 8 <= throat < inlet and throttle diameters <= 100 mm")
    if max(d.inlet_mm, d.throttle_mm) > 100:
        raise ValueError("CAD inlet and throttle diameters must be <= 100 mm")
    for c in (d.wet_methanol, d.fuel, d.water):
        if not 0 <= c.idle_jet_mm <= c.main_jet_mm < d.throat_mm / 3:
            raise ValueError("CAD requires 0 <= idle jet <= main jet < throat/3")
        if not 0 < c.needle_seat_mm < 10:
            raise ValueError("Needle seat must fit the 10 mm inlet boss")
        if not 0 <= c.float_head_mm < d.throat_mm:
            raise ValueError("Float level must lie less than one throat diameter below throat")
        if not 0 < c.jet_length_mm < 6:
            raise ValueError("Jet metering length must be positive and below 6 mm")
    if not 0 <= d.valve_full_vacuum_Pa < d.valve_starts_vacuum_Pa:
        raise ValueError("Valve thresholds must satisfy 0 <= full-open < starts-opening vacuum")


def layout(d):
    """Explicit packaging assumptions, scaled from the sized air passage."""
    radius = max(d.inlet_mm, d.throttle_mm) / 2 + 5
    height = max(80.0, 3 * d.throat_mm)
    return dict(body_radius_mm=radius, height_mm=height,
                throat_z_mm=0.62 * height, throat_land_mm=6.0,
                throttle_z_mm=0.20 * height, wall_mm=3.0,
                bowl_radius_mm=max(18.0, 0.65 * d.throat_mm),
                butterfly_angle_deg=65.0)


def build_model(d, option):
    """Return individually named solids; both liquid circuits reach the throat.

    +Z is upstream; throttle and flange are below the venturi. Option B uses
    opposite bowls. The power valve is shown open, in series with the water
    jet, with a vacuum line from below the throttle to its diaphragm.
    """
    import cadquery as cq

    if option not in ("A", "B"):
        raise ValueError("option must be A or B")
    validate_design(d)
    g = layout(d)
    r, h, zt, zb = (g[k] for k in ("body_radius_mm", "height_mm", "throat_z_mm", "throttle_z_mm"))
    rt, ri, ro = d.throat_mm / 2, d.inlet_mm / 2, d.throttle_mm / 2
    br = g["bowl_radius_mm"]

    def cyl(radius, length, start, direction=(0, 0, 1)):
        return cq.Solid.makeCylinder(radius, length, cq.Vector(*start), cq.Vector(*direction))

    def box(x, y, z, center):
        return cq.Workplane("XY").box(x, y, z).val().translate(center)

    # Revolved cutter provides an exact cylindrical throat land, two cones,
    # and a straight downstream throttle bore. It extends past both end faces.
    profile = [(0, -1), (ro, -1), (ro, zb + 8), (rt, zt - 3),
               (rt, zt + 3), (ri, h - 8), (ri, h + 1), (0, h + 1)]
    air = cq.Workplane("XZ").polyline(profile).close().revolve(360, (0, 0), (0, 1)).val()
    body = cyl(r, h, (0, 0, 0)).fuse(box(2*r+26, 2*r+16, 7, (0, 0, 3.5))).cut(air)
    cutters = []
    for x in (-r-7, r+7):
        for y in (-r, r):
            cutters.append(cyl(3.25, 9, (x, y, -1)))
    # Shaft bearing bores run along Y; the disc is a separate replaceable part.
    cutters.append(cyl(2.1, 2*r+2, (0, -r-1, zb), (0, 1, 0)))
    shaft = cyl(2, 2*r+12, (0, -r-6, zb), (0, 1, 0))
    butterfly = cyl(ro-0.35, 1.0, (0, 0, zb-0.5)).rotate((0, 0, zb), (0, 1, zb), 65)
    butterfly = butterfly.cut(cyl(2.05, 2*r+2, (0, -r-1, zb), (0, 1, 0)))
    parts = {"throttle_shaft": shaft, "throttle_butterfly": butterfly}
    circuits = [("wet_methanol", 1, d.wet_methanol)] if option == "A" else [
        ("fuel", 1, d.fuel), ("water", -1, d.water)]

    for name, side, c in circuits:
        bx = side * (r + br + 12)
        level = zt - c.float_head_mm
        floor = min(level - 24, zt - 30)
        top = zt + 10
        # The pickup well is near the body, away from the annular float.
        pickup = bx - side * (br - 6)
        tip = side * rt * 0.45
        jet_x = side * (r + 4)
        passage_r = max(2.0, c.main_jet_mm * 0.8)
        arm_r = passage_r + 2
        xlow, xhigh = sorted((tip, pickup))
        arm = cyl(arm_r, xhigh-xlow, (xlow, 0, zt), (1, 0, 0))
        bowl = cyl(br, top-floor, (bx, 0, floor)).cut(cyl(br-3, top-floor, (bx, 0, floor+3)))
        riser = cyl(arm_r, zt-floor-4, (pickup, 0, floor+4))
        body = body.fuse(arm, bowl, riser)
        half_land = c.jet_length_mm / 2
        # Feed drillings stop either side of the sized metering land. Only the
        # specified main-jet diameter cuts the land itself.
        cutters.append(cyl(c.main_jet_mm/2, xhigh-xlow+2, (xlow-1, 0, zt), (1, 0, 0)))
        cutters.append(cyl(passage_r, jet_x-half_land-xlow, (xlow, 0, zt), (1, 0, 0)))
        cutters.append(cyl(passage_r, xhigh-jet_x-half_land, (jet_x+half_land, 0, zt), (1, 0, 0)))
        cutters.append(cyl(passage_r, zt-floor-3, (pickup, 0, floor+3)))
        if c.idle_jet_mm > 0:
            # Idle drilling and gallery: bowl pickup to a port below the butterfly.
            idle_z = zb - 5
            ix = side * (r-2)
            low, high = sorted((ix, pickup))
            gallery = cyl(2.5, high-low, (low, 0, idle_z), (1, 0, 0))
            gallery = gallery.fuse(cyl(2.5, zt-idle_z, (pickup, 0, idle_z)))
            body = body.fuse(gallery)
            cutters.append(cyl(1, high-low, (low, 0, idle_z), (1, 0, 0)))
            cutters.append(cyl(1, zt-idle_z, (pickup, 0, idle_z)))
            cutters.append(cyl(c.idle_jet_mm/2, r-ro+4, (side*(ro-1), 0, idle_z), (side, 0, 0)))
        # Float and removable lid with a dimensioned inlet/needle-seat bore.
        float_shape = cyl(br-5, 8, (bx, 0, level-6)).cut(cyl(br-10, 10, (bx, 0, level-7)))
        # Keep a channel around the pickup riser, avoiding component overlap.
        float_shape = float_shape.cut(cyl(arm_r+0.5, 12, (pickup, 0, level-8)))
        parts[name+"_float"] = float_shape
        lid = cyl(br, 3, (bx, 0, top+0.2)).fuse(cyl(5, 8, (bx, 0, top+3.2)))
        lid = lid.cut(cyl(c.needle_seat_mm/2, 13, (bx, 0, top-0.5)))
        parts[name+"_bowl_lid"] = lid

        if name == "water":
            # Series water valve upstream of the metering land: the source
            # gates the entire water circuit, rather than adding a bypass jet.
            vx, vy, vz = jet_x-6, 0.0, zt+18
            body = body.fuse(cyl(6, 18, (vx, vy, zt)))
            cutters.append(cyl(2.5, 19, (vx, vy, zt-1)))
            # Chamber and cover with diaphragm separating vacuum from water.
            chamber = cyl(13, 10, (vx, vy, vz)).cut(cyl(10, 9, (vx, vy, vz+2)))
            chamber = chamber.cut(cyl(2.5, 4, (vx, vy, vz-1)))
            parts["water_power_valve_housing"] = chamber
            parts["water_power_valve_diaphragm"] = cyl(9.9, 0.5, (vx, vy, vz+3))
            parts["water_power_valve_poppet_open"] = cyl(1, 20, (vx, vy, zt+1)).fuse(cyl(2.3, 1, (vx, vy, zt+1)))
            cover = cyl(13, 2, (vx, vy, vz+10))
            parts["water_power_valve_cover"] = cover
            # Vacuum gallery uses a rear route so it cannot intersect either
            # main jet. Four drilled segments meet at their endpoints.
            rear = r + 18
            vac_z = 9.0
            nodes = [(0, 0, vac_z), (0, rear, vac_z),
                     (vx, rear, vac_z), (vx, rear, vz+7), (vx, vy, vz+7)]
            outer, inner = [], []
            for start, end in zip(nodes, nodes[1:]):
                direction = cq.Vector(*end).sub(cq.Vector(*start))
                length = direction.Length
                direction = direction.normalized().toTuple()
                outer.append(cyl(2.5, length, start, direction))
                inner.append(cyl(1.2, length+0.02, start, direction))
            tube = outer[0].fuse(*outer[1:])
            # Trim only the tube material inside the air bore, then open the
            # corresponding body wall with the vacuum lumen.
            tube = tube.cut(air).cut(*inner)
            cutters.extend(inner)
            parts["vacuum_signal_tube"] = tube
            parts["water_power_valve_housing"] = chamber.cut(*inner)

    parts["body_bowls_and_passages"] = body.cut(*cutters).clean()
    for name, shape in parts.items():
        if not shape.isValid() or shape.Volume() <= 0:
            raise ValueError(f"Invalid or empty CAD component: {name}")
    return parts


def measure_throat(shape, throat_z):
    """Measure the actual cylindrical throat face, including STEP re-imports.

    Inspect analytic surfaces, not input metadata or a pre-cut tool. Nozzle
    holes split the face but leave its radius and axial bounds unchanged.
    """
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.GeomAbs import GeomAbs_Cylinder
    candidates = []
    for face in shape.Faces():
        surf = BRepAdaptor_Surface(face.wrapped)
        if surf.GetType() != GeomAbs_Cylinder:
            continue
        cylinder = surf.Cylinder()
        axis, position = cylinder.Axis().Direction(), cylinder.Location()
        bounds = face.BoundingBox()
        if (abs(axis.Z()) > 0.999999 and abs(position.X()) < 1e-5
                and abs(position.Y()) < 1e-5
                and abs(bounds.zmin-(throat_z-3)) < 1e-4
                and abs(bounds.zmax-(throat_z+3)) < 1e-4):
            candidates.append(2*cylinder.Radius())
    if not candidates:
        raise ValueError("No analytic throat surface found in CAD geometry")
    if max(candidates)-min(candidates) > 1e-5:
        raise ValueError("Ambiguous throat geometry")
    return candidates[0]


def export_option(design, option, destination):
    import cadquery as cq

    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    parts = build_model(design, option)
    shape = cq.Compound.makeCompound(list(parts.values()))
    # CadQuery's STL exporter with a tolerance mutates the source shape's face
    # bounding boxes in place, so the analytic throat must be measured before
    # any export, not between the STEP and STL writes.
    before = measure_throat(shape, layout(design)["throat_z_mm"])
    base = destination / f"carb_option{option}"
    cq.exporters.export(shape, str(base.with_suffix(".step")))
    cq.exporters.export(shape, str(base.with_suffix(".stl")), tolerance=0.02, angularTolerance=0.1)
    cq.exporters.export(shape, str(base.with_suffix(".svg")), opt={
        "width": 1100, "height": 850, "projectionDir": (1, -1.5, 1),
        "showAxes": False, "showHidden": True,
        "strokeWidth": 0.5, "strokeColor": (35, 48, 58),
        "hiddenColor": (170, 180, 188), "marginLeft": 40, "marginTop": 40})
    reloaded = cq.importers.importStep(str(base.with_suffix(".step"))).val()
    after = measure_throat(reloaded, layout(design)["throat_z_mm"])
    valid = reloaded.isValid() and all(s.isValid() for s in reloaded.Solids())
    volume_error = abs(reloaded.Volume()-shape.Volume()) / shape.Volume()
    solid_count_matches = len(shape.Solids()) == len(reloaded.Solids())
    passed = (valid and solid_count_matches and volume_error < 1e-6
              and abs(before-design.throat_mm) <= 0.1
              and abs(after-design.throat_mm) <= 0.1)
    result = dict(passed=passed, design_throat_mm=design.throat_mm,
                  measured_throat_mm=before, step_throat_mm=after,
                  throat_error_mm=abs(after-design.throat_mm), tolerance_mm=0.1,
                  step_reimport_valid=valid, step_volume_relative_error=volume_error,
                  solid_count=len(shape.Solids()), step_solid_count=len(reloaded.Solids()),
                  components=list(parts),
                  files={ext: str(base.with_suffix('.'+ext)) for ext in ("step", "stl", "svg")})
    if not passed:
        raise ValueError(f"Option {option} CAD verification failed: {result}")
    return result


def main(argv=None):
    parser = argument_parser("07_cad")
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--cad-out", type=Path, default=REPO_ROOT / "cad")
    args = parser.parse_args(argv)
    start = time.perf_counter()
    design = load_design(args.design)
    try:
        import cadquery as cq
    except ImportError as exc:
        raise SystemExit("CadQuery is required: python -m pip install -r requirements-cad.txt") from exc
    results = {option: export_option(design, option, args.cad_out) for option in ("A", "B")}
    write_summary(args.out, "07_cad", VERSION, args.mode,
                  dict(input_path=str(args.design), input_sha256=hashlib.sha256(args.design.read_bytes()).hexdigest(),
                       cadquery_version=cq.__version__, dimensions_mm=asdict(design), packaging=layout(design),
                       model_scope="Concept geometry; no calibrated spring, seals, threads, float linkage or manufacturing tolerances",
                       water_power_valve_state="Open; high manifold vacuum closes the conceptual poppet; calibration not simulated",
                       execution="Sequential CAD; quick and full produce identical geometry"),
                  results, dict(passed=True, throat_tolerance_mm=0.1, step_reimports=True),
                  time.perf_counter()-start)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
