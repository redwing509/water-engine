"""Side-by-side normal vs hot Module 03 comparison (dual-temperature rule). Writes results/dual_temp/03_compare/."""
import csv, json
from pathlib import Path
import numpy as np
R = Path("results/dual_temp")
def load(n): return [r for r in csv.DictReader((R / f"03_engine_cycle_{n}" / "cycle_points.csv").open())]
N, H = load("normal"), load("hot")
f = lambda r, k: float(r[k]) if r[k] not in ("", "None", "nan") else float("nan")
key = lambda r: (r["fuel"], float(r["CR"]), float(r["w"]), float(r["T_intake_K"]))
METRICS = ["gross_indicated_efficiency", "IMEP_Pa", "peak_pressure_Pa", "peak_temperature_K", "peak_burned_temperature_K",
           "wall_heat_J", "ca50_used_deg", "burn_10_90_deg", "knock_integral_at_default_ca50", "relative_NO", "NO_mol_per_J_fuel"]
nn = {key(r): r for r in N if r["status"] == "computed"}
pairs = []
for h in H:
    if h["status"] != "computed": continue
    k = key(h)
    n = nn.get(k) or nn.get((k[0], k[1], k[2], 360.0))  # hot 400 K intake compared with normal 360 K
    if not n: continue
    row = dict(fuel=k[0], CR=k[1], w=k[2], T_intake_hot_K=k[3], T_intake_normal_K=float(n["T_intake_K"]),
               knock_limited_normal=n["knock_limited"], knock_limited_hot=h["knock_limited"])
    for m in METRICS:
        row[m + "_normal"], row[m + "_hot"] = f(n, m), f(h, m)
    row["d_eta_pts"] = 100 * (row["gross_indicated_efficiency_hot"] - row["gross_indicated_efficiency_normal"])
    pairs.append(row)
out = R / "03_compare"; out.mkdir(parents=True, exist_ok=True)
with (out / "normal_vs_hot.csv").open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(pairs[0])); w.writeheader(); w.writerows(pairs)
def best(rows, fuel, wmin=0.0, wmax=1.0):
    c = [r for r in rows if r["status"] == "computed" and r["fuel"] == fuel and wmin <= float(r["w"]) <= wmax]
    b = max(c, key=lambda r: f(r, "gross_indicated_efficiency"))
    return dict(CR=float(b["CR"]), w=float(b["w"]), T_intake_K=float(b["T_intake_K"]), eta=f(b, "gross_indicated_efficiency"),
                ca50=f(b, "ca50_used_deg"), knock_limited=b["knock_limited"], peak_p_bar=f(b, "peak_pressure_Pa") / 1e5,
                rel_NO=f(b, "relative_NO"))
summary = dict(status="executed (Module 03 code unchanged; only wall_T_K and T_intake sweep patched). Normal regime reproduces the committed Module 03 baseline to 8e-12. Hot regime NOT yet verified by a second engine.",
               n_pairs=len(pairs), best={})
for fuel in ("CH3OH", "C2H5OH"):
    summary["best"][fuel] = {reg: dict(dry=best(rows, fuel, 0, 0), overall=best(rows, fuel), water_majority=best(rows, fuel, 0.5, 1))
                             for reg, rows in (("normal", N), ("hot", H))}
for fuel in sorted({p["fuel"] for p in pairs}):
    for Tn in (320.0, 360.0, 400.0):
        ps = [p for p in pairs if p["fuel"] == fuel and p["T_intake_hot_K"] == Tn]
        if not ps: continue
        d = np.array([p["d_eta_pts"] for p in ps])
        summary.setdefault("same_point_delta", {})[f"{fuel} T_intake_hot={Tn:g}"] = dict(
            n=len(ps), d_eta_pts_mean=float(np.nanmean(d)), d_eta_pts_min=float(np.nanmin(d)), d_eta_pts_max=float(np.nanmax(d)),
            knock_limited_normal=sum(p["knock_limited_normal"] == "True" for p in ps),
            knock_limited_hot=sum(p["knock_limited_hot"] == "True" for p in ps),
            wall_heat_ratio_mean=float(np.nanmean([p["wall_heat_J_hot"] / p["wall_heat_J_normal"] for p in ps if p["wall_heat_J_normal"] > 0])),
            peak_T_dK_mean=float(np.nanmean([p["peak_burned_temperature_K_hot"] - p["peak_burned_temperature_K_normal"] for p in ps])))
json.dump(summary, (out / "summary.json").open("w"), indent=2)
print(json.dumps(summary, indent=1))
