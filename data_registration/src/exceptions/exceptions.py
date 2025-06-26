class BaseException(Exception):
    def __init__(self, message: str, detail: str) -> None:
        self.message = message
        self.detail = detail


class DatabaseException(BaseException):
    def __init__(self, message: str, detail: str) -> None:
        super().__init__(message=message, detail=detail)
        self.__message = f"database exception: {self.message}"

    def __str__(self) -> str:
        return self.__message
