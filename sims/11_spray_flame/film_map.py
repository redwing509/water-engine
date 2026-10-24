"""Module 11 bound (ii) film sensitivity MAP (Claude box-queue J4, 2026-10-24).

Where does the bound-(ii) misfire boundary lie in port-wall temperature, as a function of wetted length,
film heat-transfer coefficient h_film, and film loading (thickness)?

Reuses, unchanged, the per-cycle port-film budget of sims/dual_temp/port_film_wall_T.py (copied from wme1-hiT
b9387fa): capacity = min(gas-side Spalding/Gilliland mass transfer while the valve is open, wall heat supply
h_film*(T_wall - T_bubble) capped at CHF), Raoult bubble point of the deposited film; film deposit and the
critical strip fraction x_crit(MIE > 100 mJ) per SMD from Module 11 film_strip (results/11_spray_flame/
bound_ii_film_strip/design_points.csv). Misfire reachable  <=>  X_strip_max = 1 - f_film_evap >= x_crit.

Axes
  T_wall      350 ... 440 K, 1 K steps plus 363.15 / 388.15 exactly (regime points 363.15 normal / 388.15 hot / 420 heated port marked)
  L_wet       0.02 ... 0.10 m, 0.01 m steps
  h_film      5e3, 1e4, 2e4, 3e4, 5e4 W/m2K
  film_mult   0.5, 1, 2 x the Module 09 deposit (film thickness proxy; equivalent mean thickness reported)
  T_plenum    360 K (normal intake) and 400 K (hot intake) - only the gas-side branch sees it
  SMD         200, 350, 500 um (Module 11 bound-(ii) strip drop sizes)
Boundary T*(case) = lowest T_wall at and above which misfire is unreachable for every grid T (non-monotone cases
are flagged). Status: EXECUTED estimate, NOT verified by a second engine, NOT validated (no port-film data).
usage (repo root): python -m sims.11_spray_flame.film_map --workers 6
"""
import argparse, csv, importlib, json, math
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "11_spray_flame" / "film_map"
T_WALL = tuple(sorted({float(t) for t in range(350, 441)} | {363.15, 388.15}))  # 1 K grid + exact regime points
L_WET = tuple(round(0.02 + 0.01 * i, 2) for i in range(9))
H_FILM = (5e3, 1e4, 2e4, 3e4, 5e4)
FILM_MULT = (0.5, 1.0, 2.0)
T_PLENUM = (360.0, 400.0)
SMDS = ("200", "350", "500")
RHO_LIQ = {"CH3OH": 792.0, "C2H5OH": 789.0, "H2O": 997.0}
REG_PTS = {"normal 363 K": 363.15, "hot 388 K": 388.15, "heated port 420 K": 420.0}


def load_cases():
    FS = importlib.import_module("sims.11_spray_flame.film_strip")
    R = importlib.import_module("sims.11_spray_flame.run")
    fits, sas, dp = R.load_inputs()
    ep = json.loads(FS.EP_PATH.read_text())
    xcrit = {}
    for r in csv.DictReader((ROOT / "results/11_spray_flame/bound_ii_film_strip/design_points.csv").open()):
        xc = r["x_strip_for_MIE_100mJ"]
        xcrit.setdefault((r["case"], r["atomiser"], r["variant"]), {})[f"{float(r['SMD_um']):g}"] = None if xc == "never" else float(xc)
    cases = []
    for key, c in sas["cases"].items():
        ms = R.masses(dp["per_fuel"][c["fuel"]][c["point"]], c["fuel"])
        for an, a in c["atomisers"].items():
            for v in R.VARIANTS:
                fm = FS.film_masses(a[v], ep[f"{key}/{an}/{v}"], ms)
                cases.append(dict(case=key, atomiser=an, variant=v, fuel=c["fuel"], film_a=fm["film_alcohol_kg"],
                                  film_w=fm["film_water_kg"], xcrit=xcrit[(key, an, v)]))
    return cases


