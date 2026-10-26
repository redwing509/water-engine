"""Track B surrogate fuels. Run in a subprocess so the fuel registration stays out of the other tests."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

CODE = r"""
import json, sys
sys.path.insert(0, %r)
from sims.track_b import fuels_b as F
F.register()
from sims.common import fuels
out = {}
for b in F.BLENDS:
    x = F.mole_fractions(b)
    out[b] = dict(xsum=sum(x.values()), lhv=fuels.lhv(b), afr=fuels.stoich_air_fuel_ratio(b),
                  A=F.ignition_fit(b)["A"], sl=F.flame_fit(b, 0.75)["coefficients_highest_first"])
print(json.dumps(out))
""" % str(REPO)


def test_track_b_blends():
    res = subprocess.run([sys.executable, "-c", CODE], capture_output=True, text=True, check=True, cwd=REPO)
    out = json.loads(res.stdout.strip().splitlines()[-1])
    for b, d in out.items():
        assert abs(d["xsum"] - 1) < 1e-12
        assert d["sl"][-1] > 0.08
    # NASA-Glenn isooctane LHV 44.3 MJ/kg (Heywood App. D 44.3); E85 ~29 MJ/kg
    assert 43.8e6 < out["PRF91"]["lhv"] < 44.8e6
    assert 28.0e6 < out["E85"]["lhv"] < 30.5e6
    assert 14.9 < out["PRF91"]["afr"] < 15.2
    assert out["PRF87"]["A"] < out["PRF91"]["A"] < out["PRF97"]["A"]  # longer delay for higher ON
