import sys
import asyncio
import streamlit as st
import json
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv()

# Windows 호환성 설정
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# MCP 서버 설정 함수
async def setup_mcp_servers():
    servers = []
    # mcp.json 파일에서 설정 읽기
    with open('mcp.json', 'r') as f:
        config = json.load(f)

    # 구성된 MCP 서버들을 순회
    for server_name, server_config in config.get('mcpServers', {}).items():
        print(f"DEBUG: Attempting to connect to MCP server: {server_name}")
        mcp_server = MCPServerStdio(
            params={
                "command": server_config.get("command"),
                "args": server_config.get("args", [])
            },
            cache_tools_list=True
        )
        await mcp_server.connect()
        print(f"DEBUG: Successfully connected to MCP server: {server_name}")
        servers.append(mcp_server)

    return servers

# 에이전트 설정 함수
async def setup_agent():
    mcp_servers = await setup_mcp_servers()
    agent = Agent(
        name="Assistant",
        instructions="너는 유튜브 컨텐츠 분석을 도와주는 에이전트야",
        model="gpt-4o-mini",
        mcp_servers=mcp_servers
    )
    return agent, mcp_servers

# 사용자 메시지 처리 함수 (비동기 함수 내부에 async for 사용)
async def process_user_message():
    agent, mcp_servers = await setup_agent()
    messages = st.session_state.chat_history

    result = Runner.run_streamed(agent, input=messages)
    response_text = ""
    placeholder = st.empty()

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            response_text += event.data.delta or ""
            with placeholder.container():
                with st.chat_message("assistant"):
                    st.markdown(response_text)
        elif event.type == "run_item_stream_event":
            item = event.item
            if item.type == "tool_call_item":
                tool_name = item.raw_item.name
                st.toast(f"🛠 도구 활용: `{tool_name}`")
    
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response_text
    })

    # MCP 서버 종료 처리
    for server in mcp_servers:
        await server.__aexit__(None, None, None)

# Streamlit UI 메인 함수
def main():
    st.set_page_config(page_title="유튜브 에이전트", page_icon="🎥")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.title("🎥 유튜브 컨텐츠 에이전트")
    st.caption("유튜브 컨텐츠 제작, 아이디어, 트렌드에 대해 물어보세요!")

    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    user_input = st.chat_input("대화를 해주세요")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        # 비동기 응답 처리
        asyncio.run(process_user_message())

if __name__ == "__main__":
    main()
