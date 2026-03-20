# Phase 1, Experiment 4: Structured Output

## Learning Goals

- [ ] Define response schemas with Pydantic
- [ ] Generate structured outputs
- [ ] Validate agent responses
- [ ] Use structured output for reliability

## Concepts

### Why Structured Output?

Without structure, agent responses are unpredictable:
```python
# User asks for weather in 3 cities
# Without structure:
response = "Weather in SF is sunny and 72F. New York is rainy, 68F. London is cloudy, 55F."
# ❌ Can't easily parse or programmatically use

# With structure:
response = WeatherResponse(
    cities=[
        CityWeather(name="SF", condition="Sunny", temp=72),
        CityWeather(name="NYC", condition="Rainy", temp=68),
        CityWeather(name="London", condition="Cloudy", temp=55),
    ]
)
# ✅ Easy to use in code!
```

### Response Schemas

Using Pydantic for type-safe responses:

```python
from pydantic import BaseModel

class WeatherData(BaseModel):
    city: str
    condition: str
    temperature: int
    humidity: int
    
class Response(BaseModel):
    weather: WeatherData
    summary: str
    recommendation: str
```

## Code Walkthrough

See `main.py` for:
- Defining Pydantic models
- Using structured output with agents
- Parsing and validating responses

## Running the Example

```bash
export ANTHROPIC_API_KEY="your-key-here"
python main.py
```

## Exercises

### Exercise 1: Complex Schema
Create a multi-level schema:

```python
class ForecastDay(BaseModel):
    date: str
    high_temp: int
    low_temp: int
    condition: str

class WeatherForecast(BaseModel):
    city: str
    forecast_days: list[ForecastDay]
    summary: str
```

### Exercise 2: Validation
Add custom validation:

```python
class WeatherResponse(BaseModel):
    temp: int
    
    @field_validator('temp')
    @classmethod
    def validate_temp(cls, v):
        assert -100 <= v <= 150, 'Temperature out of range'
        return v
```

### Exercise 3: Enum Response Types
Use Enums for consistent options:

```python
from enum import Enum

class WeatherCondition(str, Enum):
    SUNNY = "sunny"
    RAINY = "rainy"
    CLOUDY = "cloudy"
    
class Response(BaseModel):
    condition: WeatherCondition
```

## Key Takeaways

- Structured output improves reliability
- Pydantic validates response format
- Typed responses enable programmatic usage
- Agent can follow schema requirements
- Great for integrating with downstream systems

## Validation Patterns

| Pattern | Use Case |
|---------|----------|
| **Type hints** | Basic validation |
| **Field validators** | Complex rules |
| **Root validators** | Cross-field validation |
| **Enums** | Restricted choices |

## Production Benefits

- ✅ Validate agent outputs
- ✅ Prevent malformed responses
- ✅ Enable downstream automation
- ✅ Clear API contracts
- ✅ Type safety in Python

## Next Steps

You've completed Phase 1 foundations! You now understand:
- Basic agents
- Tools and binding
- Memory and state
- Structured output

Ready for **Phase 2: LangGraph**!
