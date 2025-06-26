from typing import List

from sqlalchemy.dialects.postgresql import insert

from src.domain.repository.prices_repository import AbstractPricesRepository
from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.models import Prices as PricesModel
from src.infrastructure.schema.prices_schema import Prices
from src.infrastructure.schema.tables_schema import TABLES


class PricesRepository(AbstractPricesRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ) -> None:
        super().__init__(db_client=db_client)
        self.table_name = TABLES.PRICES.value

    def bulk_insert(
        self,
        records: List[Prices],
    ) -> None:
        with self.db_client.get_session() as session:
            values = [
                {
                    k: v
                    for k, v in record.model_dump().items()
                    if k in PricesModel.__table__.columns.keys()
                }
                for record in records
            ]
            stmt = insert(PricesModel).values(values)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=["store_id", "item_id", "wm_yr_wk"]
            )
            session.execute(stmt)
            session.commit()
