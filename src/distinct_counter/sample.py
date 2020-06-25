import faust


app = faust.App(
    'sample',
    broker='kafka://localhost:9092'
)


class StreamData(faust.Record):
    uid: str
    ts: str


sample_topic = app.topic('sample', value_type=StreamData)
print('sample_topic: ', sample_topic)

streaming_data_table = app.Table('sample', default=int).tumbling(60.0, expires=60.0)

distinct_count = app.Table('distinct_count', default=int).tumbling(60.0, expires=60.0)


@app.agent(sample_topic)
async def count_streaming_data_table(views):
    async for view in views.group_by(StreamData.uid):
        uid = view.uid
        streaming_data_table[uid] += 1
        if streaming_data_table[uid].current() == 1:
            distinct_count['total'] += 1
