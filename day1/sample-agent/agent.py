import os
import asyncio
from dotenv import load_dotenv # <-- NEW IMPORT

# Load environment variables from the .env file in the current directory
load_dotenv() # <-- NEW LINE!

try:

    # Check if the key was loaded from the .env file
    if os.getenv("GOOGLE_API_KEY"):
        # The key is now available in os.environ
        print("✅ Gemini API key loaded from .env file.")
    else:
        # If the .env file didn't contain it, this message will help
        print("⚠️ GOOGLE_API_KEY not found in .env or environment.")

except Exception as e:
    print(f"🔑 Setup Error: Details: {e}")

# ... (rest of your imports, agent, and runner definition remain the same) ...



from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

print("✅ ADK components imported successfully.")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)

print("✅ Root Agent defined.")

runner = InMemoryRunner(agent=root_agent)

print("✅ Runner created.")

async def main():
    prompt = input("$: ")
    response = await runner.run_debug(prompt)



    return response


if __name__ == "__main__":
    asyncio.run(main())
