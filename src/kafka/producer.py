from kafka import KafkaProducer
import jsonlines
import json


producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

filename = 'temp.jsonl'
with jsonlines.open(filename) as f:
    for line in f:
        try:
            line = f.read()
            print('line: ', line)
            data = producer.send('sample', json.dumps(line).encode('utf-8'))
            data.get(timeout=60)
        except EOFError:
            break
