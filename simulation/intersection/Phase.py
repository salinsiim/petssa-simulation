import dataclasses as dc


@dc.dataclass(unsafe_hash=True)
class Phase:
    id: int
    flow_ids: list
    best_green: int = None
    green_phase_state: str = None
    # List of ProtectionPhase
    protection_phases: list = None
    # List of Flow
    flows: list = None
    # List of Crossings
    crossings: list = None
