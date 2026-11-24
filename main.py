#imports
import asyncio
import tomllib
from llm import LLM
from session_context import SessionContext

#load_config
with open("config.toml", "rb") as f:
    data = tomllib.load(f)

llm = LLM(base_url=data["base_url"], model=data["model"])

session_ctx = SessionContext()


async def main():

    await session_ctx.add_ctx_block(role="system", content="You are helpful assistant")

    while True:
        user_prompt =  input("Enter your command:")
        model_response = ""

        await session_ctx.add_ctx_block(content=user_prompt, role="user")

        stream = await llm.streaming_response(await session_ctx.get_session_ctx())

        async for chunk in stream:
            if chunk.choices:
                model_response += chunk.choices[0].delta.content or ""



                print(chunk.choices[0].delta.content or "", end="", flush=True)

            if chunk.usage:
                print("\n", chunk.usage)

        await session_ctx.add_ctx_block(role="assistant", content=model_response)

        print(await session_ctx.get_session_ctx())





if __name__ == "__main__":
    asyncio.run(main())
