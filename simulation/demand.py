#!/usr/bin/env python
import optparse

from traffic_types import PEAK, OFFPEAK
from vehicles import generate as generate_vehicles
from buses import generate as generate_buses
from pedestrians import generate as generate_pedestrians

def generate_demand(type):
    generate_vehicles(type, "map")
    generate_buses(type, "map")
    generate_pedestrians(type, "map")

if __name__ == "__main__":
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--type", action="store", type="string", dest="type", help=PEAK + " or " + OFFPEAK)
    options, args = opt_parser.parse_args()
    generate_demand(options.type)
    print("Generated vehicles, buses and pedestrians for {0} traffic", options.type)