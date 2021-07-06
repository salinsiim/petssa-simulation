import os

TL_LOGIC_ID = 'cluster_11791147_2032404487_27789090_81290972'
MAX_SPEED = 13.9
INTERSECTION_NAME = 'Tammsaare-Sõpruse'

PATH = os.environ['TS_SIMULATION']

INPUT_PATH = '/input/map/'

FLOWS_PATH = PATH + INPUT_PATH + 'flows.csv'
CROSSINGS_PATH = PATH + INPUT_PATH + 'crossings.csv'
PRIORITIES_PATH = PATH + INPUT_PATH + 'priorities.csv'
PHASES_PATH = PATH + INPUT_PATH + 'phases.csv'
GREEN_TSL_STATES_PATH = PATH + INPUT_PATH + 'green_tsl_states.csv'
PROTECTION_TSL_STATES_PATH = PATH + INPUT_PATH + 'protection_tsl_states.csv'
LOGGING_PATH = PATH + '/output/map/petssa'
