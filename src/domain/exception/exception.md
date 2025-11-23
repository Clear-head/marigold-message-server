# Domain Exception

## 목적
도메인 규칙 위반 시 발생하는 예외를 정의합니다.

## 특징
- 비즈니스 규칙 위반을 표현
- 명확한 예외 메시지
- 계층별 예외 변환의 기준

## 포함될 파일
- `domain_exception.py`: 도메인 예외 베이스 클래스
- `invalid_message_exception.py`: 유효하지 않은 메시지
- `room_not_found_exception.py`: 채팅방을 찾을 수 없음

## 책임
- 도메인 규칙 위반 표현
- 명확한 에러 메시지 제공