#!/usr/bin/env bash
# TTL_MIN=720
# LOCK=box-173-pr10fair-C2H5OH-hot
# RESOURCE=water-engine
# CORES=2
# MEM_MB=1200
# EST_H=4
# DESC=PR 10 fair high-CR rerun (James t282u + 2:15 PM factory-CR update): C2H5OH hot, humid_evap + liquid wet at w grid, CR 10-26 vs dry DEI CR 8-20 (own knock-limited CR each), M03 + CRN -> /workspace/self-jobs/pr10-fair-highcr/C2H5OH-hot. Executed, not validated.
set -uo pipefail
cd /workspace/self-jobs/pr10-fair-highcr
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MPLBACKEND=Agg FUEL=C2H5OH REGIME=hot
for st in points crn; do nice -n 15 /workspace/venv-we09/bin/python runs.py $st 2 > C2H5OH-hot.$st.log 2>&1; rc=$?; echo "$(date -Is) $st rc=$rc"; [ $rc -eq 0 ] || exit $rc; done
/workspace/venv-we09/bin/python summary.py > summary.log 2>&1; echo summary rc=$?
