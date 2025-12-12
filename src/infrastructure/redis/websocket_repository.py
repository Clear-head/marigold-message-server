from typing import List, Set, Optional
from redis.asyncio import Redis

from src.util.custom_logger import get_logger

logger = get_logger(__name__)


class WebSocketRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    # ========== 사용자 온라인 상태 관리 ==========

    async def set_user_online(self, user_id: str, connection_id: str, ttl: int = 3600) -> None:
        """
        사용자를 온라인 상태로 설정

        Args:
            user_id: 사용자 ID
            connection_id: WebSocket 연결 ID
            ttl: 만료 시간 (초, 기본 1시간)
        """
        try:
            key = f"ws:user:{user_id}"
            await self.redis.setex(key, ttl, connection_id)
            logger.info(f"사용자 온라인: user_id={user_id}, conn={connection_id}")

        except Exception as e:
            logger.error(f"사용자 온라인 설정 실패: {e}")

    async def set_user_offline(self, user_id: str) -> None:
        """
        사용자를 오프라인 상태로 설정

        Args:
            user_id: 사용자 ID
        """
        try:
            key = f"ws:user:{user_id}"
            await self.redis.delete(key)
            logger.info(f"사용자 오프라인: user_id={user_id}")

        except Exception as e:
            logger.error(f"사용자 오프라인 설정 실패: {e}")

    async def is_user_online(self, user_id: str) -> bool:
        """
        사용자 온라인 여부 확인

        Args:
            user_id: 사용자 ID

        Returns:
            bool: 온라인 여부
        """
        try:
            key = f"ws:user:{user_id}"
            return await self.redis.exists(key) > 0

        except Exception as e:
            logger.error(f"사용자 온라인 확인 실패: {e}")
            return False

    async def get_user_connection_id(self, user_id: str) -> Optional[str]:
        """
        사용자의 WebSocket 연결 ID 조회

        Args:
            user_id: 사용자 ID

        Returns:
            Optional[str]: 연결 ID (오프라인이면 None)
        """
        try:
            key = f"ws:user:{user_id}"
            return await self.redis.get(key)

        except Exception as e:
            logger.error(f"연결 ID 조회 실패: {e}")
            return None

    # ========== 채팅방별 접속자 관리 ==========

    async def add_user_to_room(self, room_id: int, user_id: str) -> None:
        """
        채팅방에 사용자 추가

        Args:
            room_id: 채팅방 ID
            user_id: 사용자 ID
        """
        try:
            key = f"ws:room:{room_id}:users"
            await self.redis.sadd(key, user_id)
            logger.info(f"채팅방 입장: room_id={room_id}, user_id={user_id}")

        except Exception as e:
            logger.error(f"채팅방 입장 실패: {e}")

    async def remove_user_from_room(self, room_id: int, user_id: str) -> None:
        """
        채팅방에서 사용자 제거

        Args:
            room_id: 채팅방 ID
            user_id: 사용자 ID
        """
        try:
            key = f"ws:room:{room_id}:users"
            await self.redis.srem(key, user_id)
            logger.info(f"채팅방 퇴장: room_id={room_id}, user_id={user_id}")

        except Exception as e:
            logger.error(f"채팅방 퇴장 실패: {e}")

    async def get_room_users(self, room_id: int) -> Set[str]:
        """
        채팅방의 현재 접속자 목록

        Args:
            room_id: 채팅방 ID

        Returns:
            Set[str]: 사용자 ID 집합
        """
        try:
            key = f"ws:room:{room_id}:users"
            members = await self.redis.smembers(key)
            return set(members) if members else set()

        except Exception as e:
            logger.error(f"채팅방 사용자 조회 실패: {e}")
            return set()

    async def get_room_online_users(self, room_id: int) -> List[str]:
        """
        채팅방의 온라인 사용자만 조회

        Args:
            room_id: 채팅방 ID

        Returns:
            List[str]: 온라인 사용자 ID 목록
        """
        try:
            room_users = await self.get_room_users(room_id)
            online_users = []

            for user_id in room_users:
                if await self.is_user_online(user_id):
                    online_users.append(user_id)

            return online_users

        except Exception as e:
            logger.error(f"온라인 사용자 조회 실패: {e}")
            return []

    async def get_room_offline_users(self, room_id: int) -> List[str]:
        """
        채팅방의 오프라인 사용자 조회 (Firebase 알림용)

        Args:
            room_id: 채팅방 ID

        Returns:
            List[str]: 오프라인 사용자 ID 목록
        """
        try:
            room_users = await self.get_room_users(room_id)
            offline_users = []

            for user_id in room_users:
                if not await self.is_user_online(user_id):
                    offline_users.append(user_id)

            return offline_users

        except Exception as e:
            logger.error(f"오프라인 사용자 조회 실패: {e}")
            return []

    async def get_room_count(self, room_id: int) -> int:
        """
        채팅방 현재 인원 수

        Args:
            room_id: 채팅방 ID

        Returns:
            int: 인원 수
        """
        try:
            key = f"ws:room:{room_id}:users"
            return await self.redis.scard(key)

        except Exception as e:
            logger.error(f"채팅방 인원 수 조회 실패: {e}")
            return 0

    async def clear_room(self, room_id: int) -> None:
        """
        채팅방 접속자 전체 삭제

        Args:
            room_id: 채팅방 ID
        """
        try:
            key = f"ws:room:{room_id}:users"
            await self.redis.delete(key)
            logger.info(f"채팅방 초기화: room_id={room_id}")

        except Exception as e:
            logger.error(f"채팅방 초기화 실패: {e}")

    # ========== 사용자별 입장한 채팅방 관리 ==========

    async def add_room_to_user(self, user_id: str, room_id: int) -> None:
        """
        사용자가 입장한 채팅방 기록

        Args:
            user_id: 사용자 ID
            room_id: 채팅방 ID
        """
        try:
            key = f"ws:user:{user_id}:rooms"
            await self.redis.sadd(key, str(room_id))

        except Exception as e:
            logger.error(f"사용자 채팅방 추가 실패: {e}")

    async def remove_room_from_user(self, user_id: str, room_id: int) -> None:
        """
        사용자가 퇴장한 채팅방 제거

        Args:
            user_id: 사용자 ID
            room_id: 채팅방 ID
        """
        try:
            key = f"ws:user:{user_id}:rooms"
            await self.redis.srem(key, str(room_id))

        except Exception as e:
            logger.error(f"사용자 채팅방 제거 실패: {e}")

    async def get_user_rooms(self, user_id: str) -> Set[int]:
        """
        사용자가 현재 입장한 채팅방 목록

        Args:
            user_id: 사용자 ID

        Returns:
            Set[int]: 채팅방 ID 집합
        """
        try:
            key = f"ws:user:{user_id}:rooms"
            rooms = await self.redis.smembers(key)
            return {int(room_id) for room_id in rooms} if rooms else set()

        except Exception as e:
            logger.error(f"사용자 채팅방 목록 조회 실패: {e}")
            return set()

    async def clear_user_rooms(self, user_id: str) -> None:
        """
        사용자의 모든 채팅방 정보 삭제 (연결 종료 시)

        Args:
            user_id: 사용자 ID
        """
        try:
            # 사용자가 입장한 모든 채팅방에서 제거
            rooms = await self.get_user_rooms(user_id)
            for room_id in rooms:
                await self.remove_user_from_room(room_id, user_id)

            # 사용자의 채팅방 목록 삭제
            key = f"ws:user:{user_id}:rooms"
            await self.redis.delete(key)

            logger.info(f"사용자 채팅방 정보 초기화: user_id={user_id}")

        except Exception as e:
            logger.error(f"사용자 채팅방 정보 초기화 실패: {e}")