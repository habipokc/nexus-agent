from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from nexus_agent.core.state import AgentState
from nexus_agent.core.router import classify_user_input
from nexus_agent.tools import tools
from nexus_agent.agents.technical import tech_node
from nexus_agent.agents.general import general_node, greeting_node

# --- Router Logic ---
def route_logic(state: AgentState) -> Literal["tech_agent", "greeting_agent", "general_agent"]:
    messages = state["messages"]
    last_message = messages[-1]
    decision = classify_user_input(last_message.content)
    
    if decision == "tech":
        return "tech_agent"
    elif decision == "greeting":
        return "greeting_agent"
    else:
        return "general_agent"

# --- Worker -> Tool Logic ---
def worker_to_tool(state: AgentState) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# --- Graph ---
builder = StateGraph(AgentState)

# Node'lar
builder.add_node("tech_agent", tech_node)
builder.add_node("general_agent", general_node)
builder.add_node("greeting_agent", greeting_node) # Yeni Ajan
builder.add_node("tools", ToolNode(tools))

# Başlangıç -> Router
builder.add_conditional_edges(
    START,
    route_logic,
    {
        "tech_agent": "tech_agent",
        "greeting_agent": "greeting_agent",
        "general_agent": "general_agent"
    }
)

# Tool Kullananlar
builder.add_conditional_edges("tech_agent", worker_to_tool)
builder.add_conditional_edges("general_agent", worker_to_tool)

# Tool Kullanmayanlar (Direkt Bitiş)
builder.add_edge("greeting_agent", END)

# Tool Çıkışı -> General'a dön (Fallback)
builder.add_edge("tools", "general_agent")

graph = builder.compile()