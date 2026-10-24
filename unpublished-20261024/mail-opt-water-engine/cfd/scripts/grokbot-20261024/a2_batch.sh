#!/bin/bash
# A2 mail batch: C2H5OH (Tc clamp) + C2H5OH ReitzDiwakar concurrently at 4 ranks, then EBLEND at 4 ranks.
R=/opt/water-engine/cfd/runs; S=/opt/water-engine/cfd/scripts/grokbot-20261024
bash $S/a2_case.sh $R/A2-C2H5OH-mail 4 & p1=$!
bash $S/a2_case.sh $R/A2-C2H5OH-RD-mail 4 & p2=$!
wait $p1; r1=$?; wait $p2; r2=$?
bash $S/a2_case.sh $R/A2-EBLEND-mail 4; r3=$?
echo "A2-C2H5OH-mail rc=$r1 A2-C2H5OH-RD-mail rc=$r2 A2-EBLEND-mail rc=$r3"
[ $r1 -eq 0 ] && [ $r2 -eq 0 ] && [ $r3 -eq 0 ]
