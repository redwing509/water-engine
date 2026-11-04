#!/bin/bash
# Grok Bot detached finisher (2026-10-25) for water-engine-dryevap-baseline-20261025-1420.
# Waits for the resume run, then: tests -> report -> commit -> push track-ab/box-20261025 -> PR 10 comment ->
# TRACKS.md section -> result note. Never touches main. Log: results/dryevap/finish.log (gitignored *.log).
set -u
cd /workspace/wt0915
PY=/workspace/venv-we09/bin/python
RES=/workspace/self-jobs/water-engine-dryevap-baseline-20261025-1420.result.md
RUNPID=${1:-770859}
while kill -0 "$RUNPID" 2>/dev/null; do sleep 60; done
echo "run finished $(date)"; tail -2 results/dryevap/run_resume.log
LEFT=$($PY - <<'P' 2>/dev/null | tail -1
import sys, json, importlib; sys.path.insert(0, '.')
D = importlib.import_module("sims.03_engine_cycle.dryevap_baseline")
done = {json.loads(l)["_job"] for f in D.OUT.glob("points*.jsonl") for l in open(f)}
print(sum(1 for t in D.jobs() if D.jkey(t) not in done))
P
)
echo "jobs left: $LEFT"
if [ "$LEFT" != "0" ]; then
  sed -i "s/^STATUS: .*/STATUS: NEEDS_ATTENTION (finisher: $LEFT jobs not done after the resume run exited; see results\/dryevap\/run_resume.log)/" "$RES"
  exit 1
fi
[ -f results/dryevap/crn_cache.json ] || { [ -f /tmp/dryevap_preview/crn_cache.json ] && cp /tmp/dryevap_preview/crn_cache.json results/dryevap/crn_cache.json; }
$PY -m pytest -q -p no:warnings tests/test_m03_fuel_evap.py tests/test_energy_audit.py::test_quick_smoke tests/test_cost.py > results/dryevap/pytest.txt 2>&1; TESTRC=$?
tail -3 results/dryevap/pytest.txt
$PY -m sims.03_engine_cycle.dryevap_report > results/dryevap/report_stdout.txt 2>&1 || { sed -i "s/^STATUS: .*/STATUS: NEEDS_ATTENTION (report failed, see results\/dryevap\/report_stdout.txt)/" "$RES"; exit 1; }
git add engines/m03_cantera/engine.py sims/03_engine_cycle/run.py sims/03_engine_cycle/dryevap_baseline.py \
  sims/03_engine_cycle/dryevap_report.py tests/test_m03_fuel_evap.py results/dryevap/*.jsonl results/dryevap/*.csv \
  results/dryevap/REPORT.md results/dryevap/crn_cache.json results/dryevap/pytest.txt results/dryevap/*.sh
git commit -q -m "dryevap baseline check of PR 10 (Claude job water-engine-dryevap-baseline-20261025-1420): Module 03 optional fuel evaporation (intake DEI / port DEP), M03-CRN fuel latent credit, dry-evap baselines CH3OH/C2H5OH/PRF87/E85 normal+hot, symmetric wet re-runs, any-CA50 sensitivity, cost vs new baselines; resumed by Grok Bot after the worker died; NOT validated (pytest rc $TESTRC)"
git push origin HEAD:track-ab/box-20261025 > results/dryevap/push.txt 2>&1; PUSHRC=$?
SHA=$(git rev-parse --short HEAD)
URL="https://github.com/redwing509/water-engine/commit/$(git rev-parse HEAD)"
if [ $PUSHRC -eq 0 ]; then
  { echo "## Dry-evap baseline check (commit $SHA, Claude job water-engine-dryevap-baseline-20261025-1420)"; echo;
    echo "Executed on the box, M03-CRN cross-check; **NOT validated**. Finished by Grok Bot after the original worker died. Full tables: results/dryevap/REPORT.md, headline_rows.csv, baselines.csv."; echo;
    cat results/dryevap/SUMMARY.md 2>/dev/null || sed -n 1,80p results/dryevap/REPORT.md; } > /tmp/dryevap_pr_comment.md
  gh pr comment 10 --repo redwing509/water-engine --body-file /tmp/dryevap_pr_comment.md > results/dryevap/pr_comment.txt 2>&1
fi
T=/workspace/water-engine-tracks/TRACKS.md
cp "$T" "$T.bak-20261025-dryevap"
$PY - "$T" "$SHA" <<'P'
import sys, pathlib
t, sha = pathlib.Path(sys.argv[1]), sys.argv[2]
s = pathlib.Path("/workspace/wt0915/results/dryevap/SUMMARY.md")
body = s.read_text() if s.exists() else "(see results/dryevap/REPORT.md)"
sec = (f"\n## Dry-evap baseline check of PR 10 (Track A + Track B; commit {sha} on track-ab/box-20261025; EXECUTED, M03-CRN cross-check, NOT validated)\n\n" + body + "\n")
txt = t.read_text()
i = txt.find("\n## Best so far")
t.write_text(txt[:i] + sec + txt[i:] if i >= 0 else txt + sec)
P
sed -i "s/^STATUS: .*/STATUS: DONE (finisher $(date '+%Y-%m-%d %H:%M %Z'); commit $SHA pushed rc=$PUSHRC; pytest rc=$TESTRC)/" "$RES"
{ echo; echo "## Finisher output ($(date '+%Y-%m-%d %H:%M %Z'))"; echo "- commit: $URL (push rc $PUSHRC)"; echo "- PR 10 comment: $(cat results/dryevap/pr_comment.txt 2>/dev/null)";
  echo "- pytest: $(tail -1 results/dryevap/pytest.txt)"; echo "- TRACKS.md updated (backup TRACKS.md.bak-20261025-dryevap)"; echo; cat results/dryevap/SUMMARY.md 2>/dev/null; } >> "$RES"
echo "finisher done $(date)"
