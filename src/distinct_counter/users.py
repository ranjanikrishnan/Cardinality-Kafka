import os
import faust


kafka_host = os.environ.get('KAFKA_HOST')
kafka_port = os.environ.get('KAFKA_PORT')
app = faust.App(
    'users',
    broker=f'kafka://{kafka_host}:{kafka_port}'
)


class StreamData(faust.Record):
    uid: str
    ts: str


distinct_counter_topic = app.topic('kafka_distinct_counter',
                                   value_type=StreamData)

streaming_data_table = app.Table('grouped', default=int)\
                          .tumbling(60.0, expires=60.0)

distinct_count = app.Table('unique', default=int)\
                    .tumbling(60.0, expires=60.0)


@app.agent(distinct_counter_topic)
async def count_streaming_data_table(messages):
    async for message in messages.group_by(StreamData.uid):
        uid = message.uid
        streaming_data_table[uid] += 1
        if streaming_data_table[uid].current() == 1:
            distinct_count['total'] += 1
            print(f'current unique user count per min: \
                {distinct_count["total"].current()}')
