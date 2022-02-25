import feedparser
from helpers.db import dynamodb
from dict2xml import dict2xml
import requests
from os import environ


COLUMBIA_API = environ.get('COLUMBIA_API')


def rss_parser(event, context):
    try:
        id = event['queryStringParameters']['id']
        print('Id Received->', id)
        print(id)
        table = dynamodb.Table('Jobs')

        result = table.get_item(Key={'id': id})
        job = result.get('Item')

        etag = job.get('etag')
        modified = job.get('modified')

        feed = feedparser.parse(
            job.get('rssUrl'), etag=etag, modified=modified)

        for item in feed.entries:
            data = {
                "title": item.title,
                "description": item.body,
                "pubDate": item.date,
                "author": item.author
            }
            xml = dict2xml(data, wrap='root', indent="   ")

            headers = {'Content-Type': 'application/xml'}
            requests.post(COLUMBIA_API, data=xml, headers=headers)

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
