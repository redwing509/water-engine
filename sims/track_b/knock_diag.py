"""Diagnosis of the knock-engine-2 validation miss (job 1520 step 3: end-gas klCR PRF91 12.0 vs M03 10.0,
PRF97 13.5 vs 11.0; tolerance 1.5 CR).  Box queue job, Grok Bot, Oct 25 2026.  No blind retry: this does NOT
re-run the failed validation; it measures WHICH physical modelling difference produces the gap.

Fact established before this job (validate_m03_rows.jsonl): Module 03 is a Livengood-Wu integral with the
Douaud-Eyzat 1978 correlation (tau = 17.68 ms (ON/100)^3.402 p^-1.7 exp(3800/T)); its spark is retarded until
the LW integral = 1 at xb 0.90 and a point is eligible iff that CA50 <= 15.  At PRF91 CR 12 M03 needs CA50 20.3,
while the end-gas engine (CRECK full LT chemistry, single homogeneous adiabatic mean-cycle parcel) sees no knock
at CA50 15.  So at identical p(theta), T(theta) the two engines disagree on end-gas ignition timing.
Hypotheses tested (each a separate, labelled sweep; nothing is tuned and adopted here):
  H1 chemistry: CRECK constant-volume IDT vs Douaud-Eyzat tau at end-gas states (idt).
  H2 thermal stratification / hot spots: a homogeneous mean parcel misses hot spots; T0 offset sweep
     dT = 0,10,20,30,40 K -> equivalent hot-spot dT that would close the gap per fuel (offsets).
  H3 cycle-to-cycle variation: knock limits are set by the fast cycles; CA50 advanced 3 and 6 CAD (offsets, ca50).
  H4 criterion: dT/dt>1e7 / X_OH>1e-3 vs LW=1 (reported from max_dTdt / max_X_OH margins in the same rows).
Both regimes (normal + hot).  Status: EXECUTED, numerically cross-checked, NOT validated.
Usage (cwd = repo):
  python -m sims.track_b.knock_diag m03 REGIME OUT.jsonl N                 PRF91/PRF97 w0 liquid M03 rows, CR 8..15
  python -m sims.track_b.knock_diag offsets M03ROWS.jsonl OUT.jsonl N DT_LIST CA50_LIST
  python -m sims.track_b.knock_diag idt OUT.json
  python -m sims.track_b.knock_diag summary OUTDIR
  python -m sims.track_b.knock_diag split M03ROWS.jsonl OUT.jsonl N CA50|m03 [lw]   (Oct 26, Claude review item 2)
Split mode (mechanism vs method vs CA50 vs parcel): per M03 row, on the SAME CRN p(theta) trace and the SAME
isentropic end-gas path: (a) Livengood-Wu integral with CRECK constant-volume IDT tau (same CRECK LT mechanism as the
end-gas engine; tau at nodes every KD_LW_NODE CAD, log-interpolated; no ignition within KD_TAU_CAP s -> rate 0, upper
bound with 1/cap also reported), (b) the end-gas full-chemistry run (skipped with 'lw'), (c') Douaud-Eyzat LW on the
same path; (c) M03's own LW is the row's knock_integral_at_xb90. CA50 = fixed number, or 'm03' = matched CA50 (the
row's own M03 selection, ca50_used_deg).
LABEL (Claude review Oct 26, Track B): knock engine 2: ranking validated, absolute klCR offset +2-2.5 CR vs M03 (gate
FAILED). Not retuned. A 'knock ok' row means both knock engines are knock-free, NOT two-engine-validated knock.
"""
import gc, json, math, os, sys, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from sims.track_b import chains_sym as CS
from sims.track_b import run as R
from sims.track_b import knock_sym as KS

CRS = (8.0, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 15.0)
FUELS = tuple(os.environ.get("KD_FUELS", "PRF91,PRF97").split(","))  # Oct 26: env override for the other blends
from sims.track_b import fuels_b as _FB
ON = {f: float(_FB.BLENDS[f]["ON"]) for f in _FB.BLENDS}  # cited ON per blend (fuels_b.py); PRF91/97 unchanged


