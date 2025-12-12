from datetime import datetime
from uuid import uuid4
from src.domain.value_object.message_content import MessageContent
from src.domain.value_object.user_id import UserId
from src.domain.value_object.room_id import RoomId


class Message:

    def __init__(
            self,
            id: str,
            content: MessageContent,
            created_at: datetime,
            room_id: RoomId,
            sender_id: UserId,
            seq: int
    ):
        self.id = id
        self.content = content
        self.created_at = created_at
        self.room_id = room_id
        self.sender_id = sender_id
        self.seq = seq

    @classmethod
    def create(
            cls,
            content: str,
            room_id: int,
            sender_id: str,
            seq: int = None,
            message_id: str = None,
            created_at: datetime = None
    ) -> 'Message':
        return cls(
            id=message_id or str(uuid4()),
            content=MessageContent(content),
            created_at=created_at or datetime.utcnow(),
            room_id=RoomId(room_id),
            sender_id=UserId(sender_id),
            seq=seq or 0
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Message):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"Message(id='{self.id}', "
            f"sender_id='{self.sender_id.value}', "
            f"room_id={self.room_id.value}, "
            f"seq={self.seq})"
        )