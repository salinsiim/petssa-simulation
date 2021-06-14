#!/bin/sh
pids=""

AGG_PREFIX="aggregated_result"

PRIORITY=True
TYPE=peak
for maxGreen in 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
do
	for mgDiff in 1 2 3 4 5 6 7
	do
		python $TS_SIMULATION/simulation.py --type ${TYPE} --max-green ${maxGreen} --mg-diff ${mgDiff} --priority ${PRIORITY} --nogui
		pids="$pids $!"
	done
done

wait $pids

pids=""
for maxGreen in 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
do
	for mgDiff in 1 2 3 4 5 6 7
	do
		python $SUMO_HOME/tools/xml/xml2csv.py "${TS_SIMULATION}/output/tammsaare_sopruse/petssa/trip_info-${TYPE}-${maxGreen}-${mgDiff}-${PRIORITY}.xml" --output "${TS_SIMULATION}/output/tammsaare_sopruse/petssa/result-${TYPE}-${maxGreen}-${mgDiff}-${PRIORITY}.csv"
		pids="$pids $!"
	done
done

wait $pids

pids=""
for maxGreen in 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
do
	for mgDiff in 1 2 3 4 5 6 7
	do
		python $TS_SIMULATION/output/aggregate_output.py --input "${TS_SIMULATION}/output/tammsaare_sopruse/petssa/result-${TYPE}-${maxGreen}-${mgDiff}-${PRIORITY}.csv" --output "${TS_SIMULATION}/output/tammsaare_sopruse/petssa/${AGG_PREFIX}-${TYPE}-${maxGreen}-${mgDiff}-${PRIORITY}.csv"
		pids="$pids $!"
	done
done

wait $pids

PRIORITY=False
TYPE=peak
for maxGreen in 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
do
	for mgDiff in 1 2 3 4 5 6 7
	do
		python $TS_SIMULATION/simulation.py --type ${TYPE} --nogui --max-green ${maxGreen} --mg-diff ${mgDiff}
		pids="$pids $!"
	done
done

wait $pids

pids=""
for maxGreen in 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
do
	for mgDiff in 1 2 3 4 5 6 7
	do
		python $SUMO_HOME/tools/xml/xml2csv.py "${TS_SIMULATION}/output/tammsaare_sopruse/petssa/trip_info-${TYPE}-${maxGreen}-${mgDiff}-${PRIORITY}.xml" --output "${TS_SIMULATION}/output/tammsaare_sopruse/petssa/result-${TYPE}-${maxGreen}-${mgDiff}-${PRIORITY}.csv"
		pids="$pids $!"
	done
done

wait $pids

pids=""
for maxGreen in 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
do
	for mgDiff in 1 2 3 4 5 6 7
	do
		python $TS_SIMULATION/output/aggregate_output.py --input "${TS_SIMULATION}/output/tammsaare_sopruse/petssa/result-${TYPE}-${maxGreen}-${mgDiff}-${PRIORITY}.csv" --output "${TS_SIMULATION}/output/tammsaare_sopruse/petssa/${AGG_PREFIX}-${TYPE}-${maxGreen}-${mgDiff}-${PRIORITY}.csv"
		pids="$pids $!"
	done
done

wait $pids

# Generate report
REP_INPUT_FOLDER="${TS_SIMULATION}/output/tammsaare_sopruse/petssa/"
REP_OUTPUT_FILE="${TS_SIMULATION}/output/tammsaare_sopruse/petssa/report.csv"
python $TS_SIMULATION/output/generate_report.py --folder ${REP_INPUT_FOLDER} --prefix ${AGG_PREFIX} --output ${REP_OUTPUT_FILE}