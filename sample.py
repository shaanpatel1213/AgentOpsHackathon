import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API key if not already in environment
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from agents import Agent, Runner, function_tool
import agentops

agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."


agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)


async def main():
    result = await Runner.run(agent, 
                              input="What's the weather in San Francisco?")
    print(result.final_output)
    # The weather in San Francisco is sunny.


if __name__ == "__main__":
    asyncio.run(main())