#!/bin/bash
# r340 smoke (0.1 ms, 12 ranks) - Grok Bot, job water-engine-mail-20261025-1830, Track A
B=/opt/water-engine/cfd/gci-20261024; R=$B/runs; IMG=opencfd/openfoam-default:2512
docker run --rm --name gci-A2-BLEND-r340-smoke --network none --cap-drop ALL --security-opt no-new-privileges:true \
  --pids-limit 1024 --cpus 12 --memory 34g --memory-swap 34g -v $B:$B $IMG \
  nice -n 19 bash $B/gci_case.sh $R/A2-BLEND-r340-smoke 12 > $R/A2-BLEND-r340-smoke.docker.log 2>&1
