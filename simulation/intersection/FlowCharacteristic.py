import dataclasses as dc


@dc.dataclass(unsafe_hash=True)
class FlowCharacteristic:
    id: int
    density: int
    density_in_dgreen: int
    lv_speed: float
    lv_dist: int
