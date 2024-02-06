from pydantic import Extra
from src.model.abstract_model import AbstractModel


class Calendar(AbstractModel):
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
        extra = Extra.forbid