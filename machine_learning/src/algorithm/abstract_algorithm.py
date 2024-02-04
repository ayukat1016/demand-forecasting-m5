from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, List, Optional

import pandas as pd
from src.entity.evaluation_data import FeatureImportance


class AbstractExtractor(ABC):
    def __init__(self):
        pass
        # self.logger = getLogger(__name__)

    @abstractmethod
    def run(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        raise NotImplementedError


class AbstractModel(ABC):
    def __init__(self):
        self.name: str = "base_model"
        self.params: Dict = {}
        self.train_params: Dict = {}
        self.model = None
        self.logger = getLogger(__name__)

    @abstractmethod
    def reset_model(
        self,
        params: Optional[Dict] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def train(
        self,
        x_train: pd.DataFrame,
        y_train: pd.DataFrame,
        x_test: Optional[pd.DataFrame] = None,
        y_test: Optional[pd.DataFrame] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        x: pd.DataFrame,
    ) -> List[float]:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        file_path: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
        file_path: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_feature_importance(self) -> List[FeatureImportance]:
        raise NotImplementedError
