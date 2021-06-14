# PETSSA in Tammsaare-Sõpruse
Priority-driven Enhanced Traffic Signal Scheduling Algorithm in Tammsaare-Sõpruse

## Set up
Add SUMO_HOME to env variable
https://sumo.dlr.de/docs/Basics/Basic_Computer_Skills.html#sumo_home

Add TS_SIMULATION to env variable
```
export TS_SIMULATION = ${clone_path}/simulation
```


## Commands
Run PETSSA simulation with GUI: 
```
sh run_petssa.sh
```
Run current Tammsaare-Sõpruse intersection traffic signal logic simulation with GUI: 
```
sh run_baseline.sh
```
