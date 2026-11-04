#!/bin/bash
# Grok Bot takeover 2026-10-25: resume dryevap_baseline (all remaining phases) fully detached.
cd /workspace/wt0915
export PYTHONUNBUFFERED=1
/workspace/venv-we09/bin/python -m sims.03_engine_cycle.dryevap_baseline run --workers 4 --out points_resume.jsonl
echo "EXIT $? $(date)"
