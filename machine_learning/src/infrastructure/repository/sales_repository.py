from typing import List

from src.domain.repository.sales_repository import AbstractSalesRepository
from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.models import Sales as SalesModel
from src.infrastructure.schema.sales_schema import Sales
from src.infrastructure.schema.tables_schema import TABLES


class SalesRepository(AbstractSalesRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.table_name = TABLES.SALES.value

    def select(
        self,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Sales]:
        with self.db_client.get_session() as session:
            query = session.query(SalesModel).offset(offset).limit(limit)
            results = query.all()
            data = [
                Sales(**{k: getattr(row, k) for k in Sales.model_fields.keys()})
                for row in results
            ]
        return data
