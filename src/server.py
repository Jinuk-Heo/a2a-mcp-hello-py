"""A2A Server for Hello MCP Agent."""
import os
import uvicorn
import requests # 이 줄 때문에 위 1단계가 필수입니다.

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent_executor import HelloMCPAgentExecutor

# ★ 중요: 날씨 전문가는 '옛날 집(666155)'에 있습니다. 여기로 연결합니다.
MCP_SERVER_URL = os.environ.get(
    "MCP_SERVER_URL",
    "https://mcp-hello-py-hjk-666155174404.asia-northeast3.run.app"
)

# 내 주소(통역사)는 자동으로 가져옵니다.
SERVICE_URL = os.environ.get("SERVICE_URL", "")

def create_agent_card(host: str, port: int) -> AgentCard:
    skill = AgentSkill(
        id="korean_greeting",
        name="Korean Greeting",
        description="인사와 날씨 정보를 제공합니다.",
        tags=["greeting", "weather"],
        examples=["안녕", "강남구 날씨 어때?"],
    )

    if SERVICE_URL:
        agent_url = SERVICE_URL
    else:
        agent_url = f"http://{host}:{port}/"

    return AgentCard(
        name="Hello MCP Agent",
        description="MCP 서버와 연결된 A2A 에이전트입니다.",
        url=agent_url,
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

def main():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))

    agent_card = create_agent_card(host, port)
    
    # 여기서 MCP 서버(666155)와 연결을 맺습니다.
    request_handler = DefaultRequestHandler(
        agent_executor=HelloMCPAgentExecutor(MCP_SERVER_URL),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    print(f"Agent(Me): {SERVICE_URL}")
    print(f"MCP(Target): {MCP_SERVER_URL}")

    uvicorn.run(server.build(), host=host, port=port)

if __name__ == "__main__":
    main()
