# Phase 1, Experiment 1: Basic Agent

## Learning Goals

- [ ] Understand how agents work
- [ ] Create your first LangChain agent
- [ ] Understand the agent invocation flow
- [ ] See tool calling in action

## Concepts

### What is an Agent?

An agent is an **autonomous entity** that:
1. Receives a user query
2. Decides what to do (think)
3. Calls tools if needed (act)
4. Returns a result

### The Agent Loop

```
User Query
    ↓
Agent Decision (LLM)
    ↓
Need tools?
    ├─ YES → Call Tools
    │         ↓
    │     Process Results
    │         ↓
    │     Loop back to Agent Decision
    └─ NO → Return Final Answer
```

## Code Walkthrough

See `main.py` for the implementation.

### Key Components

1. **Model**: The LLM that powers the agent
2. **Tools**: Functions the agent can call
3. **System Prompt**: Instructions for the agent
4. **Agent**: Orchestrates it all together

## Running the Example

```bash
# Set up environment
export ANTHROPIC_API_KEY="your-key-here"

# Run the agent
python main.py
```

## Expected Output

```
User: "What's the weather in San Francisco?"

Agent thinks: "The user wants weather info. I should call get_weather tool."

Calling tool: get_weather with city="San Francisco"
Tool result: "It's always sunny in San Francisco!"

Final response: "The weather in San Francisco is sunny! Perfect day to visit the Golden Gate Bridge. ☀️"
```

## Exercises

### Exercise 1: Add Another Tool
Modify `main.py` to add a `get_temperature()` tool:

```python
@tool
def get_temperature(city: str) -> str:
    """Get temperature for a city."""
    return "72°F"
```

Then modify the system prompt to mention this new tool.

### Exercise 2: Try Different Models
Uncomment different models in the code and see how they respond differently:

```python
# Try different models
model = init_chat_model("gpt-4-turbo")  # OpenAI
model = init_chat_model("gemini-1.5-pro")  # Google
```

### Exercise 3: Change the System Prompt
Modify the system prompt to change agent behavior:

```python
system_prompt = "You are a grumpy weather reporter who always complains."
system_prompt = "You are an enthusiastic weather forecaster."
system_prompt = "You are a weather expert focused on climate science."
```

## Key Takeaways

- Agents use LLMs to make decisions
- Tools extend agent capabilities
- System prompts guide agent behavior
- Agents can reason about when to use tools

## Next Steps

Move to **Experiment 2: Tools & Binding** to learn how to:
- Create complex tools
- Pass multiple tools to agents
- Understand tool documentation and schemas
