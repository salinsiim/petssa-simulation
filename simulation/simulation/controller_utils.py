import traci

from logging import log
from sensors.sensors import sense_characteristics, sense_pedestrians
from algorithm import next_phase
from intersection import NextScheduledPhase


def tsl(step, config, state):
    if state.should_switch_phase:
        p = calculate_next_phase(step, config, state.phases_state)
        if p is None:
            state.phases_state = reset_phases(step, config)
            fallback = calculate_next_phase(step, config, state.phases_state)
            state.next_phase = NextScheduledPhase(0, 1) if fallback is None else fallback
            state = schedule_phase(step, state, config)
        else:
            state.next_phase = p
            state = schedule_phase(step, state, config)
    else:
        state = schedule_phase(step, state, config)
    return state


def calculate_next_phase(step, config, phases_state):
    phases = enrich_phases(config.phases, config.max_speed, config.max_green, config.max_green_diff, config.is_priority)
    if config.crossings is not None:
        crossings = enrich_crossings(config.crossings)
        phases = merge(step, config, phases, crossings)
    log_characteristics(step, config.logging_file, config.intersection_name, phases)
    log(step, config.logging_file, config.intersection_name, "cycle state: %s" % phases_state)
    p = next_phase(phases, phases_state, config.max_green, config.max_green_diff, config.is_priority)
    log(step, config.logging_file, config.intersection_name,
        "proposed Phase by PETSSA: %s" % (None if p is None else p.id))
    return p


def merge(step, config, phases, crossings):
    for p in phases:
        phase_crossings = [c for c in crossings if c.phase_id == p.id]
        if phase_crossings:
            p.crossings = phase_crossings
        crossing = next((c for c in crossings if c.density > 0), None)
        if crossing is not None:
            log(step, config.logging_file, config.intersection_name, "adding pedestrian density to Phase %s" % p.id)
            for f in p.flows:
                f.characteristics.density += 1
    return phases


def log_characteristics(step, file_path, intersection_name, phases):
    log(step, file_path, intersection_name, "characteristics: ")
    for p in phases:
        if p.crossings:
            waiting_persons = 0
            for c in [c for c in p.crossings if c.density > 0]:
                waiting_persons += c.density
            if waiting_persons > 0:
                log(step, file_path, intersection_name, "Phase %s, %i persons waiting" % (p.id, waiting_persons))
        for f in p.flows:
            c = f.characteristics
            log(step, file_path, intersection_name,
                "Phase %s, Flow %s: density: %i, density_in_dgreen: %i, lv_speed: %sm/s, lv_dist: %sm"
                % (p.id, f.id, c.density, c.density_in_dgreen, c.lv_speed, c.lv_dist))


def all_scheduled(phases):
    return not [scheduled for id, scheduled in phases if not scheduled]


def enrich_phases(phases, max_speed, max_green, max_green_diff, is_priority):
    enriched = phases
    for p in enriched:
        characteristics = sense_characteristics(p.flows, max_speed, max_green, max_green_diff, is_priority)
        for f in p.flows:
            f.characteristics = next(p for p in characteristics if p.id == f.id)
    return enriched


def enrich_crossings(crossings):
    for c in crossings:
        c.density = sense_pedestrians(c)
    return crossings


def schedule_phase(step, state, config):
    # Protections from active phase to next phase
    protections = next(
        s.states for s in config.protection_phases if
        s.from_phase == state.active_phase and s.to_phase == state.next_phase.id)

    if state.protection_pointer == len(protections):
        # Protection phases have been already scheduled
        state.protection_pointer = 0

        if state.next_phase.id == 0:
            # If next phase is all reds then reset cycle
            state.phases_state = reset_phases(step, config)
        else:
            # Schedule all phases that contain next_phase flows
            flows_to_schedule = []
            for p in config.phases:
                if p.id == state.next_phase.id:
                    for f in p.flows:
                        flows_to_schedule.append(f.id)

            phases_to_schedule = []
            for p in config.phases:
                for f in p.flows:
                    if f.id in flows_to_schedule and p.id not in phases_to_schedule:
                        phases_to_schedule.append(p.id)

            for id in phases_to_schedule:
                state.phases_state[id - 1] = (id, True)


            if all_scheduled(state.phases_state):
                # Reset phases for next step
                state.phases_state = reset_phases(step, config)

        green_state = next(s.state for s in config.green_states if s.phase == state.next_phase.id)

        log(step, config.logging_file, config.intersection_name,
            "scheduling Phase %s for %i seconds" % (state.next_phase.id, state.next_phase.best_green))

        traci.trafficlight.setRedYellowGreenState(config.tl_logic_id, green_state)
        traci.trafficlight.setPhaseDuration(config.tl_logic_id, int(state.next_phase.best_green))

        state.active_phase = state.next_phase.id
        state.should_switch_phase = True
    else:
        # Protection phase must be scheduled
        log(step, config.logging_file, config.intersection_name, "scheduling Protection Phase from %s to %s [%s]" % (
            state.active_phase, state.next_phase.id, state.protection_pointer))

        traci.trafficlight.setRedYellowGreenState(config.tl_logic_id, protections[state.protection_pointer])
        traci.trafficlight.setPhaseDuration(config.tl_logic_id, 2)
        state.protection_pointer += 1
        state.should_switch_phase = False

    return state


def reset_phases(step, config):
    log(step, config.logging_file, config.intersection_name, "resetting cycle")
    return [(p.id, False) for p in config.phases]
