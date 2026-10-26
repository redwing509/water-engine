"""Track B step 3: Cantera free-flame S_L with water dilution, w = 0..0.3, for PRF87/91/97, E10, E85.
Mechanism: CRECK TPRF_HT_ALC_254_7568 (Ranzi et al. 2012 PECS 38:468; Ranzi et al. 2014 IJCK 46:512),
mixture-averaged transport, phi = 1, water as vapour in the fresh mixture (w = water mass fraction of fuel+water).
States: Module 03 unburned states at IVC (p_ivc = 1e5 Pa, T_IVC of the chains: normal ~312 K at T_intake 320 K,
hot ~389 K at T_intake 400 K) and the existing fit's reference state (400 K, 1 atm) for the w = 0 validation."""
import json, sys, time
import cantera as ct
import numpy as np
MECH = sys.argv[1]
blend, state = sys.argv[2], sys.argv[3]
out = sys.argv[4]
VOL = {"PRF87": {"IC8H18": 0.87, "NC7H16": 0.13}, "PRF91": {"IC8H18": 0.91, "NC7H16": 0.09},
       "PRF97": {"IC8H18": 0.97, "NC7H16": 0.03},
       "E10": {"IC8H18": 0.9 * 0.91, "NC7H16": 0.9 * 0.09, "C2H5OH": 0.10},
       "E85": {"IC8H18": 0.15 * 0.91, "NC7H16": 0.15 * 0.09, "C2H5OH": 0.85}}
COMP = {"IC8H18": (114.231, 0.6919, (8, 18, 0)), "NC7H16": (100.202, 0.6795, (7, 16, 0)), "C2H5OH": (46.069, 0.7893, (2, 6, 1))}
STATES = {"normal": (312.35, 1.0e5), "hot": (388.8, 1.0e5), "ref400": (400.0, ct.one_atm)}
T, p = STATES[state]
WS = [0.0] if state == "ref400" else [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
import os  # Oct 26 fit-edge job: optional override, default unchanged
if os.environ.get("FL_WS"):
    WS = [float(v) for v in os.environ["FL_WS"].split(",")]
mol = {k: v * COMP[k][1] / COMP[k][0] for k, v in VOL[blend].items()}
n = sum(mol.values()); x = {k: v / n for k, v in mol.items()}
mw_f = sum(x[k] * COMP[k][0] for k in x)
o2 = sum(x[k] * (COMP[k][2][0] + COMP[k][2][1] / 4 - COMP[k][2][2] / 2) for k in x)  # mol O2 per mol fuel (phi=1)
gas = ct.Solution(MECH)
f = None
res = []
for w in WS:
    r = w / (1 - w)
    n_h2o = r * mw_f / 18.015  # mol water per mol fuel
    X = dict(x); X["O2"] = o2; X["N2"] = 3.76 * o2; X["H2O"] = n_h2o
    gas.TPX = T, p, X
    t0 = time.time()
    if f is None:
        f = ct.FreeFlame(gas, width=0.03)
        f.set_refine_criteria(ratio=3, slope=0.06, curve=0.12)
        f.transport_model = "mixture-averaged"
        f.solve(loglevel=0, auto=True)
    else:
        f.inlet.T = T; f.inlet.X = gas.X; f.P = p
        f.solve(loglevel=0)
    Y_h2o = gas.Y[gas.species_index("H2O")]
    row = dict(blend=blend, state=state, T_u_K=T, p_Pa=p, w=w, S_L_m_s=float(f.velocity[0]), Y_H2O_fresh=float(Y_h2o),
               T_ad_K=float(f.T[-1]), n_points=len(f.grid), sec=time.time() - t0)
    res.append(row); print(json.dumps(row), flush=True)
json.dump(res, open(out, "w"), indent=1)
