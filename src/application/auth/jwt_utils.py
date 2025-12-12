"""
JWT 토큰 관리

JWT 토큰 생성, 검증 및 사용자 인증을 처리합니다.
"""

import traceback
from datetime import datetime, timedelta, timezone
from typing import Tuple

import jwt as jwt_token
from fastapi import Header

from src.config.settings import Settings
from src.infrastructure.redis.redis_client import get_redis
from src.infrastructure.redis.session_repository import SessionRepository
from src.application.exception.auth_exception import MissingTokenException, InvalidTokenException, ExpiredAccessTokenException
from src.util.custom_logger import get_logger

settings = Settings()
logger = get_logger(__name__)


# ========== JWT 토큰 생성 ==========

async def create_jwt_token(user_id: str) -> Tuple[str, str]:
    """
    JWT Access/Refresh 토큰 생성

    Args:
        user_id: 사용자 ID

    Returns:
        Tuple[str, str]: (access_token, refresh_token)
    """
    redis = await get_redis()
    session_repo = SessionRepository(redis)

    now = datetime.now(timezone.utc)
    access_token_expires = now + timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRE_HOURS)
    refresh_token_expires = now + timedelta(hours=settings.JWT_REFRESH_TOKEN_EXPIRE_HOURS)

    now_timestamp = int(now.timestamp())
    access_exp = int(access_token_expires.timestamp())
    refresh_exp = int(refresh_token_expires.timestamp())

    # Access Token Payload
    access_payload = {
        "userId": user_id,
        "exp": access_exp,
        "iat": now_timestamp,
        "iss": "marigold-chat-server",
        "type": "access"
    }

    # Refresh Token Payload
    refresh_payload = {
        "userId": user_id,
        "exp": refresh_exp,
        "iat": now_timestamp,
        "iss": "marigold-chat-server",
        "type": "refresh"
    }

    # 토큰 생성
    access_token = jwt_token.encode(
        access_payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    refresh_token = jwt_token.encode(
        refresh_payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    # Redis에 세션 저장
    access_ttl = access_exp - now_timestamp
    await session_repo.set_session(
        session_id=access_token,
        user_id=user_id,
        token_type="access",
        ttl=access_ttl,
        data={"refresh_token": refresh_token}
    )

    refresh_ttl = refresh_exp - now_timestamp
    await session_repo.set_session(
        session_id=refresh_token,
        user_id=user_id,
        token_type="refresh",
        ttl=refresh_ttl,
        data={"access_token": access_token}
    )

    logger.info(f"JWT 토큰 생성: user_id={user_id}")
    return access_token, refresh_token


# ========== JWT 토큰 검증 (HTTP Header용) ==========

async def get_jwt_user_id(authorization: str = Header(None)) -> str:
    """
    HTTP Header에서 JWT 토큰 검증 및 사용자 ID 추출

    Args:
        authorization: Authorization 헤더 (Bearer <token>)

    Returns:
        str: 사용자 ID

    Raises:
        MissingTokenException: 토큰이 없는 경우
        InvalidTokenException: 유효하지 않은 토큰
        ExpiredAccessTokenException: 만료된 토큰
    """
    if not authorization:
        logger.error("Authorization 헤더 없음")
        raise MissingTokenException()

    # Bearer 토큰 추출
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise InvalidTokenException()
    except ValueError:
        raise InvalidTokenException()

    return await _verify_token(token, "access")


# ========== JWT 토큰 검증 (WebSocket용) ==========

async def get_jwt_user_id_from_query(token: str) -> str:
    """
    WebSocket 쿼리 파라미터에서 JWT 토큰 검증 및 사용자 ID 추출

    Args:
        token: JWT 토큰 문자열

    Returns:
        str: 사용자 ID

    Raises:
        MissingTokenException: 토큰이 없는 경우
        InvalidTokenException: 유효하지 않은 토큰
        ExpiredAccessTokenException: 만료된 토큰

    Usage:
        @app.websocket("/ws")
        async def websocket_endpoint(
            websocket: WebSocket,
            token: str = Query(...)
        ):
            user_id = await get_jwt_user_id_from_query(token)
    """
    if not token:
        logger.error("토큰이 쿼리 파라미터에 없음")
        raise MissingTokenException()

    return await _verify_token(token, "access")


# ========== 토큰 검증 공통 로직 ==========

async def _verify_token(token: str, token_type: str) -> str:
    """
    JWT 토큰 검증 (내부 함수)

    Args:
        token: JWT 토큰
        token_type: 토큰 타입 (access/refresh)

    Returns:
        str: 사용자 ID

    Raises:
        InvalidTokenException: 유효하지 않은 토큰
        ExpiredAccessTokenException: 만료된 토큰
    """
    try:
        now = int(datetime.now(timezone.utc).timestamp())

        # JWT 디코딩
        decoded = jwt_token.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]  # 리스트로 전달
        )

        # Redis 세션 확인
        redis = await get_redis()
        session_repo = SessionRepository(redis)
        session = await session_repo.get_session(token, token_type)

        if not session:
            logger.error(f"세션 없음: {token[:20]}...")
            raise InvalidTokenException()

        # 토큰 위조 검증
        if (
            decoded["iss"] != "marigold-chat-server"
            or decoded["iat"] > decoded["exp"]
            or decoded["iat"] > now
            or decoded.get("type") != token_type
        ):
            logger.error(f"토큰 위조 감지: {token[:20]}...")
            raise jwt_token.InvalidTokenError()

        # 토큰 만료 검증
        if decoded["exp"] < now:
            logger.error(f"토큰 만료: {token[:20]}...")
            raise jwt_token.ExpiredSignatureError()

        return decoded["userId"]

    except jwt_token.ExpiredSignatureError as e:
        logger.error(f"ExpiredSignatureError: {type(e).__name__}")
        traceback.print_exc()
        raise ExpiredAccessTokenException()

    except jwt_token.InvalidTokenError as e:
        logger.error(f"InvalidTokenError: {type(e).__name__}")
        traceback.print_exc()
        raise InvalidTokenException()

    except Exception as e:
        logger.error(f"토큰 검증 중 예외: {e}")
        traceback.print_exc()
        raise InvalidTokenException()


