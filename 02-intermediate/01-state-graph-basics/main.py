"""
Phase 2, Experiment 1: State Graph Basics
Foundation of LangGraph - building blocks for agentic workflows
"""

import operator
import os
import sys

# Add workspace root to path so we can import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from langchain.chat_models import init_chat_model
from langchain.messages import (AnyMessage, HumanMessage, SystemMessage,
                                ToolMessage)
from langchain.tools import tool
from langgraph.graph import END, START, StateGraph
from typing_extensions import Annotated, TypedDict

# Import centralized configuration
from config import MODEL_CONFIG, MODEL_NAME, MODEL_PROVIDER

# ============================================================================
# STEP 1: Define State with Annotated Types
# ============================================================================

class CalculatorState(TypedDict):
    """State for calculator workflow."""
    # Annotated with operator.add means messages accumulate (append)
    messages: Annotated[list[AnyMessage], operator.add]
    
    # Regular field (gets overwritten, not accumulated)
    llm_calls: int
    tool_calls: int
    result: str | None


print("✓ State defined")


# ============================================================================
# STEP 2: Define Tools
# ============================================================================

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def divide(a: int, b: int) -> float:
    """Divide two numbers."""
    if b == 0:
        return "Error: Division by zero"
    return a / b


tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}

print(f"✓ Tools defined: {[t.name for t in tools]}")


# ============================================================================
# STEP 3: Initialize Model
# ============================================================================

model = init_chat_model(
    MODEL_NAME,
    model_provider=MODEL_PROVIDER,
    temperature=0  # Deterministic for calculator
)
model_with_tools = model.bind_tools(tools)

print("✓ Model initialized with tools")


# ============================================================================
# STEP 4: Define Nodes
# ============================================================================

def model_node(state: CalculatorState):
    """Call the LLM to decide what to do."""
    
    response = model_with_tools.invoke(
        [
            SystemMessage(content="You are a helpful calculator assistant."),
            *state["messages"]
        ]
    )
    
    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


def tool_node(state: CalculatorState):
    """Execute tools called by the LLM."""
    
    results = []
    
    # Get last message (should be from LLM with tool_calls)
    last_message = state["messages"][-1]
    
    # Process each tool call
    for tool_call in last_message.tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        
        # Create tool message for the result
        results.append(
            ToolMessage(
                content=str(observation),
                tool_call_id=tool_call["id"]
            )
        )
    
    return {
        "messages": results,
        "tool_calls": state.get("tool_calls", 0) + len(last_message.tool_calls)
    }


print("✓ Node functions defined")


# ============================================================================
# STEP 5: Define Conditional Edge
# ============================================================================

def should_continue(state: CalculatorState) -> str:
    """Decide whether to continue to tool_node or end."""
    
    last_message = state["messages"][-1]
    
    # If LLM made tool calls, go to tool_node
    if last_message.tool_calls:
        return "tool_node"
    
    # Otherwise, finish
    return "end"


print("✓ Conditional edge defined")


# ============================================================================
# STEP 6: Build the Graph
# ============================================================================

builder = StateGraph(CalculatorState)

# Add nodes
builder.add_node("model", model_node)
builder.add_node("tool_node", tool_node)

# Add edges
builder.add_edge(START, "model")  # Start with model
builder.add_conditional_edges("model", should_continue, ["tool_node", "end"])
builder.add_edge("tool_node", "model")  # Go back to model after tools

print("✓ Graph structure built")


# ============================================================================
# STEP 7: Compile the Graph
# ============================================================================

graph = builder.compile()

print("✓ Graph compiled and ready")


# ============================================================================
# STEP 8: Run the Graph
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("LangGraph State Graph Basics")
    print("="*60 + "\n")
    
    # Example queries
    queries = [
        "What is 15 + 27?",
        "Multiply 8 by 9",
        "Divide 100 by 5",
        "First add 10 and 20, then tell me about it",
    ]
    
    for query in queries:
        print(f"❓ Query: {query}")
        print("-" * 60)
        
        # Initial state
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "llm_calls": 0,
            "tool_calls": 0,
            "result": None
        }
        
        # Run graph
        output = graph.invoke(initial_state)
        
        # Display results
        print(f"📊 Statistics:")
        print(f"   LLM calls: {output['llm_calls']}")
        print(f"   Tool calls: {output['tool_calls']}")
        print(f"   Final response:")
        
        # The final message from LLM
        final_message = output["messages"][-1]
        print(f"   {final_message.content}")
        print()


print("\n" + "="*60)
print("Key Learning Points:")
print("- State is shared across nodes")
print("- Annotated types define how state updates")
print("- Conditional edges enable branching logic")
print("- Nodes transform state step-by-step")
print("="*60)
