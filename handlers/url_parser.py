import feedparser
from helpers.aws import dynamodb
from dict2xml import dict2xml
from helpers.aws import event_client, s3_client, XML_BUCKET_NAME
from os import environ


COLUMBIA_API = environ.get('COLUMBIA_API')


def rss_parser(event, context):
    try:
        id = event['id']
        name = event['name']
        table = dynamodb.Table('Jobs')

        result = table.get_item(Key={'id': id})
        job = result.get('Item')

        if not job:
            event_client.remove_targets(Rule=name, Ids=[id])
            event_client.delete_rule(Name=name)

        etag = job.get('etag')
        modified = job.get('modified')

        feed = feedparser.parse(
            job.get('rssUrl'), etag=etag, modified=modified)

        for item in feed.entries:
            data = {
                "title": item.title,
                "body": item.description,
                "date": item.published,
                "author": item.author
            }
            xml = dict2xml(data, wrap='root', indent="   ")

            s3_client.put_object(
                Bucket=XML_BUCKET_NAME, Key=f'{item.title}.xml', Body=xml)

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