# ========== Refresh Token으로 Access Token 갱신 ==========

async def refresh_access_token(refresh_token: str) -> Tuple[str, str]:
    """
    Refresh Token으로 새로운 Access Token 발급

    Args:
        refresh_token: Refresh Token

    Returns:
        Tuple[str, str]: (new_access_token, refresh_token)

    Raises:
        InvalidTokenException: 유효하지 않은 Refresh Token
    """
    try:
        # Refresh Token 검증
        user_id = await _verify_token(refresh_token, "refresh")

        # 새로운 Access Token 생성
        redis = await get_redis()
        session_repo = SessionRepository(redis)

        now = datetime.now(timezone.utc)
        access_token_expires = now + timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRE_HOURS)
        now_timestamp = int(now.timestamp())
        access_exp = int(access_token_expires.timestamp())

        access_payload = {
            "userId": user_id,
            "exp": access_exp,
            "iat": now_timestamp,
            "iss": "marigold-chat-server",
            "type": "access"
        }

        new_access_token = jwt_token.encode(
            access_payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        # Redis에 새 Access Token 세션 저장
        access_ttl = access_exp - now_timestamp
        await session_repo.set_session(
            session_id=new_access_token,
            user_id=user_id,
            token_type="access",
            ttl=access_ttl,
            data={"refresh_token": refresh_token}
        )

        logger.info(f"Access Token 갱신: user_id={user_id}")
        return new_access_token, refresh_token

    except Exception as e:
        logger.error(f"토큰 갱신 실패: {e}")
        raise InvalidTokenException()


# ========== 로그아웃 (세션 삭제) ==========

async def logout(access_token: str, refresh_token: str) -> None:
    """
    로그아웃 처리 (Redis 세션 삭제)

    Args:
        access_token: Access Token
        refresh_token: Refresh Token
    """
    try:
        redis = await get_redis()
        session_repo = SessionRepository(redis)

        await session_repo.delete_session(access_token, "access")
        await session_repo.delete_session(refresh_token, "refresh")

        logger.info("로그아웃 성공")

    except Exception as e:
        logger.error(f"로그아웃 실패: {e}")