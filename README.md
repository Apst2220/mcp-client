# MCP Expense Tracker Client

An AI-powered expense management client built with **Python, LangChain, and Google Gemini 2.5 Flash**. It connects to a remotely deployed MCP server over Streamable HTTP, dynamically discovers available tools, and uses LLM-based tool calling to execute expense-related actions.

### Tech Stack
- Python and asyncio
- LangChain and Google Gemini
- Model Context Protocol (MCP)
- `langchain-mcp-adapters`
- `python-dotenv`

### Setup
1. Install dependencies: `uv sync`
2. Add your `GOOGLE_API_KEY` to a `.env` file.
3. Run the client: `uv run client.py`

**Note:** The deployed MCP server must be accessible, and any required authentication must be configured.