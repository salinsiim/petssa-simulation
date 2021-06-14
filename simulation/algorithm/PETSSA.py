from intersection import NextScheduledPhase
from priority import calculate_max_green


def next_phase(phases, state, max_green, max_green_diff, is_priority):
    unscheduled = [p for p in phases if p.id in [id for id, scheduled in state if not scheduled]]
    flows = [(p.id, p.flows) for p in unscheduled]
    phase_id, flow = densest_flow(flows)

    if flow.characteristics.density == 0:
        return None

    bg = best_green(next(p for p in unscheduled if p.id == phase_id), max_green, max_green_diff, is_priority)

    if bg is None or bg == 0:
        return None

    return NextScheduledPhase(phase_id, bg)


def densest_flow(flows):
    p_id, p_flows = max(flows, key=lambda item: max(f.characteristics.density for f in item[1]))
    d_flow = max(p_flows, key=lambda item: item.characteristics.density)
    return p_id, d_flow


def best_green(phase, max_green, max_green_diff, is_priority):
    bg = []
    for f in phase.flows:
        flow_max_green = calculate_max_green(max_green, max_green_diff, f.priority.priority, is_priority)
        # No vehicles/pedestrians
        if f.characteristics.density == 0:
            bg.append(0)
        # Vehicles are present and lv_dist calculated
        elif f.characteristics.lv_dist != 0:
            res = f.characteristics.lv_dist / (f.characteristics.lv_speed if f.characteristics.lv_speed >= 1 else 1)
            bg.append(flow_max_green if res > flow_max_green else max(res + 2, f.shortest_green))
        # No vehicles but pedestrians waiting
        elif next((c for c in phase.crossings if c.density > 0), None) is not None:
            bg.append(max(phase.crossings, key=lambda item: item.min_green).min_green)
        else:
            bg.append(flow_max_green)
    return max(bg)