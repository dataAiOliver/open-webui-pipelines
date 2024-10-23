from typing import List, Union, Generator, Iterator, Optional
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import sys, os
sys.path.append(os.path.abspath('/Users/oliverkoehn/repos/private/chAIda'))
import importlib
import lib.utils
importlib.reload(lib.utils)
from lib.utils import *

collection = client.get_collection(name=collection_name)


class Pipeline:
    def __init__(self):
        self.name = "Talk to your documents"
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

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        # If title generation is requested, skip the function calling filter
        if body.get("title", False):
            return body
        

        print(f"INLET:{__name__}")

        messages = body["messages"]
        #messages[-1]["content"] = "Wie gehts dir?"

        return body
    

    def pipe(
            self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"PIPE:{__name__}")
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
        
        
        # in first call, two prompts are fired, one original and one for title generation.
        if not(user_message.startswith("Create a concise")):
            print(f"Real (non-title) Prompt: {user_message}")
            messages = body["messages"]
            rag_prompt = get_rag_prompt(collection, user_message)
            print(f"OLD PROMPT: {messages[-1]['content']}")
            messages[-1]["content"] = rag_prompt
            print(f"NEW PROMPT: {messages[-1]['content']}")
            with open("/Users/oliverkoehn/repos/private/chAIda/out/dummy.txt", "w") as f: f.write(rag_prompt)

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
