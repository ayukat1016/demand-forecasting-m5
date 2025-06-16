from typing import List
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.domain.repository.sales_repository import AbstractSalesRepository
from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.sales_schema import Sales
from src.infrastructure.schema.models import Sales as SalesModel
from src.infrastructure.schema.tables_schema import TABLES


class SalesRepository(AbstractSalesRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.table_name = TABLES.SALES.value

    def bulk_insert(
        self,
        records: List[Sales],
    ):
        with self.db_client.get_session() as session:
            values = [
                {k: v for k, v in record.model_dump().items() if k in SalesModel.__table__.columns.keys()}
                for record in records
            ]
            stmt = insert(SalesModel).values(values)
            stmt = stmt.on_conflict_do_nothing(index_elements=['key'])
            session.execute(stmt)
            session.commit()
