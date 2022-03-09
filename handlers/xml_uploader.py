import json
from os import environ
import requests
import urllib.parse
from helpers.aws import AWS_REGION

COLUMBIA_API_URL = environ.get('COLUMBIA_API_URL')
COLUMBIA_API_ACCESS_TOKEN = environ.get('COLUMBIA_API_ACCESS_TOKEN')


def xml_uploader(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        data = {
            "mode": "formdata",
            "formdata": [
                {
                    "key": "documentId",
                    "value": f'{bucket}-{key}',
                    "type": "text"
                },
                {
                    "key": "xml",
                    "type": "file",
                    "src": f'https://s3.{AWS_REGION}.amazonaws.com/{bucket}/{key}'
                }
            ]

        }
        headers = json.dumps({
            "auth": {
                "type": "bearer",
                "bearer": [
                    {
                        "key": "token",
                        "value": COLUMBIA_API_ACCESS_TOKEN,
                        "type": "string"
                    }
                ]
            },
        })
        requests.post(COLUMBIA_API_URL, data=data, headers=headers)
    except Exception as e:
        print(e)
        raise e
