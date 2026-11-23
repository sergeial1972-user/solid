class SessionContext:

    def __init__(self, session_ctx):
        self.session_ctx = []

    async def get_session_ctx(self):
        return self.session_ctx

    async def add_ctx_block(self, role: str, content: str):
        block = {"role": role, "content": content}
        self.session_ctx.append(block)