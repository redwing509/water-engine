"""X1 dual-temperature sweep: T_ad and S_L for CH3OH / C2H5OH, AramcoMech 2.0 vs San Diego.

Grok Bot takeover of Hermes job "X1 flame width sweep Aramco" (failed rc=1 on mail,
2026-10-24 18:29Z: ModuleNotFoundError 'sims' because the script was run by path from /root).
Run from the repo root as a module:  python -m sims.xcheck_chem.run_x1_dualT --mech aramco --workers 7

Regimes (James's dual-temperature rule, sims/dual_temp/regimes.py on wme1-hiT):
  normal : intake charge 320-360 K  -> unburned T_u = 360 K (upper normal; 320 K also run)
  hot    : intake charge 400 K      -> T_u = 400 K (this is also the original X1 contract point)
p = 1 atm, phi = 1, w = m_water/(m_water+m_fuel) in {0, 0.3, 0.6}; mixtures from sims/common/fuels.py.
Gas-phase fuel and water vapour (no latent heat), same convention as run_x1.py / module 02.

Flame solver: Cantera FreeFlame, mixture-averaged transport, no Soret, width 0.03 m.
Stage 1 auto=True with ratio 3 / slope 0.1 / curve 0.2; stage 2 refine to ratio 2 / slope 0.05 /
curve 0.1 / prune 0.01. S_L is the stage-2 value; |stage2-stage1|/stage2 is reported as a grid indicator.

Aramco (493 species) is too slow/heavy from a cold start (>30 min/case and 4-6 GB RSS per solve on the
box; that is the "FreeFlame hangs >10 min" Hermes hit).  With --seed (default for aramco) each case is
first solved with San Diego (same conditions, two-stage), and its T / u / shared-species profiles and grid
are used as the INITIAL GUESS for Aramco, which is then solved to its own steady state with the stage-2
refine criteria. The converged answer is Aramco's; the seed only changes the starting point.
For seeded runs S_L_coarse_m_s is the San Diego seed value (not an Aramco coarse grid).
A per-worker address-space cap (--mem-gb) turns OOM into a recorded solver_error instead of killing
other jobs on the host.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
import warnings
from multiprocessing import Pool
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:  # root-cause fix: works when invoked by path too
    sys.path.insert(0, str(REPO_ROOT))

import cantera as ct  # noqa: E402
from sims.common import fuels  # noqa: E402

MECHS = {"aramco": REPO_ROOT / "mechanisms" / "aramco20.yaml",
         "sandiego": REPO_ROOT / "mechanisms" / "sandiego.yaml"}
FUELS_X1 = ("CH3OH", "C2H5OH")
W = (0.0, 0.3, 0.6)
REGIME_TU = {"normal": (320.0, 360.0), "hot": (400.0,)}
T_AD_K = (300.0, 320.0, 360.0, 400.0)
P = ct.one_atm
PHI = 1.0
_GAS = None
_MECH = None


_SEED = None
_SEED_MECH = None
_OPTS = {}


def _init(mech_path, seed, mem_gb, max_points):
    global _GAS, _MECH, _SEED, _SEED_MECH
    warnings.filterwarnings("ignore")
    if mem_gb:
        import resource
        lim = int(mem_gb * 2**30)
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    _OPTS["max_points"] = max_points
    _MECH = str(mech_path)
    _GAS = ct.Solution(_MECH)
    if seed:
        _SEED_MECH = str(MECHS["sandiego"])
        _SEED = ct.Solution(_SEED_MECH)


def _seed_flame(fuel, w, T):
    _SEED.TPX = T, P, fuels.mixture(fuel, PHI, w, mech=_SEED_MECH)
    s = ct.FreeFlame(_SEED, width=0.03)
    s.transport_model = "mixture-averaged"
    s.soret_enabled = False
    s.set_refine_criteria(ratio=3.0, slope=0.1, curve=0.2)
    s.solve(loglevel=0, auto=True)
    s.set_refine_criteria(ratio=2.0, slope=0.05, curve=0.1, prune=0.01)
    s.solve(loglevel=0, refine_grid=True)
    return s


def _regime(T):
    return "hot" if T >= 400.0 else "normal"


def t_ad(case):
    fuel, w, T = case
    _GAS.TPX = T, P, fuels.mixture(fuel, PHI, w, mech=_MECH)
    _GAS.equilibrate("HP")
    return dict(kind="T_ad", fuel=fuel, w=w, T_u_K=T, regime=_regime(T), T_ad_K=float(_GAS.T))


def s_l(case):
    fuel, w, T = case
    t0 = time.time()
    row = dict(kind="S_L", fuel=fuel, w=w, T_u_K=T, regime=_regime(T), S_L_m_s=None,
               S_L_coarse_m_s=None, grid_rel_change=None, grid_points=None, T_max_K=None,
               status="solver_error", reason="", secs=None)
    try:
        _GAS.TPX = T, P, fuels.mixture(fuel, PHI, w, mech=_MECH)
        if _SEED is not None:
            import numpy as np
            sd = _seed_flame(fuel, w, T)
            s1 = float(sd.velocity[0])
            f = ct.FreeFlame(_GAS, grid=sd.grid.copy())
            f.transport_model = "mixture-averaged"
            f.soret_enabled = False
            f.set_initial_guess()
            z = (sd.grid - sd.grid[0]) / (sd.grid[-1] - sd.grid[0])
            f.flame.set_profile("T", z, sd.T)
            f.flame.set_profile("velocity", z, sd.velocity)
            names = sd.gas.species_names
            for n in _GAS.species_names:
                f.flame.set_profile(n, z, sd.Y[names.index(n)] if n in names else np.zeros_like(z))
            Tmid = 0.75 * f.T[0] + 0.25 * f.T[-1]
            f.fixed_temperature = f.T[np.flatnonzero(f.T < Tmid)[-1]]
            row["seed"] = "sandiego"
        else:
            f = ct.FreeFlame(_GAS, width=0.03)
            f.transport_model = "mixture-averaged"
            f.soret_enabled = False
            f.set_refine_criteria(ratio=3.0, slope=0.1, curve=0.2)
            f.solve(loglevel=0, auto=True)
            s1 = float(f.velocity[0])
        if _OPTS.get("max_points"):
            f.max_grid_points = _OPTS["max_points"]
        f.set_refine_criteria(ratio=2.0, slope=0.05, curve=0.1, prune=0.01)
        f.solve(loglevel=0, refine_grid=True)
        s2 = float(f.velocity[0])
        ok = math.isfinite(s2) and s2 > 0.02
        row.update(S_L_m_s=s2 if ok else None, S_L_coarse_m_s=s1, grid_points=len(f.grid),
                   grid_rel_change=abs(s2 - s1) / s2 if ok else None, T_max_K=float(max(f.T)),
                   status="computed" if ok else "no_flame")
    except Exception as exc:  # recorded, never hidden
        row["reason"] = f"{type(exc).__name__}: {exc}"[:500]
    row["secs"] = round(time.time() - t0, 1)
    print(f"[{_MECH.split('/')[-1]}] S_L {fuel} w={w} Tu={T:.0f} -> {row['S_L_m_s']} "
          f"({row['status']}, {row['secs']} s, {row['grid_points']} pts)", flush=True)
    return row


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--mech", choices=sorted(MECHS), required=True)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--out", default=str(REPO_ROOT / "results" / "xcheck" / "x1_dualT"))
    ap.add_argument("--temps", default="400,360,320", help="S_L unburned temperatures [K]")
    ap.add_argument("--tag", default="", help="suffix for the output JSON (partial runs)")
    ap.add_argument("--seed", choices=("auto", "yes", "no"), default="auto")
    ap.add_argument("--mem-gb", type=float, default=0.0, help="per-worker RLIMIT_AS cap")
    ap.add_argument("--max-points", type=int, default=600)
    ap.add_argument("--skip-from", default="", help="glob of earlier JSONs; skip S_L cases already computed")
    ap.add_argument("--no-tad", action="store_true", help="skip T_ad (already in an earlier part)")
    a = ap.parse_args(argv)
    seed = a.seed == "yes" or (a.seed == "auto" and a.mech == "aramco")
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    mech = MECHS[a.mech]
    t0 = time.time()
    ad_cases = [(f, w, T) for f in FUELS_X1 for w in W for T in T_AD_K]
    temps = [float(t) for t in a.temps.split(",") if t]
    sl_cases = [(f, w, T) for T in temps for f in FUELS_X1 for w in W]
    if a.skip_from:
        done = set()
        for p in sorted(Path().glob(a.skip_from)) if not Path(a.skip_from).is_absolute() else \
                sorted(Path("/").glob(a.skip_from.lstrip("/"))):
            done |= {(r["fuel"], r["w"], r["T_u_K"]) for r in json.loads(p.read_text())["S_L"]
                     if r["status"] == "computed"}
        sl_cases = [c for c in sl_cases if c not in done]
        print(f"skipping {len(done)} computed cases; {len(sl_cases)} to run", flush=True)
    if a.no_tad:
        ad_cases = []
    with Pool(a.workers, initializer=_init, initargs=(mech, seed, a.mem_gb, a.max_points),
              maxtasksperchild=1) as pool:
        ad = pool.map(t_ad, ad_cases) if ad_cases else []
        sl = pool.map(s_l, sl_cases, chunksize=1)
    import hashlib
    payload = dict(
        mechanism=str(mech.relative_to(REPO_ROOT)),
        mechanism_sha256_lf=hashlib.sha256(mech.read_bytes()).hexdigest(),
        cantera=ct.__version__, p_Pa=P, phi=PHI, regimes_T_u_K=REGIME_TU,
        regime_source="sims/dual_temp/regimes.py (wme1-hiT): intake charge 320/360 K normal, 400 K hot",
        solver=dict(width_m=0.03, transport="mixture-averaged", soret=False,
                    stage1=dict(ratio=3.0, slope=0.1, curve=0.2, auto=True),
                    stage2=dict(ratio=2.0, slope=0.05, curve=0.1, prune=0.01)),
        seeded_from_sandiego=seed, mem_gb_cap=a.mem_gb, max_grid_points=a.max_points,
        T_ad=ad, S_L=sl, runtime_s=round(time.time() - t0, 1),
        host=os.uname().nodename, workers=a.workers)
    (out / f"x1_dualT_{a.mech}{('_' + a.tag) if a.tag else ''}.json").write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    print(f"done {a.mech} in {payload['runtime_s']} s -> {out}")
    return 0 if all(r["status"] == "computed" for r in sl) else 1


if __name__ == "__main__":
    raise SystemExit(main())
