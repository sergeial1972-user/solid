from tool_system import ToolHandler, Tool
from session_context import SessionContext


user_prompt = "Какая погода ?"

async def agent_loop(start_prompt: str):

    session_context = SessionContext()
    tool_handler = ToolHandler()

    await tool_handler.add_tool(Tool(name="Weather", description="Returns current weather"))



    system_prompt = "you are helpful assistant"

    init_prompt = [
        session_context.add_ctx_block(role="system", content=system_prompt),
        session_context.add_ctx_block(role="system", content=await tool_handler.get_tools_prompt()),
        session_context.add_ctx_block(role="user", content=user_prompt),
    ]

    max_steps = 10
    agent_steps
