"""Track B fuels: gasoline surrogates (PRF), E10, E85 - registration for Module 03 and M03-CRN.

Track B (James's two-track rule, 2026-10-24): start from normal fuels and add water in steps of
<= 0.1 percentage point of water content in the fuel mix, only while each step gives a real
efficiency gain. This module adds the normal fuels that the repository did not have yet.

Surrogates (lumped single pseudo-species, ideal-mixture thermo):
  PRF87, PRF91, PRF97  primary reference fuels, isooctane/n-heptane by volume (ON = vol% isooctane).
                       PRF91 ~ US regular (87 AKI is typically 91-93 RON, Anderson et al. 2012 Fuel 97:585,
                       doi:10.1016/j.fuel.2012.03.017); PRF87 = conservative lower bound for regular;
                       PRF97 ~ US premium (97.4 RON / 92.7 AKI blendstock in Anderson et al. 2012, SAE 2012-01-1274).
  E10                  10 vol% ethanol in PRF91 base; knock ON 96.1 = measured RON of E10 on the 92-RON
                       blendstock (SAE 2012-01-1274, Table via Hoekstra 2025 reproduction).
  E85                  85 vol% ethanol in PRF91 base; knock ON 108.5 (between measured E75 108.1 and neat
                       ethanol ~109, SAE 2012-01-1274) - beyond the PRF scale, an EXTRAPOLATION of Douaud-Eyzat.

Thermo: NASA Glenn coefficients (McBride, Zehe & Gordon 2002, NASA/TP-2002-211556) as shipped in
Cantera's nasa_gas.yaml for C8H18,isooctane / C7H16,n-heptane / C2H5OH; the lumped species' NASA-7
coefficients are the mole-fraction-weighted coefficients (exact for cp, h; entropy of mixing omitted,
which only affects the equilibrium fuel fraction, ~0 in burned gas). Products/air: GRI-Mech 3.0 thermo.
Vaporisation enthalpies (298.15 K, NIST SRD 69): isooctane 35.1, n-heptane 36.6, ethanol 42.3 kJ/mol,
mole-weighted. Densities at 20 C: isooctane 0.6919, n-heptane 0.6795, ethanol 0.7893 g/cm3 (CRC Handbook).

Knock (Module 03 ignition-fit schema): Douaud & Eyzat (1978) SAE 780080, as given by Heywood (1988)
section 9.6: tau = 17.68 ms (ON/100)^3.402 p[atm]^-1.7 exp(3800 K/T); fitted to PRFs ON 80-100.
Water enters only through the end-gas temperature (c = 0). This is a published correlation, NOT the
Module 02 detailed-kinetics fit used for the alcohols - a methodological difference stated in TRACKS.md.

Flame speed (Module 03 flame-fit schema, only S_L(w)/S_L(0) and the 0.08 m/s floor are used):
Metghalchi & Keck (1982) Combust. Flame 48:191, isooctane phi = 1: S_L0 = Bm + Bphi (1 - phim)^2,
Bm 26.32 cm/s, Bphi -84.72 cm/s, phim 1.13, alpha 2.18 (400 K, 1 atm), diluent factor (1 - 2.1 Y_dil)
with Y_dil = water mass fraction of the fresh mixture. E85 uses the Module 02 ethanol S_L(0) as the
absolute value with the same diluent factor.
"""
import math
from pathlib import Path

import cantera as ct
import numpy as np

from sims.common import fuels

REPO = Path(__file__).resolve().parents[2]
MECH = REPO / "mechanisms" / "trackb_fuels.yaml"
MECH_REL = "mechanisms/trackb_fuels.yaml"

COMPONENTS = {  # name in nasa_gas.yaml, MW g/mol, density g/cm3, h_vap J/mol (298.15 K)
    "IC8H18": ("C8H18,isooctane", 114.231, 0.6919, 35100.0),
    "NC7H16": ("C7H16,n-heptane", 100.202, 0.6795, 36600.0),
    "C2H5OH": ("C2H5OH", 46.069, 0.7893, 42300.0),
}
# volume fractions and knock octane number
BLENDS = {
    "PRF87": dict(vol={"IC8H18": 0.87, "NC7H16": 0.13}, ON=87.0, role="regular gasoline, conservative (RON 87)"),
    "PRF91": dict(vol={"IC8H18": 0.91, "NC7H16": 0.09}, ON=91.0, role="regular gasoline (US 87 AKI ~ RON 91)"),
    "PRF97": dict(vol={"IC8H18": 0.97, "NC7H16": 0.03}, ON=97.0, role="premium gasoline (US 91-93 AKI ~ RON 97)"),
    "E10": dict(vol={"IC8H18": 0.9 * 0.91, "NC7H16": 0.9 * 0.09, "C2H5OH": 0.10}, ON=96.1,
                role="E10 on regular base"),
    "E85": dict(vol={"IC8H18": 0.15 * 0.91, "NC7H16": 0.15 * 0.09, "C2H5OH": 0.85}, ON=108.5,
                role="E85 flex fuel (ON beyond PRF scale: extrapolated)"),
}
ATOMS = {"IC8H18": (8, 18, 0), "NC7H16": (7, 16, 0), "C2H5OH": (2, 6, 1)}


