from .dynamo.dynamoUtils import DynamoUtils


def lambda_handler(event, context):
    ddb = DynamoUtils()
    table = ddb.table_resource('Music')
    record = {
        'SongTitle': 'Happy Day',
        'AlbumTitle': 'Songs About Life',
        'Artist': 'Acme Band',
    }
    ddb.put_item(table, record)
    value = table.get_item(Key={'SongTitle': 'Happy Day'})

    return value['Item']
