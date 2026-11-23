#imports
import tomllib
from openai import AsyncOpenAI
import asyncio


with open("config.toml", "rb") as f:
    data = tomllib.load(f)

class LLM:
    def __init__(self, base_url, model):
        base_url = data["base_url"]
        self.model = data["model"]
        self.base_url = base_url
        self.api_key = data["api_key"]
        self.openai_client = AsyncOpenAI(base_url=self.base_url, api_key=self.api_key)

    async def response(self, messages: list):
        response = await self.openai_client.chat.completions.create(model=self.model, messages=messages)
        return response

llm = LLM(data["base_url"], data["model"])