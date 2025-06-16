from src.domain.repository.tables_repository import AbstractTablesRepository
from src.infrastructure.database.db_client import AbstractDBClient
from src.infrastructure.schema.models import Base


class TablesRepository(AbstractTablesRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)

    def create_tables(
        self,
        query: str,
    ):
        Base.metadata.create_all(self.db_client.engine)
