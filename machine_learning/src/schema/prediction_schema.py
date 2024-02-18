from pydantic import Extra
from src.schema.abstract_schema import AbstractSchema


class Prediction(AbstractSchema):
    store_id: str    
    item_id: str
    date_id: int
    prediction: float

    class Config:
        allow_mutation = False
        extra = Extra.forbid
