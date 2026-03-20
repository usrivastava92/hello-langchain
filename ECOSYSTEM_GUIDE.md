# LangChain Ecosystem Guide 🏗️

A comprehensive guide to understanding and working with the LangChain platform and its components.

---

## Table of Contents

1. [Ecosystem Overview](#ecosystem-overview)
2. [LangChain Core](#langchain-core)
3. [LangGraph](#langgraph)
4. [LangSmith](#langsmith)
5. [Integration Patterns](#integration-patterns)
6. [Common Use Cases](#common-use-cases)

---

## Ecosystem Overview

The LangChain platform is designed for **agent engineering** and consists of four main components:

```
┌─────────────────────────────────────────────────────┐
│            LangChain Ecosystem Platform              │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ LangChain    │  │ LangGraph    │  │ LangSmith  │ │
│  │ (Core)       │──│ (Workflows)  │──│ (DevOps)   │ │
│  └──────────────┘  └──────────────┘  └────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │    LangChain Community (Integrations)            │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## LangChain Core

### What is LangChain?

LangChain is a framework for building LLM applications with built-in patterns for:
- Agent creation and orchestration
- Tool integration
- Memory management
- Model abstraction
- Conversation management

### Core Components

#### 1. **Models**
Abstraction layer over LLMs and other models.

```python
from langchain.chat_models import init_chat_model

# Works with any provider
model = init_chat_model(
    "claude-sonnet-4-6",  # OpenAI, Anthropic, Gemini, etc.
    temperature=0.5,
    max_tokens=1000,
    timeout=10
)
```

**Key Concepts:**
- Provider agnostic (OpenAI, Anthropic, Google, etc.)
- Configurable parameters (temperature, timeout, tokens)
- Tool binding capability

#### 2. **Messages**
Structured message types for conversations.

```python
from langchain.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

# Different message types
messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="What is 2+2?"),
    AIMessage(content="2+2=4"),
    ToolMessage(content="Confirmed", tool_call_id="123")
]
```

**Message Types:**
- `SystemMessage` - Instructions for the model
- `HumanMessage` - User input
- `AIMessage` - Model response
- `ToolMessage` - Tool results

#### 3. **Tools**
Functions that agents can call to interact with external systems.

```python
from langchain.tools import tool, ToolRuntime
from dataclasses import dataclass

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"Sunny in {city}"

# Tools with runtime context
@dataclass
class Context:
    user_id: str

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Get user location from context."""
    user_id = runtime.context.user_id
    return "San Francisco"

tools = [get_weather, get_user_location]
```

**Key Concepts:**
- Well-documented (name, description, arguments)
- Function-based with `@tool` decorator
- Runtime context injection
- Type-safe argument schemas

#### 4. **Agents**
Autonomous entities that decide what actions to take.

```python
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=[get_weather, get_user_location],
    system_prompt="You are a helpful assistant",
    checkpointer=checkpointer  # For memory
)

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather?"}]},
    config={"configurable": {"thread_id": "1"}}
)
```

**Agent Types:**
- Tool-calling agents (agentic loop)
- Structured output agents
- Conversational agents

#### 5. **Memory & State Management**

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

# Use in agent
agent = create_agent(
    model=model,
    tools=tools,
    checkpointer=checkpointer
)

# Maintain conversation with thread_id
config = {"configurable": {"thread_id": "user_123"}}
response1 = agent.invoke({"messages": [...]}, config=config)
response2 = agent.invoke({"messages": [...]}, config=config)  # Remembers previous
```

**Memory Patterns:**
- In-memory storage for development
- Persistent checkpoints for production
- Thread-based conversation tracking

---

## LangGraph

### What is LangGraph?

LangGraph is a framework for building **state machines** and **agentic workflows** using a graph-based architecture.

### Key Concepts

#### 1. **State**
Shared mutable data structure that flows through the graph.

```python
from typing_extensions import TypedDict, Annotated
import operator
from langchain.messages import AnyMessage

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]  # Messages accumulate
    llm_calls: int
    intermediate_steps: list

# The `operator.add` means new values append instead of replace
```

**State Patterns:**
- `Annotated` for reducer functions
- `operator.add` - accumulate lists
- `operator.replace` - replace values
- Custom reducers for complex logic

#### 2. **Nodes**
Functions that process state and return updates.

```python
def model_node(state: MessagesState):
    """Call the model and return response."""
    response = model.invoke(state["messages"])
    return {
        "messages": [response],
        "llm_calls": state["llm_calls"] + 1
    }

def tool_node(state: MessagesState):
    """Execute tools from last message."""
    results = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        result = tool.invoke(tool_call["args"])
        results.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
    return {"messages": results}
```

**Node Characteristics:**
- Pure functions (deterministic)
- Take state, return state updates
- Transform state progressively

#### 3. **Edges**
Connections between nodes that specify flow.

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(MessagesState)

# Sequential edges
graph.add_edge(START, "model_node")
graph.add_edge("tool_node", "model_node")

# Conditional edges
def should_continue(state: MessagesState) -> str:
    if state["messages"][-1].tool_calls:
        return "tool_node"
    return END

graph.add_conditional_edges("model_node", should_continue)
```

**Edge Types:**
- `add_edge()` - Always go to target
- `add_conditional_edges()` - Decision-based routing
- `START` - Entry point
- `END` - Exit point

#### 4. **Graph Architecture**

```
START
  │
  ├─▶ model_node (call LLM)
  │       │
  │   Has tool calls?
  │    ╱     ╲
  ├─▶ YES   NO
  │   │       │
  │   │   END (return)
  │   │
  │   ├─▶ tool_node (execute tools)
  │   │       │
  │   └───────┴─▶ back to model_node
```

#### 5. **StateGraph vs Functional API**

**StateGraph (Recommended)**
```python
from langgraph.graph import StateGraph

builder = StateGraph(MessagesState)
builder.add_node("model", model_node)
builder.add_node("tools", tool_node)
builder.add_edge(START, "model")
builder.add_conditional_edges("model", should_continue, ["tools", END])
builder.add_edge("tools", "model")
graph = builder.compile()
```

**Functional API (Alternative)**
```python
from langgraph.func import entrypoint

@entrypoint
def agent(state):
    while should_continue(state):
        state = model_node(state)
        state = tool_node(state)
    return state
```

### LangGraph Patterns

#### Pattern 1: ReAct (Reasoning + Acting)
```
Thought → Action → Observation → Thought → (repeat)
```

#### Pattern 2: Multi-Agent Coordination
```
Supervisor → Delegate to agents → Collect results → Summarize
```

#### Pattern 3: Hierarchical Workflows
```
Main task
├── SubTask A → Parallel processing
├── SubTask B → Parallel processing
└── Merge Results
```

---

## LangSmith

### What is LangSmith?

LangSmith is a **platform for AI engineering** that provides:
- **Tracing**: See exactly what your agent is doing
- **Evaluation**: Test and benchmark agents
- **Deployment**: Manage agents in production
- **Monitoring**: Track performance metrics

### Key Components

#### 1. **Tracing**

```python
import os
from langsmith import Client

# Set up LangSmith
os.environ["LANGSMITH_API_KEY"] = "your-key"
os.environ["LANGSMITH_PROJECT"] = "my-project"

# Automatic tracing with LangChain
agent = create_agent(...)
result = agent.invoke(...)  # Automatically traced
```

**Trace Information:**
- All LLM calls and responses
- Tool invocations and results
- Token usage and latency
- Errors and exceptions
- Custom metadata

#### 2. **Evaluation**

```python
from langsmith import evaluate

# Define evaluation function
def evaluate_accuracy(example, result):
    return result["response"] == example["expected"]

# Run evaluation
results = evaluate(
    client,
    data="my-dataset",
    experiment_prefix="v1",
    prediction_fn=agent.invoke,
    evaluators=[evaluate_accuracy]
)
```

**Evaluation Metrics:**
- Accuracy, precision, recall
- Custom metrics
- Batch evaluation
- Performance comparisons

#### 3. **Datasets**

```python
from langsmith import Client

client = Client()

# Create dataset
dataset = client.create_dataset(
    name="weather-queries",
    description="Common weather questions"
)

# Add examples
client.create_examples(
    inputs=[
        {"question": "What's the weather in SF?"},
        {"question": "Is it raining?"}
    ],
    outputs=[
        {"expected_tool": "weather"},
        {"expected_tool": "weather"}
    ],
    dataset_id=dataset.id
)
```

#### 4. **Production Deployment**

```
Development (Local Testing)
    ↓
LangSmith Evaluation
    ↓
Production Deployment
    ↓
Monitoring & Observability
    ↓
Feedback Loop → Iteration
```

---

## Integration Patterns

### Pattern 1: LangChain + LangGraph

```python
# Use LangChain agents within LangGraph
from langgraph.graph import StateGraph

def agent_node(state):
    # Create a LangChain agent
    agent = create_agent(...)
    result = agent.invoke(state["messages"])
    return {"messages": [result]}

# Embed in graph
graph = StateGraph(...)
graph.add_node("agent", agent_node)
```

### Pattern 2: LangGraph + LangSmith

```python
# Automatic tracing of LangGraph execution
import os

os.environ["LANGSMITH_API_KEY"] = "key"

# Build graph
graph = StateGraph(...).compile()

# Run graph - automatically traced
result = graph.invoke({"messages": [...]})
```

### Pattern 3: Multi-Agent with LangSmith

```python
# Coordinate multiple agents
supervisor = create_agent(
    tools=[weather_agent, research_agent],
    system_prompt="Delegate to appropriate agent"
)

# Monitor all with LangSmith
result = supervisor.invoke(...)
# All delegated agent calls traced automatically
```

---

## Common Use Cases

### Use Case 1: Customer Support Bot
```
LangChain: Simple agent with tools
LangGraph: Not needed (simple flow)
LangSmith: Track conversations, evaluate satisfaction
```

### Use Case 2: Research Assistant
```
LangChain: Base framework
LangGraph: Multi-step research workflow
LangSmith: Evaluate research quality
```

### Use Case 3: Data Analysis Agent
```
LangChain: Create data tools
LangGraph: Complex analysis workflow
LangSmith: Monitor performance, cost tracking
```

### Use Case 4: Multi-Specialist System
```
LangChain: Individual specialist agents
LangGraph: Coordinator orchestration
LangSmith: Track delegation and performance
```

---

## Best Practices

### ✅ DO

- [ ] Use LangChain for agent building
- [ ] Use LangGraph for complex workflows
- [ ] Always implement LangSmith tracing
- [ ] Define clear tool descriptions
- [ ] Test with diverse inputs
- [ ] Monitor production with LangSmith
- [ ] Version your agents
- [ ] Maintain conversation threads

### ❌ DON'T

- [ ] Ignore token costs
- [ ] Skip error handling
- [ ] Use unbounded loops
- [ ] Ignore LangSmith traces
- [ ] Hard-code API keys
- [ ] Deploy without evaluation
- [ ] Forget about context limits
- [ ] Use tools without rate limiting

---

## Architecture Decision Tree

```
Does your task require...

Multi-step workflow?
├─ YES → Use LangGraph
│   └─ Complex conditional logic?
│       ├─ YES → StateGraph API
│       └─ NO → Functional API
└─ NO → Use LangChain Agent

Need production monitoring?
├─ YES → Add LangSmith
└─ NO → Use free tier

Need to coordinate multiple agents?
├─ YES → LangGraph supervisor pattern
└─ NO → Single agent sufficient
```

---

## Key Takeaways

1. **LangChain** = Core building blocks (agents, tools, models)
2. **LangGraph** = Orchestration layer (workflows, state, control flow)
3. **LangSmith** = DevOps layer (tracing, evaluation, deployment)
4. **Community** = Integrations (databases, APIs, services)

Together, they form a complete platform for **agent engineering**.

---

**Next Steps:**
- Start with Phase 1 experiments
- Build basic agents with LangChain
- Progress to LangGraph workflows
- Add LangSmith monitoring
- Deploy to production

Questions? See `docs/troubleshooting.md`
