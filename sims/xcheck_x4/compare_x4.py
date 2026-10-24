"""X4: third spray model for the Module 09 vs CFD cross-check (Claude box-queue job J3, 2026-10-24).

The CFD 'base' cases (water-engine-cfd wme1-cfd, aachenBomb-derived sprayFoam, coarse mesh) use
phaseChangeModel liquidEvaporationBoil + breakupModel ReitzKHRT. X4 re-runs cases A1-H2O and A2-BLEND with
  RD    : liquidEvaporationBoil + ReitzDiwakar  (the spec's 'third spray model': different breakup physics)
  LE-RD : liquidEvaporation     + ReitzDiwakar  (also swaps the evaporation sub-model; no boiling branch)
everything else identical (mesh, injector, chemistry, time step).
For each CFD variant Module 09's 0-D chamber (sims/09_spray_evaporation/run.chamber_run, Wilson activity) is rerun
at THAT CFD's own SMD at EOI, so breakup-model differences in SMD are not counted as an evaporation error.
Also the two documented Module 09 biases are bounded (results/xcheck/m09_bias_diag.py logic):
  cone  - vapour confined to the spray cone volume (theta 10 deg, CFD end penetration) instead of the full chamber
  slip  - initial droplet slip halved (entrained-gas co-flow)
Criterion (from water-engine-xcheck-20261023-1445): evaporated fraction agrees within +-15 % relative.
usage (repo root): python -m sims.xcheck_x4.compare_x4 [--cfd /workspace/water-engine-cfd/cfd]
"""
import argparse, csv, importlib, json, math
from pathlib import Path
import numpy as np

R = importlib.import_module("sims.09_spray_evaporation.run")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "xcheck" / "x4_spray"
TOL = 0.15
VARIANTS = {"A1-H2O": {"KHRT": "A1-H2O", "RD": "X4-A1-H2O-RD", "LE-RD": "X4-A1-H2O-LE-RD"},
            "A2-BLEND": {"KHRT": "A2-BLEND", "RD": "X4-A2-BLEND-RD", "LE-RD": "X4-A2-BLEND-LE-RD"}}
MODEL = {"KHRT": "liquidEvaporationBoil + ReitzKHRT (base)", "RD": "liquidEvaporationBoil + ReitzDiwakar",
         "LE-RD": "liquidEvaporation + ReitzDiwakar"}


def load_parser(cfd_root):
    """parse() from the CFD repo's own postprocess.py, without running its side effects."""
    src = (cfd_root / "scripts" / "postprocess.py").read_text()
    head = src.split("summary = {}")[0]
    ns = {"__file__": str(cfd_root / "scripts" / "postprocess.py"), "__name__": "pp"}
    exec(compile(head, "postprocess.py(head)", "exec"), ns)
    return ns["parse"]


def m09_series(meta, smd_m, t_end, vol=None, slip=1.0):
    meta = dict(meta); meta["U_bernoulli_m_s"] = slip * meta["U_bernoulli_m_s"]
    V0 = R.CFD_CHAMBER_V_m3
    try:
        if vol is not None:
            R.CFD_CHAMBER_V_m3 = vol
        s = R.chamber_run(meta, smd_m, t_end, "wilson")
    finally:
        R.CFD_CHAMBER_V_m3 = V0
    return np.array([x["t_s"] for x in s]), np.array([100 * x["evaporated_frac"] for x in s])


