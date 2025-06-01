import asyncio

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

async def main():
    client = MultiServerMCPClient(
        {
            "weather": {
                "command": "node",
                "args": [
                    "/Users/sudiptakundu/repos/mcp/mcpServers/quickstart-resources/weather-server-typescript/build/index.js"
                ],
                "transport": "stdio"
            },
            "wikipediaSearch": {
                "url": "http://localhost:3000/mcp",
                "transport": "streamable_http"
            }
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    messages = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
        messages.append(HumanMessage(content=user_input))
        result = await agent.ainvoke({"messages": messages})
        messages = result["messages"]
        print("Agent:", result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())