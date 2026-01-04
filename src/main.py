from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import Settings
from src.infrastructure.mongodb.mongo_connection import MongoDBConnection
from src.infrastructure.redis.redis_client import redis_client
from src.util.custom_logger import get_logger


settings = Settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 60)
    logger.info("MariGold Message Server 시작 중...")
    logger.info(f"환경: {settings.APP_ENV}")
    logger.info(f"디버그 모드: {settings.DEBUG}")
    logger.info("=" * 60)

    try:
        logger.info("MongoDB 연결 중...")
        await MongoDBConnection.connect()
        logger.info(f"MongoDB 연결 완료: {settings.MONGODB_DB_NAME}")

        logger.info("Redis 연결 중...")
        await redis_client.connect(
            url=settings.REDIS_URL,
            max_connections=settings.REDIS_MAX_CONNECTIONS or 10
        )
        logger.info("Redis 연결 완료")

        logger.info("=" * 60)
        logger.info("모든 인프라 연결 완료. 서버 준비 완료!")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"서버 시작 실패: {e}")
        raise

    yield

    logger.info("=" * 60)
    logger.info("MariGold Message Server 종료 중...")
    logger.info("=" * 60)

    try:
        logger.info("Redis 연결 해제 중...")
        await redis_client.disconnect()
        logger.info("Redis 연결 해제 완료")

        logger.info("MongoDB 연결 해제 중...")
        await MongoDBConnection.disconnect()
        logger.info("MongoDB 연결 해제 완료")

        logger.info("=" * 60)
        logger.info("서버 종료 완료")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"서버 종료 중 오류: {e}")


app = FastAPI(
    title="MariGold Message Server",
    description="MariGold Message Server",
    version="0.1.0",
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "service": "MariGold Message Server",
        "version": "0.1.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )
