from dataclasses import dataclass

from src.domain.common_data import XY


@dataclass(frozen=True)
class TrainingDataset:
    training_data: XY
    validation_data: XY
