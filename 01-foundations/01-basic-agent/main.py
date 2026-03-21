"""
Phase 1, Experiment 1: Basic Agent
Build your first LangChain agent
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
# STEP 1: Define Tools
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
    """
    Get the current weather for a given city.
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        Current weather description
    """
    # In a real app, this would call a weather API
    weather_data = {
        "San Francisco": "Sunny, 72°F",
        "New York": "Rainy, 68°F",
        "London": "Cloudy, 55°F",
        "Tokyo": "Clear, 75°F"
    }
    
    if city in weather_data:
        return weather_data[city]
    else:
        return f"I don't have weather data for {city}, but it's probably nice!"


# ============================================================================
# STEP 2: Initialize Language Model
# ============================================================================

model = init_chat_model(
    MODEL_NAME,
    model_provider=MODEL_PROVIDER,
    **MODEL_CONFIG
)


# ============================================================================
# STEP 3: Create the Agent
# ============================================================================

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="""You are a helpful weather assistant. 
    You have access to a weather tool to get current conditions.
    Always be friendly and provide accurate information.
    If you don't have data for a city, tell the user honestly."""
)

print("✓ Agent created")


# ============================================================================
# STEP 4: Run the Agent
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("LangChain Basic Agent Demo")
    print("="*60 + "\n")
    
    # Test queries
    queries = [
        "What's the weather in San Francisco?",
        "Is it raining in London?",
        "Compare weather in Tokyo vs New York",
    ]
    
    for query in queries:
        print(f"User: {query}")
        print("-" * 60)
        
        # Invoke the agent
        response = agent.invoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        
        # Print only the final assistant text, not the full response payload
        final_messages = response.get("messages", [])
        final_text = ""
        if final_messages:
            final_text = _to_text(final_messages[-1].content)

        print(f"Agent: {final_text}")
        print()
