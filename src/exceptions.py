class ApplicationError(Exception):
    def __init__(self, message: str, error_code: int, extras: dict = None, status_code: int = 400):
        self.message = message
        self.error_code = error_code
        self.extras = extras
        self.status_code = status_code


class ObjectNotFoundError(ApplicationError):
    def __init__(self, message: str, status_code: int = 404):
        super().__init__(message, 10001, None, status_code)


class RedisObjectNotFound(Exception):
    ...
