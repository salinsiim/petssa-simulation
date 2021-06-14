import os

TL_LOGIC_ID = 'cluster_11791147_2032404487_27789090_81290972'
MAX_SPEED = 13.9
INTERSECTION_NAME = 'Tammsaare-Sõpruse'

PATH = os.environ['TS_SIMULATION']

FLOWS_PATH = PATH + '/input/map/flows.csv'
CROSSINGS_PATH = PATH + '/input/map/crossings.csv'
PRIORITIES_PATH = PATH + '/input/map/priorities.csv'
PHASES_PATH = PATH + '/input/map/phases.csv'
GREEN_TSL_STATES_PATH = PATH + '/input/map/green_tsl_states.csv'
PROTECTION_TSL_STATES_PATH = PATH + '/input/map/protection_tsl_states.csv'
LOGGING_PATH = PATH + '/output/map/petssa'
