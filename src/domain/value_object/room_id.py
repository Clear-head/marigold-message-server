"""채팅방 ID 값 객체"""

from src.domain.exception.domain_exception import DomainException


class RoomId:
    """
        숫자만.
    """
    MAX_VALUE = 2147483647
    MIN_VALUE = 0

    def __init__(self, value: int):
        """
        Args:
            value: 채팅방 ID

        Raises:
            DomainException: 유효하지 않은 ID인 경우
        """
        self._value = self._validate(value)

    def _validate(self, value: int) -> int:
        """ID 검증"""
        if not isinstance(value, int):
            raise DomainException("채팅방 ID는 문자열이어야 합니다")
        if value > RoomId.MAX_VALUE:
            raise DomainException("채팅방 번호는 int 범위")
        if value < RoomId.MIN_VALUE:
            raise DomainException("채팅방 번호는 0~")

        return value

    @property
    def value(self) -> int:
        """ID 값 반환"""
        return self._value

    def __str__(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return f"RoomId(value='{self._value}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, RoomId):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)