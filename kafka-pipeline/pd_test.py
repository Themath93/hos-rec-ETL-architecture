import time
from kafka import KafkaProducer
broker = ["localhost:19092","localhost:19093","localhost:19094"]
# broker = ["localhost:19092"]

# producer 객체 생성
# acks 0 -> 빠른 전송우선, acks 1 -> 데이터 정확성 우선
# producer = KafkaProducer(acks=0, compression_type='gzip',bootstrap_servers=broker)
producer = KafkaProducer(acks="all",bootstrap_servers=broker,linger_ms=1,batch_size=3000)

start = time.time()

for i in range(10000):
 producer.send('test1',str(f'{i}_message').encode('utf-8'))
 producer.flush() #queue에 있는 데이터를 보냄

end = time.time() - start
print(end)