#!/usr/bin/env python
import os
import sys
import optparse

if 'SUMO_HOME' in os.environ and 'TS_SIMULATION' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variables 'SUMO_HOME', 'TS_SIMULATION'")

from sumolib import checkBinary
import traci

from traffic_types import PEAK, OFFPEAK
from vehicles import generate as generate_vehicles
from buses import generate as generate_buses
from pedestrians import generate as generate_pedestrians

from map_controllers.i1 import control as control_tln_i1


def simulate_tln(max_green, max_green_diff, priority):
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        control_tln_i1(step, max_green, max_green_diff, priority)
        traci.simulationStep()
        step += 1
    traci.close()
    sys.stdout.flush()


def options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")
    opt_parser.add_option("--new", action="store_true", default=False, help="generate new trip files")
    opt_parser.add_option("--priority", action="store_true", default=False, help="run with priority")
    opt_parser.add_option("--type", action="store", type="string", dest="type", help=PEAK + " or " + OFFPEAK)
    opt_parser.add_option("--max-green", action="store", type="int", dest="max_green", help="max green in seconds")
    opt_parser.add_option("--mg-diff", action="store", type="int", dest="mg_diff", help="max green diff in seconds")
    options, args = opt_parser.parse_args()
    return options


if __name__ == "__main__":
    options = options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    if options.new:
        generate_vehicles(options.type, "map")
        generate_buses(options.type, "map")
        generate_pedestrians(options.type, "map")

    config_name = ""
    if options.type == PEAK:
        config_name = PEAK + ".sumo.cfg"
    elif options.type == OFFPEAK:
        config_name = OFFPEAK + ".sumo.cfg"

    path = os.environ['TS_SIMULATION']
    identifier = options.type + "-" + str(options.max_green) + "-" + str(options.mg_diff) + "-" + str(options.priority)

    traci.start([sumoBinary, "-c", path + "/input/map/" + config_name, "--tripinfo-output",
                 path + "/output/map/petssa/trip_info-" + identifier + ".xml",
                 "--device.emissions.probability", "1.0", "--duration-log.statistics", "--log", path + "/output/map/petssa/statistics-" + identifier + ".txt"])
    print("Simulating Tammsaare-Sõpruse %s with MAX_GREEN: %s, MG_DIFF: %s, PRIORITY: %s" % (options.type, options.max_green, options.mg_diff, options.priority))
    simulate_tln(options.max_green, options.mg_diff, options.priority)
    print("Simulation completed")
