from dotenv import load_dotenv
from langchain_teddynote import logging

load_dotenv(override=True)
logging.langsmith("LangGraph MCP Adapters")

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from langchain_teddynote.messages import astream_graph

# LLM 모델 초기화
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# 클라이언트 생성
client = MultiServerMCPClient(
    {
        # "server-sequential-thinking": {
        #     "command": "npx",
        #     "args": [
        #         "-y",
        #         "@smithery/cli@latest",
        #         "run",
        #         "@smithery-ai/server-sequential-thinking",
        #         "--key",
        #         "a94d0233-912b-4752-82e4-78949f447de7"
        #     ],
        #     "transport": "stdio",  # stdio 방식으로 통신을 추가합니다.
        # },
        "desktop-commander": {
            "command": "npx",
            "args": [
                "-y",
                "@smithery/cli@latest",
                "run",
                "@wonderwhy-er/desktop-commander",
                "--key",
                "a94d0233-912b-4752-82e4-78949f447de7"
            ],
            "transport": "stdio",  # stdio 방식으로 통신을 추가합니다.
        },
        # "document-retriever": {
        #     "command": "./.venv/bin/python",
        #     # mcp_server_rag.py 파일의 절대 경로로 업데이트해야 합니다
        #     "args": ["./mcp_server_rag.py"],
        #     # stdio 방식으로 통신 (표준 입출력 사용)
        #     "transport": "stdio",
        # },
        "duckduckgo-mcp-server": {
            "command": "npx",
            "args": [
                "-y",
                "@smithery/cli@latest",
                "run",
                "@nickclyde/duckduckgo-mcp-server",
                "--key",
                "a94d0233-912b-4752-82e4-78949f447de7"
            ],
            "transport": "stdio",  # stdio 방식으로 통신을 추가합니다.
        }
    }
)

# 명시적으로 연결 초기화
client.__aenter__()
    
# 설정 및 에이전트 생성
config = RunnableConfig(recursion_limit=30, thread_id=1)
agent = create_react_agent(model, client.get_tools(), checkpointer=MemorySaver())

print("[client]")
print(client)
print("[agent]")
print(agent)
print("클라이언트 및 에이전트 생성 완료")

async def send(query):
    return await astream_graph(
        agent,
        {
            "messages": query
        },
        config=config,
    )