import sys, json, math, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, "verification/x5_m03"); sys.path.insert(0, ".")
import gci_study as g
x5, fake = g.load_x5(); m = g.load_m03()
ch5 = x5.Charge("CH3OH", 16, 0.0, 320.0); ch3 = m.Charge("CH3OH", 16, 0.0, 320.0)
def scal(o):
    return {k: float(v) for k, v in vars(o).items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
a, b = scal(ch5), scal(ch3)
print("X5 attrs:", a); print("M03 attrs:", b)
for k in sorted(set(a) & set(b)):
    if b[k] != 0: print(f"{k:24s} X5 {a[k]:.8g}  M03 {b[k]:.8g}  rel {(a[k]-b[k])/b[k]*100:+.4f}%")
import numpy as np
s5 = ch5.state(ch5.U_ivc, ch5.V_ivc, x5.wiebe(x5.IVC, x5.CA50, 25*x5.RAD), 0.0, (320.0, 1e5))
s3 = ch3.state(ch3.U_ivc, ch3.V_ivc, m.wiebe(m.DEFAULTS.ivc_rad, 14*m.RAD, 25*m.RAD, m.DEFAULTS), 0.0, (320.0, 1e5))
print("IVC T,p,n,mass X5", s5["T"], s5["p"], s5["n"], s5["mass"]); print("IVC T,p,n,mass M03", s3["T"], s3["p"], s3["n"], s3["mass"])
names = ch3.ph.gas.species_names if hasattr(ch3.ph, "gas") else None
print("names", names[:3] if names else None, len(s3["masses"]), len(s5["masses"]))
d = np.array(s5["masses"]) - np.array(s3["masses"])
for i in np.argsort(-abs(d))[:6]: print(names[i] if names else i, s5["masses"][i], s3["masses"][i])
print("X5 resid frac", getattr(x5, "R_RESID", None), " M03 resid", m.DEFAULTS.residual_fraction if hasattr(m.DEFAULTS, "residual_fraction") else [k for k in vars(m.DEFAULTS) if "resid" in k])
dur = 25 * m.RAD; ca = 14 * m.RAD; st = 0.5 * m.RAD
for wall in (True, False):
    r5 = x5.integrate(ch5, ca, dur, None, step=st, wall=wall)
    r3 = m.integrate_cycle(ch3, ca, dur, None, step_rad=st, wall=wall, track_no=False)
    print("wall", wall, "X5 keys", sorted(r5)[:30])
    print("  eff X5 %.6f M03 %.6f rel %+.4f%%" % (r5["eff"], r3["gross_indicated_efficiency"], (r5["eff"]/r3["gross_indicated_efficiency"]-1)*100))
    for k5, k3 in (("Qw", "wall_heat_J"), ("W", "indicated_work_J"), ("released", "released_energy_J"), ("TEVO", "EVO_T_K"), ("pmax", "peak_pressure_Pa")):
        if k5 in r5: print(f"  {k5:9s} X5 {r5[k5]:.6g}  M03 {r3[k3]:.6g}  rel {(r5[k5]/r3[k3]-1)*100 if r3[k3] else 0:+.4f}%")
