"""
Phase 1, Experiment 1: Advanced Example
Add streaming and better output formatting
"""

import os
import sys

# Add workspace root to path so we can import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

# Import centralized configuration
from config import MODEL_CONFIG, MODEL_NAME, MODEL_PROVIDER

# ============================================================================
# STEP 1: Helper Functions
# ============================================================================

def _to_text(content: object) -> str:
    """Normalize model content to plain text for console output."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
            else:
                parts.append(str(item))
        return " ".join(part for part in parts if part).strip()

    return str(content)


@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    weather_data = {
        "San Francisco": "Sunny, 72°F, light wind",
        "New York": "Rainy, 68°F, heavy clouds",
        "London": "Cloudy, 55°F, cool",
        "Tokyo": "Clear, 75°F, humid",
    }
    return weather_data.get(city, f"No data for {city}")

@tool
def get_forecast(city: str, days: int = 3) -> str:
    """Get weather forecast for upcoming days."""
    forecasts = {
        "San Francisco": "Sunny all week",
        "New York": "Rain clearing up",
        "London": "Typical English weather",
        "Tokyo": "Warm and humid",
    }
    return f"{forecasts.get(city, 'No data')}: {days}-day forecast"


# Multiple tools now!
tools = [get_weather, get_forecast]

model = init_chat_model(
    MODEL_NAME,
    model_provider=MODEL_PROVIDER,
    **MODEL_CONFIG
)

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""You are an expert weather assistant.
    Help users understand current weather and forecasts.
    Use tools to provide accurate information.
    Be conversational and helpful."""
)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Enhanced Weather Agent with Multiple Tools")
    print("="*60 + "\n")
    
    # More complex queries
    queries = [
        "What's the weather in San Francisco and what's the 5-day forecast?",
        "Should I bring an umbrella to New York?",
        "Compare forecasts for London and Tokyo",
    ]
    
    for query in queries:
        print(f"📍 User: {query}")
        print("-" * 60)
        
        response = agent.invoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        
        # Extract the final assistant message from the response
        final_messages = response.get("messages", [])
        if final_messages:
            final_text = _to_text(final_messages[-1].content)
            print(f"🤖 Agent: {final_text}")
        print()
