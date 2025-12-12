from src.domain.exception.domain_exception import DomainException


class UserAlreadyExistsException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)
