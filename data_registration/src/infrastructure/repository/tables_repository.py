from src.domain.repository.tables_repository import AbstractTablesRepository
from src.infrastructure.database.db_client import AbstractDBClient


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
        self.db_client.execute_create_query(query=query)
