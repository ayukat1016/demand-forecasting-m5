from abc import ABC, abstractmethod
from logging import getLogger

import pandas as pd
from src.algorithm.abstract_algorithm import AbstractModel
from src.entity.prediction_data import Prediction, PredictionDataset
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)

# class AbstractPredictionUsecase(ABC):
#     def __init__(self):
#         self.logger = getLogger(__name__)

#     @abstractmethod
#     def predict(
#         self,
#         model: AbstractModel,
#         data: PredictionDataset,
#         mask: pd.DataFrame,
#     ) -> Prediction:
#         raise NotImplementedError


class PredictionUsecase(object):
    def __init__(self,):
        pass
        # super().__init__()

    def predict(
        self,
        model: AbstractModel,
        data: PredictionDataset,
        mask: pd.DataFrame,
    ) -> Prediction:
        logger.info(f"start prediction: {model.name}...")

        prediction = model.predict(x=data.prediction_data.x[mask].copy())
        
        d = [
            dict(
                store_id=s,
                item_id=i,
                date_id=d,
                prediction=p,
            )
            for s, i, d, p in zip(
                data.prediction_data.keys[mask]["store_id"].tolist(),
                data.prediction_data.keys[mask]["item_id"].tolist(),
                data.prediction_data.keys[mask]["date_id"].tolist(),                
                prediction,
            )
        ]
        data = pd.DataFrame(d).sort_values(["store_id", "item_id", "date_id"]).reset_index(drop=True)
        prediction_data = Prediction(prediction=data)

        logger.info(f"done prediction: {model.name}")
        logger.info(
            f"""prediction:
{prediction_data.prediction}
        """
        )
        return prediction_data