def jl(p):
    return [json.loads(l) for l in open(p) if l.strip()] if Path(p).exists() else []


def _m03(task):
    return CS.point(dict(task, crn=False))


def m03(regime, outp, n):
    done = {(r["fuel"], r["CR"]) for r in jl(outp)}
    tasks = [dict(fuel=f, regime=regime, CR=c, w=0.0, mode="liquid", key=f"{f}|{regime}|{c}")
             for f in FUELS for c in CRS if (f, c) not in done]
    with ProcessPoolExecutor(n, max_tasks_per_child=1) as ex, open(outp, "a") as fh:
        for r in ex.map(_m03, tasks):
            fh.write(json.dumps(r, default=str) + "\n"); fh.flush()


LABEL = ("knock engine 2: ranking validated, absolute klCR offset +2-2.5 CR vs M03 (gate FAILED). Not retuned. "
         "A 'knock ok' row means both knock engines are knock-free, not two-engine-validated knock.")


def lw_creck(tr, th0, th_end, T0, Y0, omega, node_deg=None, cap=None):
    """Livengood-Wu integral with CRECK constant-volume IDT along the isentropic end-gas path from (T0, p(th0))."""
    import cantera as ct
    import engines.m03_cantera.knock as K
    node_deg = float(os.environ.get("KD_LW_NODE", "1.0")) if node_deg is None else node_deg
    cap = float(os.environ.get("KD_TAU_CAP", "0.05")) if cap is None else cap
    g = K.gas(); g.TPY = T0, float(np.interp(th0, tr[:, 0], tr[:, 1])), Y0; s0 = g.entropy_mass
    nodes = list(np.arange(th0, th_end, node_deg * math.pi / 180)) + [th_end]
    rate, ncap = [], 0
    for th in nodes:
        g.SPY = s0, float(np.interp(th, tr[:, 0], tr[:, 1])), Y0
        T = g.T
        rr = ct.IdealGasReactor(g, clone=False); net = ct.ReactorNet([rr]); tig = None  # no per-node mechanism clone (OOM fix 2026-10-26)
        while net.time < cap:
            net.step()
            if rr.T > T + 400: tig = net.time; break
        if tig is None: ncap += 1
        rate.append(None if tig is None else 1.0 / tig)
        del net, rr; gc.collect()
    lw = lwu = 0.0; th1 = None
    for i in range(len(nodes) - 1):
        a, b = rate[i], rate[i + 1]
        dt = (nodes[i + 1] - nodes[i]) / omega
        if a and b:   # log-linear rate between nodes (exact for exponential T dependence)
            seg = dt * (b - a) / math.log(b / a) if abs(b / a - 1) > 1e-9 else dt * a
        else:
            seg = 0.5 * dt * ((a or 0.0) + (b or 0.0))
        segu = 0.5 * dt * ((a or 1.0 / cap) + (b or 1.0 / cap))
        if th1 is None and lw + seg >= 1.0:
            th1 = nodes[i] + (nodes[i + 1] - nodes[i]) * (1.0 - lw) / seg
        lw += seg; lwu += max(segu, seg)
    return dict(LW_CRECK_same_path=lw, LW_CRECK_upper_cap=lwu, LW_CRECK_nodes=len(nodes), LW_CRECK_capped=ncap,
                LW_CRECK_node_deg=node_deg, LW_CRECK_tau_cap_s=cap,
                theta_LW_CRECK_1_deg=None if th1 is None else th1 * 180 / math.pi)


