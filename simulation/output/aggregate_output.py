import csv
import optparse

CAR_TYPE = "veh_passenger"
BUS_TYPE = "bus_bus"

VEHICLE_TYPE = 'tripinfo_vType'
WAITING_TIME = 'tripinfo_waitingTime'
TRIP_DURATION = 'tripinfo_duration'
FUEL_CONSUMPTION = 'emissions_fuel_abs'
CO2_EMISSION = 'emissions_CO2_abs'


def aggregate_results(input_path, output_path):
    print("Aggregating results")
    car_waiting_time = 0
    car_trip_duration = 0
    car_fuel_consumption = 0
    car_co2_emission = 0
    car_count = 0

    bus_waiting_time = 0
    bus_trip_duration = 0
    bus_fuel_consumption = 0
    bus_co2_emission = 0
    bus_count = 0

    with open(input_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        row_count = 0
        for row in reader:
            if row_count > 0:
                if row[VEHICLE_TYPE] == BUS_TYPE:
                    bus_count += 1
                    bus_waiting_time += float(row[WAITING_TIME])
                    bus_trip_duration += float(row[TRIP_DURATION])
                    bus_fuel_consumption += float(row[FUEL_CONSUMPTION])
                    bus_co2_emission += float(row[CO2_EMISSION])
                if row[VEHICLE_TYPE] == CAR_TYPE:
                    car_count += 1
                    car_waiting_time += float(row[WAITING_TIME])
                    car_trip_duration += float(row[TRIP_DURATION])
                    car_fuel_consumption += float(row[FUEL_CONSUMPTION])
                    car_co2_emission += float(row[CO2_EMISSION])
            row_count += 1
    with open(output_path, 'w') as aggregated:
        writer = csv.writer(aggregated, delimiter=';')
        writer.writerow(
            ['Vehicle Type',
             'AVG Waiting Time',
             'AVG Trip Duration',
             'AVG Fuel Consumption',
             'AVG CO2 Emission',
             'Vehicle Count'])
        writer.writerow(
            [CAR_TYPE,
             car_waiting_time / car_count,
             car_trip_duration / car_count,
             car_fuel_consumption / car_count,
             car_co2_emission / car_count,
             car_count])
        writer.writerow(
            [BUS_TYPE,
             bus_waiting_time / bus_count,
             bus_trip_duration / bus_count,
             bus_fuel_consumption / bus_count,
             bus_co2_emission / bus_count,
             bus_count])
    print("Aggregation completed")

def options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--input", action="store", type="string", dest="input", help="result to aggregate")
    opt_parser.add_option("--output", action="store", type="string", dest="output", help="aggregation output")
    options, args = opt_parser.parse_args()
    return options


if __name__ == "__main__":
    options = options()
    aggregate_results(options.input, options.output)
