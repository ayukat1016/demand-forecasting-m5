from dataclasses import dataclass

from pandera import Check, Column, DataFrameSchema, Field, Index, SchemaModel
from pandera.typing import Series
from src.entity.common_data import XY


class ExtractedPriceSchema(SchemaModel):
    price_max: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    price_min: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    price_std: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    price_mean: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    price_norm: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    price_nunique: Series[int] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    item_nunique: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )


    class Config:
        name = "ExtractedPriceSchema"
        strict = True
        coerce = True



class ExtractedLagSalesSchema(SchemaModel):
    lag_21_7: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_8: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_9: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_10: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_11: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_12: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_13: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_14: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_15: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_16: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_17: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_18: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_19: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_20: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    lag_21_21: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    rolling_mean_7: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    rolling_std_7: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    rolling_mean_14: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    rolling_std_14: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    rolling_mean_30: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    rolling_std_30: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    rolling_mean_60: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    rolling_std_60: Series[float] = Field(
        ge=0.0,
        le=1000.0,
        nullable=True,
        coerce=True,
    )
    class Config:
        name = "ExtractedLagSalesSchema"
        strict = True
        coerce = True


@dataclass(frozen=True)
class PreprocessedDataset:
    training_data: XY
    validation_data: XY
    prediction_data: XY
