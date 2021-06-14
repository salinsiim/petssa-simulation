import sys
import os

from intersection.FlowCharacteristic import FlowCharacteristic
from priority import calculate_max_green

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variables 'SUMO_HOME'")

import traci


def sense_characteristics(flows, max_speed, max_green, max_green_diff, is_priority):
    res = []
    for f in flows:
        flow_max_green = calculate_max_green(max_green, max_green_diff, f.priority.priority, is_priority)
        d_green = flow_max_green * max_speed
        density = 0
        density_in_d_green = 0
        lv_speed = 0
        lv_distance = 0

        # Vehicles in Edge 1
        for l_id in f.e1_lane_ids:
            density += traci.lane.getLastStepVehicleNumber(l_id)
            for v in traci.lane.getLastStepVehicleIDs(l_id):
                dist = traci.lane.getLength(l_id) - traci.vehicle.getLanePosition(v)
                if dist <= d_green:
                    if dist > lv_distance:
                        lv_distance = dist
                        lv_speed = traci.vehicle.getSpeed(v)
                    density_in_d_green += 1

        # Vehicles in Edge 2
        for l_id in f.e2_lane_ids:
            density += traci.lane.getLastStepVehicleNumber(l_id)
            for v in traci.lane.getLastStepVehicleIDs(l_id):
                # Consider Edge 1 length
                dist = traci.lane.getLength(f.e1_lane_ids[0]) + traci.lane.getLength(l_id) - traci.vehicle.getLanePosition(v)
                if dist <= d_green:
                    if dist > lv_distance:
                        lv_distance = dist
                        lv_speed = traci.vehicle.getSpeed(v)
                    density_in_d_green += 1

        # Vehicles in Edge 3
        for l_id in f.e3_lane_ids:
            density += traci.lane.getLastStepVehicleNumber(l_id)
            for v in traci.lane.getLastStepVehicleIDs(l_id):
                # Consider Edge 1 and 2 length
                dist = traci.lane.getLength(f.e1_lane_ids[0]) + traci.lane.getLength(f.e2_lane_ids[0]) + traci.lane.getLength(l_id) - traci.vehicle.getLanePosition(v)
                if dist <= d_green:
                    if dist > lv_distance:
                        lv_distance = dist
                        lv_speed = traci.vehicle.getSpeed(v)
                    density_in_d_green += 1

        res.append(FlowCharacteristic(f.id, density, density_in_d_green, round(lv_speed, 2), round(lv_distance, 2)))
    return res


def sense_pedestrians(crossing):
    persons = list(traci.person.getIDList())
    waiting_persons = []
    for p in persons:
        route_edges = traci.person.getEdges(p)
        if crossing.from_edge in route_edges:
            for e in crossing.to_edges:
                # to_edge should be after from_edge in the edge list
                # person must have waited more than 5 seconds
                if e in route_edges and route_edges.index(crossing.from_edge) < route_edges.index(e) and traci.person.getWaitingTime(p) > 5.0:
                    waiting_persons.append(p)
    return len(waiting_persons)

