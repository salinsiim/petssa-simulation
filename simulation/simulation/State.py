import dataclasses as dc
from intersection import NextScheduledPhase


@dc.dataclass(unsafe_hash=True)
class State:
    phases_state: list
    next_phase: NextScheduledPhase = None
    protection_pointer: int = 0
    should_switch_phase: bool = True
    active_phase: int = 0
