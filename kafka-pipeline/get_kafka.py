from kafka import KafkaProducer
from kafka import KafkaConsumer
import json


class MessageProducer:
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=self.broker,
            value_serializer=lambda x: json.dumps(x,ensure_ascii=False).encode("utf-8"),
            acks=0,
            request_timeout_ms=30000,
            retries=1,
            linger_ms=1000
        )

    def send_message(self, msg, auto_close=True):
        try:
            future = self.producer.send(self.topic, msg)
            self.producer.flush()  # 비우는 작업
            if auto_close:
                self.producer.close()
            future.get(timeout=2)
            return {"status_code": 200, "error": None}
        except Exception as exc:
            print("exception")
            raise exc

class Consumer:
    def __init__(self, broker, topic, group_id):
        self.broker = broker
        self.topic = topic
        self.group_id = group_id
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.broker,
            group_id=self.group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            consumer_timeout_ms=1000,
        )
