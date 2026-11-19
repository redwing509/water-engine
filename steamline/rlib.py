"""Steamline ranking helpers: best dry, eligible preferred; best wet by cost_gain, then cost/mile, then d_eta.
Model arithmetic only; not validation; factory CR withheld. Water is never a fuel.
"""
import json, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "reference"))
from sims.cost import cost as C

HERE = Path(__file__).resolve().parent
prices = C.load_prices()

def load(p):
    out = []
    for l in open(p):
        if l.strip():
            r = json.loads(l)
            if r.get("status") == "computed":
                out.append(r)
    return out

def gk(r):
    return (r.get("fuel"), r.get("regime"), r.get("bore_mm"), r.get("stroke_mm"), int(r.get("rpm") or 0),
            r.get("intake_mode") or r.get("water_mode"))

def best(rows):
    dry = [x for x in rows if abs(float(x.get("w") or 0)) < 1e-12]
    wet = [x for x in rows if float(x.get("w") or 0) > 1e-12 and x.get("eligible")]
    if not dry or not wet:
        return None
    d = max([x for x in dry if x.get("eligible")] or dry, key=lambda x: x.get("gross_indicated_efficiency") or 0)
    sc = []
    for w in wet:
        try:
            sc.append((C.compare(w, d, prices), w))
        except Exception:
            pass
    if not sc:
        return None
    rank = lambda it: (1 if (it[0].get("m03") or {}).get("cost_gain") else 0,
                       -((it[0].get("m03") or {}).get("cost_per_mile_pct") or 0),
                       (it[0].get("m03") or {}).get("d_eta_pp") or 0)
    sc.sort(key=rank, reverse=True)
    c, w = sc[0]; m = c.get("m03") or {}
    return dict(dry_CR=d.get("CR"), dry_eligible=bool(d.get("eligible")), wet_CR=w.get("CR"), wet_w=w.get("w"),
                cost=m.get("cost_per_mile_pct"), power=m.get("power_change_pct"), verdict=C.verdict(c))

def gain(b):  # same "gainish" test as cost_rescore_AHBH.py
    return b and (b["cost"] or 0) < -0.01 and (b["power"] if b["power"] is not None else -1) >= -0.01
