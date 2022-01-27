import feedparser
from helpers.db import dynamodb


def rss_parser(event, context):
    try:
        id = event['queryStringParameters']['id']
        table = dynamodb.Table('Jobs')

        result = table.get_item(Key={'id': id})
        job = result.get('Item')

        etag = job.get('etag')
        modified = job.get('modified')

        feed = feedparser.parse(
            job.get('rssUrl'), etag=etag, modified=modified)

        for item in feed.entries:
            print(item.title)
            print(item.published)

        etag = feed.get('etag')
        modified = feed.get('modified')

        table.update_item(
            Key={'id': id},
            UpdateExpression="SET etag=:etag, modified=:modified",
            ExpressionAttributeValues={
                ':etag': etag,
                ':modified': modified,
            },
            ReturnValues="UPDATED_NEW"
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": 'Ok'
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": 'Internal Server Error'
        }