def endgas(r, ca50, dT, full=True, creck=False):
    import engines.m03_cantera.knock as K
    E = R.crn_engine()
    credit = float(r.get("fuel_evap_intake_fraction") or 0.0) + float(r.get("fuel_evap_port_fraction") or 0.0)
    c = E.Case(fuel=r["fuel"], cr=r["CR"], T_ivc=r["T_IVC_K"], m_fuel=r["fuel_mass_kg"], m_air=r["air_mass_kg"],
               m_residual=r["residual_mass_kg"], m_water=r["water_mass_kg"], e_intake=r["f_evap_intake_effective"],
               ca50_deg=ca50, d1090_deg=r["burn_10_90_deg"], wall_T=r["chamber_wall_K"], heat_transfer="woschni",
               sat_blend_frac=R.CRN_SAT_BLEND, fuel_latent_credit=credit)
    eng = E.Engine(c)
    eng.run()
    wb = E.Wiebe(ca50 * E.RAD, r["burn_10_90_deg"] * E.RAD)
    Y0, dropped = K.endgas_Y(E.build_gas(False), eng.anchor["Y"], KS.split_map())
    th0 = min(E.EVAP_END, wb.start)
    tr = eng.trace
    T0 = float(np.interp(th0, tr[:, 0], tr[:, 2]))
    out = K.run_endgas(tr, wb, Y0, T_override=T0 + dT, theta0=th0, rpm=E.RPM,
                      dtheta_deg=float(os.environ.get("KD_DTHETA", "0.05"))) if full else dict(endgas_run="skipped (lw)")
    # Douaud-Eyzat LW integral on the SAME end-gas path (isentropic from T0 on the CRN pressure trace), H1/H4
    g = K.gas(); g.TPY = T0, float(np.interp(th0, tr[:, 0], tr[:, 1])), Y0
    s0 = g.entropy_mass; th_end = K.theta_xb(wb, 0.90); omega = E.RPM * 2 * math.pi / 60.0
    lw, th, d, thde = 0.0, th0, 0.25 * math.pi / 180, None
    while th < th_end:
        p = float(np.interp(th, tr[:, 0], tr[:, 1])); g.SPY = s0, p, Y0
        tau = 17.68e-3 * (ON[r["fuel"]] / 100.0) ** 3.402 * (p / 101325.0) ** -1.7 * math.exp(3800.0 / (g.T + dT))
        lw += d / omega / tau; th += d
        if thde is None and lw >= 1.0: thde = th
    out.update(LW_DE_at_xb90_same_path=lw)
    if creck:
        out.update(theta_LW_DE_1_deg=None if thde is None else thde * 180 / math.pi, theta0_deg=th0 * 180 / math.pi,
                   theta_xb90_deg=th_end * 180 / math.pi, T0_K=T0)
        out.update(lw_creck(tr, th0, th_end, T0 + dT, Y0, omega))
    return out


def _eg(a):
    r, ca50, dT = a
    base = {k: r.get(k) for k in ("fuel", "regime", "CR", "eligible", "ca50_used_deg", "knock_integral_at_xb90")}
    base.update(ca50_test=ca50, dT_K=dT)
    t = time.time()
    try:
        base.update(endgas(r, ca50, dT)); base["status"] = "ok"
    except Exception as exc:  # recorded once, never retried
        base["status"] = f"failed: {type(exc).__name__}: {exc}"
    base["seconds"] = time.time() - t
    return base


def _sp(a):
    r, ca50, full = a
    c = r["ca50_used_deg"] if ca50 == "m03" else float(ca50)
    base = {k: r.get(k) for k in ("fuel", "regime", "CR", "eligible", "ca50_used_deg", "knock_integral_at_xb90")}
    base.update(ca50_test=c, ca50_mode="matched_m03" if ca50 == "m03" else "fixed", dT_K=0.0, full_endgas=full)
    t = time.time()
    try:
        base.update(endgas(r, c, 0.0, full=full, creck=True)); base["status"] = "ok"
    except Exception as exc:  # recorded once, never retried
        base["status"] = f"failed: {type(exc).__name__}: {exc}"
    base["seconds"] = time.time() - t
    return base


