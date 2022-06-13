import subprocess

import boto3
import pytest

from src.app import lambda_handler

TABLE_NAME = "Music"
DYNALITE_PORT = "4567"


@pytest.fixture
def expected_record():
    return {'SongTitle': 'Happy Day', 'AlbumTitle': 'Songs About Life', 'Artist': 'Acme Band'}


@pytest.fixture
def local_dynamodb(request, aws_credentials):
    proc = subprocess.Popen(
        ["dynalite", "--port", DYNALITE_PORT, "--createTableMs", "0"]
    )
    dynamo = boto3.resource(
        "dynamodb",
        endpoint_url=f"http://localhost:{DYNALITE_PORT}",
        region_name='eu-central-1'
    )

    request.addfinalizer(lambda: proc.kill())

    return dynamo


@pytest.fixture
def music_table(local_dynamodb):
    try:
        table = local_dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "SongTitle", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "SongTitle", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield table
    except Exception:
        yield local_dynamodb.Table(TABLE_NAME)


def test_lambda_handler(aws_credentials, music_table, expected_record, mocker):
    mocker.patch(
        'src.app.DynamoUtils.table_resource',
        return_value=music_table,
    )
    result = lambda_handler({}, None)

    assert result == expected_record
