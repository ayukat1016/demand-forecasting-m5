from pydantic import Extra
from src.schema.abstract_schema import AbstractSchema


class Sales(AbstractSchema):
    key: str
    id: str    
    item_id: str
    dept_id: str
    cat_id: str
    store_id: str
    state_id: str
    date_id: int
    sales: float

    class Config:
        allow_mutation = False
        extra = Extra.forbid