def split(rowsp, outp, n, ca50, full=True, crs=None):
    rows = [r for r in jl(rowsp) if r.get("status") == "computed" and r["fuel"] in FUELS and (not crs or r["CR"] in crs)]
    done = {(x["fuel"], x["CR"]) for x in jl(outp)}
    tasks = [(r, ca50, full) for r in rows if (r["fuel"], r["CR"]) not in done]
    print(f"split: {len(tasks)} rows, CA50 {ca50}, end-gas {'full' if full else 'skipped'}", flush=True)
    with ProcessPoolExecutor(n, max_tasks_per_child=1) as ex, open(outp, "a") as fh:
        for x in ex.map(_sp, tasks):
            fh.write(json.dumps(x, default=str) + "\n"); fh.flush()
            print(x["fuel"], x["regime"], x["CR"], round(x["ca50_test"], 2), "LW M03/DE/CRECK",
                  x.get("knock_integral_at_xb90") and round(x["knock_integral_at_xb90"], 2),
                  x.get("LW_DE_at_xb90_same_path") and round(x["LW_DE_at_xb90_same_path"], 2),
                  x.get("LW_CRECK_same_path") and round(x["LW_CRECK_same_path"], 2), "knock", x.get("knock"),
                  x["status"][:60], f"{x['seconds']:.0f}s", flush=True)


def offsets(rowsp, outp, n, dts, ca50s):
    rows = [r for r in jl(rowsp) if r.get("status") == "computed"]
    done = {(x["fuel"], x["CR"], x["ca50_test"], x["dT_K"]) for x in jl(outp)}
    tasks = [(r, c, d) for c in ca50s for d in dts for r in rows if (r["fuel"], r["CR"], c, d) not in done]
    print(f"{len(tasks)} end-gas runs", flush=True)
    with ProcessPoolExecutor(n, max_tasks_per_child=1) as ex, open(outp, "a") as fh:
        for x in ex.map(_eg, tasks):
            fh.write(json.dumps(x, default=str) + "\n"); fh.flush()
            print(x["fuel"], x["regime"], x["CR"], x["ca50_test"], x["dT_K"], x.get("knock"), x["status"],
                  f"{x['seconds']:.0f}s", flush=True)


def idt(outp):
    import cantera as ct
    import engines.m03_cantera.knock as K
    g = K.gas(); res = []
    sp = KS.split_map()
    for f in FUELS:
        for P_bar in (20.0, 40.0, 60.0):
            for T in (700.0, 750.0, 800.0, 850.0, 900.0, 950.0, 1000.0):
                x = {}
                g.set_equivalence_ratio(1.0, sp[f], "O2:1, N2:3.76", basis="mass")
                g.TP = T, P_bar * 1e5
                rr = ct.IdealGasReactor(g, clone=True); net = ct.ReactorNet([rr]); T0 = rr.T; tig = None
                while net.time < 0.2:
                    net.step()
                    if rr.T > T0 + 400: tig = net.time; break
                de = 17.68e-3 * (ON[f] / 100.0) ** 3.402 * (P_bar * 1e5 / 101325.0) ** -1.7 * math.exp(3800.0 / T)
                res.append(dict(fuel=f, P_bar=P_bar, T_K=T, tau_creck_s=tig, tau_DE_s=de,
                                ratio=None if tig is None else tig / de))
                print(res[-1], flush=True)
    json.dump(res, open(outp, "w"), indent=1)


