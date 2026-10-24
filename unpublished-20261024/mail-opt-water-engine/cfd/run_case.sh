#!/bin/bash
# usage: run_case.sh <casedir> <nprocs>
set -e
. /usr/lib/openfoam/openfoam2512/etc/bashrc >/dev/null 2>&1 || true
cd "$1"; N=${2:-6}
[ -d 0 ] || cp -r 0.orig 0
blockMesh > log.blockMesh 2>&1
decomposePar -force > log.decomposePar 2>&1
start=$(date +%s)
mpirun --oversubscribe --allow-run-as-root -np $N sprayFoam -parallel > log.sprayFoam 2>&1
echo "runtime_s $(( $(date +%s)-start ))" > runtime.txt
