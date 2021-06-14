import dataclasses as dc


@dc.dataclass(unsafe_hash=True)
class Priority:
    id: int
    priority: int
