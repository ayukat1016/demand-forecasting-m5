import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extras import DictCursor
from logger import configure_logger

logger = configure_logger(__name__)


class AbstractDBClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_connection(self):
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

    def execute_select(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> List[Dict[str, Any]]:
        # logger.info(f"select query: {query}, parameters: {parameters}")
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, parameters)
                rows = cursor.fetchall()
        return rows
