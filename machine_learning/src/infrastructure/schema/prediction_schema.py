from src.infrastructure.schema.abstract_schema import AbstractSchema


class Prediction(AbstractSchema):
    store_id: str
    item_id: str
    date_id: int
    prediction: float

    class Config:
        frozen = True
        extra = "forbid"
