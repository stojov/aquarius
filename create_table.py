from helpers.db import dynamodb


def create_jobs_table():
    try:
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
    except Exception as e:
        print(e)


def create_parse_record_table():
    try:
        table = dynamodb.create_table(
            TableName='ParseRecords',
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
    except Exception as e:
        print(e)


if __name__ == '__main__':
    job_table = create_jobs_table()
    parse_record_table = create_parse_record_table()
    print("Table status:", job_table.table_status)
    print("Table status:", parse_record_table.table_status)

