# REST API Controller

## 목적
HTTP REST API 엔드포인트를 제공합니다.

## 특징
- FastAPI 라우터 사용
- Request 검증 (Pydantic)
- Use Case 호출
- Response 변환

## 포함될 파일
- `v1/message_controller.py`: 메시지 관련 API
- `v1/room_controller.py`: 채팅방 관련 API

## 책임
- HTTP 요청 처리
- 요청 데이터 검증
- Use Case 실행
- HTTP 응답 반환