import boto3
from os import environ


AWS_ACCESS_KEY = environ.get('ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = environ.get('SECRET_ACCESS_KEY')
AWS_REGION = environ.get('REGION')
DB_URL = environ.get('DB_URL')
XML_BUCKET_NAME = environ.get('XML_BUCKET_NAME')


dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_REGION,
                          endpoint_url=DB_URL)

event_client = boto3.client('events',
                            aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=AWS_REGION)

s3_client = boto3.client('s3',
                         aws_access_key_id=AWS_ACCESS_KEY,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         region_name=AWS_REGION)
