import pandas as pd

from src.domain.algorithm.lightgbm_regressor import AbstractModel
from src.domain.model.prediction_data import Prediction, PredictionDataset
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class PredictionUsecase(object):
    def __init__(self) -> None:
        pass

    def predict(
        self,
        model: AbstractModel,
        data: PredictionDataset,
        mask: pd.DataFrame,
    ) -> Prediction:
        logger.info(f"start prediction: {model.name}...")

        prediction = model.predict(
            x=data.prediction_data.x[mask].reset_index(drop=True)
        )

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
        df = (
            pd.DataFrame(d)
            .sort_values(["store_id", "item_id", "date_id"])
            .reset_index(drop=True)
        )
        prediction_output = Prediction(data=df)

        logger.info(f"done prediction: {model.name}")
        logger.info(
            f"""prediction:
{prediction_output.data}
        """
        )
        return prediction_output
