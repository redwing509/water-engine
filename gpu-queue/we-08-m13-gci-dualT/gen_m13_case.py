#!/usr/bin/env python3
"""Generate one M13 case for the GCI x dual-temperature matrix WITHOUT editing the committed generator.
usage: gen_m13_case.py <port13_dir> <out_runs_dir> <name> <injector> <level coarse|med|fine> <T_wall_K> <T_intake_K> <np>
Mesh levels: uniform background spacing dx = 2.5 / 1.768 / 1.25 mm (r = sqrt(2)), same snappy refinement levels,
so the whole mesh refines uniformly. 'fine' == the generator's own 'prod' level."""
import importlib.util, json, math, sys
from pathlib import Path
port13, out, name, inj, level, Tw, Tin, npx = sys.argv[1:9]
Tw, Tin, npx = float(Tw), float(Tin), int(npx)
spec = importlib.util.spec_from_file_location("mpc", str(Path(port13) / "make_port_case.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
base = dict(m.MESH["coarse"])
dx = {"coarse": base["dx"], "med": base["dx"] / math.sqrt(2), "fine": base["dx"] / 2}[level]
key = "coarse" if level == "coarse" else "prod"          # generator treats non-coarse as prod (parcels/s 6e6)
m.MESH[key] = dict(base, dx=dx)
def split(n):                                            # n = a*b*c, decomposition along z first (long axis)
    best = (n, 1, 1)
    for c in range(1, n + 1):
        if n % c: continue
        for b in range(1, n // c + 1):
            if (n // c) % b: continue
            a = n // c // b
            if c >= b >= a and (max(a, b, c) / min(a, b, c)) < (max(best) / min(best)): best = (a, b, c)
    return best
m.DECOMP[key] = split(npx)
_orig = m.design_inputs
def di():
    d = _orig(); d["T_intake_K"] = Tin; return d
m.design_inputs = di
d = m.design_inputs()
case = m.make_case(name, inj, key, d, out=Path(out))
case = Path(out) / name
meta = json.loads((case / "case_meta.json").read_text())
meta.update(T_wall_K=Tw, gci_level=level, gci_dx_m=dx, decomposition=list(m.DECOMP[key]),
            dual_temp_regime=dict(T_port_wall_K=Tw, T_intake_K=Tin,
                                  source="dual-temperature rule 2026-10-24 (sims/dual_temp/regimes.py, wme1-hiT)"))
(case / "case_meta.json").write_text(json.dumps(meta, indent=2))
print(json.dumps(dict(case=str(case), level=level, dx=dx, decomp=m.DECOMP[key], T_wall_K=Tw, T_intake_K=Tin)))
