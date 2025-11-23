"""

    메시지 비즈니스 로직

"""
from src.domain.exception.message_exception import InvalidMessageException


class MessageContent:
    """
    - 메시지는 비어있을 수 없음
    - 메시지는 1000자를 초과할 수 없음
    """

    MIN_LENGTH = 1
    MAX_LENGTH = 1000

    def __init__(self, value: str):
        self._value = self._validate_and_clean(value)

    def _validate_and_clean(self, value: str) -> str:
        """메시지 검증 및 정제"""
        if not isinstance(value, str):
            raise InvalidMessageException("메시지는 문자열이어야 합니다")


        # 빈 메시지 검증
        if len(value) < self.MIN_LENGTH:
            raise InvalidMessageException("메시지는 비어있을 수 없습니다")

        # 길이 검증
        if len(value) > self.MAX_LENGTH:
            raise InvalidMessageException(
                f"메시지는 {self.MAX_LENGTH}자를 초과할 수 없습니다"
            )

        return value

    @property
    def value(self) -> str:
        """메시지 내용 반환"""
        return self._value

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"MessageContent(value='{self._value}')"

    def __eq__(self, other) -> bool:
        """값 객체는 값으로 비교"""
        if not isinstance(other, MessageContent):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        """불변 객체이므로 해시 가능"""
        return hash(self._value)