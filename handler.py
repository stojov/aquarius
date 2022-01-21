import json
import os
import logging
import boto3
import uuid


def put_job(event, context):
    try:
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
    except Exception:
        logging.exception(Exception)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps('Internal Server Error')
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }


def update_job(event, context):
    try:
        id = event['pathParameters']['id']
        data = json.loads(event['body'])
        rssUrl = data['rssUrl']
        schedule = data['schedule']

        dynamodb = boto3.resource('dynamodb', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get(
            'AWS_SECRET_ACCESS_KEY'), region_name=os.environ.get('AWS_REGION'), endpoint_url=os.environ.get('DB_URL'))

        table = dynamodb.Table('Jobs')
        response = table.update_item(
            Key={'id': id},
            UpdateExpression="SET rssUrl=:rssUrl, schedule=:schedule",
            ConditionExpression="attribute_exists(id)",
            ExpressionAttributeValues={
                ':rssUrl': schedule,
                ':schedule': rssUrl,
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception:
        logging.exception(Exception)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps('Internal Server Error')
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response["Attributes"])
    }


def get_job(event, context):
    try:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get(
            'AWS_SECRET_ACCESS_KEY'), region_name=os.environ.get('AWS_REGION'), endpoint_url=os.environ.get('DB_URL'))

        table = dynamodb.Table('Jobs')
        response = table.scan()
    except Exception:
        logging.exception(Exception)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps('Internal Server Error')
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response['Items'])
    }


def get_job_by_id(event, context):
    try:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get(
            'AWS_SECRET_ACCESS_KEY'), region_name=os.environ.get('AWS_REGION'), endpoint_url=os.environ.get('DB_URL'))

        id = event['pathParameters']['id']

        table = dynamodb.Table('Jobs')
        response = table.get_item(Key={'id': id})
    except Exception:
        logging.exception(Exception)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps('Internal Server Error')
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response['Item'])
    }
