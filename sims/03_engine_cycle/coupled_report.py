"""Item B report: results/03_engine_cycle/coupled_comparison.{csv,md} from the coupled runs.

Inputs: results/03_engine_cycle/coupled/coupled_points.csv (Module 03, this branch) and
results/engines/m03_cantera/compare_coupled.csv (M03-CRN two-engine check).
Status: executed + cross-checked by 2 engines where the CRN row is within tolerance;
NOT validated against experiment.
"""
import csv
import json
import math
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "results" / "03_engine_cycle" / "coupled" / "coupled_points.csv"
CRN = REPO / "results" / "engines" / "m03_cantera" / "compare_coupled.csv"
OUT = REPO / "results" / "03_engine_cycle"
MATCH_PP = 0.5          # |d_eta| <= 0.5 pp counts as "match"
T_LIMIT = 1500.0        # Module 03 limit_flame_temperature_K (ignition/misfire screen)
E_NO = 38370.0          # Zeldovich N2 + O -> NO + N activation temperature [K]
E_NO_TOT = 69090.0      # initial NO rate incl. O/O2 equilibrium, Heywood (1988) eq. 11.8: 6e16 T^-0.5 exp(-69090/T) [O2]^0.5 [N2]


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def eligible(r):
    return (r["status"] == "computed" and r["knock"] == "False" and r["knock_limited"] == "False"
            and fnum(r["ca50_used_deg"]) <= 15 + 1e-9 and fnum(r["S_L_m_s"]) >= 0.08
            and fnum(r["peak_pressure_Pa"]) <= 120e5 and abs(fnum(r["energy_closure_error_fraction"])) <= 0.02)


