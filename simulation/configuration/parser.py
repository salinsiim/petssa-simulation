import csv
from intersection import Flow, Priority, Phase, ProtectionPhase, GreenState, Crossing

_flows_cache = {}
_crossings_cache = {}
_phases_cache = {}
_protection_states_cache = {}
_green_states_cache = {}


def construct_phases(intersection_name, phases_path, flows_path, priorities_path):
    phases = read_phases(intersection_name, phases_path)
    flows = read_flows(intersection_name, flows_path)
    priorities = read_priorities(priorities_path)
    for p in phases:
        if p.flows is None:
            p.flows = []
        for f_id in p.flow_ids:
            p.flows.append(next(f for f in flows if f.id == int(f_id)))
        for f in p.flows:
            f.priority = next(p for p in priorities if p.id == f.id)
    return phases


def read_crossings(intersection_name, path):
    global _crossings_cache
    try:
        return _crossings_cache[intersection_name]
    except KeyError:
        res = []
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            counter = 0
            for row in reader:
                if counter > 0:
                    phase_id = int(row[0])
                    from_edge = row[1]
                    to_edges = row[2].split(',')
                    min_green = int(row[3])
                    res.append(Crossing(phase_id, from_edge, to_edges, min_green))
                counter += 1
        _crossings_cache[intersection_name] = res
        return _crossings_cache[intersection_name]


def read_protection_states(intersection_name, path):
    global _protection_states_cache
    try:
        return _protection_states_cache[intersection_name]
    except KeyError:
        res = []
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            counter = 0
            for row in reader:
                if counter > 0:
                    phase_id = int(row[0])
                    from_id = int(row[1])
                    states = row[2].split(',')
                    res.append(ProtectionPhase(phase_id, from_id, states))
                counter += 1
        _protection_states_cache[intersection_name] = res
        return _protection_states_cache[intersection_name]


def read_green_states(intersection_name, path):
    global _green_states_cache
    try:
        return _green_states_cache[intersection_name]
    except KeyError:
        res = []
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            counter = 0
            for row in reader:
                if counter > 0:
                    phase_id = int(row[0])
                    state = str(row[1])
                    res.append(GreenState(phase_id, state))
                counter += 1
        _green_states_cache[intersection_name] = res
        return _green_states_cache[intersection_name]


def read_phases(intersection_name, path):
    global _phases_cache
    try:
        return _phases_cache[intersection_name]
    except KeyError:
        res = []
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            counter = 0
            for row in reader:
                if counter > 0:
                    id = int(row[0])
                    flow_ids = row[1].split(',')
                    res.append(Phase(id, flow_ids))
                counter += 1
        _phases_cache[intersection_name] = res
        return _phases_cache[intersection_name]


def read_flows(intersection_name, path):
    global _flows_cache
    try:
        return _flows_cache[intersection_name]
    except KeyError:
        res = []
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            counter = 0
            for row in reader:
                if counter > 0:
                    id = int(row[0])
                    e1_lane_ids = list(filter(None, row[1].split(',')))
                    e2_lane_ids = list(filter(None, row[2].split(',')))
                    e3_lane_ids = list(filter(None, row[3].split(',')))
                    shortest_green = int(row[4])
                    res.append(Flow(id, e1_lane_ids, e2_lane_ids, e3_lane_ids, shortest_green))
                counter += 1
        _flows_cache[intersection_name] = res
        return _flows_cache[intersection_name]


def read_priorities(path):
    priorities = []
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        counter = 0
        for row in reader:
            if counter > 0:
                id = int(row[0])
                priority = int(row[1])
                priorities.append(Priority(id, priority))
            counter += 1
        return priorities
