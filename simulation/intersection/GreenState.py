import dataclasses as dc


@dc.dataclass(unsafe_hash=True)
class GreenState:
    phase: int
    state: str
