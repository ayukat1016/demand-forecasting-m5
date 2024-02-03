from pydantic import Extra
from src.model.abstract_model import AbstractModel


class Prices(AbstractModel):
    key: str
    store_id: str
    item_id: str
    wm_yr_wk: int
    sell_price: float

    class Config:
        allow_mutation = False
        extra = Extra.forbid