import jsonlines
import json
import os
from kafka import KafkaProducer

kafka_host = os.environ.get('KAFKA_HOST')
kafka_port = os.environ.get('KAFKA_PORT')
producer = KafkaProducer(bootstrap_servers=[f'{kafka_host}:{kafka_port}'])

filename = 'stream.jsonl'
with jsonlines.open(filename) as f:
    for line in f:
        try:
            line = f.read()
            data = producer.send('kafka_distinct_counter',
                                 json.dumps(line).encode('utf-8'))
            data.get(timeout=60)
        except EOFError:
            break
    print('Done.')
