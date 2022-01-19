import json
import os
import boto3


def put_job(event, context):
    data = json.loads(event['body'])
    rssUrl = data['rssUrl']
    schedule = data['schedule']

    dynamodb = boto3.resource('dynamodb', endpoint_url=os.environ.get('DB_URL'))

    table = dynamodb.Table('Jobs')
    response = table.put_item(
        Item={
            'rssUrl': rssUrl,
            'schedule': schedule,
        }
    )

    return response
