import re
import shlex
import ast
import asyncio
import tools
import inspect

class Tool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


tool_re = r"(?<=\[TOOL\]).*?(?=\[ENDTOOL\])"


def parse_arg(val: str):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return val


class ToolHandler:
    def __init__(self):
        self.tools = []

    async def add_tool(self, tool: Tool):
        self.tools.append(tool)

    async def handle_call(self, text: str):
        result = re.findall(tool_re, text, flags=re.DOTALL)

        tool_responses = ""

        for tool in result:
            parts = shlex.split(tool.strip())

            if not parts:
                continue

            tool_name = parts[0]
            tool_args = [parse_arg(arg.rstrip(",")) for arg in parts[1:]]

            func = getattr(tools, tool_name)


            if inspect.iscoroutinefunction(func):

                tool_responses += tool_name

                tool_responses += ": "



                call_result = await func(*tool_args)
                tool_responses += str(call_result)
                tool_responses += " "
            else:
                tool_responses += tool_name
                tool_responses += ": "


                call_result = func(*tool_args)
                tool_responses += str(call_result)
                tool_responses += " "

            if len(tool_args) < 1:
                tool_args = None

        return tool_responses



    async def get_tools_prompt(self):
        prompt = " You have  tools to call tool use[TOOL]tool[ENDTOOL] if you need to add variables to tool use [TOOL]tool_name tool_var1 tool_var2 etc [ENDTOOL]"
        prompt += "Available tools:"
        for tool in self.tools:
            prompt += f" name:{tool.name}, desc:{tool.description}"
        return prompt






async def test():
    tool_handler = ToolHandler()
    await tool_handler.add_tool(Tool(name="Sum", description="Sum"))

    print(await tool_handler.handle_call("[TOOL]Weather[ENDTOOL], [TOOL]Sum 2 5[ENDTOOL]"))

if __name__ == "__main__":
    asyncio.run(test())
