# Phase 2, Experiment 1: State Graph Basics

## Learning Goals

- [ ] Understand StateGraph architecture
- [ ] Define and manage state with Annotated types
- [ ] Build basic graph workflows
- [ ] Compile and visualize graphs

## Concepts

### What is LangGraph?

LangGraph is a **state machine framework** for building agentic workflows.

### Why LangGraph?

LangChain agents are simple linear flows:
```
User Query → LLM → Tool Call → Result → User Response
```

**LangGraph** enables complex workflows:
```
Start
  ├─→ Decision Node (conditional logic)
  ├─→ Multiple paths (parallel or sequential)
  ├─→ Loops (retry, refinement)
  ├─→ Complex branching
  └─→ End
```

### Key Concepts

- **State**: Shared data structure throughout workflow
- **Nodes**: Functions that process and transform state
- **Edges**: Connections between nodes
- **Graph**: Node + Edge structure
- **Compilation**: Convert graph definition to executable

## Code Walkthrough

See `main.py` for basic state graph implementation showing:
- State definition with Annotated types
- Adding nodes
- Sequential edges
- Compilation

Running the example shows how data flows through nodes.

## Running the Example

```bash
export ANTHROPIC_API_KEY="your-key-here"
python main.py
```

## Exercises

### Exercise 1: Add Another Node
Add a processing node that doubles the counter.

### Exercise 2: Visualize the Graph
Display graph structure:

```python
from IPython.display import Image, display
graph = builder.compile()
display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
```

### Exercise 3: Dynamic State
Add complex state types and process them.

## Key Takeaways

- StateGraph enables complex workflows
- Annotated types define state reducers
- Nodes are pure functions
- Graphs compile to executables

## Next Steps

Move to **Experiment 2: Nodes & Edges** to learn:
- Creating multi-node workflows
- Different edge types
- Complex state flows
