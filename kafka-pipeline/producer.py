from kafka import KafkaProducer
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
                


# # 브로커와 토픽명을 지정한다.
# broker = ["localhost:19092","localhost:19093","localhost:19094"]
# # broker = ["localhost:9092"]
# topic = "test1"
# pd = MessageProducer(broker, topic)
# print(pd.producer.bootstrap_connected())
# # print(pd.producer.)
# msg = {"name": "John", "age": 30}
# # msg = b'this is message'
# res = pd.send_message(msg)
# print(res)