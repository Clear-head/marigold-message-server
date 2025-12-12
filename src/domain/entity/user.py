from datetime import datetime
from src.domain.value_object.user_id import UserId


class User:

    def __init__(
            self,
            id: UserId,
            username: str,
            created_at: datetime,
            is_active: bool = True
    ):
        self.id = id
        self.username = username
        self.created_at = created_at
        self.is_active = is_active

    @classmethod
    def create(
            cls,
            user_id: str,
            username: str,
            created_at: datetime = None
    ) -> 'User':
        return cls(
            id=UserId(user_id),
            username=username,
            created_at=created_at or datetime.now(),
            is_active=True
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"User(id='{self.id.value}', username='{self.username}')"