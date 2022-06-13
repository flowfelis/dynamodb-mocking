import os
import subprocess

import boto3
import pytest


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


TABLE_NAME = "PersonTestTable"
DYNALITE_PORT = "4567"


@pytest.fixture
def dynamodb_table(request):
    proc = subprocess.Popen(
        ["dynalite", "--port", DYNALITE_PORT, "--createTableMs", "0"]
    )
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=f"http://localhost:{DYNALITE_PORT}",
        region_name='eu-central-1',
    )

    request.addfinalizer(lambda: proc.kill())

    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield table
    except Exception:
        yield dynamodb.Table(TABLE_NAME)
