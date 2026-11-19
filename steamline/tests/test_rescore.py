"""Tests for the AH26/BH26 rescore.

Rows built in this file are synthetic fixtures. Rows loaded from
evidence/sample-rows-from-input-summary.json are the attached executed samples.
The cost-module checks call the real sims.cost functions.
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "reference"
sys.path.insert(0, str(REFERENCE))

from sims.cost import cost as C  # noqa: E402


def load_rescore():
    spec = importlib.util.spec_from_file_location("rescore_ah26_bh26", ROOT / "rescore_ah26_bh26.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


R = load_rescore()
CONFIG = json.loads((ROOT / "stage_config.json").read_text())
SAMPLES = json.loads((ROOT / "evidence" / "sample-rows-from-input-summary.json").read_text())["rows"]


def row(key, eta=0.40, imep=1.0e6, crn=0.39, eligible=True, knock=False, integral=0.2,
        mechanism=None, evidence="synthetic_fixture"):
    parts = R.split_key(key)
    w = float(parts["w"])
    mf = 1.0e-5
    return {
        "_key": key,
        "status": "computed",
        "fuel": parts["fuel"],
        "regime": parts["regime"],
        "CR": float(parts["cr"]),
        "w": w,
        "bore_mm": float(parts["bore"]),
        "stroke_mm": float(parts["stroke"]),
        "rpm": int(parts["rpm"]),
        "intake_mode": "humid_ambient",
        "water_mode": "humid_ambient",
        "gross_indicated_efficiency": eta,
        "IMEP_Pa": imep,
        "crn_status": "ok",
        "crn_efficiency": crn,
        "eligible": eligible,
        "knock": knock,
        "knock_limited": knock,
        "knock_integral_at_xb90": integral,
        "fuel_mass_kg": mf,
        "water_mass_kg": 0.0 if w == 0 else mf * w / (1.0 - w),
        "fuel_treatment": "DEI (fuel_evap_intake=1.0)",
        "mechanism": mechanism or ("mechanisms/sandiego.yaml" if parts["eng"] == "A2" else "mechanisms/trackb_fuels.yaml"),
        "flame_fit": "module_02" if parts["eng"] == "A2" else "cantera_w030",
        "track": "A" if parts["eng"] == "A2" else "B",
        "track_tag": "Track A" if parts["eng"] == "A2" else "Track B",
        "evidence_class": evidence,
    }


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


def allow_from(keys):
    return {"campaigns": ["AH26", "BH26"], "count": len(keys), "keys": keys}


class CostModuleTests(unittest.TestCase):
    """Actual calls into the reviewed sims.cost module, not a reimplementation."""

    def test_headline_water_and_tolerances(self):
        info = R.self_check(CONFIG["cost_reference"]["blob_sha1"])
        self.assertTrue(info["blob_matches_reference"])
        self.assertTrue(info["constants_ok"])
        self.assertEqual(C.HEADLINE_WATER, "headline")

    def test_cost_formula_matches_module_definition(self):
        prices = C.load_prices()
        dry = {"fuel": "PRF87", "w": 0.0, "gross_indicated_efficiency": 0.40, "IMEP_Pa": 1.0e6,
               "fuel_mass_kg": 1.0e-5, "water_mass_kg": 0.0, "crn_status": "ok", "crn_efficiency": 0.39}
        wet = dict(dry, w=0.10, gross_indicated_efficiency=0.41, water_mass_kg=1.0e-5 * 0.10 / 0.90, crn_efficiency=0.40)
        got = C.compare(wet, dry, prices)["m03"]
        ratio = C.usd_per_kg("water", prices) / C.usd_per_kg("PRF87", prices)
        self.assertAlmostEqual(got["cost_per_mile_pct"], 100 * ((1 + ratio / 9) * 0.40 / 0.41 - 1))
        self.assertAlmostEqual(got["cost_per_mile_water_free_pct"], 100 * (0.40 / 0.41 - 1))

    def test_attached_bh_sample_pair_loses_power_at_the_same_cr(self):
        dry = SAMPLES["BH24"]
        wet = SAMPLES["BH26"]
        self.assertEqual(dry["fuel"], wet["fuel"])
        self.assertEqual(dry["CR"], wet["CR"])
        self.assertEqual(dry["w"], 0.0)
        self.assertEqual(wet["w"], 0.1)
        compared = C.compare(wet, dry)
        self.assertEqual(C.verdict(compared), "power loss")
        self.assertLess(compared["m03"]["power_change_pct"], -0.5)
        self.assertGreater(compared["m03"]["power_change_pct"], -2.0)
        self.assertFalse(compared["cost_gain_all_engines"])
        self.assertIn(wet["_key"], json.loads((ROOT / "duplicate-guard-all-9900.json").read_text())["keys"])


class GridAuditTests(unittest.TestCase):
    def test_executed_grid_has_no_interior_hole_and_no_new_point(self):
        audit = json.loads((ROOT / "evidence" / "grid-audit.json").read_text())
        self.assertEqual(audit["total_keys"], 9900)
        self.assertEqual(audit["next_simulation"], "WITHHELD")
        for name, ladder in audit["ladders"].items():
            self.assertEqual(ladder["interior_missing"], 0, name)
        for pair, rel in audit["body_equality"].items():
            self.assertEqual(rel["only_left"], 0, pair)
            self.assertEqual(rel["only_right"], 0, pair)
        guard = set(json.loads((ROOT / "duplicate-guard-all-9900.json").read_text())["keys"])
        allow = json.loads((ROOT / "allow-keys-AH26-BH26.json").read_text())["keys"]
        self.assertEqual(len(allow), 3300)
        self.assertTrue(set(allow) <= guard)
        invented = "A24:A2/1500/65.0x81.2/CH3OH/normal/18.0/0.4"
        self.assertNotIn(invented, guard)
        withheld = json.loads((ROOT / "nextsim_WITHHELD.json").read_text())
        self.assertFalse(withheld["launch"])
        self.assertIsNone(withheld["inputs"])


class RescoreBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="rescore-test-"))
        self.jobs = self.tmp / "jobs"
        self.jobs.mkdir()
        self.out = self.tmp / "out"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _run(self, keys, rows, siblings=None, resume=False, out=None):
        allow = self.tmp / "allow.json"
        allow.write_text(json.dumps(allow_from(keys)))
        by_file = {"points_AH26.jsonl": [], "points_BH26.jsonl": []}
        for item in rows:
            eng = R.split_key(item["_key"])["eng"]
            by_file["points_AH26.jsonl" if eng == "A2" else "points_BH26.jsonl"].append(item)
        for name, content in by_file.items():
            write_jsonl(self.jobs / name, content)
        for name, content in (siblings or {}).items():
            write_jsonl(self.jobs / name, content)
        return R.run(self.jobs, CONFIG, allow, out or self.out, resume=resume,
                     reference_blob=CONFIG["cost_reference"]["blob_sha1"])

    def test_reoptimized_dry_not_the_same_cr_row(self):
        keys = []
        rows = []
        base = "A24:A2/1500/65.0x81.2/CH3OH/normal"
        for cr, w, eta, imep, crn, knock, integral in (
            ("18.0", "0.0", 0.40, 1.00e6, 0.39, False, 0.2),
            ("22.0", "0.0", 0.50, 1.20e6, 0.49, False, 0.4),
            ("26.0", "0.0", 0.55, 1.30e6, 0.54, True, 1.4),
            ("18.0", "0.1", 0.46, 1.10e6, 0.45, False, 0.2),
            ("22.0", "0.1", 0.47, 1.05e6, 0.46, False, 0.3),
            ("26.0", "0.1", 0.60, 1.40e6, 0.59, True, 1.2),
        ):
            key = "%s/%s/%s" % (base, cr, w)
            keys.append(key)
            rows.append(row(key, eta=eta, imep=imep, crn=crn, eligible=not knock, knock=knock, integral=integral))
        meta = self._run(keys, rows)
        self.assertFalse(meta["science_claim"])
        self.assertTrue(meta["contains_non_executed"])
        self.assertEqual(meta["promoted"], 0)
        group = json.loads(next((self.out / "by-group").glob("*.json")).read_text())
        self.assertEqual(group["dry"]["CR"], 22.0)
        self.assertEqual(group["dry"]["klCR"], 22.0)
        self.assertFalse(group["dry"]["dry_scan_edge"])
        self.assertIsNone(group["promoted"])
        self.assertEqual(group["factory_cr_recommendation"] if "factory_cr_recommendation" in group else "WITHHELD", "WITHHELD")
        flags = json.dumps(group["flags"])
        self.assertIn("same_cr_dry_would_overstate_gain", flags)

    def test_promotes_equal_or_better_power_and_keeps_factory_cap(self):
        keys = []
        rows = []
        base = "A24:B2/1500/65.0x81.2/E85/hot"
        # E85 order cap is 18. CR 20 is inside this fixture and above that cap.
        for cr, w, eta, imep, crn in (
            ("12.0", "0.0", 0.30, 1.00e6, 0.29),
            ("20.0", "0.0", 0.31, 1.01e6, 0.30),
            ("12.0", "0.1", 0.33, 1.02e6, 0.32),
            ("20.0", "0.2", 0.40, 1.20e6, 0.39),
        ):
            key = "%s/%s/%s" % (base, cr, w)
            keys.append(key)
            rows.append(row(key, eta=eta, imep=imep, crn=crn))
        meta = self._run(keys, rows)
        self.assertEqual(meta["promoted"], 1)
        group = json.loads(next((self.out / "by-group").glob("*.json")).read_text())
        self.assertEqual(group["promoted"]["CR"], 20.0)
        self.assertTrue(group["promoted"]["above_documented_order_cap"])
        self.assertEqual(group["promoted"]["factory_cr_recommendation"], "WITHHELD")
        self.assertFalse(group["promoted"]["factory_cr_update_allowed"])
        self.assertFalse(group["promoted"]["independent_validation"])
        self.assertEqual(group["promoted"]["validation_status"], "executed_not_validated")
        text = (self.out / "SUMMARY.md").read_text()
        self.assertIn("WITHHELD", text)
        self.assertIn("Not validated", text)

    def test_water_fraction_above_rule_is_not_promoted(self):
        keys = []
        rows = []
        base = "A24:A2/2500/86.0x86.0/CH3OH/normal"
        specs = (("18.0", "0.0", 0.40, 1.0e6, 0.39), ("18.0", "0.4", 0.55, 1.3e6, 0.54))
        for cr, w, eta, imep, crn in specs:
            key = "%s/%s/%s" % (base, cr, w)
            keys.append(key)
            rows.append(row(key, eta=eta, imep=imep, crn=crn))
        meta = self._run(keys, rows)
        self.assertEqual(meta["promoted"], 0)
        group = json.loads(next((self.out / "by-group").glob("*.json")).read_text())
        self.assertIn("R-WE-22", json.dumps(group["flags"]))
        self.assertEqual(group["raw_best_key"], keys[1])

    def test_duplicate_conflict_and_unknown_key_are_not_scored(self):
        key = "A24:A2/1500/65.0x81.2/CH3OH/hot/18.0/0.0"
        other = "A24:A2/1500/65.0x81.2/CH3OH/hot/18.0/0.1"
        first = row(key, eta=0.40)
        second = row(key, eta=0.50)
        wet = row(other, eta=0.42, imep=1.1e6, crn=0.41)
        stray = row("A24:A2/1500/65.0x81.2/CH3OH/hot/19.0/0.1")
        allow = self.tmp / "allow.json"
        allow.write_text(json.dumps(allow_from([key, other])))
        write_jsonl(self.jobs / "points_AH26.jsonl", [first, second, wet, stray])
        write_jsonl(self.jobs / "points_BH26.jsonl", [])
        meta = R.run(self.jobs, CONFIG, allow, self.out, reference_blob=CONFIG["cost_reference"]["blob_sha1"])
        self.assertEqual(meta["promoted"], 0)
        quarantined = json.loads((self.out / "quarantined.json").read_text())
        reasons = {item["reason"] for item in quarantined}
        self.assertIn("conflicting_duplicate", reasons)
        self.assertIn("key_not_in_allow_list", reasons)
        group = json.loads(next((self.out / "by-group").glob("*.json")).read_text())
        self.assertEqual(group["reason"], "incomplete_group")

    def test_identical_duplicate_is_scored_once(self):
        dry_key = "A24:A2/4000/105.0x131.2/C2H5OH/hot/18.0/0.0"
        wet_key = "A24:A2/4000/105.0x131.2/C2H5OH/hot/18.0/0.1"
        dry = row(dry_key, eta=0.40, crn=0.39)
        wet = row(wet_key, eta=0.46, imep=1.1e6, crn=0.45)
        meta = self._run([dry_key, wet_key], [dry, wet, json.loads(json.dumps(wet))])
        self.assertEqual(meta["promoted"], 1)
        scored = [json.loads(line) for line in (self.out / "scored.jsonl").read_text().splitlines()]
        self.assertEqual([item["_key"] for item in scored], [wet_key])

    def test_resume_does_not_duplicate_and_rejects_changed_inputs(self):
        dry_key = "A24:A2/5000/65.0x81.2/CH3OH/normal/18.0/0.0"
        wet_key = "A24:A2/5000/65.0x81.2/CH3OH/normal/18.0/0.1"
        rows = [row(dry_key, eta=0.40, crn=0.39), row(wet_key, eta=0.46, imep=1.1e6, crn=0.45)]
        first = self._run([dry_key, wet_key], rows)
        run_id = first["run_id"]
        (self.out / "SUMMARY.md").unlink()
        second = self._run([dry_key, wet_key], rows, resume=True, out=self.out)
        self.assertEqual(second["run_id"], run_id)
        self.assertEqual(len(list((self.out / "by-group").glob("*.json"))), 1)
        self.assertTrue((self.out / "SUMMARY.md").is_file())
        scored = (self.out / "scored.jsonl").read_text().strip().splitlines()
        self.assertEqual(len(scored), 1)
        # Changing an input checksum must not resume into the same directory.
        changed = json.loads(json.dumps(rows[0]))
        changed["gross_indicated_efficiency"] = 0.41
        with self.assertRaises(SystemExit):
            self._run([dry_key, wet_key], [changed, rows[1]], resume=True, out=self.out)

    def test_sibling_mismatch_blocks_promotion(self):
        dry_key = "A24:B2/1500/86.0x86.0/PRF87/normal/5.0/0.0"
        wet_key = "A24:B2/1500/86.0x86.0/PRF87/normal/5.0/0.1"
        dry = row(dry_key, eta=0.30, crn=0.29)
        wet = row(wet_key, eta=0.36, imep=1.2e6, crn=0.35)
        sibling = json.loads(json.dumps(dry))
        sibling["_key"] = "H24:" + dry_key.split(":", 1)[1]
        sibling["intake_mode"] = "humid_evap"
        sibling["water_mode"] = "humid_evap"
        sibling["gross_indicated_efficiency"] = 0.36
        meta = self._run([dry_key, wet_key], [dry, wet], siblings={"points_BH24.jsonl": [sibling]})
        self.assertEqual(meta["promoted"], 0)
        group = json.loads(next((self.out / "by-group").glob("*.json")).read_text())
        self.assertEqual(group["reason"], "sibling_dry_mismatch")
        self.assertFalse(group["sibling_dry"]["ok"])

    def test_existing_directory_is_not_overwritten(self):
        self.out.mkdir()
        allow = self.tmp / "allow.json"
        allow.write_text(json.dumps(allow_from(["A24:A2/1500/65.0x81.2/CH3OH/normal/18.0/0.0"])))
        write_jsonl(self.jobs / "points_AH26.jsonl", [])
        write_jsonl(self.jobs / "points_BH26.jsonl", [])
        with self.assertRaises(SystemExit):
            R.run(self.jobs, CONFIG, allow, self.out, reference_blob=CONFIG["cost_reference"]["blob_sha1"])

    def test_workers_above_one_refused(self):
        with self.assertRaises(SystemExit):
            R.main(["--config", str(ROOT / "stage_config.json"), "--jobs", str(self.jobs),
                    "--allow-keys", str(ROOT / "allow-keys-AH26-BH26.json"),
                    "--outdir", str(self.out), "--workers", "2"])

    def test_attached_samples_do_not_promote_against_the_real_allow_list(self):
        allow = ROOT / "allow-keys-AH26-BH26.json"
        write_jsonl(self.jobs / "points_AH26.jsonl", [SAMPLES["AH26"]])
        write_jsonl(self.jobs / "points_BH26.jsonl", [SAMPLES["BH26"]])
        write_jsonl(self.jobs / "points_BH24.jsonl", [SAMPLES["BH24"]])
        meta = R.run(self.jobs, CONFIG, allow, self.out, expect_full_grid=True,
                     reference_blob=CONFIG["cost_reference"]["blob_sha1"])
        self.assertEqual(meta["groups"], 132)
        self.assertEqual(meta["promoted"], 0)
        self.assertEqual(meta["quarantined"], 0)
        self.assertEqual(meta["evidence_classes"], ["executed_row"])
        self.assertFalse(meta["contains_non_executed"])
        self.assertFalse(meta["science_claim"])
        reasons = {}
        for line in (self.out / "ledger.jsonl").read_text().splitlines():
            reason = json.loads(line)["reason"]
            reasons[reason] = reasons.get(reason, 0) + 1
        self.assertEqual(reasons, {"incomplete_group": 132})


class LauncherTests(unittest.TestCase):
    def test_source_has_no_publish_or_combustion_commands(self):
        text = (ROOT / "launch_rescore_ah26_bh26.sh").read_text()
        for lineno, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            self.assertNotIn("run_geom24", stripped, lineno)
            self.assertNotIn("git ", stripped, lineno)
            self.assertNotIn("ssh ", stripped, lineno)
            self.assertNotIn("docker", stripped, lineno)
        source = (ROOT / "rescore_ah26_bh26.py").read_text()
        self.assertNotIn("subprocess", source)
        self.assertNotIn("socket", source)
        self.assertNotIn("urllib", source)

    def test_plan_does_not_score_and_execute_requires_explicit_paths(self):
        launcher = ROOT / "launch_rescore_ah26_bh26.sh"
        plan = subprocess.run(["bash", str(launcher)], check=False, text=True, capture_output=True)
        self.assertEqual(plan.returncode, 0, plan.stderr)
        self.assertIn("plan only", plan.stdout)
        missing = Path(tempfile.mkdtemp(prefix="rescore-should-not-exist-"))
        missing_out = missing / "out"
        env = os.environ.copy()
        env.update({
            "WE_PYTHON": sys.executable,
            "WE_PYTHONPATH": str(REFERENCE),
        })
        env.pop("WE_JOBS", None)
        env.pop("WE_RESULTS_ROOT", None)
        refused = subprocess.run(["bash", str(launcher), "--execute"], check=False, text=True, capture_output=True, env=env)
        self.assertEqual(refused.returncode, 3, refused.stdout + refused.stderr)
        self.assertFalse(missing_out.exists())
        shutil.rmtree(missing)

    def test_launcher_on_attached_samples_promotes_nothing(self):
        jobs = ROOT / "smoke" / "sample-jobs"
        results = ROOT / "smoke" / "sample-results"
        if jobs.exists():
            shutil.rmtree(jobs)
        if results.exists():
            shutil.rmtree(results)
        jobs.mkdir(parents=True)
        results.mkdir()
        write_jsonl(jobs / "points_AH26.jsonl", [SAMPLES["AH26"]])
        write_jsonl(jobs / "points_BH26.jsonl", [SAMPLES["BH26"]])
        write_jsonl(jobs / "points_BH24.jsonl", [SAMPLES["BH24"]])
        env = os.environ.copy()
        env.update({
            "WE_JOBS": str(jobs),
            "WE_RESULTS_ROOT": str(results),
            "WE_PYTHON": sys.executable,
            "WE_PYTHONPATH": str(REFERENCE),
        })
        proc = subprocess.run(["bash", str(ROOT / "launch_rescore_ah26_bh26.sh"), "--execute"],
                              check=False, text=True, capture_output=True, env=env)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        created = list(results.glob("rescore-AH26-BH26-*"))
        self.assertEqual(len(created), 1)
        meta = json.loads((created[0] / "run_meta.json").read_text())
        self.assertEqual(meta["promoted"], 0)
        self.assertEqual(meta["groups"], 132)
        self.assertEqual(meta["evidence_classes"], ["executed_row"])
        self.assertFalse(meta["science_claim"])
        self.assertTrue((created[0] / "EXIT.txt").read_text().strip().endswith("rc=0"))


if __name__ == "__main__":
    unittest.main()
