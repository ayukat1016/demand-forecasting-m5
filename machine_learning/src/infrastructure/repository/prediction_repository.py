from typing import List

from src.domain.repository.prediction_repository import AbstractPredictionRepository
from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.prediction_schema import Prediction
from src.infrastructure.schema.tables_schema import TABLES
from src.infrastructure.schema.models import Prediction as PredictionModel
from sqlalchemy.dialects.postgresql import insert


class PredictionRepository(AbstractPredictionRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.table_name = TABLES.PREDICTION.value

    def bulk_insert(
        self,
        records: List[Prediction],
    ):
        with self.db_client.get_session() as session:
            values = [
                {k: v for k, v in record.model_dump().items() if k in PredictionModel.__table__.columns.keys()}
                for record in records
            ]
            stmt = insert(PredictionModel).values(values)
            stmt = stmt.on_conflict_do_nothing(index_elements=['store_id', 'item_id', 'date_id'])
            session.execute(stmt)
            session.commit()
