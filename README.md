# Serverless ChatBot for keeping and rating jokes

## Overview
This implementation is a Telegram callback that processes webhook calls from Telegram and persists 
new jokes.

The following commands are processed:

* Adding the bot to the room Join Room
  * Bot saves messages in the room in format:
    `(room_id, author_id, message_id, text)` for all messages received more than 2 reactions
  * if all voted for the phrase, then the query to LLM is sent

Note: Dialogue with Bot must be initiated before receving queries

The main task is to accumulate data:
`(text, rating, user_id)` for the joke

Model is retrained multiple times based on this data and suggests how each user would like the text

## Data Model

### Messages

Jokes container:

(message_id, author_id, text)

## Local Usage

### Prerequisites

In order to package your dependencies locally with `serverless-python-requirements`, you need to have `Python3.9` installed locally. You can create and activate a dedicated virtual environment with the following command:

```bash
python3.9 -m venv ./venv
source ./venv/bin/activate
```

Alternatively, you can also use `dockerizePip` configuration from `serverless-python-requirements`. For details on that, please refer to corresponding [GitHub repository](https://github.com/UnitedIncome/serverless-python-requirements).

### Deployment

This example is made to work with the Serverless Framework dashboard, which includes advanced features such as CI/CD, monitoring, metrics, etc.

In order to deploy with dashboard, you need to first login with:

```
serverless login
```

install dependencies with:

```
npm install
```

and then perform deployment with:

```
serverless deploy
```

After running deploy, you should see output similar to:

```bash
Deploying aws-python-flask-dynamodb-api-project to stage dev (us-east-1)

✔ Service deployed to stack aws-python-flask-dynamodb-api-project-dev (182s)

endpoint: ANY - https://xxxxxxxx.execute-api.us-east-1.amazonaws.com
functions:
  api: aws-python-flask-dynamodb-api-project-dev-api (1.5 MB)
```

_Note_: In current form, after deployment, your API is public and can be invoked by anyone. For production deployments, you might want to configure an authorizer. For details on how to do that, refer to [httpApi event docs](https://www.serverless.com/framework/docs/providers/aws/events/http-api/).

### Invocation

After successful deployment, you can create a new user by calling the corresponding endpoint:

```bash
curl --request POST 'https://xxxxxx.execute-api.us-east-1.amazonaws.com/users' --header 'Content-Type: application/json' --data-raw '{"name": "John", "userId": "someUserId"}'
```

Which should result in the following response:

```bash
{"userId":"someUserId","name":"John"}
```

You can later retrieve the user by `userId` by calling the following endpoint:

```bash
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/users/someUserId
```

Which should result in the following response:

```bash
{"userId":"someUserId","name":"John"}
```

If you try to retrieve user that does not exist, you should receive the following response:

```bash
{"error":"Could not find user with provided \"userId\""}
```

### Local development

Thanks to capabilities of `serverless-wsgi`, it is also possible to run your application locally, however, in order to do that, you will need to first install `werkzeug`, `boto3` dependencies, as well as all other dependencies listed in `requirements.txt`. It is recommended to use a dedicated virtual environment for that purpose. You can install all needed dependencies with the following commands:

```bash
pip install werkzeug boto3
pip install -r requirements.txt
```

Additionally, you will need to emulate DynamoDB locally, which can be done by using `serverless-dynamodb-local` plugin. In order to do that, execute the following commands:

```bash
serverless plugin install -n serverless-dynamodb-local
serverless dynamodb install
```

It will add the plugin to `devDependencies` in `package.json` file as well as to `plugins` section in `serverless.yml`. Additionally, it will also install DynamoDB locally.

You should also add the following config to `custom` section in `serverless.yml`:


```yml
custom:
  (...)
  dynamodb:
    start:
      migrate: true
    stages:
      - dev
```

Additionally, we need to reconfigure DynamoDB Client to connect to our local instance of DynamoDB. We can take advantage of `IS_OFFLINE` environment variable set by `serverless-wsgi` plugin and replace:


```python
dynamodb_client = boto3.client('dynamodb')
```

with

```python
dynamodb_client = boto3.client('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client('dynamodb', region_name='localhost', endpoint_url='http://localhost:8000')
```

Now you can start DynamoDB local with the following command:

```bash
serverless dynamodb start
```

At this point, you can run your application locally with the following command:

```bash
serverless wsgi serve
```

For additional local development capabilities of `serverless-wsgi` and `serverless-dynamodb-local` plugins, please refer to corresponding GitHub repositories:
- https://github.com/logandk/serverless-wsgi 
- https://github.com/99x/serverless-dynamodb-local
