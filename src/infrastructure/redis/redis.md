# Redis Infrastructure

## 목적
Redis를 사용한 WebSocket 연결 정보 저장 및 캐싱을 구현합니다.

## 특징
- 인메모리 데이터 저장
- WebSocket 연결 정보 관리
- 빠른 데이터 접근

## 포함될 파일
- `connection_store.py`: WebSocket 연결 저장소

## 책임
- 활성 WebSocket 연결 추적
- 채팅방별 참여자 관리
- 캐시 데이터 관리