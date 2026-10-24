"""Run Module 04 six_stroke in a named temperature regime (wall_T_K patched) on that regime's Module 03 output.

usage: python -m sims.dual_temp.run_m04 --regime hot --cycle-dir results/dual_temp/03_engine_cycle_hot --out results/dual_temp/04_six_stroke_hot
"""
import argparse, importlib, json, sys
from pathlib import Path
from sims.dual_temp.regimes import REGIMES

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regime", choices=sorted(REGIMES), required=True)
    ap.add_argument("--cycle-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--workers", default="4")
    ap.add_argument("--design-points", action="store_true", help="design-point mode (adiabatic, zero water: wall T has no effect)")
    a = ap.parse_args()
    reg = REGIMES[a.regime]
    m = importlib.import_module("sims.04_six_stroke.run")
    object.__setattr__(m.DEFAULTS, "wall_T_K", float(reg["chamber_wall_K"]))
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "regime.json").write_text(json.dumps(reg, indent=2))
    return m.main(["--full", "--workers", a.workers, "--cycle-dir", a.cycle_dir, "--out", a.out] + (["--design-points"] if a.design_points else []))

if __name__ == "__main__":
    sys.exit(main())
