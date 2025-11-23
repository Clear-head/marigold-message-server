# MongoDB Infrastructure

## 목적
MongoDB를 사용한 데이터 영속성을 구현합니다.

## 특징
- Repository 인터페이스 구현체
- Motor (async MongoDB driver) 사용
- 도메인 객체 ↔ MongoDB Document 변환
- ODM 없이 순수 Motor 사용

## 포함될 파일
- `connection.py`: MongoDB 연결 설정
- `message_repository_impl.py`: 메시지 리포지토리 구현
- `room_repository_impl.py`: 채팅방 리포지토리 구현

## 책임
- 도메인 객체를 MongoDB에 저장
- MongoDB Document를 도메인 객체로 변환
- 데이터베이스 연결 관리