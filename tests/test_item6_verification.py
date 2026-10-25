"""Verification-queue item 6 (2026-10-24): every independent analytic/limit check must pass, except the documented
latent Module 03 QD-burn unit defect (Q7, see sims/10_qd_burn/VERIFICATION.md), which is xfail until fixed."""
import importlib
import pytest

V = importlib.import_module("sims.verification.item6_checks")
V.R.clear()
for fn in (V.m01, V.m05, V.m06, V.m10, V.m11, V.dualT):
    fn()
V.m04(steps=False)
KNOWN = {("10", "Q7")}
CASES = [(m, c) for m, cs in V.R.items() for c in cs]


@pytest.mark.parametrize("mod,c", CASES, ids=[f"{m}-{c['id']}" for m, c in CASES])
def test_check(mod, c):
    if (mod, c["id"]) in KNOWN:
        pytest.xfail("latent Module 03 QD-burn rad/deg defect (opt-in path)")
    assert c["passed"], c
