from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
print('producer: ', producer)
for i in range(10):
    producer.send('test', b'Hello, World!').get(timeout=60)
