#!/usr/bin/env python3
"""Job #8 3-mesh GCI (Celik et al. 2008, Fs=1.25) for A1-BLEND and A2-BLEND spray cases.
Reads results CSVs written by the same parser as cfd/scripts/postprocess.py. Criteria: ACCEPTANCE_CRITERIA.md (pre-registered)."""
import csv, json, math, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent; RES = HERE/"results"; CFD = HERE.parents[1]
num = r"([-+0-9.eE]+)"
def parse(log):  # identical logic to cfd/scripts/postprocess.py parse()
    rows, cur = [], None
    for line in open(log, errors="ignore"):
        if line.startswith("Time = "): cur = {"t_s": float(line.split("=")[1])}; continue
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
        if m: cur["pen_mm"] = 1e3*float(m.group(1)); rows.append(cur); cur = None
    out = []
    for r in rows:
        if r.get("m_inj", 0) <= 0: continue
        lost = r.get("m_escape", 0.0) + r.get("m_stick", 0.0)
        out.append(dict(t_ms=1e3*r["t_s"], penetration_mm=r["pen_mm"], SMD_um=r.get("D32_um", float("nan")),
                        evaporated_pct=100*(1-(r["m_sys"]+lost)/r["m_inj"])))
    return out
def load_csv(p): return [{k: float(v) for k, v in r.items()} for r in csv.DictReader(open(p))]
def at(rows, t): return min(rows, key=lambda r: abs(r["t_ms"]-t))
def gci(f1, f2, f3, N1, N2, N3, Fs=1.25):
    """f1 finest. Returns dict with p, R, extrapolated value, GCI_fine %."""
    r21, r32 = (N1/N2)**(1/3), (N2/N3)**(1/3); e21, e32 = f2-f1, f3-f2
    out = dict(r21=r21, r32=r32, e21=e21, e32=e32)
    if e32 == 0 or e21 == 0: out.update(status="zero difference (converged or noise)"); return out
    R = e21/e32; out["R"] = R
    if not (0 < R < 1): out.update(status="oscillatory" if R < 0 else "divergent"); return out
    s = 1.0; p = abs(math.log(abs(e32/e21)))/math.log(r21)
    for _ in range(200):
        q = math.log((r21**p - s)/(r32**p - s)); p = abs(math.log(abs(e32/e21)) + q)/math.log(r21)
    ext = (r21**p*f1 - f2)/(r21**p - 1)
    out.update(status="monotone", p=p, f_ext=ext, GCI_fine_pct=100*Fs*abs((f1-f2)/f1)/(r21**p - 1))
    return out
LIMIT = dict(penetration_mm=5.0, evaporated_pct=10.0, SMD_um=10.0)
N = {"r100": 168100, "r150": 576600, "r225": 1904400}
def main():
    RES.mkdir(exist_ok=True); runs = HERE/"runs"; data = {}
    for log in sorted(runs.glob("*/log.sprayFoam")):
        rows = parse(log); data[log.parent.name] = rows
        with open(RES/f"{log.parent.name}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    box = {"A1-BLEND": load_csv(CFD/"results/A1-BLEND.csv"), "A2-BLEND": load_csv(CFD/"results/A2-BLEND.csv"),
           "A1-BLEND-r150": load_csv(CFD/"results/A1-BLEND-fine.csv")}
    summary = {}
    for case, eoi in (("A1-BLEND", 5.0), ("A2-BLEND", 2.0)):
        f150 = data.get(f"{case}-r150") or box.get(f"{case}-r150")
        lv = {"r100": data.get(f"{case}-r100-mail"), "r150": f150, "r225": data.get(f"{case}-r225")}
        if not all(lv.values()): summary[case] = dict(status="incomplete", have=[k for k, v in lv.items() if v]); continue
        res = {}
        for q, lim in LIMIT.items():
            f = {k: at(v, eoi)[q] for k, v in lv.items()}
            g = gci(f["r225"], f["r150"], f["r100"], N["r225"], N["r150"], N["r100"])
            g["values"] = f; g["limit_pct"] = lim
            g["pass"] = g.get("status") == "monotone" and 0.5 <= g["p"] <= 4 and g["GCI_fine_pct"] <= lim
            res[q] = g
        b, m = at(box[case], eoi), at(lv["r100"], eoi)
        rep = dict(pen_dev_pct=100*abs(b["penetration_mm"]-m["penetration_mm"])/m["penetration_mm"],
                   evap_dev_pct=100*abs(b["evaporated_pct"]-m["evaporated_pct"])/m["evaporated_pct"])
        rep["pass"] = rep["pen_dev_pct"] <= 3 and rep["evap_dev_pct"] <= 5
        res["base_reproducibility_box_vs_mail"] = rep
        res["verdict"] = ("PASS (mesh-verified, one engine)" if all(res[q]["pass"] for q in LIMIT) and rep["pass"]
                          else "noise-limited" if not rep["pass"] else "NOT PASSED")
        summary[case] = dict(eoi_ms=eoi, **res)
    (RES/"gci_summary.json").write_text(json.dumps(summary, indent=1, default=float))
    print(json.dumps(summary, indent=1, default=float))
if __name__ == "__main__": main()
