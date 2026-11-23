#imports
import asyncio
import tomllib
from llm import LLM

#load_config
with open("config.toml", "rb") as f:
    data = tomllib.load(f)

llm = LLM(base_url=data["base_url"], model=data["model"])

messages = [
    {
        "role": "system",
        "content": "You are helpful assistant"

    },
    {
        "role": "user",
        "content": "Меня зовут Алекс"
    }
]

async def main():
    result = await llm.response(messages)
    print(result.choices[0].message.content)
    messages.append(
        {
            "role": "assistant",
            "content": result.choices[0].message.content
        })

    messages.append(
        {
            "role": "user",
            "content": "Как меня зовут ?"
        })

    result = await llm.response(messages)
    print(result.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(main())

