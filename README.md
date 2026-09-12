# 🕸️ LangGraph — Basics & Core Concepts

Was the first time my friend introduced langgraph to me soo got curios, and curiosity led me here
A quick-reference README for understanding how LangGraph works under the hood.

---

## What is LangGraph?

**LangGraph** is a library (built by the LangChain team) for building **stateful, multi-step AI applications** — especially agents — by modeling them as a **graph** instead of a straight-line chain.

Normal LangChain chains run **linearly**: step 1 → step 2 → step 3.
Real agents don't work like that — they need to **loop, branch, retry, and call tools conditionally**. LangGraph gives you that control by letting you define:

- **Nodes** → units of work (functions)
- **Edges** → how control flows between nodes
- **State** → shared memory that flows through the whole graph

Think of it like a **flowchart** you can actually execute in code.

---

## 🧩 Core Concepts

### 1. State
The **State** is a shared object (usually a `TypedDict` or Pydantic model) that gets passed between every node. Each node can read from it and update it.

```python
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    step_count: int
```

Every node receives the current state and returns updates to merge into it.

---

### 2. Nodes
A **Node** is just a Python function that does one job — call an LLM, run a tool, transform data, etc. It takes the state in and returns a (partial) state update.

```python
def call_model(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}
```

Nodes are the **"boxes"** in your flowchart.

---

### 3. Edges
**Edges** connect nodes and define execution order.

- **Normal edge** → always go from Node A to Node B.
- **Conditional edge** → a function decides which node to go to next, based on the current state (this is how branching/looping happens).

```python
graph.add_edge("call_model", "check_tools")

graph.add_conditional_edges(
    "check_tools",
    should_continue,   # function returning a node name
    {"continue": "call_model", "end": END}
)
```

---

### 4. Tools
**Tools** are functions the LLM can decide to call — search the web, query a database, do a calculation, etc. In LangGraph, tools are usually wrapped and attached to a special **ToolNode**, which:

1. Looks at the LLM's output for a tool call request
2. Executes the actual Python function
3. Returns the result back into the state

```python
from langgraph.prebuilt import ToolNode

tools = [search_tool, calculator_tool]
tool_node = ToolNode(tools)
```

The LLM doesn't "run" the tool itself — it just *requests* one, and the graph executes it.

---

### 5. The Graph (StateGraph)
This is where you wire everything together.

```python
from langgraph.graph import StateGraph, END

graph = StateGraph(AgentState)

graph.add_node("call_model", call_model)
graph.add_node("tools", tool_node)

graph.set_entry_point("call_model")
graph.add_conditional_edges("call_model", should_continue, {
    "tools": "tools",
    "end": END
})
graph.add_edge("tools", "call_model")

app = graph.compile()
```

- `set_entry_point` → where execution starts
- `END` → a special marker meaning "stop here"
- `.compile()` → turns your graph definition into a runnable app

---

### 6. Checkpointer (Memory)
A **Checkpointer** lets the graph **save and resume state** — useful for multi-turn conversations, human-in-the-loop pauses, or crash recovery.

```python
from langgraph.checkpoint.memory import MemorySaver

app = graph.compile(checkpointer=MemorySaver())
```

Without a checkpointer, every `.invoke()` starts fresh.

---

## 🔁 The Typical Agent Loop

```
User input → call_model (LLM decides) 
     ↓ (if tool call requested)
   tools node executes tool
     ↓
   back to call_model with tool result
     ↓ (if no more tool calls)
   END → return final answer
```

This loop is what lets an agent **think → act → observe → think again** until it's done.

---

## 🗝️ Quick Glossary

| Term | Meaning |
|---|---|
| **State** | Shared data object passed between all nodes |
| **Node** | A function that does one unit of work |
| **Edge** | Connection defining what runs next |
| **Conditional Edge** | Branch logic — chooses the next node dynamically |
| **Tool** | External function the LLM can call |
| **ToolNode** | Prebuilt node that executes requested tools |
| **Entry Point** | The first node the graph runs |
| **END** | Special node marking graph completion |
| **Checkpointer** | Saves/restores state across runs (memory) |
| **Compile** | Converts the graph definition into a runnable app |

---

## 📌 Why Use LangGraph Instead of Plain LangChain Chains?

- Supports **loops** (agents retrying or re-planning)
- Supports **branching** (different paths based on conditions)
- Explicit, inspectable **state** at every step
- Easier to debug — you can visualize the graph itself
- Built-in support for **human-in-the-loop** and **persistence**

---

*Personal practice notes while learning LangGraph — will expand as I build more agent workflows.*
