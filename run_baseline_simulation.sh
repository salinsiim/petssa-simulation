#!/bin/sh

sumo -c $TS_SIMULATION/input/tammsaare_sopruse/peak.sumo.cfg --tripinfo-output $TS_SIMULATION/output/tammsaare_sopruse/baseline/trip_info.xml --device.emissions.probability 1.0 --duration-log.statistics --log $TS_SIMULATION/output/tammsaare_sopruse/baseline/statistics.txt

python $SUMO_HOME/tools/xml/xml2csv.py "${TS_SIMULATION}/output/tammsaare_sopruse/baseline/trip_info.xml" --output "${TS_SIMULATION}/output/tammsaare_sopruse/baseline/result.csv"

python $TS_SIMULATION/output/aggregate_output.py --input "${TS_SIMULATION}/output/tammsaare_sopruse/baseline/result.csv" --output "${TS_SIMULATION}/output/tammsaare_sopruse/baseline/aggregated-result.csv"