def at(t, y, tt):
    return float(np.interp(tt, t, y))


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--cfd", default="/workspace/water-engine-cfd/cfd")
    a = ap.parse_args(argv); cfd_root = Path(a.cfd); parse = load_parser(cfd_root)
    OUT.mkdir(parents=True, exist_ok=True)
    rows, summary = [], {}
    for case, vs in VARIANTS.items():
        summary[case] = {}
        for tag, run in vs.items():
            d = cfd_root / "runs" / run
            log = d / "log.sprayFoam"
            if not (d / "runtime.txt").exists() or not log.exists():
                summary[case][tag] = dict(run=run, status="not complete"); continue
            meta = json.loads((d / "case_meta.json").read_text())
            pr = parse(log)
            t = np.array([r["t_ms"] for r in pr]) * 1e-3
            ev = np.array([r["evaporated_pct"] for r in pr]); smd = np.array([r["SMD_um"] for r in pr])
            pen = np.array([r["penetration_mm"] for r in pr])
            eoi, t_end = meta["dur"], float(t[-1])
            smd_eoi = at(t, smd, eoi)
            tm, em = m09_series(meta, smd_eoi * 1e-6, t_end)
            L = float(pen[-1]) * 1e-3
            Vc = math.pi * (L * math.tan(math.radians(10))) ** 2 * L / 3
            tc, ec = m09_series(meta, smd_eoi * 1e-6, t_end, vol=Vc)
            ts, es = m09_series(meta, smd_eoi * 1e-6, t_end, slip=0.5)
            res = dict(run=run, model=MODEL[tag], exec_s=float((d / "runtime.txt").read_text().split()[1]),
                       SMD_eoi_um=smd_eoi, penetration_eoi_mm=at(t, pen, eoi), penetration_end_mm=float(pen[-1]),
                       eoi_ms=1e3 * eoi, end_ms=1e3 * t_end,
                       cfd_eoi_pct=at(t, ev, eoi), cfd_end_pct=float(ev[-1]),
                       m09_eoi_pct=at(tm, em, eoi), m09_end_pct=float(em[-1]),
                       m09_cone_end_pct=float(ec[-1]), cone_volume_over_chamber=Vc / R.CFD_CHAMBER_V_m3,
                       m09_halfslip_end_pct=float(es[-1]))
            for k in ("eoi", "end"):
                res[f"ratio_m09_over_cfd_{k}"] = res[f"m09_{k}_pct"] / res[f"cfd_{k}_pct"]
                res[f"pass_15pct_{k}"] = abs(res[f"ratio_m09_over_cfd_{k}"] - 1) <= TOL
            summary[case][tag] = res
            for tt in np.arange(1e-4, t_end + 1e-12, 1e-4):
                rows.append(dict(case=case, cfd_model=tag, t_ms=round(1e3 * tt, 4), evaporated_cfd_pct=at(t, ev, tt),
                                 evaporated_m09_pct=at(tm, em, tt), SMD_cfd_um=at(t, smd, tt), penetration_cfd_mm=at(t, pen, tt)))
        done = {k: v for k, v in summary[case].items() if "cfd_end_pct" in v}
        if len(done) >= 2:
            e = [v["cfd_end_pct"] for v in done.values()]
            summary[case]["cfd_model_spread"] = dict(min_end_pct=min(e), max_end_pct=max(e), max_over_min=max(e) / min(e),
                                                     models=list(done))
            m09_in_band = [k for k, v in done.items()]
            summary[case]["m09_end_vs_cfd_band"] = dict(
                m09_end_at_each_cfd_smd={k: v["m09_end_pct"] for k, v in done.items()},
                inside_cfd_band_widened_15pct=[k for k, v in done.items()
                                               if (1 - TOL) * min(e) <= v["m09_end_pct"] <= (1 + TOL) * max(e)])
    with (OUT / "x4_timeseries.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    (OUT / "x4_summary.json").write_text(json.dumps(summary, indent=1))
    for case, s in summary.items():
        for tag, v in s.items():
            if isinstance(v, dict) and "cfd_end_pct" in v:
                print(f"{case:9s} {tag:6s} SMD {v['SMD_eoi_um']:6.1f}  CFD eoi/end {v['cfd_eoi_pct']:.3f}/{v['cfd_end_pct']:.3f}  "
                      f"M09 {v['m09_eoi_pct']:.3f}/{v['m09_end_pct']:.3f}  ratio {v['ratio_m09_over_cfd_eoi']:.2f}/{v['ratio_m09_over_cfd_end']:.2f}  "
                      f"cone {v['m09_cone_end_pct']:.3f} halfslip {v['m09_halfslip_end_pct']:.3f}")
            elif tag in ("KHRT", "RD", "LE-RD"):
                print(case, tag, v.get("status"))


if __name__ == "__main__":
    main()
