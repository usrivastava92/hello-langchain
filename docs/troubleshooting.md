# Troubleshooting Guide

Common issues and their solutions.

## Installation Issues

### `ModuleNotFoundError: No module named 'langchain'`

**Solution:**
```bash
pip install langchain langchain-core langchain-anthropic
pip install -r requirements.txt
```

### `cryptography ImportError`

**Solution (macOS):**
```bash
pip install --upgrade cryptography
```

---

## API Key Issues

### `AuthenticationError: Invalid API key`

**Checklist:**
1. ✅ Get key from [Anthropic](https://console.anthropic.com/)
2. ✅ Set in terminal: `export ANTHROPIC_API_KEY="sk-ant-..."`
3. ✅ Or create `.env` file:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```
4. ✅ Load in Python: `from dotenv import load_dotenv; load_dotenv()`

### `API call failed - rate limited`

**Solution:**
- Wait a few minutes
- Check billing/quota in console
- Implement retry logic:
  ```python
  from tenacity import retry, wait_exponential
  
  @retry(wait=wait_exponential())
  def call_api():
      return agent.invoke(...)
  ```

---

## Agent Issues

### Agent not using tools

**Checklist:**
- [ ] Tool is in the tools list
- [ ] Tool has clear docstring description
- [ ] Tool returns string or structured data
- [ ] Model supports tool_calling (Claude/GPT-4 do)

**Example:**
```python
# ✅ GOOD - Clear description
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.
    
    Args:
        city: Name of the city
    """
    return f"Weather in {city}"

# ❌ BAD - Unclear description
@tool
def get_weather(city):
    """Utility function."""
    return f"Weather in {city}"
```

### Agent goes into infinite loop

**Solution:**
```python
# Add max iterations
response = agent.invoke(
    {...},
    config={"recursion_limit": 5}  # Max 5 tool calls
)
```

### Agent response is empty

**Solution:**
- Check if model has max_tokens too low
- Increase: `init_chat_model(..., max_tokens=2000)`

---

## Memory Issues

### Agent doesn't remember previous messages

**Checklist:**
- [ ] Checkpointer is created: `checkpointer = InMemorySaver()`
- [ ] Agent has checkpointer: `create_agent(..., checkpointer=checkpointer)`
- [ ] Same thread_id used: `config = {"configurable": {"thread_id": "id"}}`

**Example:**
```python
# ✅ CORRECT - Same thread remembers
config = {"configurable": {"thread_id": "user_123"}}
result1 = agent.invoke({...}, config=config)
result2 = agent.invoke({...}, config=config)  # Remembers result1

# ❌ WRONG - Different threads don't share memory
result1 = agent.invoke({...}, config={"configurable": {"thread_id": "id1"}})
result2 = agent.invoke({...}, config={"configurable": {"thread_id": "id2"}})
```

---

## Structured Output Issues

### `ValidationError: Response format not matched`

**Solution:**
Check that response format matches schema:

```python
# Define response format
from dataclasses import dataclass

@dataclass
class Response:
    answer: str
    confidence: float

# Use in agent
agent = create_agent(
    ...,
    response_format=ToolStrategy(Response)
)

# When invoking, access with:
result = agent.invoke(...)
structured = result['structured_response']
print(structured.answer)  # ✅ Works
```

---

## Performance Issues

### Agent is slow

**Causes:**
- Model inference latency (normal for LLMs)
- Too many tool calls
- Network request to APIs

**Optimization:**
```python
# Use faster model
model = init_chat_model("claude-3-haiku")  # Faster, cheaper

# Reduce tokens
model = init_chat_model(..., max_tokens=500)

# Pre-cache context
from langchain import cache
langchain.llm_cache = InMemoryCache()
```

### High token usage

**Solutions:**
- Summarize long conversations
- Use cheaper models (Haiku < Sonnet < Opus)
- Reduce system prompt length
- Cache common results

---

## LangGraph Issues

### `KeyError` in State Graph

**Solution:**
Check state key names match:

```python
# ✅ CORRECT
class State(TypedDict):
    messages: list
    counter: int

def my_node(state):
    return {"messages": [], "counter": 1}  # Exact keys

# ❌ WRONG
def my_node(state):
    return {"message": [], "count": 1}  # Wrong keys!
```

### Conditional edge returns invalid path

**Solution:**
```python
# ✅ CORRECT - Return valid node name or END
def should_continue(state):
    return "node_a" if True else END

# ❌ WRONG - Invalid node names
def should_continue(state):
    return "invalid_node"
```

---

## Testing Issues

### Tests fail with `ModuleNotFoundError`

**Solution:**
```bash
# Install pytest
pip install pytest pytest-asyncio

# Run tests
pytest tests.py -v
```

### Async test errors

**Solution:**
```python
import pytest

@pytest.mark.asyncio
async def test_async_agent():
    response = await agent.ainvoke(...)
    assert response
```

---

## Environment Issues

### `dotenv` not loading environment variables

**Solution:**
```python
# Make sure to import and call FIRST
from dotenv import load_dotenv
import os

load_dotenv()  # Load before imports
api_key = os.getenv("ANTHROPIC_API_KEY")
print(api_key)  # Should print key
```

---

## Getting Help

### Debug Information to Collect

```python
import langchain
import platform

print(f"LangChain version: {langchain.__version__}")
print(f"Python: {platform.python_version()}")
print(f"OS: {platform.system()}")

# Test import
try:
    from langchain.agents import create_agent
    print("✓ Can import create_agent")
except ImportError as e:
    print(f"✗ Import error: {e}")
```

### Get Help

1. **Check docs:** [docs.langchain.com](https://docs.langchain.com/)
2. **Search forum:** [forum.langchain.com](https://forum.langchain.com/)
3. **GitHub issues:** [github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain/issues)
4. **Discord:** [Join community](https://discord.gg/langchain)

---

**Found a solution?** Add it here for others!
