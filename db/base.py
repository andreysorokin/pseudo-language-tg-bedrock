import boto3
from abc import ABC, abstractmethod


class BaseDAO(ABC):
    def __init__(self, dynamodb, table_name):
        self.dynamodb = dynamodb
        self.table = self.dynamodb.Table(table_name)

    @abstractmethod
    def to_item(self, record):
        """Converts a Python object to a DynamoDB item."""
        pass

    @abstractmethod
    def from_item(self, item):
        """Converts a DynamoDB item to a Python object."""
        pass

    def put(self, record):
        """Create a new record in the DynamoDB table."""
        item = self.to_item(record)
        self.table.put_item(Item=item)

    def get(self, key):
        """Retrieve a record by its key."""
        response = self.table.get_item(Key=key)
        item = response.get('Item', None)
        if item:
            return self.from_item(item)
        return None

    def update(self, key, update_expression, expression_attribute_names, expression_attribute_values, return_values='UPDATED_NEW'):
        """Update a record's information."""
        return self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues=return_values
        )

    def delete(self, key):
        """Delete a record from the table."""
        self.table.delete_item(Key=key)
