from fastapi import WebSocketException, status


class WebSocketAuthException(WebSocketException):
    """WebSocket 인증 실패"""

    def __init__(self):
        super().__init__(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="인증에 실패했습니다"
        )


class WebSocketConnectionException(WebSocketException):
    """WebSocket 연결 실패"""

    def __init__(self, reason: str = "연결에 실패했습니다"):
        super().__init__(
            code=status.WS_1011_INTERNAL_ERROR,
            reason=reason
        )


class WebSocketMessageException(WebSocketException):
    """WebSocket 메시지 처리 실패"""

    def __init__(self, reason: str = "메시지 처리 중 오류가 발생했습니다"):
        super().__init__(
            code=status.WS_1011_INTERNAL_ERROR,
            reason=reason
        )


class WebSocketRoomNotFoundException(WebSocketException):
    """채팅방을 찾을 수 없음"""

    def __init__(self):
        super().__init__(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="채팅방을 찾을 수 없습니다"
        )


class WebSocketUnauthorizedRoomException(WebSocketException):
    """채팅방 접근 권한 없음"""

    def __init__(self):
        super().__init__(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="채팅방에 접근할 권한이 없습니다"
        )