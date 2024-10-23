from typing import List, Union, Generator, Iterator, Optional
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

```citations
{"/Users/oliverkoehn/repos/private/chAIda/in/files/txt/attentionIsAllYouNeed.pdf": ["quote1", "quote2"], "/Users/oliverkoehn/repos/private/chAIda/in/files/txt/companyExpansionPolicy.txt": ["quote3", "quote4"]}
```

```citations
{
    "/Users/oliverkoehn/repos/private/chAIda/in/files/txt/aiRegAct.txt": [
        "Most of the text addresses high-risk AI systems, which are regulated.",
        "High risk AI systems are those: used as a safety component or a product covered by EU laws in Annex I AND required to undergo a third-party conformity assessment under those Annex I laws; OR those under Annex III use cases (below)",
        "AI systems used in researching and interpreting facts and applying the law to concrete facts or used in alternative dispute resolution."
    ]
}
```

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

