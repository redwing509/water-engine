import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "verification/x5_m03"); sys.path.insert(0, ".")
import gci_study as g, numpy as np
x5, fake = g.load_x5(); m = g.load_m03(); P = m.DEFAULTS
ch5 = x5.Charge("CH3OH", 16, 0.0, 320.0); ch3 = m.Charge("CH3OH", 16, 0.0, 320.0)
ca, dur = 14 * m.RAD, 25 * m.RAD
for th in (-30, 0, 14, 30, 60):
    print("wiebe", th, x5.wiebe(th*m.RAD, ca, dur), m.wiebe(th*m.RAD, ca, dur, P), " V", x5.volume(th*m.RAD, 16), m.volume(th*m.RAD, 16, P))
V = m.volume(10*m.RAD, 16, P)
for xb in (0.0, 0.3, 0.7, 1.0):
    for dU in (0.0, 600.0, 1200.0):
        s5 = ch5.state(ch5.U_ivc + dU, V, xb, 0.0, (1500.0, 5e6)); s3 = ch3.state(ch3.U_ivc + dU, V, xb, 0.0, (1500.0, 5e6))
        print(f"xb {xb} dU {dU}: T X5 {s5['T']:.3f} M03 {s3['T']:.3f}  p X5 {s5['p']:.6g} M03 {s3['p']:.6g} rel {(s5['p']/s3['p']-1)*100:+.4f}%")
