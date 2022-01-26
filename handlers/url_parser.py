import feedparser


def rss_parser(event, context):
    try:
        data = json.loads(event['body'])
        rssUrl = data['rssUrl']

        feed = feedparser.parse(url)

        return
