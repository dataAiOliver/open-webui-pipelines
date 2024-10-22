from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

class Pipeline:
    def __init__(self):
        self.name = "Mock Response"
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

        return """## Sources

```citation
[
		{
			"source": "source1",
			"url": "www.google.com",
			"url_type": "weblink",
			"quotes": ["quote11", "quote12", "quote13"]
		},
		{
			"source": "source2",
			"url": "oliver/dummy/file.txt",
			"url_type": "local_file",
			"quotes": ["quote21", "quote22", "quote23"]
		}
]
````
dummy
123
```python
print("hello world")
```
dsadsa

- adssa
- dsad

# hallo
"""

