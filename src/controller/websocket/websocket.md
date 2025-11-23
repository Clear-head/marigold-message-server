# WebSocket Controller

## 목적
WebSocket 연결을 관리하고 실시간 통신을 처리합니다.

## 특징
- 클라이언트와 양방향 실시간 통신
- 연결 생명주기 관리
- 메시지 브로드캐스팅

## 포함될 파일
- `connection_manager.py`: WebSocket 연결 관리자
- `websocket_handler.py`: WebSocket 핸들러

## 책임
- WebSocket 연결 수락/종료
- 메시지 수신 및 전달
- 채팅방별 브로드캐스팅