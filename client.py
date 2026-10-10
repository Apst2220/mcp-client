import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters import client
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import ToolMessage   

load_dotenv()

SERVERS = {
    "expense": {
        "transport": "streamable_http",
        "url": "https://expensetrackerrr.fastmcp.app/mcp"
    }
}


async def main():
    client = MultiServerMCPClient(SERVERS)
    tools=await client.get_tools()

    namedTools={}
    for tool in tools:
        namedTools[tool.name]=tool

    llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=1.8)
    llm_with_tools=llm.bind_tools(tools)

    prompt="Add an expense of rupees 300 for cab ride to office"
    response=await llm_with_tools.ainvoke(prompt)

    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return

    tool_messages=[]
    for tc in response.tool_calls:
        selected_tool=tc["name"]
        selected_tool_args=tc["args"] or {}
        selected_tool_id=tc["id"]

        result=await namedTools[selected_tool].ainvoke(selected_tool_args, tool_call_id=selected_tool_id)
        tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, tool_name=selected_tool, content=result))

    final_response=await llm_with_tools.ainvoke(prompt, response, tool_messages=tool_messages)
    print("\nFinal response:", final_response.content)

    
if __name__ == "__main__":
    asyncio.run(main())

