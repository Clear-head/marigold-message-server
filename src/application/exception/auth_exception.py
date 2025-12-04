from fastapi import HTTPException
from starlette import status


class MissingTokenException(HTTPException):
    """토큰이 없는 경우"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 토큰이 필요합니다"
        )


class InvalidTokenException(HTTPException):
    """유효하지 않은 토큰"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다"
        )


class ExpiredAccessTokenException(HTTPException):
    """만료된 토큰"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 만료되었습니다"
        )