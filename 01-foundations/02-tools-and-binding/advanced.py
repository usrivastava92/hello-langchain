"""
Phase 1, Experiment 2: Advanced - Tool Runtime Context
Inject runtime context into tools
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import ToolRuntime, tool

load_dotenv()

# ============================================================================
# STEP 1: Define Runtime Context
# ============================================================================

@dataclass
class UserContext:
    """User-specific context that tools can access."""
    user_id: str
    username: str
    location: str
    preferred_units: str = "F"  # Fahrenheit or Celsius
    language: str = "English"


# ============================================================================
# STEP 2: Create Tools with Runtime Context
# ============================================================================

@tool
def get_user_location(runtime: ToolRuntime[UserContext]) -> str:
    """
    Get the current user's location from context.
    
    This tool accesses the runtime context to get user information.
    """
    context = runtime.context
    return f"User {context.username} is in {context.location}"


@tool
def get_user_weather(
    runtime: ToolRuntime[UserContext],
    city: str = None
) -> str:
    """
    Get weather for user's location or specified city.
    
    Args:
        runtime: User context injected by framework
        city: City name (if None, uses user's location)
    """
    context = runtime.context
    target_city = city or context.location
    
    # Mock weather data
    weather_db = {
        "San Francisco": {"temp": 72, "condition": "Sunny"},
        "New York": {"temp": 68, "condition": "Rainy"},
        "London": {"temp": 55, "condition": "Cloudy"},
    }
    
    weather = weather_db.get(target_city, {"temp": 70, "condition": "Unknown"})
    temp = weather["temp"]
    
    # Convert to user's preferred units if needed
    if context.preferred_units == "C":
        temp = int((temp - 32) * 5/9)
        units = "°C"
    else:
        units = "°F"
    
    return f"Weather in {target_city}: {weather['condition']}, {temp}{units}"


@tool
def log_user_activity(
    runtime: ToolRuntime[UserContext],
    activity: str
) -> str:
    """
    Log user activity (demonstrates tool side effects).
    
    Args:
        runtime: User context
        activity: Activity description
    """
    context = runtime.context
    log_entry = f"[{context.user_id}] {context.username}: {activity}"
    print(f"📝 Log: {log_entry}")
    return "Activity logged"


# ============================================================================
# STEP 3: Create Agent with Context
# ============================================================================

model = init_chat_model("claude-sonnet-4-6", temperature=0.7)

tools = [get_user_location, get_user_weather, log_user_activity]

agent = create_agent(
    model=model,
    tools=tools,
    context_schema=UserContext,  # Specify context schema
    system_prompt="""You are a personalized weather assistant.
    You have access to the user's location and preferences.
    Always be helpful and use their preferred units."""
)

print("✓ Agent created with runtime context support")


# ============================================================================
# STEP 4: Run Agent with Context
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Tools with Runtime Context Demo")
    print("="*60 + "\n")
    
    # Create different user contexts
    users = [
        UserContext(
            user_id="user_001",
            username="Alice",
            location="San Francisco",
            preferred_units="F"
        ),
        UserContext(
            user_id="user_002",
            username="Bob",
            location="London",
            preferred_units="C"
        ),
    ]
    
    queries = [
        "What's the weather where I am?",
        "How's the weather in New York?",
        "Where am I?",
    ]
    
    for user in users:
        print(f"\n👤 User: {user.username} ({user.location})")
        print("Location preference: " + user.preferred_units)
        print("-" * 60)
        
        for query in queries:
            print(f"  Query: {query}")
            
            # Pass context to agent
            response = agent.invoke(
                {"messages": [{"role": "user", "content": query}]},
                context=user  # Inject user context
            )
            
            print(f"  Response: {response['output']}\n")


print("\n" + "="*60)
print("Key Learning Points:")
print("- Tools can access runtime context")
print("- Context enables personalization")
print("- Different users get different results")
print("="*60)
