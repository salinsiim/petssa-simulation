import dataclasses as dc


@dc.dataclass(unsafe_hash=True)
class Config:
    phases: list
    protection_phases: list
    green_states: list
    max_speed: int
    tl_logic_id: str
    intersection_name: str
    logging_file: str
    crossings: list = None
    max_green: int = None
    max_green_diff: int = None
    is_priority: bool = True
