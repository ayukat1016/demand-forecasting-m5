from enum import Enum
# from typing import List


class TABLES(Enum):
    SALES = "sales"
    PRICES = "prices"
    CALENDAR = "calendar"
    PREDICTIONS = "predictions"

    # @staticmethod
    # def has_value(value: str) -> bool:
    #     return value in [v.value for v in TABLES.__members__.values()]

    # @staticmethod
    # def get_list() -> List[str]:
    #     return [v.value for v in TABLES.__members__.values()]
