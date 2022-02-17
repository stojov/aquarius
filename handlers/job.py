import json
import logging
import uuid
from helpers.db import dynamodb, event_client


def put_job(event, context):
    try:
        data = json.loads(event['body'])
        id = str(uuid.uuid4())
        rssUrl = data['rssUrl']
        schedule = data['schedule']

        table = dynamodb.Table('Jobs')
        response = table.put_item(
            Item={
                'id': id,
                'rssUrl': rssUrl,
                'schedule': schedule,
                'active': True,
            }
        )

        result = event_client.put_rule(Name='DEMO_EVENT',
                                     ScheduleExpression=f'cron({schedule})',
                                     State='ENABLED')
    except Exception:
        logging.exception(Exception)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps('Internal Server Error')
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(response)
    }


def update_job(event, context):
    try:
        id = event['pathParameters']['id']
        if 'body' in event:
            data = json.loads(event['body'])
        else:
            data = event
        rssUrl = data['rssUrl']
        schedule = data['schedule']

        table = dynamodb.Table('Jobs')
        response = table.update_item(
            Key={'id': id},
            UpdateExpression="SET rssUrl=:rssUrl, schedule=:schedule",
            ConditionExpression="attribute_exists(id)",
            ExpressionAttributeValues={
                ':rssUrl': rssUrl,
                ':schedule': schedule,
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception:
        logging.exception(Exception)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps('Internal Server Error')
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(response["Attributes"])
    }


def update_job_status(event, context):
    try:
        id = event['pathParameters']['id']
        data = json.loads(event['body'])
        status = data['status']

        table = dynamodb.Table('Jobs')
        response = table.update_item(
            Key={'id': id},
            UpdateExpression="SET active=:status",
            ConditionExpression="attribute_exists(id)",
            ExpressionAttributeValues={
                ':status': status
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception:
        logging.exception(Exception)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps('Internal Server Error')
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(response["Attributes"])
    }


def get_job(event, context):
    try:
        table = dynamodb.Table('Jobs')
        response = table.scan()
    except Exception:
        logging.exception(Exception)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps('Internal Server Error')
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*',
            "Content-Type": "application/json",
        },
        "body": json.dumps(response['Items'])
    }


def get_job_by_id(event, context):
    try:
        id = event['pathParameters']['id']

        table = dynamodb.Table('Jobs')
        response = table.get_item(Key={'id': id})
    except Exception:
        logging.exception(Exception)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps('Internal Server Error')
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(response['Item'])
    }


def delete_job(event, context):
    try:
        id = event['pathParameters']['id']

        table = dynamodb.Table('Jobs')
        response = table.delete_item(
            Key={'id': id}
        )
    except Exception:
        logging.exception(Exception)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps('Internal Server Error')
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(response)
    }
