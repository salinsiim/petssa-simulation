import csv
import optparse
import os
from glob import glob

PATH = os.environ['TS_SIMULATION']


def generate_report(prefix, input_path, output_path):
    print("Calculating report")
    with open(output_path, 'w') as report:
        writer = csv.writer(report, delimiter=';')
        writer.writerow(['Type', 'Max Green', 'Max Green Diff', 'Priority',
                         'Vehicle Type',
                         'AVG Waiting Time',
                         'AVG Trip Duration',
                         'AVG Fuel Consumption',
                         'AVG CO2 Emission',
                         'Vehicle Count'])
        for name in glob(input_path + prefix + '-*.csv'):
            split_name = os.path.basename(name).split('-')
            type = split_name[1]
            max_green = split_name[2]
            mg_diff = split_name[3]
            priority = split_name[4].split('.')[0]
            with open(name, 'r') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    writer.writerow([
                        type,
                        max_green,
                        mg_diff,
                        priority,
                        row['Vehicle Type'],
                        row['AVG Waiting Time'],
                        row['AVG Trip Duration'],
                        row['AVG Fuel Consumption'],
                        row['AVG CO2 Emission'],
                        row['Vehicle Count']
                    ])
    print("Report completed")


def options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--folder", action="store", type="string", dest="folder", help="folder to aggregate")
    opt_parser.add_option("--prefix", action="store", type="string", dest="prefix", help="aggregated report prefix")
    opt_parser.add_option("--output", action="store", type="string", dest="output", help="report output")
    options, args = opt_parser.parse_args()
    return options


if __name__ == "__main__":
    options = options()
    generate_report(options.prefix, options.folder, options.output)
