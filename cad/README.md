# Module 07 carburetor CAD

Current verification status: generator implementation only. A working CadQuery
runtime was unavailable in the implementation session,
so the six CAD exports have not been generated and the geometric acceptance
checks have not run. Input-validation tests passed (14); CAD tests skipped (5).

The generator reads Module 06's `carb_design.json` and exports both options as
STEP solids, STL meshes, and SVG projections. All CAD dimensions are in mm.
Option A meters premixed wet methanol; Option B has separate fuel and water
bowls and a vacuum-operated water enrichment valve, shown open.

## Generate and validate

```powershell
python -m pip install -r requirements-cad.txt
python -m sims.07_cad.run --full --design results/06_carburetor/carb_design.json
python -m pytest tests/test_cad.py -q
```

`--cad-out` changes the CAD destination (default: repository `cad/`). `--out`
changes the summary destination (default: `results/07_cad`). Both `--quick` and
`--full` generate the same complete models. `--workers` is accepted for the
common module CLI; CAD construction runs sequentially.

Successful execution writes:

- `cad/carb_optionA.step`, `cad/carb_optionA.stl`, `cad/carb_optionA.svg`
- `cad/carb_optionB.step`, `cad/carb_optionB.stl`, `cad/carb_optionB.svg`
- `results/07_cad/summary.json`: source SHA-256, dimensions, packaging
  assumptions, CadQuery version, measured throat diameters and export checks.

The generator requires a real sizing input and never substitutes test values.
Each STEP is re-imported with CadQuery and checked for valid solids, unchanged
solid count and volume (relative tolerance 1e-6). Its throat is measured from
the actual analytic cylindrical face, with a 0.1 mm diameter tolerance. Tests
also check that STL facets and SVG paths are present. Geometry tests skip if
CadQuery is absent; a skipped test is not evidence of a validated model.

## Sizing input contract

Diameter and jet-length keys accept either `_m` (SI) or `_mm` (CAD). Float
levels use signed metres as specified below. Bare numbers without a unit
suffix are rejected. If both units are supplied they must agree.
The Module 06 schema version 1 is read directly:

```text
schema_version: 1
 design_point.fuel: CH3OH
 options.A / options.B
   venturi_throat_diameter_m
   venturi_inlet_diameter_m
   throttle_bore_diameter_m
   circuits[]
     liquid: wet_methanol_w0.6 / methanol / water
     main_jet_diameter_m
     idle_jet_diameter_m
     needle_seat_diameter_m
     float_level_m
     jet_length_m
     vacuum_power_valve
 assumptions.parameters
   power_valve_starts_vacuum_Pa
   power_valve_full_vacuum_Pa
```

`float_level_m` is signed relative to the throat: -0.006 means a level 6 mm
below the throat. The water idle jet is zero in Module 06 and no water idle
passage is constructed. Its vacuum valve gates the entire water main circuit
in series; there is no additional bypass jet. Both options must share air
passage dimensions. These constraints are checked rather than silently
substituting dimensions.

A failed `validation.passed` flag or optional top-level `validation_passed: false`, `use_for_design: false`, or
`synthetic_fits: true` rejects the input. Tests use explicitly synthetic fixture
dimensions in temporary directories only.

## Model scope and packaging assumptions

Air enters along -Z from the top. The mounting flange is at Z=0; the throttle
is downstream of the throat. A revolved air-passage cutter creates the inlet,
converging cone, 6 mm cylindrical throat land, diffuser, and throttle bore.
The butterfly is shown at 65 degrees from closed, with a separate shaft.
The main liquid passages terminate inside the throat and contain sized-length
metering lands drilled to the input jet diameters. Separate idle galleries
end below the butterfly. Hollow bowls have separate annular floats and lids
with sized needle-seat inlet bores.

The Option B water circuit adds an upstream series valve chamber, lifted
poppet, diaphragm chamber and a separate vacuum tube connected below the
throttle. The intended operation is spring-open at low manifold vacuum/high
load and vacuum-closed at high vacuum. The spring, diaphragm actuation and
opening pressure are not simulated or calibrated. The source opening thresholds
(30 kPa vacuum starts opening; 10 kPa fully open) are retained in the summary;
the poppet representation does not establish a leak-tight seat or dynamic actuation.

Packaging dimensions are assumptions, recorded by `layout()` in the summary:
5 mm radial body allowance, 3 mm bowl walls, 7 mm mounting flange with four
6.5 mm mounting holes, and body height of at least 80 mm. Float buoyancy,
linkages, sealing, fasteners, threads, production clearances, material selection
and manufacturing tolerances require subsequent mechanical design. The STL
is a multi-solid concept assembly, not a single fused printable part. SVGs
are hidden-line isometric projections, not dimensioned manufacturing drawings.

The export/import implementation follows the official
[CadQuery import/export documentation](https://cadquery.readthedocs.io/en/latest/importexport.html).
