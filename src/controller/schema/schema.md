# Pydantic Schema

## 목적
API 요청/응답 데이터의 구조와 검증 규칙을 정의합니다.

## 특징
- Pydantic 모델 사용
- 자동 검증 및 직렬화
- API 문서 자동 생성
- 타입 힌팅

## 포함될 파일
- `message_schema.py`: 메시지 API 스키마
- `room_schema.py`: 채팅방 API 스키마

## 책임
- 요청 데이터 검증
- 응답 데이터 구조화
- OpenAPI 스키마 정의