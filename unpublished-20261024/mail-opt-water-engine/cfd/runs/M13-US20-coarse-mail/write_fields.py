#!/usr/bin/env python3
"""Write 0/ and 0/wallFilmRegion/ initial/boundary fields for a module 13 case
(after blockMesh/snappyHexMesh/topoSet/extrudeToRegionMesh)."""
import json
from pathlib import Path

case = Path(__file__).resolve().parent
meta = json.loads((case / "case_meta.json").read_text())
T0 = meta["design"]["T_intake_K"]
U = meta["U_port_m_s"]
Tw = meta["T_wall_K"]
hdr = """FoamFile
{{
    version 2.0; format ascii; class {cls}; {loc}object {obj};
}}
dimensions {dim};
internalField {intf};
boundaryField
{{
{bf}
}}
"""

def w(path, obj, cls, dim, intf, bf, loc=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    l = f'location "{loc}"; ' if loc else ""
    path.write_text(hdr.format(cls=cls, obj=obj, dim=dim, intf=intf, bf=bf, loc=l))

WALL = '"(region0_to.*|walls)"'
z = case / "0"
w(z/"U", "U", "volVectorField", "[0 1 -1 0 0 0 0]", f"uniform (0 0 -{U*0.1})", f"""
    ".*"   {{ type zeroGradient; }}
    inlet  {{ type fixedValue; value uniform (0 0 -{U}); }}
    outlet {{ type pressureInletOutletVelocity; value uniform (0 0 0); }}
    {WALL} {{ type noSlip; }}""")
w(z/"T", "T", "volScalarField", "[0 0 0 1 0 0 0]", f"uniform {T0}", f"""
    ".*"   {{ type zeroGradient; }}
    inlet  {{ type fixedValue; value uniform {T0}; }}
    outlet {{ type inletOutlet; inletValue uniform {T0}; value uniform {T0}; }}
    {WALL} {{ type fixedValue; value uniform {Tw}; }}""")
w(z/"p", "p", "volScalarField", "[1 -1 -2 0 0 0 0]", "uniform 100000", """
    ".*" { type calculated; value uniform 100000; }""")
w(z/"p_rgh", "p_rgh", "volScalarField", "[1 -1 -2 0 0 0 0]", "uniform 100000", f"""
    ".*"   {{ type fixedFluxPressure; value uniform 100000; }}
    outlet {{ type fixedValue; value uniform 100000; }}""")
for sp, val in (("N2", 0.767), ("O2", 0.233), ("H2O", 0.0), ("CH3OH", 0.0)):
    w(z/sp, sp, "volScalarField", "[0 0 0 0 0 0 0]", f"uniform {val}", f"""
    ".*"   {{ type zeroGradient; }}
    inlet  {{ type fixedValue; value uniform {val}; }}
    outlet {{ type inletOutlet; inletValue uniform {val}; value uniform {val}; }}""")
w(z/"k", "k", "volScalarField", "[0 2 -2 0 0 0 0]", "uniform 1.0", f"""
    ".*"   {{ type zeroGradient; }}
    inlet  {{ type turbulentIntensityKineticEnergyInlet; intensity 0.05; value uniform 3.4; }}
    outlet {{ type inletOutlet; inletValue uniform 1.0; value uniform 1.0; }}
    {WALL} {{ type kqRWallFunction; value uniform 1.0; }}""")
w(z/"epsilon", "epsilon", "volScalarField", "[0 2 -3 0 0 0 0]", "uniform 100", f"""
    ".*"   {{ type zeroGradient; }}
    inlet  {{ type turbulentMixingLengthDissipationRateInlet; mixingLength 0.0019; value uniform 500; }}
    outlet {{ type inletOutlet; inletValue uniform 100; value uniform 100; }}
    {WALL} {{ type epsilonWallFunction; value uniform 100; }}""")
w(z/"nut", "nut", "volScalarField", "[0 2 -1 0 0 0 0]", "uniform 0", f"""
    ".*"   {{ type calculated; value uniform 0; }}
    {WALL} {{ type nutkFilmWallFunction; B 5.5; yPlusCrit 11.05; value uniform 0; }}""")
w(z/"alphat", "alphat", "volScalarField", "[1 -1 -1 0 0 0 0]", "uniform 0", f"""
    ".*"   {{ type calculated; value uniform 0; }}
    {WALL} {{ type alphatFilmWallFunction; B 5.5; yPlusCrit 11.05; Cmu 0.09; kappa 0.41; Prt 0.85; value uniform 0; }}""")
f = z / "wallFilmRegion"
w(f/"Tf", "Tf", "volScalarField", "[0 0 0 1 0 0 0]", f"uniform {Tw}", """
    ".*" { type zeroGradient; }""", loc="0/wallFilmRegion")
w(f/"Uf", "Uf", "volVectorField", "[0 1 -1 0 0 0 0]", "uniform (0 0 0)", """
    ".*"         { type zeroGradient; }
    ".*top"      { type slip; }
    "region0_to.*" { type noSlip; }""", loc="0/wallFilmRegion")
w(f/"deltaf", "deltaf", "volScalarField", "[0 1 0 0 0 0 0]", "uniform 0", """
    ".*" { type zeroGradient; }""", loc="0/wallFilmRegion")
print("fields written")
