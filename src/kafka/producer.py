from kafka import KafkaProducer
import jsonlines
import json


producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

filename = 'stream.jsonl'
with jsonlines.open(filename) as f:
    for line in f:
        try:
            line = f.read()
            data = producer.send('sample', json.dumps(line).encode('utf-8'))
            data.get(timeout=60)
        except EOFError:
            break
    print('Done.')
