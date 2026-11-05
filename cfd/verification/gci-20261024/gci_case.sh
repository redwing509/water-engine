#!/bin/bash
# usage: gci_case.sh <casedir> <nprocs>   (runs INSIDE opencfd/openfoam-default:2512 as root)
# Same steps as cfd/run_case.sh + a2_case.sh (blockMesh, decomposePar simple n(1 N 1), sprayFoam -parallel).
. /usr/lib/openfoam/openfoam2512/etc/bashrc >/dev/null 2>&1 || true
cd "$1" || exit 2; N=${2:-4}
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
[ -d 0 ] || cp -r 0.orig 0
sed -i "s/^numberOfSubdomains .*/numberOfSubdomains $N;/; s/^\( *n  *\)(1 [0-9]* 1);/\1(1 $N 1);/" system/decomposeParDict
start=$(date +%s); echo "start $(date -u +%FT%TZ) ranks=$N" > run.status
blockMesh > log.blockMesh 2>&1 || { echo "blockMesh failed" >> run.status; exit 3; }
grep -m1 "nCells" log.blockMesh >> run.status
decomposePar -force > log.decomposePar 2>&1 || { echo "decomposePar failed" >> run.status; exit 4; }
mpirun --allow-run-as-root --oversubscribe -np $N sprayFoam -parallel > log.sprayFoam 2>&1; rc=$?
echo "runtime_s $(( $(date +%s)-start ))" > runtime.txt
last=$(grep "^Time = " log.sprayFoam | tail -1); nan=$(grep -ciE "\bnan\b" log.sprayFoam)
echo "end $(date -u +%FT%TZ) rc=$rc last='$last' nan_lines=$nan" >> run.status
if [ $rc -eq 0 ]; then reconstructPar -latestTime > log.reconstructPar 2>&1 && rm -rf processor*; fi
exit $rc
