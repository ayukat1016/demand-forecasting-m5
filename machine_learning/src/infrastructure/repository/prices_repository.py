from typing import List

from src.domain.repository.prices_repository import AbstractPricesRepository
from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.prices_schema import Prices
from src.infrastructure.schema.tables_schema import TABLES
from src.infrastructure.schema.models import Prices as PricesModel


class PricesRepository(AbstractPricesRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.table_name = TABLES.PRICES.value

    def select(
        self,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Prices]:
        with self.db_client.get_session() as session:
            query = session.query(PricesModel).offset(offset).limit(limit)
            results = query.all()
            data = [Prices(**{k: getattr(row, k) for k in Prices.model_fields.keys()}) for row in results]
        return data
