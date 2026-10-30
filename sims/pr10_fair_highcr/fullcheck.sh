#!/bin/bash
# [Grok Bot 2026-10-29 20:35 PDT] second-model check: full CRECK end-gas on limit-bracket rows (BRACKET=1), humid first. Once, never retried.
cd $(dirname $0); P=/opt/water-engine/.venv/bin/python
for d in CH3OH-hot-humid_evap C2H5OH-hot-humid_evap CH3OH-normal-humid_evap C2H5OH-normal-humid_evap CH3OH-hot-liquid C2H5OH-hot-liquid CH3OH-normal-liquid C2H5OH-normal-liquid; do
  F=${d%%-*}; R=$(echo $d|cut -d- -f2); I=${d#*-*-}
  FUEL=$F REGIME=$R INTAKE=$I BRACKET=1 $P runs.py full 12 > logs/$d-full.log 2>&1; touch logs/$d.FULL
done
touch logs/ALL.FULL
