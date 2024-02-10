from src.infrastructure.database import AbstractDBClient
from src.repository.abstract_repository import AbstractCreateTablesRepository


class TableRepository(AbstractCreateTablesRepository):
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
