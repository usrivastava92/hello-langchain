# Phase 1, Experiment 3: Memory & State

## Learning Goals

- [ ] Understand conversation memory
- [ ] Implement multi-turn conversations
- [ ] Use thread IDs for conversation tracking
- [ ] Persist state across invocations

## Concepts

### Why Memory?

Without memory, agents treat each query independently:
```
User: "I'm from New York"
Agent: "Nice to meet you!"

User: "What's the weather?"
Agent: "I need to know where you are..."  ❌ Forgotten context!
```

With memory, agents maintain context:
```
User: "I'm from New York"
Agent: "Nice! I'll remember that."

User: "What's the weather?"
Agent: "Here's the weather in New York..."  ✅ Context retained!
```

### Memory Types

| Type | Use Case | Persistence |
|------|----------|-------------|
| **In-Memory** | Development/testing | Lost on restart |
| **Persistent** | Production | Survives restart |
| **Checkpoint** | LangGraph workflows | Thread-based |

### Thread IDs

Each conversation gets a unique `thread_id`:

```python
config = {"configurable": {"thread_id": "user_123"}}

# Turn 1
agent.invoke({...}, config=config)  

# Turn 2 - Same thread maintains memory
agent.invoke({...}, config=config)  

# Different thread - Fresh conversation
config2 = {"configurable": {"thread_id": "user_456"}}
agent.invoke({...}, config=config2)
```

## Code Walkthrough

See `main.py` for:
- Creating checkpointers for memory
- Multi-turn conversations
- Thread-based context
- State persistence

## Running the Example

```bash
export ANTHROPIC_API_KEY="your-key-here"
python main.py
```

## Exercises

### Exercise 1: Multi-Turn Conversation
Implement a loop for continuous conversation:

```python
config = {"configurable": {"thread_id": "user_1"}}

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        break
    
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config=config
    )
    print(f"Agent: {response['output']}")
```

### Exercise 2: Multiple Conversations
Test keeping separate conversations:

```python
conversations = {}

# User A
config_a = {"configurable": {"thread_id": "alice"}}
resp_a = agent.invoke({...}, config=config_a)

# User B  
config_b = {"configurable": {"thread_id": "bob"}}
resp_b = agent.invoke({...}, config=config_b)

# Back to User A - should remember earlier context
resp_a2 = agent.invoke({...}, config=config_a)
```

### Exercise 3: Summarization
Implement conversation summarization for long chats:

```python
@tool
def summarize_conversation(runtime: ToolRuntime) -> str:
    """Summarize the conversation so far."""
    # Extract messages and summarize
    return "Summary of key points..."
```

## Key Takeaways

- Agents need memory for multi-turn conversations
- Thread IDs separate different conversations
- Checkpointers persist conversation state
- InMemorySaver for development, database for production
- Message history is critical for context

## Persistence Strategies

### Development
```python
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()
```

### Production
```python
from langgraph.checkpoint.postgres import PostgresSaver
checkpointer = PostgresSaver(connection_string="...")
```

## Next Steps

Move to **Experiment 4: Structured Output** to learn:
- Defining response schemas
- Generating structured outputs
- Pydantic models for validation
