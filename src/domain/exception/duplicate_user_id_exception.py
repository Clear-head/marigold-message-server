from src.domain.exception.domain_exception import DomainException


class DuplicateUserIdException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)
