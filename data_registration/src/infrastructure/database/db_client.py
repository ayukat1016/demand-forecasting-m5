import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

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
        parameters: Optional[Tuple] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def execute_bulk_insert_or_update_query(
        self,
        query: str,
        parameters: Optional[List[Tuple]] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def execute_select(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError


class PostgreSQLClient(AbstractDBClient):
    def __init__(self):
        self.__postgres_user = os.getenv("POSTGRES_USER")
        self.__postgres_password = os.getenv("POSTGRES_PASSWORD")
        self.__postgres_port = int(os.getenv("POSTGRES_PORT", 5432))
        self.__postgres_dbname = os.getenv("POSTGRES_DBNAME")
        self.__postgres_host = os.getenv("POSTGRES_HOST")
        self.__connection_string = f"host={self.__postgres_host} port={self.__postgres_port} dbname={self.__postgres_dbname} user={self.__postgres_user} password={self.__postgres_password}"

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
        logger.debug(f"bulk insert or update query: {query}, parameters: {parameters}")
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

    def execute_select(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> List[Dict[str, Any]]:
        logger.debug(f"select query: {query}, parameters: {parameters}")
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, parameters)
                columns = [desc[0] for desc in cursor.description]
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        logger.debug(f"rows: {rows}")
        return rows
