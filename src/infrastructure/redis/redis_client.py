from redis.asyncio import Redis, ConnectionPool
from typing import Optional

from src.util.custom_logger import get_logger

logger = get_logger(__name__)


class RedisClient:
    def __init__(self):
        self._client: Optional[Redis] = None
        self._pool: Optional[ConnectionPool] = None

    async def connect(
        self,
        url: str,
        max_connections: int = 10,
        decode_responses: bool = True
    ) -> None:
        """
        Redis 연결 초기화

        Args:
            url: Redis 연결 URL (예: redis://localhost:6379/0)
            max_connections: 최대 연결 수
            decode_responses: 자동으로 bytes를 str로 변환 여부
        """
        try:
            self._pool = ConnectionPool.from_url(
                url,
                max_connections=max_connections,
                decode_responses=decode_responses,
                socket_connect_timeout=5,
                socket_keepalive=True,
                health_check_interval=30
            )
            self._client = Redis(connection_pool=self._pool)

            # 연결 테스트
            await self._client.ping()
            logger.info(f"Redis 연결 성공: {url}")

        except Exception as e:
            logger.error(f"Redis 연결 실패: {e}")
            raise

    async def disconnect(self) -> None:
        """Redis 연결 종료"""
        try:
            if self._client:
                await self._client.close()
                logger.info("Redis 클라이언트 종료")

            if self._pool:
                await self._pool.disconnect()
                logger.info("Redis 커넥션 풀 종료")

        except Exception as e:
            logger.error(f"Redis 연결 종료 중 오류: {e}")

    @property
    def client(self) -> Redis:
        """
        Redis 클라이언트 반환
        """
        if not self._client:
            raise RuntimeError("Redis가 연결되지 않았습니다. connect()를 먼저 호출하세요.")
        return self._client

    async def health_check(self) -> bool:
        """
        Redis 연결 상태 확인

        Returns:
            bool: 연결 정상 여부
        """
        try:
            await self._client.ping()
            return True
        except Exception as e:
            logger.error(f"Redis health check 실패: {e}")
            return False


async def get_redis() -> Redis:
    return redis_client.client

# 전역 Redis 클라이언트 인스턴스
redis_client = RedisClient()

