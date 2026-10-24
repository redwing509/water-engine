#!/bin/bash
# M13 mail batch: US20 and CARB60 runs (precursor from t=0, see m13_case.sh) concurrently, 4 ranks each (8 cores total).
R=/opt/water-engine/cfd/runs; S=/opt/water-engine/cfd/scripts/grokbot-20261024
bash $S/m13_case.sh $R/M13-US20-coarse-mail & p1=$!
bash $S/m13_case.sh $R/M13-CARB60-coarse-mail & p2=$!
wait $p1; r1=$?; wait $p2; r2=$?
echo "M13-US20-coarse-mail rc=$r1 M13-CARB60-coarse-mail rc=$r2"
[ $r1 -eq 0 ] && [ $r2 -eq 0 ]
