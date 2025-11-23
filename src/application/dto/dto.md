# DTO (Data Transfer Object)

## 목적
계층 간 데이터 전송을 위한 단순 컨테이너입니다.

## 특징
- 로직 없음 (순수 데이터만)
- Request DTO와 Response DTO로 구분
- Controller ↔ Application 간 데이터 전달
- 불필요한 도메인 정보 노출 방지

## 포함될 파일
- `message_dto.py`: 메시지 관련 DTO
- `room_dto.py`: 채팅방 관련 DTO

## 책임
- 데이터 전달
- 계층 간 결합도 감소