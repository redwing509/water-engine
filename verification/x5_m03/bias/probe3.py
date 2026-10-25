"""Item 2: the X5 - M03 efficiency gap comes from the sensible-energy reference (u_ref vs h_ref)."""
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "verification/x5_m03"); sys.path.insert(0, ".")
import gci_study as g, cantera as ct
x5, fake = g.load_x5(); m = g.load_m03()
for fuel, cr, w, T in (("CH3OH", 16, 0.0, 320.0), ("C2H5OH", 24, 0.0, 320.0), ("CH3OH", 24, 0.5, 360.0)):
    ch5 = x5.Charge(fuel, cr, w, T); ch3 = m.Charge(fuel, cr, w, T)
    rows = []
    for xb in (0.0, 1.0):
        U5, n5, _ = ch5.evaluate(1000.0, 1e6, xb, 1.0 if w else 0.0)
        U3, n3, _ = ch3.evaluate(1000.0, 1e6, xb, 1.0 if w else 0.0)
        mu, mb = ch3.masses(xb, 1.0 if w else 0.0); n_fr = float((mu + mb) @ ch3.ph.inv_MW)
        rows.append((U3 - U5, n_fr * ct.gas_constant * x5.T_REF))
    dgap = rows[1][0] - rows[0][0]
    print(f"{fuel} CR{cr} w{w}: U_M03-U_X5 at xb=0 {rows[0][0]:.3f} J (n_frozen R T_ref {rows[0][1]:.3f}); at xb=1 {rows[1][0]:.3f} J;"
          f" change over burn {dgap:.3f} J = {dgap/ch3.Q_avail*100:.3f} % of Q_avail")
import numpy as np
ch5 = x5.Charge("CH3OH", 16, 0.0, 320.0); ch3 = m.Charge("CH3OH", 16, 0.0, 320.0)
print("T_REF X5", x5.T_REF, " M03", m.T_REF if hasattr(m, "T_REF") else None)
d = ch5.h_ref - ch3.ph.u_ref  # J/kg per species
rt = ct.gas_constant * x5.T_REF * ch3.ph.inv_MW
names = ch3.ph.gas.species_names
for i in np.argsort(-abs(d - rt))[:5]: print(names[i], "h_ref5-u_ref3", d[i], "R T/M", rt[i], "excess", d[i] - rt[i])
mu0, mb0 = ch3.masses(0, 0); mu1, mb1 = ch3.masses(1, 0)
print("delta n R Tref over burn", float((mu1 + mb1 - mu0 - mb0) @ rt), " excess part", float((mu1 + mb1 - mu0 - mb0) @ (d - rt)))
