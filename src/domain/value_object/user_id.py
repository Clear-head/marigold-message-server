"""사용자 ID 값 객체"""

from src.domain.exception.domain_exception import DomainException
from re import compile

class UserId:
    """

        - 비어있을 수 없음
        - only english and number

    """

    PATTERN = compile(r'^[a-zA-Z0-9-]+$')

    def __init__(self, value: str):
        """
        Args:
            value: 사용자 ID

        Raises:
            DomainException: 유효하지 않은 ID인 경우
        """
        self._value = self._validate(value)

    def _validate(self, value: str) -> str:
        """ID 검증"""
        if not isinstance(value, str):
            raise DomainException("사용자 ID는 문자열이어야 합니다")

        if not value or value.strip() == "":
            raise DomainException("사용자 ID는 비어있을 수 없습니다")

        if not self.PATTERN.match(value):
            raise DomainException("사용자 ID는 영어와 숫자만 사용 가능")

        return value.strip()

    @property
    def value(self) -> str:
        """ID 값 반환"""
        return self._value

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"UserId(value='{self._value}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, UserId):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)