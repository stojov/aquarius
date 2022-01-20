import json
import os
import boto3
import uuid


def put_job(event, context):
    data = json.loads(event['body'])
    id = str(uuid.uuid4())
    rssUrl = data['rssUrl']
    schedule = data['schedule']

    dynamodb = boto3.resource('dynamodb', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get(
        'AWS_SECRET_ACCESS_KEY'), region_name=os.environ.get('AWS_REGION'), endpoint_url=os.environ.get('DB_URL'))

    table = dynamodb.Table('Jobs')
    response = table.put_item(
        Item={
            'id': id,
            'rssUrl': rssUrl,
            'schedule': schedule,
        }
    )

    return response


def get_job(event, context):
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get(
        'AWS_SECRET_ACCESS_KEY'), region_name=os.environ.get('AWS_REGION'), endpoint_url=os.environ.get('DB_URL'))

    table = dynamodb.Table('Jobs')
    response = table.scan()

    return response['Items']
