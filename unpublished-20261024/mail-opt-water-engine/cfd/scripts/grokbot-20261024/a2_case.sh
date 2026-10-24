#!/bin/bash
# usage: a2_case.sh <casedir> <nprocs>   (inside opencfd/openfoam-default:2512, as root)
. /usr/lib/openfoam/openfoam2512/etc/bashrc >/dev/null 2>&1 || true
cd "$1" || exit 2; N=${2:-4}; ENDT=${ENDT:-}
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
[ -d 0 ] || cp -r 0.orig 0
[ -n "$ENDT" ] && sed -i "s/^endTime .*/endTime         $ENDT;/" system/controlDict
sed -i "s/^numberOfSubdomains .*/numberOfSubdomains $N;/; s/^\( *n  *\)(1 [0-9]* 1);/\1(1 $N 1);/" system/decomposeParDict
start=$(date +%s); echo "start $(date -u +%FT%TZ)" > run.status
blockMesh > log.blockMesh 2>&1 || { echo "blockMesh failed" >> run.status; exit 3; }
decomposePar -force > log.decomposePar 2>&1 || { echo "decomposePar failed" >> run.status; exit 4; }
mpirun --allow-run-as-root --oversubscribe -np $N sprayFoam -parallel > log.sprayFoam 2>&1; rc=$?
echo "runtime_s $(( $(date +%s)-start ))" > runtime.txt
last=$(grep "^Time = " log.sprayFoam | tail -1)
nan=$(grep -ciE "\bnan\b" log.sprayFoam)
echo "end $(date -u +%FT%TZ) rc=$rc last='$last' nan_lines=$nan" >> run.status
[ $rc -eq 0 ] && reconstructPar -latestTime > log.reconstructPar 2>&1
exit $rc
