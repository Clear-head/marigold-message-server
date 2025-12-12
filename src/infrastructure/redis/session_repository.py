import json
from typing import Optional, Dict, Any
from redis.asyncio import Redis

from src.util.custom_logger import get_logger

logger = get_logger(__name__)


class SessionRepository:

    def __init__(self, redis: Redis):
        self.redis = redis

    async def set_session(
            self,
            session_id: str,
            user_id: str,
            token_type: str,
            ttl: int,
            data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        세션 저장

        Args:
            session_id: 세션 ID (토큰 값)
            user_id: 사용자 ID
            token_type: 토큰 타입 (access/refresh)
            ttl: 만료 시간 (초)
            data: 추가 데이터
        """
        try:
            session_data = {
                "user_id": user_id,
                "token_type": token_type,
                **(data or {})
            }

            key = f"session:{token_type}:{session_id}"
            await self.redis.setex(
                key,
                ttl,
                json.dumps(session_data)
            )

            logger.info(f"세션 저장 성공: user_id={user_id}, type={token_type}, ttl={ttl}s")

        except Exception as e:
            logger.error(f"세션 저장 실패: {e}")
            raise

    async def get_session(self, session_id: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """
        세션 조회

        Args:
            session_id: 세션 ID (토큰 값)
            token_type: 토큰 타입 (access/refresh)

        Returns:
            Optional[Dict]: 세션 데이터 (없으면 None)
        """
        try:
            key = f"session:{token_type}:{session_id}"
            data = await self.redis.get(key)

            if not data:
                logger.debug(f"세션 없음: {session_id}")
                return None

            return json.loads(data)

        except Exception as e:
            logger.error(f"세션 조회 실패: {e}")
            return None

    async def delete_session(self, session_id: str, token_type: str = "access") -> bool:
        """
        세션 삭제 (로그아웃)

        Args:
            session_id: 세션 ID
            token_type: 토큰 타입

        Returns:
            bool: 삭제 성공 여부
        """
        try:
            key = f"session:{token_type}:{session_id}"
            result = await self.redis.delete(key)
            logger.info(f"세션 삭제: {session_id}")
            return result > 0

        except Exception as e:
            logger.error(f"세션 삭제 실패: {e}")
            return False

    async def get_user_sessions(self, user_id: str) -> list:
        """
        특정 사용자의 모든 세션 조회

        Args:
            user_id: 사용자 ID

        Returns:
            list: 세션 목록
        """
        try:
            # 패턴 매칭으로 모든 세션 키 조회
            pattern = f"session:*:*"
            keys = []

            async for key in self.redis.scan_iter(match=pattern):
                session_data = await self.redis.get(key)
                if session_data:
                    data = json.loads(session_data)
                    if data.get("user_id") == user_id:
                        keys.append(key)

            return keys

        except Exception as e:
            logger.error(f"사용자 세션 조회 실패: {e}")
            return []

    async def delete_user_sessions(self, user_id: str) -> int:
        """
        특정 사용자의 모든 세션 삭제

        Args:
            user_id: 사용자 ID

        Returns:
            int: 삭제된 세션 수
        """
        try:
            keys = await self.get_user_sessions(user_id)

            if not keys:
                return 0

            deleted = await self.redis.delete(*keys)
            logger.info(f"사용자 세션 전체 삭제: user_id={user_id}, count={deleted}")
            return deleted

        except Exception as e:
            logger.error(f"사용자 세션 삭제 실패: {e}")
            return 0

    async def extend_session(self, session_id: str, token_type: str, additional_ttl: int) -> bool:
        """
        세션 만료 시간 연장

        Args:
            session_id: 세션 ID
            token_type: 토큰 타입
            additional_ttl: 추가 만료 시간 (초)

        Returns:
            bool: 연장 성공 여부
        """
        try:
            key = f"session:{token_type}:{session_id}"
            result = await self.redis.expire(key, additional_ttl)

            if result:
                logger.info(f"세션 연장: {session_id}, +{additional_ttl}s")

            return result

        except Exception as e:
            logger.error(f"세션 연장 실패: {e}")
            return False