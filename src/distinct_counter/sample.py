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

page_views = app.Table('sample', default=int).tumbling(60.0, expires=60.0)


@app.agent(sample_topic)
async def count_page_views(views):
    async for view in views.group_by(StreamData.uid):
        # print(view)
        print(view.uid)
        # page_views[view.uid] += 1
