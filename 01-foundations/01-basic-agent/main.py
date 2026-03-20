"""
Phase 1, Experiment 1: Basic Agent
Build your first LangChain agent
"""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

# Load environment variables
load_dotenv()

# ============================================================================
# STEP 1: Define Tools
# ============================================================================

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
    "claude-sonnet-4-6",  # Using Anthropic's Claude
    temperature=0.7,      # Slightly creative responses
    max_tokens=500        # Limit response length
)

print("✓ Model initialized:", model)


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
        
        # Print the response
        print(f"Agent: {response['output']}")
        print()
