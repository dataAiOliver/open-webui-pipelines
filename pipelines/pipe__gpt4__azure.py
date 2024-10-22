from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

class Pipeline:
    def __init__(self):
        self.name = "GPT-4o"
        print("miau")
        load_dotenv("/Users/oliverkoehn/repos/private/chAIda/.env")
        print(os.getenv("AZURE_OPENAI_ENDPOINT"))
        print(os.getenv("AZURE_OPENAI_API_KEY"))
        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def pipe(
            self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")

        print(messages)
        print(user_message)

        headers = {
            "api-key": self.azure_openai_api_key,
            "Content-Type": "application/json",
        }

        allowed_params = {'messages', 'temperature', 'role', 'content', 'contentPart', 'contentPartImage',
                          'enhancements', 'dataSources', 'n', 'stream', 'stop', 'max_tokens', 'presence_penalty',
                          'frequency_penalty', 'logit_bias', 'user', 'function_call', 'funcions', 'tools',
                          'tool_choice', 'top_p', 'log_probs', 'top_logprobs', 'response_format', 'seed'}
        # remap user field
        if "user" in body and not isinstance(body["user"], str):
            body["user"] = body["user"]["id"] if "id" in body["user"] else str(body["user"])
        filtered_body = {k: v for k, v in body.items() if k in allowed_params}
        # log fields that were filtered out as a single line
        if len(body) != len(filtered_body):
            print(f"Dropped params: {', '.join(set(body.keys()) - set(filtered_body.keys()))}")

        r = requests.post(
            url=self.azure_openai_endpoint,
            json=filtered_body,
            headers=headers,
            stream=True,
        )

        r.raise_for_status()
        if body["stream"]:
            return r.iter_lines()
        else:
            return r.json()
