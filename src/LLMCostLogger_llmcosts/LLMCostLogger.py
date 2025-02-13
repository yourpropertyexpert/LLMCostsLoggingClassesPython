# This is a temporary file
# Once the class is working, it will be published on PyPi for installation by PIP
# It's just here until it's working enough to do that


import requests
import json

class LLMCostLogger:
    """
    LLMCostLogger class
    @copyright Mark Harrison 2025
    @package llmcosts/llm-cost-logger
    """

    URI = "https://llmcosts.fyi/api/logcall"

    def __init__(self, key: str = ""):
        if key == "":
            raise Exception("No Key Provided")
        self.key = key
        self.client = requests.Session()

    def log_call(self, provider: str, body: dict):
        if provider == "OpenAI":
            # We only want to send the usage, not the confidential information
            cutbody = {
                "usage": {
                    "total_tokens": body.usage.total_tokens,
                    "prompt_tokens": body.usage.prompt_tokens,
                    "completion_tokens": body.usage.completion_tokens
                }
            }
            body = cutbody

        # Make an HTTP call using requests
        try:
            response = self.client.post(
                self.URI,
                data={
                    'apikey': self.key,
                    'provider': provider,
                    'body': json.dumps(body),
                }
            )
            response.raise_for_status()  # Raises an HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to log call: {str(e)}")
