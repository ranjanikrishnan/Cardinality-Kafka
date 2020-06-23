from kafka import KafkaConsumer
import json


consumer = KafkaConsumer('sample', bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest', enable_auto_commit=True,
                         group_id='sample')
for message in consumer:
    data = json.loads(message.value)
    print(data)
