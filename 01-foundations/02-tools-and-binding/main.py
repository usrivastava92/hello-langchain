"""
Phase 1, Experiment 2: Tools & Binding
Create multiple tools and bind them to models
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
# STEP 1: Define Multiple Tools
# ============================================================================

@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a city.
    
    Args:
        city: Name of the city
        
    Returns:
        Current weather conditions and temperature
    """
    weather_db = {
        "San Francisco": {"condition": "Sunny", "temp": 72},
        "New York": {"condition": "Rainy", "temp": 68},
        "London": {"condition": "Cloudy", "temp": 55},
        "Tokyo": {"condition": "Clear", "temp": 75},
    }
    
    if city in weather_db:
        w = weather_db[city]
        return f"{w['condition']}, {w['temp']}°F"
    return f"No data for {city}"


@tool
def get_humidity(city: str) -> str:
    """
    Get humidity level for a city.
    
    Args:
        city: Name of the city
        
    Returns:
        Humidity percentage
    """
    humidity_db = {
        "San Francisco": 65,
        "New York": 78,
        "London": 72,
        "Tokyo": 85,
    }
    
    humidity = humidity_db.get(city, 50)
    return f"Humidity in {city}: {humidity}%"


@tool
def get_air_quality(city: str) -> str:
    """
    Get air quality index for a city.
    
    The Air Quality Index (AQI) ranges from 0-500:
    - 0-50: Good
    - 51-100: Moderate
    - 101-150: Unhealthy for sensitive groups
    - 151-200: Unhealthy
    - 201-300: Very unhealthy
    - 301+: Hazardous
    
    Args:
        city: Name of the city
        
    Returns:
        AQI value and interpretation
    """
    aqi_db = {
        "San Francisco": 45,
        "New York": 65,
        "London": 55,
        "Tokyo": 72,
    }
    
    aqi = aqi_db.get(city, 50)
    
    if aqi <= 50:
        level = "Good"
    elif aqi <= 100:
        level = "Moderate"
    elif aqi <= 150:
        level = "Unhealthy for sensitive groups"
    else:
        level = "Unhealthy"
    
    return f"AQI in {city}: {aqi} ({level})"


@tool
def get_forecast(city: str, days: int = 3) -> str:
    """
    Get weather forecast for upcoming days.
    
    Args:
        city: Name of the city
        days: Number of days to forecast (default: 3, max: 10)
        
    Returns:
        Weather forecast summary
    """
    days = min(days, 10)  # Cap at 10 days
    
    forecasts = {
        "San Francisco": "Sunny and pleasant all week",
        "New York": "Rain decreasing by midweek",
        "London": "Typical weather - mix of sun and clouds",
        "Tokyo": "Warm and humid throughout",
    }
    
    forecast = forecasts.get(city, "No forecast data")
    return f"{days}-day forecast for {city}: {forecast}"


# ============================================================================
# STEP 2: Bind Tools to Model
# ============================================================================

model = init_chat_model(
    MODEL_NAME,
    model_provider=MODEL_PROVIDER,
    **MODEL_CONFIG
)

# Create list of tools
tools = [get_weather, get_humidity, get_air_quality, get_forecast]

# Bind tools to model (this tells the model what tools are available)
model_with_tools = model.bind_tools(tools)

print(f"✓ Model initialized with {len(tools)} tools")
print(f"  Available tools: {[t.name for t in tools]}")


# ============================================================================
# STEP 3: Create Agent with Tools
# ============================================================================

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""You are a comprehensive weather and environmental quality assistant.
    
    You have access to tools to provide:
    - Current weather conditions
    - Humidity levels
    - Air quality information
    - Weather forecasts
    
    Always use the appropriate tools to give users accurate information.
    When multiple pieces of information would be helpful, use multiple tools.
    Be friendly and informative in your responses."""
)

print("✓ Agent created with multi-tool capability")


# ============================================================================
# STEP 4: Run the Agent
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("LangChain Tools & Binding Demo")
    print("="*60 + "\n")
    
    # Complex queries that require multiple tools
    queries = [
        "Give me a complete weather report for San Francisco",
        "Should I bring rain gear to New York considering the humidity and air quality?",
        "Compare the environmental conditions in Tokyo vs San Francisco",
        "What's the weather and forecast for London?",
    ]
    
    for query in queries:
        print(f"👤 User: {query}")
        print("-" * 60)
        
        response = agent.invoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        
        print(f"🤖 Assistant: {response['output']}")
        print()
    
    print("="*60)
    print("Key Learning Points:")
    print("- Agent automatically selected appropriate tools")
    print("- Multiple tools were combined for complex requests")
    print("- Model understood when to use which tool")
    print("="*60)
