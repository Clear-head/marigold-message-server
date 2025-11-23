# Kafka Infrastructure

## 목적
Kafka를 통한 메시지 발행/구독 기능을 구현합니다.

## 특징
- aiokafka 사용 (비동기)
- Producer: 메시지를 Kafka로 발행
- Consumer: Kafka에서 메시지 구독
- 서버 간 실시간 메시지 동기화

## 포함될 파일
- `kafka_config.py`: Kafka 설정
- `kafka_producer.py`: Kafka Producer 구현
- `kafka_consumer.py`: Kafka Consumer 구현

## 책임
- Kafka 연결 관리
- 메시지 직렬화/역직렬화
- 이벤트 발행 및 구독