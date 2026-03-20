# Phase 1, Experiment 2: Tools & Binding

## Learning Goals

- [ ] Create well-documented tools
- [ ] Understand tool binding to models
- [ ] Work with tool schemas and arguments
- [ ] Handle tool results properly

## Concepts

### What are Tools?

Tools are **functions that agents can invoke** to:
- Interact with external systems (APIs, databases)
- Perform calculations
- Access real-time data
- Modify external state

### Tool Documentation

Tools must be well-documented:

```python
@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a given city.
    
    This tool retrieves real-time weather conditions
    from a weather service.
    
    Args:
        city: Name or ID of the city
        
    Returns:
        Weather description with temperature
    """
    # Implementation
```

### Tool Binding

**Binding** = Giving a model information about available tools

```python
# Without tool binding (doesn't know about the tool)
response = model.invoke("What's the weather?")

# With tool binding (model knows about tools)
model_with_tools = model.bind_tools([get_weather, get_temperature])
response = model_with_tools.invoke("What's the weather?")
# Model can now call tools!
```

## Code Walkthrough

See `main.py` for implementation of:
- Multiple tools with different purposes
- Tool binding to models
- Tool invocation and result processing

## Running the Example

```bash
export ANTHROPIC_API_KEY="your-key-here"
python main.py
```

## Exercises

### Exercise 1: Add a New Tool
Add a `convert_temperature` tool:

```python
@tool
def convert_temperature(temp: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature between Celsius and Fahrenheit."""
    if from_unit == "C" and to_unit == "F":
        return (temp * 9/5) + 32
    elif from_unit == "F" and to_unit == "C":
        return (temp - 32) * 5/9
    return temp
```

### Exercise 2: Complex Tool with Multiple Arguments
Create an `air_quality_index` tool:

```python
@tool
def get_air_quality(city: str, pollutant: str = "PM2.5") -> dict:
    """Get air quality index for a city."""
    return {
        "city": city,
        "pollutant": pollutant,
        "index": 42,
        "level": "Good"
    }
```

### Exercise 3: Test Tool Combinations
Query the agent with combines multiple tools:
```
"What's the weather in SF and the air quality?"
"Tell me the weather in NYC and convert 68°F to Celsius"
```

## Key Takeaways

- Tools extend agent capabilities
- Good documentation is crucial (it becomes the LLM's reference)
- Tool binding enables model tool calling
- Agents automatically route to appropriate tools
- Tools return structured data that agents process

## Common Tool Patterns

| Pattern | Use Case |
|---------|----------|
| **Query Tools** | Retrieve information (weather, prices) |
| **Action Tools** | Perform actions (send email, create ticket) |
| **Transform Tools** | Convert data (temperature, currency) |
| **Compute Tools** | Perform calculations |

## Next Steps

Move to **Experiment 3: Memory & State** to learn:
- How agents remember conversations
- Managing conversation state
- Thread IDs and multi-turn interactions
