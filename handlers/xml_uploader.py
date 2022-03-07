from os import environ
import requests
import urllib.parse
from helpers.aws import AWS_REGION, s3_client
import json

COLUMBIA_API_URL = environ.get('COLUMBIA_API_URL')


def xml_uploader(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        data = json.dumps({
            "mode": "formdata",
            "formdata": [
                {
                    "key": "documentId",
                    "value": "{{documentId}}",
                    "type": "text"
                },
                {
                    "key": "customerId",
                    "value": "MorganStanley",
                    "type": "text"
                },
                {
                    "key": "xml",
                    "type": "file",
                    "src": f'https://s3.{AWS_REGION}.amazonaws.com/{bucket}/{key}'
                }
            ]

        })
        requests.post(COLUMBIA_API_URL, data)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
