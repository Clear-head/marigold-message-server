from src.domain.exception.domain_exception import DomainException


class InvalidMessageException(DomainException):
    """유효하지 않은 메시지 예외"""
    def __init__(self, message: str = "유효하지 않은 메시지입니다"):
        super().__init__(message)