def summary(d):
    d = Path(d); md = ["# Knock engine 2 diagnosis (box queue, Oct 25-26 2026) - Track B", "",
                       "Status: EXECUTED, numerically cross-checked, NOT validated. Nothing adopted here.", "",
                       f"**Label: {LABEL}**", ""]
    for g in ("normal", "hot"):
        rows = jl(d / f"offsets_{g}.jsonl")
        m = {(r["fuel"], r["CR"]): r for r in jl(d / f"m03_{g}.jsonl")}
        md.append(f"## {g} regime"); md.append("")
        md.append("| fuel | klCR M03 | CA50 test | dT K | klCR end-gas | diff |"); md.append("|---|---|---|---|---|---|")
        for f in FUELS:
            kl_m = max([c for (ff, c), r in m.items() if ff == f and r.get("eligible")], default=None)
            for c50 in sorted({r["ca50_test"] for r in rows}):
                for dT in sorted({r["dT_K"] for r in rows}):
                    e = sorted([r for r in rows if r["fuel"] == f and r["ca50_test"] == c50 and r["dT_K"] == dT
                                and r["status"] == "ok"], key=lambda r: r["CR"])
                    kl = None
                    for r in e:
                        if r["knock"]: break
                        kl = r["CR"]
                    diff = None if None in (kl, kl_m) else kl - kl_m
                    md.append(f"| {f} | {kl_m} | {c50} | {dT} | {kl} | {diff} |")
        md.append("")
    p = d / "idt_compare.json"
    if p.exists():
        md += ["## H1 CRECK constant-volume IDT / Douaud-Eyzat tau (phi 1, air)", "",
               "| fuel | P bar | T K | tau CRECK ms | tau D-E ms | ratio |", "|---|---|---|---|---|---|"]
        for r in json.load(open(p)):
            md.append(f"| {r['fuel']} | {r['P_bar']} | {r['T_K']} | "
                      f"{'-' if r['tau_creck_s'] is None else round(r['tau_creck_s'] * 1e3, 3)} | "
                      f"{round(r['tau_DE_s'] * 1e3, 3)} | {'-' if r['ratio'] is None else round(r['ratio'], 2)} |")
    md += split_md(d)
    (d / "DIAG.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


def _kl(rows, bad):
    """grid knock-limited CR: highest CR before the first failing CR (ascending)."""
    kl = None
    for r in sorted(rows, key=lambda r: r["CR"]):
        if bad(r): break
        kl = r["CR"]
    return kl


def _cross(rows, key):
    """CR where the LW value crosses 1 (linear in ln LW between grid CRs); None if no crossing."""
    e = sorted([r for r in rows if r.get(key)], key=lambda r: r["CR"])
    for a, b in zip(e, e[1:]):
        if a[key] < 1.0 <= b[key]:
            la, lb = math.log(a[key]), math.log(b[key])
            return a["CR"] + (b["CR"] - a["CR"]) * (0 - la) / (lb - la)
    return None


def split_md(d):
    md = []
    for g in ("normal", "hot"):
        s15 = [r for r in jl(d / f"split15_lw_{g}.jsonl") if r["status"] == "ok"]
        sm = [r for r in jl(d / f"split_m03ca50_{g}.jsonl") if r["status"] == "ok"]
        if not (s15 or sm):
            continue
        off = [r for r in jl(d / f"offsets_{g}.jsonl") if r["status"] == "ok"]
        m = [r for r in jl(d / f"m03_{g}.jsonl") if r.get("status") == "computed"]
        md += [f"## Split: mechanism vs method vs CA50 vs parcel - {g} regime (Track B)", "",
               "klCR on the CR grid (highest CR before the first knocking CR). Path = Douaud-Eyzat (D-E) LW on the CRN "
               "p-trace isentropic end-gas path vs M03's own LW (trace/start-state difference; BOTH models use an "
               "adiabatic isentropic end gas). Mechanism = CRECK-tau LW vs D-E LW on the same path. Method = end-gas full "
               "chemistry vs CRECK-tau LW (LW integral vs two-stage kinetics). CA50 = end-gas klCR at M03's CA50 at its "
               "klCR (interpolated from the CA50 9/12/15 sweeps) minus at CA50 15. Hot spot = smallest homogeneous dT "
               "that brings end-gas klCR down to M03's. LW crossings (continuous CR at LW = 1) in brackets.", "",
               "| fuel | M03 klCR (CA50 there) | D-E same path | CRECK-tau LW | end-gas @15 | path | mechanism | method | "
               "CA50 mismatch | hot-spot dT to close | largest term |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for f in FUELS:
            mf = [r for r in m if r["fuel"] == f]
            if not mf: continue
            klm = max([r["CR"] for r in mf if r.get("eligible")], default=None)
            c50m = next((r["ca50_used_deg"] for r in mf if r["CR"] == klm), None)
            a = [r for r in s15 if r["fuel"] == f]
            kde = _kl(a, lambda r: r["LW_DE_at_xb90_same_path"] >= 1.0) if a else None
            kcr = _kl(a, lambda r: r["LW_CRECK_same_path"] >= 1.0) if a else None
            eg = lambda c50, dT: _kl([r for r in off if r["fuel"] == f and r["ca50_test"] == c50 and r["dT_K"] == dT],
                                     lambda r: r["knock"])
            keg = eg(15.0, 0.0)
            pts = [(c, eg(c, 0.0)) for c in (9.0, 12.0, 15.0) if eg(c, 0.0) is not None]
            kca = None
            if c50m is not None and len(pts) >= 2:
                xs, ys = zip(*pts); kca = float(np.interp(c50m, xs, ys)) - keg if keg is not None else None
            hs = next((dT for dT in sorted({r["dT_K"] for r in off}) if klm is not None
                       and (eg(15.0, dT) or 99) <= klm), None)
            dif = lambda x, y: None if None in (x, y) else x - y
            terms = dict(path=dif(kde, klm), mechanism=dif(kcr, kde), method=dif(keg, kcr), CA50=kca)
            big = max(((k, v) for k, v in terms.items() if v is not None), key=lambda kv: abs(kv[1]), default=("-", None))
            fx = lambda x: "-" if x is None else f"{x:+.2f}"
            cr = lambda k: _cross(a, k)
            md.append(f"| {f} | {klm} ({'-' if c50m is None else round(c50m, 1)}) | {kde} [{fx(cr('LW_DE_at_xb90_same_path'))}] | "
                      f"{kcr} [{fx(cr('LW_CRECK_same_path'))}] | {keg} | {fx(terms['path'])} | {fx(terms['mechanism'])} | "
                      f"{fx(terms['method'])} | {fx(kca)} | {'>' + str(max(r['dT_K'] for r in off)) if hs is None and off else hs} K | "
                      f"{big[0]} |")
        if sm:
            md += ["", f"### Matched CA50 ({g}): every CR at M03's own selection CA50 (M03 LW = 1 at knock-limited rows)", "",
                   "| fuel | CR | M03 CA50 | M03 eligible | LW M03 | LW D-E same path | LW CRECK-tau (upper w/ cap) | "
                   "end-gas knock | theta knock / LW-CRECK=1 deg |", "|---|---|---|---|---|---|---|---|---|"]
            for r in sorted(sm, key=lambda r: (r["fuel"], r["CR"])):
                q = lambda k, f="%.2f": "-" if r.get(k) is None else f % r[k]
                md.append(f"| {r['fuel']} | {r['CR']} | {r['ca50_test']:.1f} | {r['eligible']} | {q('knock_integral_at_xb90')} | "
                          f"{q('LW_DE_at_xb90_same_path')} | {q('LW_CRECK_same_path')} ({q('LW_CRECK_upper_cap')}) | "
                          f"{r.get('knock')} | {q('theta_knock_deg', '%.1f')} / {q('theta_LW_CRECK_1_deg', '%.1f')} |")
            for f in FUELS:
                b = [r for r in sm if r["fuel"] == f and (r.get("knock_integral_at_xb90") or 0) > 0.99]
                if b:
                    md.append(f"\n{f} {g}: at M03's knock-border points (LW_M03 = 1, {len(b)} CRs) the end-gas engine knocks at "
                              f"{sum(1 for r in b if r.get('knock'))}; median LW ratio CRECK/M03 "
                              f"{np.median([r['LW_CRECK_same_path'] for r in b]):.2f}, D-E same path/M03 "
                              f"{np.median([r['LW_DE_at_xb90_same_path'] for r in b]):.2f}.")
        md.append("")
    return md


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "m03":
        m03(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif c == "offsets":
        offsets(sys.argv[2], sys.argv[3], int(sys.argv[4]), [float(x) for x in sys.argv[5].split(",")],
                [float(x) for x in sys.argv[6].split(",")])
    elif c == "idt":
        idt(sys.argv[2])
    elif c == "summary":
        summary(sys.argv[2])
    elif c == "split":
        crs = [float(x) for x in os.environ["KD_CRS"].split(",")] if os.environ.get("KD_CRS") else None
        split(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5] if sys.argv[5] == "m03" else float(sys.argv[5]),
              full=not (len(sys.argv) > 6 and sys.argv[6] == "lw"), crs=crs)
