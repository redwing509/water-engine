#!/bin/bash
# parse/first-steps smoke test on scratch copies in /tmp (inside container)
S=/opt/water-engine/cfd/scripts/grokbot-20261024; T=/smoke
for c in A2-C2H5OH-mail A2-EBLEND-mail M13-US20-coarse-mail; do rm -rf $T/$c; cp -r /opt/water-engine/cfd/runs/$c $T/$c; done
ENDT=2e-05 timeout 600 bash $S/a2_case.sh $T/A2-C2H5OH-mail 2; echo "A2 smoke rc=$?"; tail -2 $T/A2-C2H5OH-mail/run.status
ENDT=2e-05 timeout 600 bash $S/a2_case.sh $T/A2-EBLEND-mail 2; echo "A2E smoke rc=$?"; tail -1 $T/A2-EBLEND-mail/run.status
END0=0.00002 END1=0.00002 END2=0.00002 timeout 900 bash $S/m13_case.sh $T/M13-US20-coarse-mail; echo "M13 smoke rc=$?"; cat $T/M13-US20-coarse-mail/run.status
grep -m3 -iE "bounded|nOuter|Selecting.*liquid|C2H5OH" $T/A2-C2H5OH-mail/log.sprayFoam | head -3
grep -iE "error|FATAL" -m5 $T/*/log.* | head
