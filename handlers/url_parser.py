import json
import feedparser


def rss_parser(event, context):
    try:
        rssUrl = event['rssUrl']

        feed = feedparser.parse(rssUrl)

        for item in feed.entries:
            print(item.title)
            print(item.published)
        
    
    except e:
        print(e)


