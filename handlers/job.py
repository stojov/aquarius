import json
import logging
from os import environ
import uuid
from helpers.db import dynamodb, event_client
from helpers.validation import isValidURL

JOB_LAMBDA_ARN = environ.get('JOB_LAMBDA_ARN')


def put_job(event, context):
    try:
        data = json.loads(event['body'])
        id = str(uuid.uuid4())
        name = data['name']
        rssUrl = data['rssUrl']
        schedule = data['schedule']

        if not rssUrl.startswith('http'):
            rssUrl = 'http://'+rssUrl

        if not isValidURL(rssUrl):
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "applicationjson",
                },
                "body": json.dumps('Invalid url')
            }

        table = dynamodb.Table('Jobs')
        response = table.put_item(
            Item={
                'id': id,
                'name': name,
                'rssUrl': rssUrl,
                'schedule': schedule,
                'active': True,
            }
        )

        event_client.put_rule(Name=name,
                              ScheduleExpression=f'cron({schedule})',
                              State='ENABLED')

        event_client.put_targets(Rule=name,
                                 Targets=[
                                     {
                                         'Arn': JOB_LAMBDA_ARN,
                                         'Id': str(uuid.uuid4()),
                                         "Input": json.dumps({"id": id})
                                     }
                                 ])
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
        name = data['name'],
        rssUrl = data['rssUrl']
        schedule = data['schedule']

        table = dynamodb.Table('Jobs')
        response = table.update_item(
            Key={'id': id},
            UpdateExpression="SET name=:name, rssUrl=:rssUrl, schedule=:schedule",
            ConditionExpression="attribute_exists(id)",
            ExpressionAttributeValues={
                'name': name,
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
