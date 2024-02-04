# from abc import ABC, abstractmethod
# from logging import getLogger

import pandas as pd
from src.algorithm.abstract_algorithm import AbstractModel
from src.entity.training_data import TrainingDataset
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)

# class AbstractTrainingUsecase(ABC):
#     def __init__(self):
#         self.logger = getLogger(__name__)

#     @abstractmethod
#     def train(
#         self,
#         model: AbstractModel,
#         training_data: TrainingDataset,
#         train_mask: pd.DataFrame,
#         valid_mask: pd.DataFrame,
#     ):
#         raise NotImplementedError


class TrainingUsecase(object):
    def __init__(
            self,
            # model:AbstractModel
        ):
        pass
        # super().__init__()
        # self.model = model

    def train(
        self,
        model: AbstractModel,
        training_data: TrainingDataset,
        train_mask: pd.DataFrame,
        valid_mask: pd.DataFrame,        
    ):
        logger.info(f"start training: {model.name}...")

        model.train(
            x_train=training_data.training_data.x[train_mask].copy(),
            y_train=training_data.training_data.y[train_mask].copy(),
            x_test=training_data.validation_data.x[valid_mask].copy(),
            y_test=training_data.validation_data.y[valid_mask].copy(),
        )        
        logger.info(f"done training: {model.name}")
