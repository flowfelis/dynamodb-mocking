import boto3


class DynamoUtils:

    def table_resource(self, table_name):
        """
        Returns the table_resource
        Args:
            table_name (str): table_name to the table_resource
        Returns:
            object: table_resource
        """
        try:
            dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
            return dynamodb.Table(table_name)
        except Exception as Argument:
            print(Argument)
            # logger.info(Argument)
            # logger.info("Error while creating Table Resource object")
            # logger.info(Argument)

    def put_item(self, table, rec):
        return table.put_item(Item=rec)

    def get_item(self, table, key):
        return table.get_item(Key=key)

    def update_item(self, table, tablekey, record):
        """
        This function accepts table resource, key, and attributes need to be updated
        Returns the table_resource
        Args:
            table (str): table_name to the update_item
            tablekey (str): tablekey to the update_item
            record (dict): record to the update_item
        Returns:
        res: dict object
        """
        update_expression = ["set "]
        update_values = dict()
        update_name = dict()

        for key, val in record.items():
            update_expression.append(f"#{key} = :{key},")
            update_values[f":{key}"] = val
            update_name[f"#{key}"] = key
        resp = table.update_item(
            Key=tablekey,
            UpdateExpression="".join(update_expression)[:-1],
            ExpressionAttributeValues=dict(update_values),
            ExpressionAttributeNames=dict(update_name)
        )
        return resp
