import os
import csv
import random

from pedestrians.Demand import Demand

path = os.environ['TS_SIMULATION']


def generate(traffic_type, city):
    generate_pedestrians_traffic(city)


def generate_pedestrians_traffic(city):
    random.seed(42)
    path = os.environ['TS_SIMULATION']
    filepath = path + "/input/" + city + "/pedestrians.trips.xml"
    mode = 'a' if os.path.exists(filepath) else 'w'
    with open(filepath, mode) as routes:
        print_header(routes)
        print_pedestrians_trips(routes, 3600, read_demands(city))
        print_footer(routes)


def read_demands(city):
    demands = []
    demand_path = path + '/pedestrians/input/' + city + '/pedestrians.csv'
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


def print_pedestrians_trips(routes, number_of_steps, demands):
    ped_number = 0
    for step in range(number_of_steps):
        for d in demands:
            demand_per_second = d.demand_per_second
            origin = d.origin
            destination = d.destination

            if random.uniform(0, 1) < demand_per_second:
                print('\t<person id="ped-%i" depart="%i">' % (ped_number, step), file=routes)
                print('\t\t<walk from="%s" to="%s"/>' % (origin, destination), file=routes)
                print('\t</person>', file=routes)
                ped_number += 1


def print_header(routes):
    print("<routes>", file=routes)


def print_footer(routes):
    print("</routes>", file=routes)