import asyncio

from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

async def main():
    async with streamablehttp_client("http://localhost:3000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(llm, tools)
            result = await agent.ainvoke({"messages": [HumanMessage(content="What is palestine")],})
            print(result["messages"][-1].content)
            # print(await session.list_tools())
            # print(await session.call_tool('wikipediaSearch', {'query': 'What is IPL ?'}))



if __name__ == "__main__":
    asyncio.run(main())