def mole_fractions(blend):
    n = {k: v * COMPONENTS[k][2] / COMPONENTS[k][1] for k, v in BLENDS[blend]["vol"].items()}
    s = sum(n.values())
    return {k: v / s for k, v in n.items()}


def blend_atoms(blend):
    x = mole_fractions(blend)
    return tuple(sum(x[k] * ATOMS[k][i] for k in x) for i in range(3))


def blend_hvap(blend):
    x = mole_fractions(blend)
    return sum(x[k] * COMPONENTS[k][3] for k in x)


def blend_density(blend):
    v = BLENDS[blend]["vol"]
    return 1000.0 * sum(v[k] * COMPONENTS[k][2] for k in v)  # kg/m3, ideal volume mixing


def lumped_species(blend, nasa):
    x = mole_fractions(blend)
    lo = np.zeros(7)
    hi = np.zeros(7)
    for k, xk in x.items():
        d = nasa[COMPONENTS[k][0]].thermo.input_data
        assert d["temperature-ranges"] == [200.0, 1000.0, 6000.0]
        lo += xk * np.array(d["data"][0])
        hi += xk * np.array(d["data"][1])
    c, h, o = blend_atoms(blend)
    comp = {"C": c, "H": h}
    if o:
        comp["O"] = o
    sp = ct.Species(blend, comp)
    sp.thermo = ct.NasaPoly2(200.0, 6000.0, ct.one_atm, np.concatenate([[1000.0], hi, lo]))
    return sp


def build_mechanism(path=MECH):
    gri = ct.Species.list_from_file("gri30.yaml")
    nasa = {s.name: s for s in ct.Species.list_from_file("nasa_gas.yaml")}
    species = list(gri) + [lumped_species(b, nasa) for b in BLENDS]
    gas = ct.Solution(thermo="ideal-gas", kinetics="none", species=species)
    gas.name = "trackb_fuels"
    gas.write_yaml(str(path), header=True)
    return path


class _Fuel(fuels.Fuel):
    pass


def register():
    """Add the Track B blends to sims.common.fuels (in-process only; idempotent)."""
    if not MECH.is_file():
        build_mechanism()
    for b, d in BLENDS.items():
        if b in fuels.FUELS:
            continue
        f = fuels.Fuel(b, blend_atoms(b), "liquid", "n-Heptane", blend_hvap(b),
                       "NIST SRD 69 component values, mole-weighted (sims/track_b/fuels_b.py)",
                       "component densities (CRC), ideal volume mixing")
        f.__dict__["liquid_density"] = blend_density(b)  # cached_property override
        fuels.FUELS[b] = f
    if not getattr(fuels.select_mechanism, "_trackb", False):
        orig = fuels.select_mechanism

        def select(fuel):
            if fuel in BLENDS:
                return fuels.MechanismSelection(MECH_REL)
            return orig(fuel)
        select._trackb = True
        fuels.select_mechanism = select


def ignition_fit(blend):
    on = BLENDS[blend]["ON"]
    R = ct.gas_constant / 1000.0
    return dict(status="fitted", mode="full", A=17.68e-3 * (on / 100.0) ** 3.402 * ct.one_atm ** 1.7, n=1.7,
                E_J_per_mol=3800.0 * R, c=0.0, pressure_unit="Pa", A_unit="s*Pa**1.7",
                valid_T_K_range=None, valid_p_Pa_range=None, valid_w_range=[0.0, 0.1], octane_number=on,
                source="Douaud & Eyzat (1978) SAE 780080 (Heywood 1988 s.9.6), PRF-fitted ON 80-100; "
                       "Track B correlation, NOT Module 02 kinetics" + ("; ON>100 EXTRAPOLATED" if on > 100 else ""))


def flame_fit(blend, ethanol_SL0=None):
    if blend == "E85":
        s0 = ethanol_SL0
    else:
        s0 = (0.2632 - 0.8472 * (1.0 - 1.13) ** 2) * (400.0 / 298.0) ** 2.18
    c, h, o = blend_atoms(blend)
    mw = 12.011 * c + 1.008 * h + 15.999 * o
    afr = (c + h / 4 - o / 2) * (31.998 + 3.76 * 28.014) / mw
    ws = np.linspace(0.0, 0.1, 21)
    wfr = ws / (1 - ws)
    y = wfr / (1 + afr + wfr)
    sl = s0 * (1 - 2.1 * y)
    coeff = np.polyfit(ws, sl, 3)
    return dict(status="fitted", mode="full", S_L_unit="m/s", coefficients_highest_first=[float(v) for v in coeff],
                polynomial_degree=3, valid_w_range=[0.0, 0.1], phi=1.0, T_unburned_K=400.0, p_Pa=ct.one_atm,
                rms_m_s=float(np.sqrt(np.mean((np.polyval(coeff, ws) - sl) ** 2))),
                source="Metghalchi & Keck (1982) isooctane phi=1 correlation, 400 K 1 atm, diluent (1-2.1Y)"
                       + ("; absolute S_L(0) from Module 02 ethanol fit" if blend == "E85" else ""))
