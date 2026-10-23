#!/usr/bin/env python3
"""Parse sprayFoam logs -> per-case CSV/PNG + results/summary.json.
evaporated fraction = 1 - (liquid mass in system + mass escaped)/mass introduced."""
import re, json, csv, pathlib, sys
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ROOT = pathlib.Path(__file__).resolve().parents[1]; RUNS = ROOT/"runs"; OUT = ROOT/"results"; OUT.mkdir(exist_ok=True)
num = r"([-+0-9.eE]+)"
def parse(log):
    rows, cur = [], None
    for line in open(log, errors="ignore"):
        if line.startswith("Time = "):
            cur = {"t_s": float(line.split("=")[1])}; continue
        if cur is None: continue
        m = re.search(r"Current mass in system\s+= "+num, line)
        if m: cur["m_sys"] = float(m.group(1))
        m = re.search(r"mass introduced\s+= "+num, line)
        if m: cur["m_inj"] = float(m.group(1))
        m = re.search(r"- (escape|stick)\s+= "+num+", "+num, line)
        if m: cur["m_"+m.group(1)] = cur.get("m_"+m.group(1), 0.0) + float(m.group(3))
        m = re.search(r"D10, D32, Dmax \(mu\)\s+= "+num+", "+num+", "+num, line)
        if m: cur["D32_um"] = float(m.group(2))
        m = re.search(r"Liquid penetration 95% mass \(m\) = "+num, line)
        if m:
            cur["pen_mm"] = 1e3*float(m.group(1)); rows.append(cur); cur = None
    out = []
    for r in rows:
        if r.get("m_inj", 0) <= 0: continue
        lost = r.get("m_escape", 0.0) + r.get("m_stick", 0.0)
        out.append(dict(t_ms=1e3*r["t_s"], penetration_mm=r["pen_mm"], SMD_um=r.get("D32_um", float("nan")),
                        mass_injected_kg=r["m_inj"], liquid_mass_kg=r["m_sys"],
                        wall_or_escaped_mass_kg=lost,
                        evaporated_pct=100*(1-(r["m_sys"]+lost)/r["m_inj"])))
    return out
def at(rows, t_ms):
    return min(rows, key=lambda r: abs(r["t_ms"]-t_ms))
summary = {}
for case in sorted(p for p in RUNS.iterdir() if (p/"log.sprayFoam").exists()):
    rows = parse(case/"log.sprayFoam")
    if not rows: continue
    csvp = OUT/f"{case.name}.csv"
    with open(csvp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    fig, ax = plt.subplots(2, 2, figsize=(9, 6))
    t = [r["t_ms"] for r in rows]
    for a, k in zip(ax.flat, ["penetration_mm", "evaporated_pct", "SMD_um", "wall_or_escaped_mass_kg"]):
        a.plot(t, [r[k] for r in rows]); a.set_xlabel("t [ms]"); a.set_ylabel(k); a.grid(alpha=.3)
    fig.suptitle(case.name); fig.tight_layout(); fig.savefig(OUT/f"{case.name}.png", dpi=90); plt.close(fig)
    meta = json.loads((case/"case_meta.json").read_text()) if (case/"case_meta.json").exists() else {}
    eoi = 1e3*meta.get("dur", 1.25e-3)
    e, last = at(rows, eoi), rows[-1]
    rt = (case/"runtime.txt").read_text().split()[1] if (case/"runtime.txt").exists() else None
    summary[case.name] = dict(csv=csvp.name, eoi_ms=eoi, eoi_row_t_ms=e["t_ms"],
        penetration_eoi_mm=e["penetration_mm"], evaporated_eoi_pct=e["evaporated_pct"], SMD_eoi_um=e["SMD_um"],
        wall_or_escaped_eoi_kg=e["wall_or_escaped_mass_kg"],
        end_t_ms=last["t_ms"], penetration_end_mm=last["penetration_mm"], evaporated_end_pct=last["evaporated_pct"],
        runtime_s=int(rt) if rt else None, complete=rt is not None, meta=meta)
if "A1-BLEND" in summary and "A1-BLEND-fine" in summary:
    a, b = summary["A1-BLEND"], summary["A1-BLEND-fine"]
    summary["grid_check_A1-BLEND"] = dict(
        penetration_change_pct=100*(b["penetration_eoi_mm"]-a["penetration_eoi_mm"])/a["penetration_eoi_mm"],
        evaporated_change_pct=100*(b["evaporated_eoi_pct"]-a["evaporated_eoi_pct"])/a["evaporated_eoi_pct"],
        source="A1-BLEND.csv vs A1-BLEND-fine.csv at EOI")
(OUT/"summary.json").write_text(json.dumps(summary, indent=1))
print(json.dumps({k: {kk: v.get(kk) for kk in ("penetration_eoi_mm","evaporated_eoi_pct","runtime_s","penetration_change_pct","evaporated_change_pct")} for k, v in summary.items()}, indent=0))
