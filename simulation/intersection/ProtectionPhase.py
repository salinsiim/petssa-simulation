import dataclasses as dc


@dc.dataclass(unsafe_hash=True)
class ProtectionPhase:
    to_phase: int
    from_phase: int
    states: list
