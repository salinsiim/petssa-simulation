import os
import csv
import random

from vehicles.Demand import Demand

path = os.environ['TS_SIMULATION']


def generate(traffic_type):
    generate_traffic(traffic_type)


def generate_traffic(traffic_type):
    random.seed(42)
    path = os.environ['TS_SIMULATION']
    filepath = path + "/input/map/vehicle-" + traffic_type + ".trips.xml"
    mode = 'a' if os.path.exists(filepath) else 'w'
    with open(filepath, mode) as routes:
        print_header(routes)
        print_trips(routes, 3600, read_demands(traffic_type))
        print_footer(routes)


def print_trips(routes, number_of_steps, demands):
    veh_number = 0
    for step in range(number_of_steps):
        for d in demands:
            demand_per_second = d.demand_per_second
            origin = d.origin
            destination = d.destination

            if random.uniform(0, 1) < demand_per_second:
                print('\t<trip id="veh-%i" type="veh_passenger" depart="%i" departLane="best" from="%s" to="%s"/>'
                      % (veh_number, step, origin, destination), file=routes)
                veh_number += 1


def read_demands(traffic_type):
    demand_path = path + '/vehicles/input/map/vehicles-' + traffic_type + '.csv'
    demands = []
    with open(demand_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        counter = 0
        for row in reader:
            if counter > 0:
                route = str(row[0])
                origin = str(row[1])
                destination = str(row[2])
                demand_per_second = float(row[3])
                demands.append(Demand(route, origin, destination, demand_per_second))
            counter += 1
    return demands


def print_header(routes):
    print("<routes>", file=routes)
    print('\t<vType id="veh_passenger" vClass="passenger"/>', file=routes)


def print_footer(routes):
    print("</routes>", file=routes)
