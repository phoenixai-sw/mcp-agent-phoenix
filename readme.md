# 파이썬으로 MCP Agent 만들기

YouTube 검색, 요약, 채널 분석 기능을 갖춘 유튜브 에이전트를 MCP로 구현한 예제입니다.


## MCP (Model Context Protocol) 소개
- AI가 외부 데이터의 도구(Tools)에 효과적으로 연결할 수 있는 표준화된 방식
- 특히 다양한 도구의 표준화된 연결로 많이 활용되고 있음
    - **MCP Server**: 사용할 수 있는 도구(tool)를 정의하고 제공하는 역할  
    - **MCP Client**: 정의된 도구를 불러와 사용 (Claude Desktop, Cursor, OpenAI Agents SDK)
- 이번 예제에서는 유튜브 컨텐츠 분석을 위한 MCP Server를 만들어보고, OpenAI Agents SDK 기반의 MCP Client와도 연결해볼 예정입니다.

![image](https://github.com/user-attachments/assets/02f2e463-a22b-4fdc-83b5-b97563b8d8fd)



## 초기 셋팅

1. 레포지토리 clone 또는 다운로드하기
    ```bash
    git clone https://github.com/dabidstudio/python-mcp-agent.git
    cd python-mcp-agent
    ```
2. [OpenAI 키 발급](https://github.com/dabidstudio/dabidstudio_guides/blob/main/get-openai-api-key.md)
3. [YouTube Data API Key 발급](https://github.com/dabidstudio/dabidstudio_guides/blob/main/get-youtube-data-api.md)
4. .env.example를 복사한 후 API 키를 입력하고 .env로 저장

    ```bash
    OPENAI_API_KEY=api키_입력
    YOUTUBE_API_KEY=api_키_입력
    ```

5. [파이썬 가상환경 설정](https://github.com/dabidstudio/dabidstudio_guides/blob/main/python-set-venv.md)
    ```bash
    python -m venv venv
    venv\Scripts\activate # Mac은 source venv/bin/activate  
     ```
6. 패키지 설치


    ```bash
    pip install mcp openai-agents streamlit youtube-transcript-api python-dotenv
    ```


## MCP 클라이언트 연동을 위한 준비

Claude, Cursor와 같은 MCP 클라이언트 애플리케이션에서 로컬 MCP 서버를 연동하려면,  
서버 실행에 필요한 **Python 실행 파일 경로**와 **MCP 서버 스크립트 경로**를 JSON 설정에 입력해야 합니다.
- 내 경로에 알맞게 mcp.json을 수정해둡니다.

### 경로 구성 예시

#### ✅ Windows 예시  
(예: 프로젝트 폴더가 `C:\projects\dabidstudio_videos\python_mcp_agent`인 경우)

> **주의:** Windows에서는 JSON 문법상 `\` 대신 `\\` (역슬래시 두 번)을 사용해야 합니다.

```json
{
  "mcpServers": {
    "mcp-test": {
      "command": "C:\\projects\\dabidstudio_videos\\python_mcp_agent\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\projects\\dabidstudio_videos\\python_mcp_agent\\2_mcp_server.py"
      ]
    }
  }
}
```

---

#### ✅ macOS / Linux 예시  
(예: 프로젝트 폴더가 `/Users/yourname/projects/python_mcp_agent`인 경우)

```json
{
  "mcpServers": {
    "mcp-test": {
      "command": "/Users/yourname/projects/python_mcp_agent/venv/bin/python",
      "args": [
        "/Users/yourname/projects/python_mcp_agent/2_mcp_server.py"
      ]
    }
  }
}
```

---



## 폴더 구조

```
python-mcp-agent/
├── 1_mcp_server_functions.ipynb   # MCP 서버 함수 예제 노트북
├── 2_mcp_server.py                # MCP 서버 구현 예제
├── 3_openai_agents_basics.py      # OpenAI Agent 기본 예제
├── 4_mcp_client.py                # Streamlit MCP Client 예제
├── .env.example                   # 환경변수 예제 파일
└── mcp.json                       # MCP 서버 설정 파일
```