def capacity_table(c):
    """Capacity [kg/cycle] (alcohol, water) on the full (T_plenum, L, h, T_wall) grid for one case."""
    P = importlib.import_module("sims.dual_temp.port_film_wall_T")
    cap = np.zeros((len(T_PLENUM), len(L_WET), len(H_FILM), len(T_WALL), 2))
    reg = {}
    for i, Tg in enumerate(T_PLENUM):
        for j, L in enumerate(L_WET):
            for k, h in enumerate(H_FILM):
                for t, Tw in enumerate(T_WALL):
                    ca, cw, rg = P.capacity(c["film_a"], c["film_w"], c["fuel"], Tw, Tg, L, h)
                    cap[i, j, k, t] = (ca, cw)
                    reg[(i, j, k, t)] = rg
    # regime label only kept for the bubble-point crossing
    tb = None
    for t, Tw in enumerate(T_WALL):
        if reg[(0, 0, 0, t)].startswith("boiling"):
            tb = Tw; break
    return cap, tb


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int, default=6); a = ap.parse_args(argv)
    cases = load_cases()
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        caps = list(ex.map(capacity_table, cases))
    rows, curve = [], []
    for c, (cap, tb) in zip(cases, caps):
        dep_a, dep_w = c["film_a"], c["film_w"]
        rho = (dep_a + dep_w) / (dep_a / RHO_LIQ[c["fuel"]] + dep_w / RHO_LIQ["H2O"]) if dep_a + dep_w > 0 else 1000.0
        for m in FILM_MULT:
            da, dw = m * dep_a, m * dep_w
            for i, Tg in enumerate(T_PLENUM):
                for j, L in enumerate(L_WET):
                    A = math.pi * 0.035 * L
                    delta_um = 1e6 * (da + dw) / rho / A
                    for k, h in enumerate(H_FILM):
                        ca, cw = cap[i, j, k, :, 0], cap[i, j, k, :, 1]
                        fa = np.where(da > 0, np.minimum(1.0, ca / max(da, 1e-30)), 1.0)
                        fw = np.where(dw > 0, np.minimum(1.0, cw / max(dw, 1e-30)), 1.0)
                        ftot = (fa * da + fw * dw) / (da + dw) if da + dw > 0 else np.ones_like(ca)
                        xmax = 1.0 - ftot
                        for smd in SMDS:
                            xc = c["xcrit"].get(smd)
                            reach = np.zeros_like(xmax, bool) if xc is None else xmax >= xc
                            if not reach.any():
                                Tstar, nonmono = T_WALL[0], False   # never reachable on grid
                                code = "never"
                            elif reach[-1]:
                                Tstar, nonmono, code = None, False, "reachable at 440 K"
                            else:
                                last = int(np.nonzero(reach)[0].max())
                                Tstar = T_WALL[last + 1]
                                nonmono = bool((~reach[:last]).any())
                                code = "boundary"
                            rows.append(dict(case=c["case"], atomiser=c["atomiser"], variant=c["variant"], fuel=c["fuel"],
                                             film_mult=m, film_deposit_mg=1e6 * (da + dw), film_thickness_um=delta_um,
                                             T_plenum_K=Tg, L_wet_m=L, h_film_W_m2K=h, SMD_um=smd,
                                             x_crit=xc, T_bubble_film_K=tb, T_boundary_K=Tstar, boundary=code,
                                             non_monotone=nonmono,
                                             **{f"reach_{n.split()[0]}": bool(reach[int(np.argmin(np.abs(np.array(T_WALL) - Tw)))]) and xc is not None
                                                for n, Tw in REG_PTS.items()}))
                            curve.append(reach)
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "film_map_cases.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    # aggregate: fraction of the 84 cases reachable vs T_wall, per (film_mult, T_plenum, L, h, SMD)
    agg = []
    curve = np.array(curve).reshape(len(cases), len(FILM_MULT), len(T_PLENUM), len(L_WET), len(H_FILM), len(SMDS), len(T_WALL))
    for a_, m in enumerate(FILM_MULT):
        for i, Tg in enumerate(T_PLENUM):
            for j, L in enumerate(L_WET):
                for k, h in enumerate(H_FILM):
                    for s, smd in enumerate(SMDS):
                        n = curve[:, a_, i, j, k, s, :].sum(axis=0)
                        allsafe = next((T_WALL[t] for t in range(len(T_WALL)) if n[t:].sum() == 0), None)
                        half = next((T_WALL[t] for t in range(len(T_WALL)) if (n[t:] <= len(cases) / 2).all()), None)
                        agg.append(dict(film_mult=m, T_plenum_K=Tg, L_wet_m=L, h_film_W_m2K=h, SMD_um=smd,
                                        n_cases=len(cases), n_reach_363=int(n[T_WALL.index(363.15)]), n_reach_388=int(n[T_WALL.index(388.15)]), n_reach_420=int(n[T_WALL.index(420.0)]),
                                        T_all_safe_K=allsafe, T_half_safe_K=half,
                                        n_reach_vs_T=" ".join(str(int(x)) for x in n)))
    with (OUT / "film_map_boundary.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(agg[0])); w.writeheader(); w.writerows(agg)
    json.dump(dict(status="executed estimate; NOT verified (no second engine), NOT validated",
                   axes=dict(T_wall_K=[T_WALL[0], T_WALL[-1], 1.0], L_wet_m=L_WET, h_film_W_m2K=H_FILM,
                             film_mult=FILM_MULT, T_plenum_K=T_PLENUM, SMD_um=SMDS), n_cases=len(cases)),
              (OUT / "meta.json").open("w"), indent=1)
    print("rows", len(rows), "agg", len(agg))


if __name__ == "__main__":
    main()
