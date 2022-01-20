import boto3
import os


def create_jobs_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get(
            'AWS_SECRET_ACCESS_KEY'), region_name=os.environ.get('AWS_REGION'), endpoint_url=os.environ.get('DB_URL'))

    table = dynamodb.create_table(
        TableName='Jobs',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == '__main__':
    job_table = create_jobs_table()
    print("Table status:", job_table.table_status)
