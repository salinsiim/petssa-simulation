import dataclasses as dc


@dc.dataclass(unsafe_hash=True)
class Crossing:
    phase_id: int
    from_edge: str
    to_edges: list
    min_green: int
    density: int = 0
