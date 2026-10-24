#!/bin/bash
# A1-BLEND-fine grid check launcher (runs inside container as root)
set -e
cd /opt/water-engine/cfd
bash run_case.sh runs/A1-BLEND-fine 6
echo "cfd done rc=0 $(date -u +%FT%TZ)" > /opt/water-engine/cfd/cfd_run.log
