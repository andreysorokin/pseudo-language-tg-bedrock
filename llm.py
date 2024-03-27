import json

import boto3
from botocore.exceptions import ClientError
from logger import logger


class LLMJoker:
    def __init__(self):
        self._END_TOKEN = '<END>'
        self._START_TOKEN = '<START>'
        self._bedrock_runtime_client = boto3.client(
            service_name="bedrock-runtime", region_name="us-east-1"
        )

    def get_joke(self, russian_text):
        result = self._invoke_mistral_7b(
            "Use tokens <START> and <END> in the output to mark the actual response in pseudo language,"
            " use the funniest way to translate this into pseudo-language that uses Kazakh alphabet from Russian: \"{}\"".format(
                russian_text))
        result = "".join(result)
        if (self._START_TOKEN in result and self._END_TOKEN in result):
            start_pos = result.find(self._START_TOKEN)
            end_pos = result.find(self._END_TOKEN)
            if start_pos != -1 and end_pos != -1 and start_pos < end_pos:
                return result[start_pos + len(self._START_TOKEN):end_pos]
        return None

    def _invoke_mistral_7b(self, prompt):
        """
        Invokes the Mistral 7B model to run an inference using the input
        provided in the request body.

        :param prompt: The prompt that you want Mistral to complete.
        :return: List of inference responses from the model.
        """

        try:
            # Mistral instruct models provide optimal results when
            # embedding the prompt into the following template:
            instruction = f"<s>[INST] {prompt} [/INST]"

            model_id = "mistral.mistral-7b-instruct-v0:2"

            body = {
                "prompt": instruction,
                "max_tokens": 200,
                "temperature": 0.5,
            }

            response = self._bedrock_runtime_client.invoke_model(
                modelId=model_id, body=json.dumps(body)
            )

            response_body = json.loads(response["body"].read())
            outputs = response_body.get("outputs")

            completions = [output["text"] for output in outputs]

            return completions

        except ClientError:
            logger.error("Couldn't invoke Mistral 7B")
            raise


joker = LLMJoker()