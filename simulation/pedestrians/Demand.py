import dataclasses as dc


@dc.dataclass(unsafe_hash=True)
class Demand:
    route: str
    origin: str
    destination: str
    demand_per_second: float
