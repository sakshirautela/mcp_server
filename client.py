import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

async def main():
    cl = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio"
            }
        }
    )

    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
    else:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in your .env file or environment.")

    all_server_tools = await cl.get_tools()
    flat_tools = []
    for server_tools_list in all_server_tools:
        if isinstance(server_tools_list, list):
            flat_tools.extend(server_tools_list)
        else:
            flat_tools.append(server_tools_list)

    model = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", api_key=os.getenv("GROQ_API_KEY"))

    prompt = PromptTemplate.from_template(
        "You are a helpful assistant that can answer Math questions and help with tasks. {input}"
    )

    agent = create_react_agent(
        model,
        tools=flat_tools,
    )

    print("Asking: What is the area of a circle with radius 5?")
    math_response = await agent.ainvoke({"input": "What is the area of a circle with radius 5?"})
    print("Agent's Response 1:")
    print(math_response)

    print("\nAsking: What is the area of a circle with rectangle length 5 and width 10?")
    result = await agent.ainvoke({"input": "What is the area of a circle with rectangle length 5 and width 10?"})
    print("Agent's Response 2:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
