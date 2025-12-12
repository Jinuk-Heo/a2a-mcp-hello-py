"""A2A Agent that uses MCP Hello Server."""

from mcp_client import MCPHelloClient  # type: ignore


class HelloMCPAgent:
    """Agent that greets users using MCP Hello Server."""

    def __init__(self, mcp_url: str):
        self.mcp_client = MCPHelloClient(mcp_url)

    async def invoke(self, user_message: str) -> str:
        """Process user message and return greeting."""
        return await self.mcp_client.say_hello(user_message.strip())
