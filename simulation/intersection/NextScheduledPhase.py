import dataclasses as dc


@dc.dataclass(unsafe_hash=True)
class NextScheduledPhase:
    id: int
    best_green: int
