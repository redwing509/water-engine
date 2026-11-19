#!/usr/bin/env python3
"""Matched-dry cost-per-mile rescore for the finished AH26 and BH26 grids.

This process only reads existing result rows and applies sims.cost. It does not
run combustion, write mechanisms, publish, or touch git. A finished rescore is
still executed model output, not validation.

Dry baseline for a group (engine, speed, geometry, fuel, regime): the eligible
DEI w=0 row at or below the first knocked dry compression ratio, chosen by
gross indicated efficiency. Wet rows are compared with that row, not with the
dry row that happens to share their compression ratio. Promotion also requires
equal-or-better power in both engines and W/F <= 0.6. Factory CR is not updated.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from pathlib import Path

SCHEMA = 1
KNOCK_LIMIT = 1.0
LABELS = {
    "validation_status": "executed_not_validated",
    "independent_validation": False,
    "executed_does_not_mean_validated": True,
    "factory_cr_recommendation": "WITHHELD",
    "factory_cr_update_allowed": False,
    "two_engine_note": (
        "M03 and M03-CRN are two engines in the same toolchain. "
        "They are not independent experimental validation."
    ),
}


def blob_sha1(data: bytes) -> str:
    header = ("blob %d\0" % len(data)).encode()
    return hashlib.sha1(header + data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(path: Path) -> list:
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit("bad json %s:%d: %s" % (path, lineno, exc))
    # A points file may be one object per line, or one object with a rows array.
    flat = []
    for obj in rows:
        if isinstance(obj, dict) and isinstance(obj.get("rows"), list) and "_key" not in obj:
            flat.extend(obj["rows"])
        else:
            flat.append(obj)
    return flat


def split_key(key: str) -> dict:
    try:
        prefix, rest = key.split(":", 1)
        eng, rpm, geom, fuel, regime, cr, w = rest.split("/")
        bore, stroke = geom.split("x")
        float(bore); float(stroke); float(cr); float(w); int(rpm)
    except (ValueError, AttributeError):
        raise ValueError("unparsed key %r" % (key,))
    if eng not in ("A2", "B2") or regime not in ("normal", "hot"):
        raise ValueError("unparsed key %r" % (key,))
    return {
        "prefix": prefix, "body": rest, "eng": eng, "rpm": rpm, "geom": geom,
        "bore": bore, "stroke": stroke, "fuel": fuel, "regime": regime, "cr": cr, "w": w,
    }


def group_id(campaign: str, parts: dict) -> str:
    return "|".join((campaign, parts["eng"], parts["rpm"], parts["geom"], parts["fuel"], parts["regime"]))


def load_cost():
    from sims.cost import cost as C
    return C


def imported_cost_file(C) -> Path:
    return Path(C.__file__).resolve()


def check_cost_module(C, reference_blob: str) -> dict:
    path = imported_cost_file(C)
    data = path.read_bytes()
    prices = path.parent / "prices_20261025.json"
    info = {
        "file": str(path),
        "blob_sha1": blob_sha1(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "prices_file": str(prices),
        "prices_present": prices.is_file(),
        "reference_blob_sha1": reference_blob,
    }
    if prices.is_file():
        info["prices_blob_sha1"] = blob_sha1(prices.read_bytes())
        info["prices_sha256"] = sha256_file(prices)
    water = C.usd_per_kg("water")
    expected = 0.10 / (C.US_GAL_M3 * C.WATER_RHO)
    info["headline_water_usd_per_kg"] = water
    info["constants_ok"] = bool(
        abs(water - expected) <= 1e-12
        and C.POWER_TOL_REL == 1.0e-4
        and C.COST_TOL_REL == 1.0e-4
        and C.WORK_KWH_PER_MILE == 0.40
        and C.HEADLINE_WATER == "headline"
    )
    info["blob_matches_reference"] = info["blob_sha1"] == reference_blob
    return info


def self_check(reference_blob: str) -> dict:
    C = load_cost()
    info = check_cost_module(C, reference_blob)
    if not info["constants_ok"] or not info["prices_present"] or not info["blob_matches_reference"]:
        raise SystemExit("cost module self-check failed: %s" % json.dumps(info, sort_keys=True))
    return info


def _close(a, b) -> bool:
    return abs(float(a) - float(b)) <= 1e-9


def knocked(row):
    """True, False, or None when the knock integral is missing."""
    if row.get("knock") is True or row.get("knock_limited") is True:
        return True
    integral = row.get("knock_integral_at_xb90")
    if integral is None:
        return None
    return float(integral) >= KNOCK_LIMIT


def engines_ok(row) -> bool:
    return (
        row.get("gross_indicated_efficiency") is not None
        and row.get("IMEP_Pa") is not None
        and row.get("crn_status") == "ok"
        and row.get("crn_efficiency") is not None
    )


def is_dei(row) -> bool:
    treatment = row.get("fuel_treatment")
    return isinstance(treatment, str) and treatment.startswith("DEI")


def wf_of(row) -> float:
    w = float(row.get("w") or 0.0)
    return w / (1.0 - w)


def order_cap_flags(fuel: str, cr: float, caps: dict) -> dict:
    if fuel not in caps:
        return {"order_cap_CR": None, "order_cap_status": "not_in_engine_order_spec",
                "above_documented_order_cap": False, "on_documented_order_cap": False}
    cap = float(caps[fuel])
    return {
        "order_cap_CR": cap,
        "order_cap_status": "documented_order_cap",
        "above_documented_order_cap": cr > cap + 1e-9,
        "on_documented_order_cap": abs(cr - cap) <= 1e-9,
    }


def identity_problems(row: dict, parts: dict, campaign: dict) -> list:
    problems = []
    if not isinstance(row, dict):
        return ["not_an_object"]
    if row.get("fuel") != parts["fuel"]:
        problems.append("fuel_disagrees_with_key")
    if str(row.get("regime")) != parts["regime"]:
        problems.append("regime_disagrees_with_key")
    for field, token in (("CR", "cr"), ("w", "w"), ("bore_mm", "bore"), ("stroke_mm", "stroke")):
        if field not in row or not _close(row[field], parts[token]):
            problems.append(field + "_disagrees_with_key")
    if "rpm" not in row or int(row["rpm"]) != int(parts["rpm"]):
        problems.append("rpm_disagrees_with_key")
    if row.get("intake_mode") != campaign["intake_mode"] or row.get("water_mode") != campaign["intake_mode"]:
        problems.append("intake_mode")
    if parts["prefix"] != campaign["key_prefix"] or parts["eng"] != campaign["eng"]:
        problems.append("campaign_key")
    return problems


def dedup_rows(rows: list, campaign: str) -> tuple:
    """Keep the first copy of each key. Conflicting repeats are quarantined and not scored."""
    kept = {}
    order = []
    quarantined = []
    for row in rows:
        key = row.get("_key") if isinstance(row, dict) else None
        if not isinstance(key, str):
            quarantined.append({"campaign": campaign, "reason": "missing_key", "row": row})
            continue
        if key not in kept:
            kept[key] = row
            order.append(key)
            continue
        if json.dumps(kept[key], sort_keys=True) != json.dumps(row, sort_keys=True):
            quarantined.append({"campaign": campaign, "reason": "conflicting_duplicate", "_key": key})
            kept.pop(key)
            order.remove(key)
        # an identical repeat is a duplicate, not a second result
    return [kept[k] for k in order], quarantined


def load_allow(path: Path, campaigns: dict) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    keys = payload["keys"] if isinstance(payload, dict) else payload
    by_group = {}
    by_key = {}
    for key in keys:
        parts = split_key(key)
        campaign = None
        for name, cfg in campaigns.items():
            if parts["eng"] == cfg["eng"] and parts["prefix"] == cfg["key_prefix"]:
                campaign = name
                break
        if campaign is None:
            raise SystemExit("allow-list key is not AH26 or BH26: %s" % key)
        gid = group_id(campaign, parts)
        by_group.setdefault(gid, []).append(key)
        by_key[key] = gid
    return {"by_group": by_group, "by_key": by_key, "count": len(by_key)}


def assert_full_grid(allow: dict, expected: dict) -> None:
    counts = {}
    for gid, keys in allow["by_group"].items():
        campaign = gid.split("|", 1)[0]
        counts[campaign] = counts.get(campaign, 0) + 1
        if len(keys) != int(expected["keys_per_group"]) or len(set(keys)) != len(keys):
            raise SystemExit("group %s has %d keys, expected %s" % (gid, len(keys), expected["keys_per_group"]))
    if counts.get("AH26") != int(expected["AH26_groups"]) or counts.get("BH26") != int(expected["BH26_groups"]):
        raise SystemExit("group counts %s do not match the executed grid" % counts)
    if allow["count"] != int(expected["allow_keys"]):
        raise SystemExit("allow-list count %d" % allow["count"])


def select_dry(dry_rows: list) -> dict:
    """Fair reoptimized DEI dry row, or a withhold reason."""
    if not dry_rows:
        return {"ok": False, "reason": "no_dry_row"}
    ordered = sorted(dry_rows, key=lambda r: (float(r["CR"]), r["_key"]))
    limit = None
    for row in ordered:
        state = knocked(row)
        if state is None:
            return {"ok": False, "reason": "dry_knock_field_missing", "_key": row.get("_key")}
        if state:
            break
        limit = row
    if limit is None:
        return {"ok": False, "reason": "no_unknocked_dry"}
    limit_cr = float(limit["CR"])
    eligible = []
    for row in ordered:
        if float(row["CR"]) > limit_cr + 1e-9:
            break
        if knocked(row):
            continue
        if row.get("eligible") is not True:
            continue
        if not engines_ok(row):
            continue
        if not is_dei(row):
            return {"ok": False, "reason": "dry_not_dei", "_key": row.get("_key")}
        if row.get("mechanism") is None:
            return {"ok": False, "reason": "dry_mechanism_missing", "_key": row.get("_key")}
        eligible.append(row)
    if not eligible:
        return {"ok": False, "reason": "no_eligible_matched_dry"}
    best_eta = max(float(r["gross_indicated_efficiency"]) for r in eligible)
    tied = [r for r in eligible if float(r["gross_indicated_efficiency"]) == best_eta]
    chosen = sorted(tied, key=lambda r: r["_key"])[0]
    max_cr = max(float(r["CR"]) for r in ordered)
    return {
        "ok": True,
        "row": chosen,
        "klCR": limit_cr,
        "dry_scan_edge": abs(limit_cr - max_cr) <= 1e-9,
        "eta_tie": len(tied) > 1,
    }


def _public_compare(C, compared: dict) -> dict:
    out = {}
    for eng in ("m03", "crn"):
        block = compared.get(eng)
        if not block:
            out[eng] = None
            continue
        keep = (
            "d_eta_pp", "power_change_pct", "power_drop", "cost_per_mile_pct",
            "cost_per_mile_water_free_pct", "cost_per_mile_retail_water_pct",
            "fuel_volume_per_work_pct", "cost_gain", "mpg_pct",
        )
        out[eng] = {k: block.get(k) for k in keep}
    out["verdict"] = C.verdict(compared)
    out["engines"] = compared.get("engines")
    out["cost_gain_all_engines"] = compared.get("cost_gain_all_engines")
    out["power_ok_all_engines"] = compared.get("power_ok_all_engines")
    return out


def score_group(C, gid, rows_by_key, expected_keys, campaign_cfg, caps, wf_max, siblings) -> dict:
    result = {
        "group": gid,
        "campaign": gid.split("|", 1)[0],
        "expected_keys": len(expected_keys),
        "present_keys": 0,
        "status": "withheld",
        "reason": None,
        "promoted": None,
        "scored": [],
        "flags": [],
    }
    missing = [k for k in expected_keys if k not in rows_by_key]
    result["missing_keys"] = missing
    result["present_keys"] = len(expected_keys) - len(missing)
    if missing:
        result["reason"] = "incomplete_group"
        return result
    rows = [rows_by_key[k] for k in expected_keys]
    dry_rows = [r for r in rows if split_key(r["_key"])["w"] == "0.0"]
    wet_rows = [r for r in rows if split_key(r["_key"])["w"] != "0.0"]
    if len(dry_rows) + len(wet_rows) != len(rows):
        result["reason"] = "unpartitioned_w"
        return result
    chosen = select_dry(dry_rows)
    if not chosen["ok"]:
        result["reason"] = chosen["reason"]
        result["detail"] = {k: v for k, v in chosen.items() if k != "row"}
        return result
    dry = chosen["row"]
    if dry.get("mechanism") != campaign_cfg["mechanism"]:
        result["reason"] = "dry_mechanism_domain"
        result["mechanism"] = dry.get("mechanism")
        return result
    try:
        C.compare(dry, dry)
    except ValueError as exc:
        result["reason"] = "dry_cost_rejected"
        result["detail"] = str(exc)
        return result
    max_w = max(float(split_key(r["_key"])["w"]) for r in wet_rows)
    max_cr = max(float(r["CR"]) for r in rows)
    eligible_wet = []
    excluded = []
    for row in wet_rows:
        reasons = []
        if row.get("status") != "computed":
            reasons.append("not_computed")
        if row.get("eligible") is not True:
            reasons.append("not_eligible")
        if not engines_ok(row):
            reasons.append("engines_incomplete")
        if not is_dei(row):
            reasons.append("not_dei")
        if knocked(row) is None:
            reasons.append("knock_field_missing")
        elif knocked(row):
            reasons.append("knocked")
        if row.get("mechanism") != campaign_cfg["mechanism"]:
            reasons.append("mechanism_domain")
        if reasons:
            excluded.append({"_key": row["_key"], "reasons": reasons})
            continue
        try:
            C.water_per_fuel(row)
        except ValueError as exc:
            excluded.append({"_key": row["_key"], "reasons": ["mass_inconsistent", str(exc)]})
            continue
        eligible_wet.append(row)
    result["excluded"] = excluded
    under_wf = [r for r in eligible_wet if wf_of(r) <= wf_max + 1e-12]
    over_wf = [r["_key"] for r in eligible_wet if wf_of(r) > wf_max + 1e-12]
    if over_wf:
        result["flags"].append({"R-WE-22": over_wf})
    best_row, best_cmp = C.best_cost(under_wf, dry)
    raw_row, raw_cmp = C.best_cost(eligible_wet, dry)
    sibling = sibling_status(C, dry, siblings)
    result["sibling_dry"] = sibling
    result["dry"] = {
        "_key": dry["_key"],
        "CR": dry["CR"],
        "klCR": chosen["klCR"],
        "dry_scan_edge": chosen["dry_scan_edge"],
        "eta_tie": chosen["eta_tie"],
        "gross_indicated_efficiency": dry["gross_indicated_efficiency"],
        "crn_efficiency": dry["crn_efficiency"],
        "IMEP_Pa": dry["IMEP_Pa"],
        "mechanism": dry.get("mechanism"),
        "flame_fit": dry.get("flame_fit"),
        "fuel_treatment": dry.get("fuel_treatment"),
        "track_field": dry.get("track"),
        "track_tag": dry.get("track_tag"),
        "track_from_key": campaign_cfg["track"],
    }
    if dry.get("track_tag") not in (None, "Track " + campaign_cfg["track"]):
        result["flags"].append("dry_track_tag_disagrees_with_key")
    if dry.get("track") not in (None, campaign_cfg["track"]):
        result["flags"].append("dry_track_field_disagrees_with_key")
    same_cr_note = []
    for row in under_wf:
        same = [r for r in dry_rows if _close(r["CR"], row["CR"])]
        if not same:
            continue
        try:
            naive = C.compare(row, same[0])
        except ValueError:
            continue
        fair = C.compare(row, dry)
        if same[0]["_key"] != dry["_key"] and naive.get("cost_gain_all_engines") and not fair.get("cost_gain_all_engines"):
            same_cr_note.append(row["_key"])
    if same_cr_note:
        result["flags"].append({"same_cr_dry_would_overstate_gain": same_cr_note})
    scored = []
    for row in eligible_wet:
        compared = _public_compare(C, C.compare(row, dry))
        caps_row = order_cap_flags(row["fuel"], float(row["CR"]), caps)
        evidence = row.get("evidence_class") or "executed_row"
        item = {
            "_key": row["_key"],
            "w": row["w"],
            "CR": row["CR"],
            "W/F": wf_of(row),
            "wet_w_edge": abs(float(row["w"]) - max_w) <= 1e-12,
            "wet_cr_edge": abs(float(row["CR"]) - max_cr) <= 1e-9,
            "evidence_class": evidence,
            "mechanism": row.get("mechanism"),
            "flame_fit": row.get("flame_fit"),
            "fit_domain_validated": False,
            "compare": compared,
        }
        item.update(caps_row)
        item.update(LABELS)
        scored.append(item)
    result["scored"] = scored
    promoted = None
    if (best_row is not dry and best_cmp.get("engines") == 2 and best_cmp.get("cost_gain_all_engines")
            and sibling.get("ok", False)):
        match = next(item for item in scored if item["_key"] == best_row["_key"])
        promoted = {
            "_key": best_row["_key"],
            "w": best_row["w"],
            "CR": best_row["CR"],
            "dry_key": dry["_key"],
            "dry_CR": dry["CR"],
            "verdict": "COST GAIN",
            "model_cost_gain": True,
            "factory_cr_recommendation": "WITHHELD",
            "above_documented_order_cap": match["above_documented_order_cap"],
            "on_documented_order_cap": match["on_documented_order_cap"],
            "wet_w_edge": match["wet_w_edge"],
            "wet_cr_edge": match["wet_cr_edge"],
            "evidence_class": match["evidence_class"],
            "compare": match["compare"],
        }
        promoted.update(LABELS)
    result["promoted"] = promoted
    result["raw_best_key"] = None if raw_row is dry else raw_row.get("_key")
    result["status"] = "scored"
    result["reason"] = None if promoted else ("sibling_dry_mismatch" if not sibling.get("ok", False) else "no_promoted_cost_gain")
    if any(item["evidence_class"] != "executed_row" for item in scored):
        result["flags"].append("contains_non_executed_rows")
    return result


def sibling_status(C, dry, siblings: dict) -> dict:
    if not siblings:
        return {"ok": True, "state": "not_provided", "compared": 0}
    body = split_key(dry["_key"])["body"]
    compared = []
    for name, rows in siblings.items():
        match = None
        for row in rows:
            key = row.get("_key")
            if not isinstance(key, str) or ":" not in key:
                continue
            if key.split(":", 1)[1] == body and split_key(key)["w"] == "0.0":
                match = row
                break
        if match is None:
            compared.append({"file": name, "state": "no_matching_w0"})
            continue
        eta_d = rel_gap(match.get("gross_indicated_efficiency"), dry.get("gross_indicated_efficiency"))
        imep_d = rel_gap(match.get("IMEP_Pa"), dry.get("IMEP_Pa"))
        gap = max(x for x in (eta_d, imep_d) if x is not None) if (eta_d is not None or imep_d is not None) else None
        state = "match"
        if gap is None:
            state = "incomparable"
        elif gap > C.POWER_TOL_REL:
            state = "mismatch"
        elif gap > 0:
            state = "within_noise"
        compared.append({"file": name, "_key": match.get("_key"), "state": state, "relative_gap": gap})
    bad = [c for c in compared if c["state"] in ("mismatch", "incomparable")]
    return {"ok": not bad, "state": "checked", "compared": len(compared), "files": compared}


def rel_gap(a, b):
    if a is None or b is None:
        return None
    return abs(float(a) - float(b)) / max(abs(float(b)), 1e-30)


def atomic_write(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def group_file(outdir: Path, gid: str) -> Path:
    safe = gid.replace("|", "__")
    return outdir / "by-group" / (safe + ".json")


def prepare_outdir(outdir: Path, resume: bool) -> dict:
    checkpoint_path = outdir / "checkpoint.json"
    if resume:
        if not checkpoint_path.is_file():
            raise SystemExit("resume requested but no checkpoint in %s" % outdir)
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        if checkpoint.get("schema") != SCHEMA:
            raise SystemExit("checkpoint schema mismatch")
        return checkpoint
    if outdir.exists():
        raise SystemExit("refusing to write into existing directory %s" % outdir)
    outdir.mkdir(parents=True)
    (outdir / "by-group").mkdir()
    return {"schema": SCHEMA, "run_id": str(uuid.uuid4()), "completed_groups": [], "input_sha256": {}}


def hashes_match(checkpoint: dict, current: dict) -> bool:
    previous = checkpoint.get("input_sha256") or {}
    return previous == current


def render_summary(meta: dict, groups: list) -> str:
    promoted = [g for g in groups if g.get("promoted")]
    reasons = {}
    for g in groups:
        if g.get("status") != "scored" or not g.get("promoted"):
            reasons[g.get("reason") or g.get("status")] = reasons.get(g.get("reason") or g.get("status"), 0) + 1
    lines = [
        "# AH26/BH26 matched-dry cost-per-mile rescore",
        "",
        "Executed model arithmetic on existing rows. Not validated. Not an independent experiment.",
        "M03 and M03-CRN remain two engines from the same toolchain.",
        "Factory CR recommendations: WITHHELD. Documented order caps are unchanged.",
        "Absolute dollars per mile are not compared across fuels.",
        "",
        "run_id: %s" % meta["run_id"],
        "groups: %d" % len(groups),
        "promoted model cost gains: %d" % len(promoted),
        "synthetic_or_non_executed: %s" % meta.get("contains_non_executed"),
        "",
        "## Withheld or not promoted",
        "",
    ]
    for reason, count in sorted(reasons.items()):
        lines.append("- %s: %d" % (reason, count))
    lines += ["", "## Promoted rows (model cost gain only; factory CR still withheld)", ""]
    if not promoted:
        lines.append("None.")
    else:
        lines.append("| campaign | key | dry CR | wet CR | w | cost/mile % M03/CRN | power % M03/CRN | flags |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for g in promoted:
            p = g["promoted"]
            cmp_ = p["compare"]
            def pair(name):
                a = (cmp_.get("m03") or {}).get(name)
                b = (cmp_.get("crn") or {}).get(name)
                def fmt(v):
                    return "-" if v is None else "%+.3f" % v
                return "%s / %s" % (fmt(a), fmt(b))
            flags = []
            if p["wet_w_edge"]:
                flags.append("w edge")
            if p["wet_cr_edge"]:
                flags.append("CR edge")
            if p["above_documented_order_cap"]:
                flags.append("above order cap")
            if p["on_documented_order_cap"]:
                flags.append("on order cap")
            lines.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
                g["campaign"], p["_key"], p["dry_CR"], p["CR"], p["w"],
                pair("cost_per_mile_pct"), pair("power_change_pct"), ", ".join(flags) or "-"))
    lines += [
        "",
        "Fit domains are not established by this rescore. Mechanism ids are copied from the executed rows.",
        "A grid-edge promotion is not an interior optimum.",
        "",
    ]
    return "\n".join(lines)


def run(jobs: Path, config: dict, allow_path: Path, outdir: Path, resume: bool = False,
         expect_full_grid: bool = False, reference_blob: str = "") -> dict:
    if int(config.get("workers", 1)) != 1:
        raise SystemExit("resource cap: workers must be 1")
    C = load_cost()
    cost_info = check_cost_module(C, reference_blob or config["cost_reference"]["blob_sha1"])
    if not cost_info["constants_ok"] or not cost_info["blob_matches_reference"]:
        raise SystemExit("refusing to score with a cost module that does not match the reviewed reference: %s" % json.dumps(cost_info, sort_keys=True))
    campaigns = config["campaigns"]
    allow = load_allow(allow_path, campaigns)
    if expect_full_grid:
        assert_full_grid(allow, config["expected_full_grid"])
    inputs = {}
    current_hashes = {"allow_keys": sha256_file(allow_path), "config_stage": config["stage_id"]}
    for name, cfg in campaigns.items():
        path = jobs / cfg["file"]
        if not path.is_file():
            raise SystemExit("missing input %s" % path)
        current_hashes[name] = sha256_file(path)
        inputs[name] = path
    siblings = {}
    for name, cfg in campaigns.items():
        loaded = {}
        for filename in cfg.get("sibling_dry_files") or []:
            path = jobs / filename
            if path.is_file():
                current_hashes["sibling:" + filename] = sha256_file(path)
                loaded[filename] = [r for r in read_jsonl(path) if isinstance(r, dict)]
        siblings[name] = loaded
    checkpoint = prepare_outdir(outdir, resume)
    if resume and not hashes_match(checkpoint, current_hashes):
        raise SystemExit("resume refused: input checksums changed")
    checkpoint["input_sha256"] = current_hashes
    checkpoint["cost"] = cost_info
    atomic_write(outdir / "checkpoint.json", json.dumps(checkpoint, indent=2, sort_keys=True) + "\n")
    rows_by_key = {}
    quarantined = []
    seen_duplicate = set()
    for name, path in inputs.items():
        kept, bad = dedup_rows(read_jsonl(path), name)
        quarantined.extend(bad)
        cfg = campaigns[name]
        for row in kept:
            key = row["_key"]
            try:
                parts = split_key(key)
            except ValueError as exc:
                quarantined.append({"campaign": name, "reason": "bad_key", "_key": key, "detail": str(exc)})
                continue
            problems = identity_problems(row, parts, cfg)
            if key not in allow["by_key"] or allow["by_key"][key].split("|", 1)[0] != name:
                quarantined.append({"campaign": name, "reason": "key_not_in_allow_list", "_key": key})
                continue
            if problems:
                quarantined.append({"campaign": name, "reason": "identity", "_key": key, "problems": problems})
                continue
            if key in rows_by_key:
                if key not in seen_duplicate:
                    quarantined.append({"campaign": name, "reason": "duplicate_across_inputs", "_key": key})
                    seen_duplicate.add(key)
                continue
            rows_by_key[key] = row
    atomic_write(outdir / "quarantined.json", json.dumps(quarantined, indent=2, sort_keys=True) + "\n")
    for gid in sorted(allow["by_group"]):
        path = group_file(outdir, gid)
        if resume and path.is_file():
            continue
        campaign = gid.split("|", 1)[0]
        result = score_group(
            C, gid, rows_by_key, allow["by_group"][gid], campaigns[campaign],
            config.get("order_cap_CR") or {}, float(config["wf_promotion_max"]), siblings.get(campaign) or {},
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(path, json.dumps(result, indent=2, sort_keys=True) + "\n")
        checkpoint.setdefault("completed_groups", [])
        if gid not in checkpoint["completed_groups"]:
            checkpoint["completed_groups"].append(gid)
            checkpoint["completed_groups"].sort()
        atomic_write(outdir / "checkpoint.json", json.dumps(checkpoint, indent=2, sort_keys=True) + "\n")
    (outdir / "by-group").mkdir(exist_ok=True)
    all_groups = []
    for path in sorted((outdir / "by-group").glob("*.json")):
        all_groups.append(json.loads(path.read_text(encoding="utf-8")))
    all_groups.sort(key=lambda g: g["group"])
    scored_lines = []
    ledger = []
    for group in all_groups:
        ledger.append({"group": group["group"], "reason": group.get("reason"), "status": group.get("status")})
        for item in group.get("scored") or []:
            scored_lines.append(dict(item, group=group["group"]))
    atomic_write(outdir / "groups.jsonl", "".join(json.dumps({k: v for k, v in g.items() if k != "scored"}, sort_keys=True) + "\n" for g in all_groups))
    atomic_write(outdir / "scored.jsonl", "".join(json.dumps(item, sort_keys=True) + "\n" for item in scored_lines))
    atomic_write(outdir / "ledger.jsonl", "".join(json.dumps(item, sort_keys=True) + "\n" for item in ledger))
    checkpoint["completed_groups"] = [g["group"] for g in all_groups]
    atomic_write(outdir / "checkpoint.json", json.dumps(checkpoint, indent=2, sort_keys=True) + "\n")
    classes = sorted({(row.get("evidence_class") or "executed_row") for row in rows_by_key.values()})
    meta = {
        "schema": SCHEMA,
        "run_id": checkpoint["run_id"],
        "stage_id": config["stage_id"],
        "workers": 1,
        "combustion_runs": 0,
        "publish": False,
        "validation_status": "executed_not_validated",
        "independent_validation": False,
        "executed_does_not_mean_validated": True,
        "factory_cr_recommendation": "WITHHELD",
        "cost": cost_info,
        "input_sha256": current_hashes,
        "groups": len(all_groups),
        "promoted": sum(1 for g in all_groups if g.get("promoted")),
        "quarantined": len(quarantined),
        "evidence_classes": classes,
        "contains_non_executed": any(item != "executed_row" for item in classes),
        "science_claim": False,
        "exit_meaning": "rescore_finished_see_summary_not_a_validation",
    }
    atomic_write(outdir / "run_meta.json", json.dumps(meta, indent=2, sort_keys=True) + "\n")
    atomic_write(outdir / "SUMMARY.md", render_summary(meta, all_groups))
    return meta


def main(argv: list) -> int:
    if "--self-check" in argv:
        parser = argparse.ArgumentParser()
        parser.add_argument("--self-check", action="store_true")
        parser.add_argument("--config", required=True)
        args = parser.parse_args(argv)
        config = json.loads(Path(args.config).read_text(encoding="utf-8"))
        info = self_check(config["cost_reference"]["blob_sha1"])
        json.dump(info, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    parser = argparse.ArgumentParser(description="AH26/BH26 matched-dry cost rescore")
    parser.add_argument("--config", required=True)
    parser.add_argument("--jobs", required=True)
    parser.add_argument("--allow-keys", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--expect-full-grid", action="store_true")
    args = parser.parse_args(argv)
    if args.workers != 1:
        raise SystemExit("resource cap: workers must be 1")
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    meta = run(
        Path(args.jobs), config, Path(args.allow_keys), Path(args.outdir),
        resume=args.resume, expect_full_grid=args.expect_full_grid,
        reference_blob=config["cost_reference"]["blob_sha1"],
    )
    print(json.dumps({"run_id": meta["run_id"], "promoted": meta["promoted"], "groups": meta["groups"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except BrokenPipeError:
        raise SystemExit(0)
