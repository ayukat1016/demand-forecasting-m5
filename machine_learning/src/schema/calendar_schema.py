from src.schema.abstract_schema import AbstractSchema


class Calendar(AbstractSchema):
    date: str
    wm_yr_wk: int
    weekday : str
    wday: int    
    month: int
    year: int
    date_id: int
    event_name_1 : str
    event_type_1 : str
    event_name_2 : str
    event_type_2 : str
    snap_ca: int
    snap_tx: int
    snap_wi: int

    class Config:
        allow_mutation = False
        extra = "forbid"