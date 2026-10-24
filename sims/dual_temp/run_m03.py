"""Run Module 03 engine_cycle in a named temperature regime (wall_T_K and T_intake sweep patched, nothing else).

usage: python -m sims.dual_temp.run_m03 --regime hot --workers 6 --out results/dual_temp/03_engine_cycle_hot
"""
import argparse, importlib, json, sys
from pathlib import Path
from sims.dual_temp.regimes import REGIMES

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regime", choices=sorted(REGIMES), required=True)
    ap.add_argument("--workers", default="4")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    reg = REGIMES[a.regime]
    m = importlib.import_module("sims.03_engine_cycle.run")
    object.__setattr__(m.DEFAULTS, "wall_T_K", float(reg["chamber_wall_K"]))  # same instance used by all default args
    m.FULL_T_INTAKE = tuple(reg["T_intake_K"])
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "regime.json").write_text(json.dumps(reg, indent=2))
    rc = m.main(["--quick" if a.quick else "--full", "--workers", a.workers, "--out", a.out])
    return rc

if __name__ == "__main__":
    sys.exit(main())
