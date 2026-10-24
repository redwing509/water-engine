#!/usr/bin/env python3
"""Post-process a module 13 port-film case: mass accounting at IVC (t_end).

Outputs cfd/results/M13/<case>.json and cfd/results/M13/<case>.csv (time history).
Mass balance at t: injected = film + airborne droplets + liquid escaped (outlet ->
cylinder, inlet -> backflow) + evaporated.  'Evaporated' is the closure of that
balance, cross-checked against the cloud + film phase-change totals and against
the gas-phase vapour inventory (in-domain integral + time-integrated outflow).
Labels: EXECUTED model output, model-vs-model only; nothing here is VALIDATED.
"""
import csv, json, re, sys
from pathlib import Path

CFD = Path(__file__).resolve().parent.parent

def parse_log(log):
    rows, cur, patch = [], None, None
    pat = {
        "n_parcels": r"Current number of parcels\s+=\s+(\S+)",
        "m_drops": r"Current mass in system\s+=\s+(\S+)",
        "m_injected": r"- mass introduced\s+=\s+(\S+)",
        "m_absorbed_film": r"- mass absorbed\s+=\s+(\S+)",
        "m_phase_change_drops": r"Mass transfer phase change\s+=\s+(\S+)",
        "m_film": r"current mass\s+=\s+(\S+)",
        "m_phase_change_film": r"mass phase change\s+=\s+(\S+)",
        "film_coverage": r"coverage\s+=\s+(\S+)",
        "film_delta_max": r"min/max\(delta\)\s+=\s+\S+,\s+(\S+)",
    }
    for line in open(log, errors="replace"):
        m = re.match(r"^Time = (\S+)", line)
        if m:
            if cur: rows.append(cur)
            cur = {"t": float(m.group(1)), "esc_inlet": 0.0, "esc_outlet": 0.0, "esc_system": 0.0}
            continue
        if cur is None: continue
        m = re.search(r"Parcel fate: patch \(number, mass\) (\S+)", line)
        if m: patch = m.group(1); continue
        if "Parcel fate: system" in line: patch = "system"; continue
        m = re.search(r"- escape\s+=\s+\S+,\s+(\S+)", line)
        if m:
            if patch in ("inlet", "outlet", "system"): cur["esc_" + patch] = float(m.group(1))
            continue
        for k, p in pat.items():
            m = re.search(p, line)
            if m:
                try: cur[k] = float(m.group(1))
                except ValueError: pass
                break
    if cur: rows.append(cur)
    return [r for r in rows if "m_film" in r and "m_drops" in r]

def read_dat(dirpath):
    out = {}
    for f in sorted(Path(dirpath).rglob("*.dat")):
        for line in open(f):
            if line.startswith("#") or not line.strip(): continue
            v = line.split()
            out[float(v[0])] = [float(x) for x in v[1:]]
    return sorted(out.items())

def main(name):
    case = CFD / "runs" / name
    meta = json.loads((case / "case_meta.json").read_text())
    rows = parse_log(case / "log.reactingParcelFoam")
    if not rows: raise SystemExit(f"{name}: no data in log")
    last = rows[-1]
    t_end = meta["t_end_s"]
    complete = last["t"] >= t_end * (1 - 1e-6)
    vin = read_dat(case / "postProcessing/vapourInDomain")
    vout = read_dat(case / "postProcessing/vapourOut")
    m_vout, tp = 0.0, None
    for t, v in vout:
        if t > last["t"]: break
        if tp is not None: m_vout += (v[0] + v[1]) * (t - tp)
        tp = t
    v_dom = [v for t, v in vin if t <= last["t"]]
    m_vdom = sum(v_dom[-1]) if v_dom else float("nan")
    inj = last.get("m_injected") or float("nan")
    esc = last["esc_inlet"] + last["esc_outlet"]
    evap_closure = inj - last["m_film"] - last["m_drops"] - esc
    evap_pc = last.get("m_phase_change_drops", 0.0) + last.get("m_phase_change_film", 0.0)
    peak_film = max(r["m_film"] for r in rows)
    pr = case / "peak_rss_mb.txt"
    res = dict(
        case=name, injector=meta["injector_label"], smd_um=meta["smd_m"] * 1e6, mesh=meta["mesh"],
        status="EXECUTED (model output; coarse mesh; not mesh-converged; not VALIDATED)",
        complete=complete, t_last_s=last["t"], t_end_ivc_s=t_end,
        m_injected_kg=inj, m_liq_design_kg=meta["m_liq_injected_kg"],
        film_pct_at_ivc=100 * last["m_film"] / inj,
        film_peak_pct=100 * peak_film / inj,
        absorbed_into_film_pct=100 * last.get("m_absorbed_film", 0.0) / inj,
        airborne_drops_pct_at_ivc=100 * last["m_drops"] / inj,
        escaped_outlet_liquid_pct=100 * last["esc_outlet"] / inj,
        escaped_inlet_liquid_pct=100 * last["esc_inlet"] / inj,
        evaporated_pct_at_ivc=100 * evap_closure / inj,
        evaporated_pct_phase_change_totals=100 * evap_pc / inj,
        vapour_inventory_pct=100 * (m_vdom + m_vout) / inj,
        film_coverage_at_ivc=last.get("film_coverage"),
        film_delta_max_m=last.get("film_delta_max"),
        peak_rss_mb=int(pr.read_text()) if pr.exists() else None,
        flagged=meta["flagged"], film_liquid=meta["film_liquid"],
    )
    outd = CFD / "results/M13"; outd.mkdir(parents=True, exist_ok=True)
    (outd / f"{name}.json").write_text(json.dumps(res, indent=2))
    keys = ["t", "m_injected", "m_film", "m_drops", "m_absorbed_film", "esc_outlet", "esc_inlet",
            "m_phase_change_drops", "m_phase_change_film", "film_coverage"]
    step = max(1, len(rows) // 400)
    with open(outd / f"{name}.csv", "w", newline="") as f:
        wr = csv.writer(f); wr.writerow(keys)
        for r in rows[::step] + [rows[-1]]:
            wr.writerow([r.get(k, "") for k in keys])
    print(json.dumps({k: res[k] for k in ("case", "complete", "film_pct_at_ivc", "evaporated_pct_at_ivc",
                                          "evaporated_pct_phase_change_totals", "vapour_inventory_pct",
                                          "escaped_outlet_liquid_pct", "airborne_drops_pct_at_ivc")}))

if __name__ == "__main__":
    for n in sys.argv[1:]: main(n)
