import os

import boto3

dynamodb_client = boto3.resource('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.resource(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )

MESSAGES_TABLE = os.environ['MESSAGES_TABLE']

from .messages import MessagesDAO

messagesDAO = MessagesDAO(dynamodb_client, MESSAGES_TABLE)
