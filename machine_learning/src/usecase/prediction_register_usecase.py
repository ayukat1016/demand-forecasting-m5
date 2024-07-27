from typing import List, Optional

import pandas as pd
from src.entity.prediction_data import PredictionDataSchema
from src.middleware.logger import configure_logger
from src.repository.prediction_repository import AbstractPredictionRepository
from src.schema.prediction_schema import Prediction

logger = configure_logger(__name__)


class PredictionRegisterUsecase(object):
    def __init__(
        self,
        prediction_repository: AbstractPredictionRepository
    ):
        self.prediction_repository = prediction_repository

    def register_prediction(
        self,
        predictions: pd.DataFrame,
    ):
        logger.info("register prediction")
        self.register_db(
            predictions=predictions,
        )
        logger.info("done register prediction")

    def register_db(
        self,
        predictions: pd.DataFrame,
    ):
        predictions = PredictionDataSchema.validate(predictions)
        records = predictions.to_dict(orient="records")
        predictions: List[Prediction] = []
        for r in records:
            predictions.append(
                Prediction(
                    store_id=r["store_id"],
                    item_id=r["item_id"],
                    date_id=r["date_id"],
                    prediction=float(r["prediction"]),
                ),
            )
        self.prediction_repository.bulk_insert(
            records=predictions,
        )
