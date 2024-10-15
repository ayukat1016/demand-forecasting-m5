import pandas as pd

from src.domain.algorithm.lightgbm_regressor import AbstractModel
from src.domain.model.training_data import TrainingDataset
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class TrainingUsecase(object):
    def __init__(self):
        pass

    def train(
        self,
        model: AbstractModel,
        training_data: TrainingDataset,
        train_mask: pd.DataFrame,
        valid_mask: pd.DataFrame,
    ):
        logger.info(f"start training: {model.name}...")

        model.train(
            x_train=training_data.training_data.x[train_mask].reset_index(drop=True),
            y_train=training_data.training_data.y[train_mask]
            .squeeze()
            .reset_index(drop=True),
            x_test=training_data.validation_data.x[valid_mask].reset_index(drop=True),
            y_test=training_data.validation_data.y[valid_mask]
            .squeeze()
            .reset_index(drop=True),
        )
        logger.info(f"done training: {model.name}")
