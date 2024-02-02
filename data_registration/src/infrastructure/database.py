import os
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

import psycopg2
from psycopg2 import extras
from psycopg2.extras import DictCursor
from src.exceptions.exceptions import DatabaseException
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractDBClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_connection(self):
        raise NotImplementedError

    @abstractmethod
    def execute_create_query(
        self,
        query: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def execute_bulk_insert_or_update_query(
        self,
        query: str,
        parameters: Optional[List[Tuple]] = None,
    ):
        raise NotImplementedError

class PostgreSQLClient(AbstractDBClient):
    def __init__(self):
        self.__postgresql_user = os.getenv("POSTGRESQL_USER")
        self.__postgresql_password = os.getenv("POSTGRESQL_PASSWORD")
        self.__postgresql_port = int(os.getenv("POSTGRESQL_PORT", 5432))
        self.__postgresql_dbname = os.getenv("POSTGRESQL_DBNAME")
        self.__postgresql_host = os.getenv("POSTGRESQL_HOST")
        self.__connection_string = f"host={self.__postgresql_host} port={self.__postgresql_port} dbname={self.__postgresql_dbname} user={self.__postgresql_user} password={self.__postgresql_password}"

    def get_connection(self):
        return psycopg2.connect(self.__connection_string)
    
    def execute_create_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ):
        logger.debug(f"create query: {query}, parameters: {parameters}")
        with self.get_connection() as conn:
            try:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query, parameters)
                conn.commit()
            except psycopg2.Error as e:
                conn.rollback()
                raise DatabaseException(
                    message=f"failed to insert or update query: {e}",
                    detail=f"{query} {parameters}: {e}",
                )

    def execute_bulk_insert_or_update_query(
        self,
        query: str,
        parameters: Optional[List[Tuple]] = None,
    ) -> bool:
        # logger.debug(f"bulk insert or update query: {query}, parameters: {parameters}")
        with self.get_connection() as conn:
            try:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    extras.execute_values(cursor, query, parameters)
                conn.commit()
                return True
            except psycopg2.Error as e:
                conn.rollback()
                raise DatabaseException(
                    message=f"failed to bulk insert or update query: {e}",
                    detail=f"{query} {parameters}: {e}",
                )
