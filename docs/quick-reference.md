# Quick Reference Guide

A quick reference for the most common LangChain patterns and APIs.

## 🚀 Quick Start (5 minutes)

### Installation & Setup

```bash
# Install LangChain
pip install -r requirements.txt

# Set up API key
export ANTHROPIC_API_KEY="sk-ant-..."
# or: export OPENAI_API_KEY="sk-..."
# or: export GOOGLE_API_KEY="..."
```

### Your First Agent (30 lines)

```python
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

# Define a tool
@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Sunny in {city}!"

# Create model
model = init_chat_model("claude-sonnet-4-6")

# Create agent
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)

# Run it
result = agent.invoke({
    "messages": [{"role": "user", "content": "What's the weather in SF?"}]
})
print(result['output'])
```

---

## 📚 Common Patterns

### Pattern: Multi-Turn Conversation

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
agent = create_agent(..., checkpointer=checkpointer)

config = {"configurable": {"thread_id": "user_123"}}

# Turn 1
result1 = agent.invoke({"messages": [...]}, config=config)

# Turn 2 - same thread, remembers context
result2 = agent.invoke({"messages": [...]}, config=config)
```

### Pattern: Structured Output

```python
from dataclasses import dataclass

@dataclass
class Response:
    answer: str
    confidence: float

from langchain.agents import ToolStrategy
agent = create_agent(
    ...,
    response_format=ToolStrategy(Response)
)
```

### Pattern: Runtime Context

```python
from dataclasses import dataclass
from langchain.tools import ToolRuntime

@dataclass
class Context:
    user_id: str

@tool
def my_tool(runtime: ToolRuntime[Context]) -> str:
    user = runtime.context.user_id
    return f"User: {user}"

agent = create_agent(..., context_schema=Context)
result = agent.invoke(..., context=Context(user_id="123"))
```

---

## 🛠️ Core APIs

### Models

```python
from langchain.chat_models import init_chat_model

# Initialize any model
model = init_chat_model(
    "claude-sonnet-4-6",  # or "gpt-4", "gemini-1.5-pro"
    temperature=0.7,
    max_tokens=1000,
    timeout=10
)

# Invoke
response = model.invoke("Hello!")

# Bind tools
model_with_tools = model.bind_tools([tool1, tool2])
```

### Tools

```python
from langchain.tools import tool

@tool
def my_function(arg1: str, arg2: int) -> str:
    """Description of what this does.
    
    Args:
        arg1: First argument
        arg2: Second argument
        
    Returns:
        Result description
    """
    return f"Result: {arg1} {arg2}"
```

### Messages

```python
from langchain.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage
)

messages = [
    SystemMessage(content="You are helpful"),
    HumanMessage(content="Hi!"),
    AIMessage(content="Hello!"),
    ToolMessage(content="Result", tool_call_id="123")
]
```

### Agents

```python
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=[tool1, tool2],
    system_prompt="You are...",
    checkpointer=checkpointer,  # For memory
    context_schema=Context,      # For user context
    response_format=ToolStrategy(Response)  # For structure
)

result = agent.invoke(
    {"messages": [...]},
    config={"configurable": {"thread_id": "..."}},
    context=Context(...)
)

# Result structure:
# {
#     'output': 'The response text',
#     'structured_response': Response(...),
#     'messages': [...]
# }
```

---

## 🔗 LangGraph Basics

### StateGraph

```python
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
import operator

class State(TypedDict):
    messages: Annotated[list, operator.add]
    counter: int

# Build graph
builder = StateGraph(State)

# Add nodes
def node_a(state):
    return {"messages": ["From A"], "counter": state["counter"] + 1}

builder.add_node("a", node_a)

# Add edges
builder.add_edge(START, "a")
builder.add_edge("a", END)

# Compile
graph = builder.compile()

# Run
result = graph.invoke({"messages": [], "counter": 0})
```

### Conditional Edges

```python
def should_continue(state: State) -> str:
    if state["counter"] > 5:
        return END
    return "a"

builder.add_conditional_edges("a", should_continue, ["a", END])
```

---

## 📊 LangSmith Integration

```python
import os

# Set up LangSmith
os.environ["LANGSMITH_API_KEY"] = "your-key"
os.environ["LANGSMITH_PROJECT"] = "my-project"

# Automatic tracing
agent = create_agent(...)
result = agent.invoke(...)  # Auto-traced in LangSmith
```

---

## 🧪 Testing

```python
import pytest

def test_agent():
    response = agent.invoke({
        "messages": [{"role": "user", "content": "Hello"}]
    })
    assert len(response['output']) > 0
    assert isinstance(response['output'], str)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

## 🐛 Debugging

### Print All Messages

```python
response = agent.invoke(...)
for msg in response['messages']:
    print(f"{msg.type}: {msg.content}")
```

### Enable Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Trace with LangSmith

Access dashboard at [smith.langchain.com](https://smith.langchain.com/)

---

## ⚠️ Common Gotchas

| Issue | Solution |
|-------|----------|
| Agent ignores tools | Make sure tool is in list and has good description |
| Agent doesn't remember | Use checkpointer + same thread_id |
| Tools not called | Bind tools with `.bind_tools()` |
| API key not found | Set environment variable AND `.env` file |
| Token limit exceeded | Reduce max_tokens or summarize messages |
| No response | Check if model supports tool_calls |

---

## 📖 File Structure

```
your-project/
├── main.py                 # Your code
├── .env                    # API keys (DON'T commit!)
├── requirements.txt        # Dependencies
├── tests.py                # Tests
└── outputs/                # Results/logs
```

---

## 🚦 Troubleshooting Steps

1. **Check API key** - Does `printenv ANTHROPIC_API_KEY` return value?
2. **Check imports** - Can you `from langchain import ...`?
3. **Check tool docs** - Is `@tool` docstring clear?
4. **Check model** - Does model support tool_calls?
5. **Enable logging** - Set `logging.DEBUG`
6. **Use LangSmith** - View traces in dashboard

---

## 📚 Next Resources

- [Full LangChain Docs](https://docs.langchain.com/)
- [API Reference](https://reference.langchain.com/)
- [LangSmith Docs](https://docs.langchain.com/langsmith/)
- [LangChain Academy](https://academy.langchain.com/)

---

**Ready to build?** Start with Phase 1!
