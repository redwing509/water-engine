#!/usr/bin/env python3
"""Generate module-12 phase-A spray cases from the stock aachenBomb tutorial (OpenFOAM v2512).
Changes vs tutorial: liquid, chamber p/T (non-reacting: chemistry off, combustion none,
gas species O2 N2 H2O CH3OH), injection (mass, duration, orifice, size distribution scaled to
orifice), breakup ReitzKHRT with tutorial default coefficients, end time = EOI + 1 ms.
Mesh, schemes, solver settings, evaporation model and wall interaction unchanged."""
import math, re, shutil, sys, json, pathlib
TUT = pathlib.Path("/usr/lib/openfoam/openfoam2512/tutorials/lagrangian/sprayFoam/aachenBomb")
RUNS = pathlib.Path(__file__).resolve().parents[1] / "runs"
NP = 6
Cd = 0.9  # tutorial discharge coefficient
LIQ = {  # density at ~300 K [kg/m3], mass fractions
    "H2O":   {"rho": 997.0, "comp": {"H2O": 1.0}},
    "CH3OH": {"rho": 787.0, "comp": {"CH3OH": 1.0}},
    "BLEND": {"rho": None, "comp": {"H2O": 0.6, "CH3OH": 0.4}},
}
LIQ["BLEND"]["rho"] = 1.0 / (0.6 / 997.0 + 0.4 / 787.0)
COND = {  # p [Pa], T [K], injection dP [Pa], orifice d [m], duration [s]
    "A1": dict(p=1.0e5, T=360.0, dP=5.0e5, d=0.25e-3, dur=5.0e-3),
    "A2": dict(p=20.0e5, T=700.0, dP=100.0e5, d=0.15e-3, dur=2.0e-3),
}
CH3OH_THERM = """CH3OH             L 8/88C   1H   4O   1     G   200.000  3500.000 1000.00      1
 1.78970791E+00 1.40938292E-02-6.36500835E-06 1.38171085E-09-1.17060220E-13    2
-2.53748747E+04 1.45023623E+01 5.71539582E+00-1.52309129E-02 6.52441155E-05    3
-7.10806889E-08 2.61352698E-11-2.56427656E+04-1.50409823E+00                   4
"""

def sub(path, pat, rep, count=1):
    s = path.read_text(); n = len(re.findall(pat, s, flags=re.S))
    if n == 0: raise SystemExit(f"pattern not found in {path}: {pat}")
    path.write_text(re.sub(pat, rep, s, count=count, flags=re.S))

def make(cond, liq, refine=1.0):
    name = f"{cond}-{liq}" + ("-fine" if refine != 1.0 else "")
    c = RUNS / name
    if c.exists(): shutil.rmtree(c)
    shutil.copytree(TUT, c)
    C, L = COND[cond], LIQ[liq]
    A = math.pi * C["d"] ** 2 / 4
    mdot = Cd * A * math.sqrt(2 * L["rho"] * C["dP"])
    mass = mdot * C["dur"]
    # chemistry: non-reacting gas with evaporating species
    ck = c / "chemkin"
    (ck / "chem.inp").write_text("ELEMENTS\n H O C N AR\nEND\nSPECIE\nO2 N2 H2O CH3OH\nEND\n")
    th = (ck / "therm.dat").read_text()
    th = re.sub(r"C7H16 .*?4\n", "", th, count=1, flags=re.S)
    th = th.replace("\nEND", "\n" + CH3OH_THERM.rstrip("\n") + "\nEND")
    (ck / "therm.dat").write_text(th)
    sub(c / "constant/chemistryProperties", r"chemistry\s+on;", "chemistry       off;")
    sub(c / "constant/combustionProperties", r"combustionModel\s+PaSR;", "combustionModel none;")
    sub(c / "constant/combustionProperties", r"active\s+yes;", "active          no;")
    sub(c / "constant/thermophysicalProperties", r"liquids\s*\{\s*C7H16;\s*\}", "liquids\n{\n    H2O;\n    CH3OH;\n}")
    sub(c / "0.orig/p", r"internalField\s+uniform\s+[^;]+;", f"internalField   uniform {C['p']:.6g};")
    sub(c / "0.orig/T", r"internalField\s+uniform\s+[^;]+;", f"internalField   uniform {C['T']:.6g};")
    cp = c / "constant/sprayCloudProperties"
    sub(cp, r"T0\s+320;", "T0              300;")
    sub(cp, r"rho0\s+1000;", f"rho0            {L['rho']:.1f};")
    sub(cp, r"massTotal\s+[^;]+;", f"massTotal       {mass:.6e};")
    sub(cp, r"duration\s+[^;]+;", f"duration        {C['dur']:.6e};")
    sub(cp, r"outerDiameter\s+[^;]+;", f"outerDiameter   {C['d']:.6e};")
    sub(cp, r"flowRateProfile table\s*\(.*?\);",
        f"flowRateProfile table\n            (\n                (0 1)\n                ({C['dur']:.6e} 1)\n                ({C['dur']*1.0004:.6e} 0)\n                (1000 0)\n            );")
    # size distribution scaled to orifice like tutorial (lambda=0.79 d, max=d)
    sub(cp, r"maxValue\s+[^;]+;", f"maxValue        {C['d']:.6e};")
    sub(cp, r"lambda\s+[^;]+;", f"lambda          {0.79*C['d']:.6e};")
    comp = "\n".join(f"                {k} {v};" for k, v in L["comp"].items())
    sub(cp, r"liquid\s*\{\s*C7H16\s+1;\s*\}", "liquid\n            {\n" + comp + "\n            }")
    sub(cp, r"activeLiquids\s*\(\s*C7H16\s*\);", "activeLiquids    ( " + " ".join(L["comp"]) + " );")
    sub(cp, r"breakupModel\s+ReitzDiwakar;[^\n]*", "breakupModel    ReitzKHRT;")
    sub(cp, r"/\*\s*(ReitzKHRTCoeffs.*?\})\s*\*/", r"\1")
    sub(c / "system/controlDict", r"endTime\s+[^;]+;", f"endTime         {C['dur']+1e-3:.6g};")
    sub(c / "system/controlDict", r"writeInterval\s+5e-05;", "writeInterval   5e-04;")  # output only, saves disk
    sub(c / "system/decomposeParDict", r"numberOfSubdomains\s+\d+;", f"numberOfSubdomains {NP};")
    sub(c / "system/decomposeParDict", r"n\s+\(1 8 1\);", "n           (1 6 1);")
    if refine != 1.0:
        sub(c / "system/blockMeshDict", r"\(41 41 100\)", "(62 62 150)")
    meta = dict(case=name, cond=cond, liquid=liq, refine=refine, **C, rho_liq=L["rho"], Cd=Cd,
                orifice_area_m2=A, mdot_kg_s=mdot, massTotal_kg=mass,
                U_bernoulli_m_s=Cd*math.sqrt(2*C["dP"]/L["rho"]), composition=L["comp"])
    (c / "case_meta.json").write_text(json.dumps(meta, indent=1))
    return name

if __name__ == "__main__":
    names = [make(cn, ln) for cn in ("A1", "A2") for ln in ("H2O", "CH3OH", "BLEND")]
    names.append(make("A1", "BLEND", refine=1.5))
    print("\n".join(names))
