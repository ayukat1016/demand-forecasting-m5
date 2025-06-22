from dataclasses import dataclass

import pandas as pd
from pandera import Field, SchemaModel
from pandera.typing import Series


@dataclass(frozen=True)
class RawDataWithTargetDates:
    data: pd.DataFrame
    date_from: int
    date_to: int

    def __post_init__(self) -> None:
        RawDataSchema.validate(self.data)


@dataclass(frozen=True)
class RawDataset:
    training_data: RawDataWithTargetDates
    validation_data: RawDataWithTargetDates
    prediction_data: RawDataWithTargetDates


class RawDataSchema(SchemaModel):
    id: Series[str] = Field(
        nullable=False,
        coerce=True,
    )
    item_id: Series[str] = Field(
        nullable=False,
        coerce=True,
    )
    dept_id: Series[str] = Field(
        nullable=False,
        coerce=True,
    )
    cat_id: Series[str] = Field(
        nullable=False,
        coerce=True,
    )
    store_id: Series[str] = Field(
        nullable=False,
        coerce=True,
    )
    state_id: Series[str] = Field(
        nullable=False,
        coerce=True,
    )
    date_id: Series[int] = Field(
        ge=1,
        nullable=False,
        coerce=True,
    )
    sales: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    wm_yr_wk: Series[int] = Field(
        ge=11101,
        nullable=False,
        coerce=True,
    )
    event_name_1: Series[str] = Field(
        nullable=False,
        coerce=True,
    )
    event_type_1: Series[str] = Field(
        nullable=False,
        coerce=True,
    )
    event_name_2: Series[str] = Field(
        nullable=False,
        coerce=True,
    )
    event_type_2: Series[str] = Field(
        nullable=False,
        coerce=True,
    )
    snap_ca: Series[int] = Field(
        isin=(0, 1),
        nullable=False,
        coerce=True,
    )
    snap_tx: Series[int] = Field(
        isin=(0, 1),
        nullable=False,
        coerce=True,
    )
    snap_wi: Series[int] = Field(
        isin=(0, 1),
        nullable=False,
        coerce=True,
    )
    sell_price: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    release: Series[int] = Field(
        ge=0,
        nullable=False,
        coerce=True,
    )

    class Config:
        name = "RawDataSchema"
        strict = True
        coerce = True