def main():
    rows = list(csv.DictReader(open(SRC)))
    crn = {}
    if CRN.exists():
        for t in csv.DictReader(open(CRN)):
            crn[(t["regime"], t["kind"], t["fuel"], t["CR"], t["w"], t["T_intake_K"], t["atomiser"], t["variant"],
                 t["bound"])] = t
    key = lambda r: (r["regime"], r["kind"], r["fuel"], r["CR"], r["w"], r["T_intake_K"], r["atomiser"],
                     r["variant"], r["bound"])
    dry = {}
    for r in rows:
        if r["kind"] == "dry" and r["status"] == "computed":
            dry[(r["regime"], r["fuel"], r["CR"], r["T_intake_K"])] = r
    best_dry = {}
    for (reg, fuel, cr, T), r in dry.items():
        if eligible(r):
            b = best_dry.get((reg, fuel))
            if b is None or fnum(r["gross_indicated_efficiency"]) > fnum(b["gross_indicated_efficiency"]):
                best_dry[(reg, fuel)] = r
    ref_dry = {}  # no SPEC-eligible dry point: best knock-free dry, CA50 limit relaxed (information only)
    for (reg, fuel, cr, T), r in dry.items():
        if (reg, fuel) in best_dry or r["knock_limited"] == "True" or r["knock"] == "True":
            continue
        b = ref_dry.get((reg, fuel))
        if b is None or fnum(r["gross_indicated_efficiency"]) > fnum(b["gross_indicated_efficiency"]):
            ref_dry[(reg, fuel)] = r
    out = []
    for r in rows:
        if r["kind"] not in ("coupled", "legacy"):
            continue
        d = dry.get((r["regime"], r["fuel"], r["CR"], r["T_intake_K"]))
        bd = best_dry.get((r["regime"], r["fuel"]))
        c = crn.get(key(r), {})
        eta = fnum(r["gross_indicated_efficiency"])
        o = dict(regime=r["regime"], fuel=r["fuel"], point=r["point"], kind=r["kind"], atomiser=r["atomiser"],
                 variant=r["variant"], bound=r["bound"] or "legacy", CR=r["CR"], w=r["w"], T_intake_K=r["T_intake_K"],
                 chamber_wall_K=r["chamber_wall_K"], port_wall_K=r["port_wall_K"], coolant_K=r["coolant_K"],
                 status=r["status"], eligible=eligible(r) if r["status"] == "computed" else False,
                 eta=eta, ca50_deg=fnum(r["ca50_used_deg"]), knock_limited=r["knock_limited"],
                 knock_integral=fnum(r["knock_integral_at_xb90"]), S_L_m_s=fnum(r["S_L_m_s"]),
                 burn_10_90_deg=fnum(r["burn_10_90_deg"]), pmax_bar=(fnum(r["peak_pressure_Pa"]) or 0) / 1e5,
                 Tmax_K=fnum(r["peak_temperature_K"]), Tb_K=fnum(r["peak_burned_temperature_K"]),
                 T_ad_K=fnum(r["peak_flame_temperature_K"]),
                 ignition_margin_K=(fnum(r["peak_flame_temperature_K"]) - T_LIMIT)
                 if fnum(r["peak_flame_temperature_K"]) else None,
                 wall_heat_frac=(fnum(r["wall_heat_J"]) / fnum(r["fuel_energy_J"])) if r["status"] == "computed" else None,
                 NO_per_J=fnum(r["NO_mol_per_J_fuel"]),
                 liquid_frac_spark=fnum(r.get("liquid_fraction_spark")), port_evap_frac=fnum(r.get("port_evap_fraction")),
                 port_limit=r.get("port_limit", ""), liquid_sink_J=fnum(r.get("liquid_sink_J")),
                 closure=fnum(r["energy_closure_error_fraction"]), caveat=r.get("caveat", ""))
        if d is not None and o["NO_per_J"] is not None and fnum(d["NO_mol_per_J_fuel"]):
            o["NO_rel_same_CR_T"] = o["NO_per_J"] / fnum(d["NO_mol_per_J_fuel"])
            tbw, tbd = o["Tb_K"], fnum(d["peak_burned_temperature_K"])
            o["Tb_dry_K"] = tbd
            o["zeldovich_ratio_Tb"] = math.exp(-E_NO * (1 / tbw - 1 / tbd)) if tbw and tbd else None
            o["heywood_rate_ratio_Tb"] = (math.sqrt(tbd / tbw) * math.exp(-E_NO_TOT * (1 / tbw - 1 / tbd))
                                          if tbw and tbd else None)
        if bd is None and (r["regime"], r["fuel"]) in ref_dry:
            bd = ref_dry[(r["regime"], r["fuel"])]
            o["best_dry_is_reference_only"] = True
        if bd is not None:
            o.update(best_dry_key=f"CR{bd['CR']}/T{float(bd['T_intake_K']):.0f}",
                     best_dry_eta=fnum(bd["gross_indicated_efficiency"]),
                     d_eta_vs_best_dry_pp=100 * (eta - fnum(bd["gross_indicated_efficiency"])) if eta else None)
        if c:
            o.update(eta_crn=fnum(c.get("eta_crn")), d_eta_crn_pp=fnum(c.get("d_eta_pp")),
                     d_pmax_crn=fnum(c.get("d_pmax_rel")), crn_within_tol=c.get("within_tol"),
                     crn_status=c.get("crn_status"))
        else:
            o.update(crn_within_tol="not run")
        out.append(o)
    cols = []
    for o in out:
        cols += [k for k in o if k not in cols]
    out.sort(key=lambda o: (o["fuel"], o["point"], o["atomiser"], o["variant"], o["bound"], o["regime"]))
    with open(OUT / "coupled_comparison.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(out)
    write_md(out, best_dry, rows, ref_dry)


def verdict(o):
    if o["status"] != "computed" or o["eta"] is None:
        return "NO (failed)"
    d = o.get("d_eta_vs_best_dry_pp")
    if d is None:
        return "n/a"
    if o.get("best_dry_is_reference_only"):
        tag = "beats" if d > MATCH_PP else ("matches" if d >= -MATCH_PP else "no")
        return f"NO (no SPEC-eligible dry point in this regime; wet {'eligible' if o['eligible'] else 'also ineligible'}; {tag} on eta vs best knock-free dry)"
    tag = "BEATS" if d > MATCH_PP else ("MATCHES" if d >= -MATCH_PP else "NO")
    if not o["eligible"]:
        return f"NO (ineligible: {'knock-limited CA50 %.0f' % o['ca50_deg'] if o['knock_limited'] == 'True' or o['ca50_deg'] > 15 else 'limits'}; {tag.lower()} on eta)"
    return tag


def f(x, fmt):
    return "-" if x is None or x == "" else fmt % x


def write_md(out, best_dry, rows, ref_dry):
    L = []
    A = L.append
    chk = json.loads((REPO / "results" / "03_engine_cycle" / "coupled" / "module06_budget_check.json").read_text())
    crn_sum = {}
    p = REPO / "results" / "engines" / "m03_cantera" / "compare_coupled.json"
    if p.exists():
        crn_sum = json.loads(p.read_text())["summary"]
    A("# Module 03 coupled retained-liquid / wall-film comparison (item B, 2026-10-24)\n")
    A("Status: **executed** (Module 03, this branch) and **cross-checked by a second engine** (M03-CRN, "
      "evap_mode=\"coupled\") where marked; **not validated against experiment**.\n")
    A("Generated by `sims/03_engine_cycle/coupled_dual_temp.py` + `coupled_report.py`; CRN check by "
      "`engines/m03_cantera/compare_coupled.py`. Full rows: `coupled_comparison.csv`, "
      "`coupled/coupled_points.csv`.\n")
    A("## Physics\n")
    A("- Airborne liquid at spark (Module 09 `liquid_spark_pct`) stays liquid: excluded from the unburned gas, "
      "vaporised into the burned zone at the burn rate (u_fg + sensible). Evaporation from the charge stops at "
      "min(spark, first heat release).")
    A("- **Bound (ii) film-carried**: the Module 09 wall film is also liquid at spark (entering as 200-500 um drops). "
      "Module 11 caveat: in that state nearly every case misfires (wme1-spray11 220e3ac); this cycle does not "
      "model misfire, so bound (ii) efficiencies are an upper bound conditional on ignition.")
    A("- **Bound (i) port-evaporated**: the film evaporates off the port wall before IVC, capped by the Module 06 "
      "exhaust-heat surplus after the air + fuel heating it already pays for, by the port-wall film capacity "
      "(wme1-hiT, L_wet 0.05 m, h_film 3e4 W/m2K) and by saturation at T_intake; excess stays as bound-(ii) liquid. "
      "Fixed point on the EVO state.")
    A(f"- Module 06 budget formula check (CH3OH CR24/w0.6/T360, legacy): recovered {chk['recovered_kW']:.3f} kW "
      f"(Module 06: 4.61), upstream need {chk['need_kW']:.3f} kW (Module 06: 2.02).")
    A("- flame_T fix: the 32b6350 debit used gas formation enthalpy h_ref with a kg/cycle liquid mass (mixed U/H "
      "bases, all water counted in Yc); restored to the per-kg-fuel H basis (1-e) m_w h_latent with the "
      "water vapour in the products.\n")
    A("Regimes (wme1-hiT `sims/dual_temp/regimes.py`, `docs/DUAL_TEMPERATURE_RULE.md` PR #5; MAHLE/VW SSP 222, "
      "SAE 960271, Heywood 1988 ch. 12): **normal** coolant 363.15 K / chamber wall 450 K / port wall 363.15 K / "
      "T_intake = design value (320 or 360 K); **hot** 388.15 / 520 / 388.15 / T_intake 400 K (Module 09 "
      "fractions of the design point reused; Module 09 was not rerun at 400 K).\n")
    A("Best dry is re-selected per regime from a dry CR 9-24 sweep (normal T_intake 320/360, hot 400) with the "
      "SPEC eligibility (knock-free at CA50 <= 15 CAD, S_L >= 0.08 m/s, p_max <= 120 bar, closure <= 2 %).\n")
    for (reg, fuel), b in sorted(best_dry.items()):
        A(f"- best dry {fuel} {reg}: CR {b['CR']}, T_intake {float(b['T_intake_K']):.0f} K, "
          f"eta {float(b['gross_indicated_efficiency']):.4f}, CA50 {float(b['ca50_used_deg']):.0f}, "
          f"p_max {float(b['peak_pressure_Pa']) / 1e5:.1f} bar")
    for (reg, fuel), b in sorted(ref_dry.items()):
        A(f"- **no SPEC-eligible dry point for {fuel} {reg}** (every knock-free CR needs CA50 > 15 CAD). Reference "
          f"only: best knock-free dry CR {b['CR']}, eta {float(b['gross_indicated_efficiency']):.4f}, CA50 "
          f"{float(b['ca50_used_deg']):.0f}, p_max {float(b['peak_pressure_Pa']) / 1e5:.1f} bar")
    A("")
    A("## Verdict: does water-majority (w > 0.5) match (|d_eta| <= 0.5 pp) or beat best-dry in BOTH bounds?\n")
    A("| fuel | regime | atomiser | variant | eta bound (i) | eta bound (ii) | best dry | d (i) pp | d (ii) pp | (i) | (ii) | both bounds | CRN agrees |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    summary = {}
    for fuel in ("CH3OH", "C2H5OH"):
        for reg in ("normal", "hot"):
            for a in ("carb_venturi", "ultrasonic_120kHz"):
                for v in ("nominal", "cfd_matched"):
                    sel = {o["bound"]: o for o in out if o["fuel"] == fuel and o["regime"] == reg and
                           o["point"] == "water_majority" and o["atomiser"] == a and o["variant"] == v}
                    oi, oii = sel.get("i"), sel.get("ii")
                    if not oi or not oii:
                        continue
                    vi, vii = verdict(oi), verdict(oii)
                    ok = vi in ("BEATS", "MATCHES") and vii in ("BEATS", "MATCHES")
                    summary.setdefault((fuel, reg), []).append(ok)
                    agree = "yes" if str(oi.get("crn_within_tol")) == "True" and str(oii.get("crn_within_tol")) == "True" \
                        else f"no/(i) {oi.get('crn_within_tol')}, (ii) {oii.get('crn_within_tol')}"
                    A(f"| {fuel} | {reg} | {a} | {v} | {f(oi['eta'], '%.4f')} | {f(oii['eta'], '%.4f')} | "
                      f"{f(oi.get('best_dry_eta'), '%.4f')} | {f(oi.get('d_eta_vs_best_dry_pp'), '%+.2f')} | "
                      f"{f(oii.get('d_eta_vs_best_dry_pp'), '%+.2f')} | {vi} | {vii} | {'YES' if ok else 'NO'} | {agree} |")
    A("")
    A("Summary per fuel and temperature (all 4 atomiser/variant cases):\n")
    for (fuel, reg), oks in summary.items():
        A(f"- {fuel} {reg}: water-majority matches/beats best dry in both bounds in {sum(oks)}/{len(oks)} cases "
          f"-> **{'YES' if all(oks) else ('PARTLY' if any(oks) else 'NO')}**")
    A("")
    A("## Side by side: normal vs hot (all design points)\n")
    A("Ignition margin = adiabatic flame T - 1500 K (Module 03 low-flame-temperature screen; bound (ii) also carries "
      "the Module 11 misfire caveat). Burn rate: S_L (Module 02) and 10-90 % duration; liquid does not change S_L "
      "in this model (caveat). NOx: NO per J fuel, and relative to the dry point at the same CR/T/regime.\n")
    A("| fuel | point | atomiser/variant | bound | eta N | eta H | CA50 N/H | knock-lim N/H | S_L N/H m/s | 10-90 N/H | "
      "p_max N/H bar | T_max N/H K | T_ad margin N/H K | wall heat N/H % | NO/J N/H | NO_rel N/H | liquid@spark N/H | port evap N/H |")
    A("|" + "---|" * 18)
    idx = {(o["fuel"], o["point"], o["atomiser"], o["variant"], o["bound"], o["regime"]): o for o in out}
    seen = []
    for o in out:
        k = (o["fuel"], o["point"], o["atomiser"], o["variant"], o["bound"])
        if k in seen:
            continue
        seen.append(k)
        n, h = idx.get(k + ("normal",)), idx.get(k + ("hot",))
        if not n or not h:
            continue
        pair = lambda key, fmt, s=1.0: f"{f(n[key] * s if n[key] is not None else None, fmt)} / {f(h[key] * s if h[key] is not None else None, fmt)}"
        A(f"| {o['fuel']} | {o['point']} | {(o['atomiser'] + '/' + o['variant']) if o['atomiser'] else 'legacy schedule'} | "
          f"{o['bound']} | {f(n['eta'], '%.4f')} | {f(h['eta'], '%.4f')} | {pair('ca50_deg', '%.0f')} | "
          f"{n['knock_limited']}/{h['knock_limited']} | {pair('S_L_m_s', '%.3f')} | {pair('burn_10_90_deg', '%.1f')} | "
          f"{pair('pmax_bar', '%.1f')} | {pair('Tmax_K', '%.0f')} | {pair('ignition_margin_K', '%.0f')} | "
          f"{pair('wall_heat_frac', '%.1f', 100)} | {pair('NO_per_J', '%.2e')} | {pair('NO_rel_same_CR_T', '%.2e')} | "
          f"{pair('liquid_frac_spark', '%.3f')} | {pair('port_evap_frac', '%.3f')} |")
    A("")
    hot_better = [(k, idx[k + ("hot",)]["eta"] > idx[k + ("normal",)]["eta"]) for k in seen
                  if k + ("hot",) in idx and k + ("normal",) in idx and idx[k + ("hot",)]["eta"] and idx[k + ("normal",)]["eta"]]
    A(f"**Does hot give better efficiency?** Hot eta > normal eta in {sum(b for _, b in hot_better)}/{len(hot_better)} "
      "design-point cases (same CR; hot also raises T_intake to 400 K, which lowers trapped mass and raises knock).\n")
    bd_n = {f_: best_dry.get(("normal", f_)) for f_ in ("CH3OH", "C2H5OH")}
    bd_h = {f_: best_dry.get(("hot", f_)) or ref_dry.get(("hot", f_)) for f_ in ("CH3OH", "C2H5OH")}
    for f_ in ("CH3OH", "C2H5OH"):
        if bd_n[f_] and bd_h[f_]:
            A(f"- {f_} best dry: normal {float(bd_n[f_]['gross_indicated_efficiency']):.4f} vs hot "
              f"{float(bd_h[f_]['gross_indicated_efficiency']):.4f}"
              f"{' (reference only, CA50 %.0f, not SPEC-eligible)' % float(bd_h[f_]['ca50_used_deg']) if ('hot', f_) not in best_dry else ''}")
    A("")
    A("## Two-engine check (M03-CRN)\n")
    if crn_sum:
        A(f"Rows {crn_sum['n']}, CRN ok {crn_sum['n_ok']}, all within C1 tolerance "
          f"(|d_eta| <= {crn_sum['tolerance']['eta_pp']} pp, |d_pmax| <= {100 * crn_sum['tolerance']['pmax_rel']:.0f} %): "
          f"**{crn_sum['all_within_tol']}**; max |d_eta| {crn_sum['max_abs_d_eta_pp']:.3f} pp, max |d_pmax| "
          f"{100 * crn_sum['max_abs_d_pmax_rel']:.2f} %.\n")
        A("Shared between the engines (problem definition, not cross-checked): trapped masses, T_IVC and the "
          "intake/port-evaporated fraction from the Module 03 row, the Module 09 schedule, CA50 (Module 03 "
          "knock retard) and 10-90 duration. Independent: thermo, the cycle integrator, wall heat implementation, "
          "liquid sink formulation (CRN single-zone, H2O(g) inflow at the burn rate). Knock, NO and flame "
          "temperature are Module 03 only.\n")
    else:
        A("Not run.\n")
    A("## Water-majority NO_rel ~ 1e-5: explanation\n")
    wm = [o for o in out if o["point"] == "water_majority" and o.get("NO_rel_same_CR_T")]
    if wm:
        A("| fuel | regime | case | bound | T_b wet K | T_b dry K | NO_rel | exp(-38370/T) ratio | Heywood 11.8 rate ratio |")
        A("|---|---|---|---|---|---|---|---|---|")
        for o in wm:
            A(f"| {o['fuel']} | {o['regime']} | {o['atomiser'] or 'legacy'}/{o['variant']} | {o['bound']} | "
              f"{f(o['Tb_K'], '%.0f')} | {f(o.get('Tb_dry_K'), '%.0f')} | {f(o['NO_rel_same_CR_T'], '%.2e')} | "
              f"{f(o.get('zeldovich_ratio_Tb'), '%.2e')} | {f(o.get('heywood_rate_ratio_Tb'), '%.2e')} |")
    A("")
    A("NO_rel is NO per J of fuel at the wet point divided by NO per J of fuel at the dry point with the same "
      "CR, T_intake and regime. T_b is the peak burned-zone temperature. The ~1e-5 for methanol water-majority (legacy "
      "schedule 1.26e-5; coupled bound (ii) 1.0e-5 to 7.9e-5) is a temperature effect, not a bug. At w = 0.6 the "
      "water's latent heat and its heat capacity as a diluent lower T_b from about 2470-2520 K (dry) to about 1800-1910 K. "
      "Thermal NO is controlled by N2 + O -> NO + N (activation temperature 38370 K), and the O-atom "
      "concentration is itself in equilibrium with O2 (another ~31000 K). So the initial NO formation rate goes as "
      "T^-0.5 exp(-69090/T) [O2]^0.5 [N2] (Heywood 1988, eq. 11.8). On peak T_b alone that predicts "
      "3.3e-5 for the methanol legacy row (computed 1.26e-5) and about 1-2e-4 for coupled bound (ii) (computed "
      "1.0e-5 to 7.9e-5). The rest of the suppression (a factor of about 0.4 for legacy and 0.1-0.6 for bound (ii)) comes "
      "from lower O2/N2 mole fractions (dilution by water vapour), a shorter time near peak T, and in bound (ii) "
      "the liquid sink cooling the burned zone while it is still hot. The bare 38370 K exponent (about 3e-3 to 8e-3) "
      "misses the suppression by 2-3 orders, so it is not the right yardstick. "
      "Ethanol water-majority runs hotter (T_b 1980-2100 K), so NO_rel is about 3e-4 to 2e-3. Bound (i) "
      "evaporates the film upstream, which also leaves a hotter charge (higher T_b) and gives NO_rel 1e-4 to 2e-2. "
      "This is executed only: the NO is Module 03 Zeldovich in the burned zone, not cross-checked by "
      "M03-CRN and not validated against experiment.\n")
    A("## Caveats\n")
    A("- Not validated against experiment. Bound (ii) misfire (Module 11) is not modelled; burn rate (S_L) is "
      "not reduced by liquid. Hot regime reuses the Module 09 fractions of the 320/360 K design point. "
      "Port-wall capacity data (wme1-hiT) is executed, not verified. Best dry is re-selected per regime but the "
      "wet points are the normal-regime design points (CR/w), not re-optimised.")
    (OUT / "coupled_comparison.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
