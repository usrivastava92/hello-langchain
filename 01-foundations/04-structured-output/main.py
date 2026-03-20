"""
Phase 1, Experiment 4: Structured Output
Generate validated, structured responses
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import ToolStrategy, create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

load_dotenv()

# ============================================================================
# STEP 1: Define Response Schema with Dataclass
# ============================================================================

@dataclass
class WeatherData:
    """Structured weather information."""
    city: str
    condition: str
    temperature: int
    humidity: int
    feels_like: int = None


@dataclass
class WeatherResponse:
    """Complete structured response."""
    weather_data: WeatherData
    summary: str
    recommendation: str


# ============================================================================
# STEP 2: Alternative: Pydantic Models
# ============================================================================

try:
    from pydantic import BaseModel, Field
    
    class PydanticWeatherData(BaseModel):
        """Structured weather using Pydantic (more validation)."""
        city: str = Field(..., description="Name of the city")
        condition: str = Field(..., description="Weather condition")
        temperature: int = Field(..., ge=-100, le=150, description="Temperature in Fahrenheit")
        humidity: int = Field(..., ge=0, le=100, description="Humidity percentage")
        
        class Config:
            json_schema_extra = {
                "example": {
                    "city": "San Francisco",
                    "condition": "Sunny",
                    "temperature": 72,
                    "humidity": 65
                }
            }
    
    class PydanticWeatherResponse(BaseModel):
        """Complete structured response with Pydantic."""
        weather_data: PydanticWeatherData
        summary: str = Field(..., description="One-line summary")
        recommendation: str = Field(..., description="Recommendation based on weather")
    
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    print("Note: Pydantic not installed, using dataclasses")


# ============================================================================
# STEP 3: Define Tools
# ============================================================================

@tool
def get_detailed_weather(city: str) -> dict:
    """Get detailed weather with structured data."""
    weather_data = {
        "San Francisco": {
            "condition": "Sunny",
            "temperature": 72,
            "humidity": 65,
            "feels_like": 71
        },
        "New York": {
            "condition": "Rainy",
            "temperature": 68,
            "humidity": 78,
            "feels_like": 66
        },
        "London": {
            "condition": "Cloudy",
            "temperature": 55,
            "humidity": 72,
            "feels_like": 52
        },
    }
    
    if city in weather_data:
        return weather_data[city]
    return {"error": f"No data for {city}"}


# ============================================================================
# STEP 4: Create Agent with Structured Output
# ============================================================================

model = init_chat_model("claude-sonnet-4-6", temperature=0.5)

tools = [get_detailed_weather]

# Use structured output response format
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    tools=tools,
    checkpointer=checkpointer,
    response_format=ToolStrategy(WeatherResponse),  # Enforce structure!
    system_prompt="""You are a weather expert providing structured information.
    When asked about weather:
    1. Get the weather data
    2. Provide a one-line summary
    3. Give a recommendation based on the weather
    
    Follow the response format exactly."""
)

print("✓ Agent created with structured output format")


# ============================================================================
# STEP 5: Run Agent and Parse Structured Response
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("LangChain Structured Output Demo")
    print("="*60 + "\n")
    
    config = {"configurable": {"thread_id": "weather_bot"}}
    
    queries = [
        "What's the weather in San Francisco?",
        "How's the weather in New York? Should I bring an umbrella?",
        "Tell me about London's weather",
    ]
    
    print("Structured Weather Responses:\n")
    
    for query in queries:
        print(f"❓ Query: {query}")
        print("-" * 60)
        
        response = agent.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config=config
        )
        
        # Access structured response
        structured = response.get('structured_response')
        
        if structured:
            print(f"🏙️  City: {structured.weather_data.city}")
            print(f"🌤️  Condition: {structured.weather_data.condition}")
            print(f"🌡️  Temperature: {structured.weather_data.temperature}°F")
            print(f"💧 Humidity: {structured.weather_data.humidity}%")
            print(f"\n📝 Summary: {structured.summary}")
            print(f"💡 Recommendation: {structured.recommendation}")
        else:
            print(f"Response: {response}")
        
        print()


# ============================================================================
# STEP 6: Demonstrate Pydantic Validation
# ============================================================================

if HAS_PYDANTIC:
    print("\n" + "="*60)
    print("Pydantic Validation Example")
    print("="*60 + "\n")
    
    try:
        # Valid data
        valid_weather = PydanticWeatherData(
            city="San Francisco",
            condition="Sunny",
            temperature=72,
            humidity=65
        )
        print("✓ Valid weather data:")
        print(valid_weather.model_dump_json(indent=2))
        
        # Invalid data will raise validation error
        print("\n✗ Attempting invalid temperature (200°F)...")
        try:
            invalid_weather = PydanticWeatherData(
                city="SF",
                condition="Sunny",
                temperature=200,  # Out of range!
                humidity=65
            )
        except ValueError as e:
            print(f"  Validation error caught: {e}")
            
    except Exception as e:
        print(f"Error: {e}")


print("\n" + "="*60)
print("Key Learning Points:")
print("- Structured output ensures consistent format")
print("- Dataclasses for simple validation")
print("- Pydantic for advanced validation")
print("- Type-safe responses enable automation")
print("="*60)
