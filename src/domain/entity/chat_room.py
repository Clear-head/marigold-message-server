from datetime import datetime
from typing import List
from src.domain.value_object.room_id import RoomId
from src.domain.value_object.user_id import UserId
from src.domain.exception.domain_exception import DomainException


class ChatRoom:
    MAX_NAME_LENGTH = 100

    def __init__(
            self,
            id: RoomId,
            name: str,
            created_at: datetime,
            creator_id: UserId,
            participant_ids: List[str]
    ):
        self.id = id
        self.name = self._validate_name(name)
        self.created_at = created_at
        self.creator_id = creator_id
        self.participant_ids = participant_ids

    def _validate_name(self, name: str) -> str:
        if not name or not name.strip():
            raise DomainException("채팅방 이름은 비어있을 수 없습니다")

        if len(name) > self.MAX_NAME_LENGTH:
            raise DomainException(f"채팅방 이름은 {self.MAX_NAME_LENGTH}자를 초과할 수 없습니다")

        return name.strip()

    @classmethod
    def create(
            cls,
            name: str,
            creator_id: str,
            room_id: int = None,
            created_at: datetime = None
    ) -> 'ChatRoom':
        creator_user_id = UserId(creator_id)

        if room_id is None:
            raise DomainException("채팅방 ID는 필수입니다")

        return cls(
            id=RoomId(room_id),
            name=name,
            created_at=created_at or datetime.now(),
            creator_id=creator_user_id,
            participant_ids=[creator_user_id.value]
        )

    def add_participant(self, user_id: str) -> None:
        validated_user_id = UserId(user_id)

        if validated_user_id.value not in self.participant_ids:
            self.participant_ids.append(validated_user_id.value)

    def remove_participant(self, user_id: str) -> None:
        validated_user_id = UserId(user_id)

        if validated_user_id.value in self.participant_ids:
            self.participant_ids.remove(validated_user_id.value)

    def is_participant(self, user_id: str) -> bool:
        try:
            validated_user_id = UserId(user_id)
            return validated_user_id.value in self.participant_ids
        except DomainException:
            return False

    @property
    def participant_count(self) -> int:
        return len(self.participant_ids)

    def update_name(self, new_name: str) -> None:
        self.name = self._validate_name(new_name)

    def __eq__(self, other) -> bool:
        if not isinstance(other, ChatRoom):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"ChatRoom(id={self.id.value}, "
            f"name='{self.name}', "
            f"participants={self.participant_count})"
        )