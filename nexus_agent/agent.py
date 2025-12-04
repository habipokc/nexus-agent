from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from nexus_agent.core.state import AgentState
from nexus_agent.core.router import classify_user_input
from nexus_agent.tools import tools
from nexus_agent.agents.technical import tech_node
from nexus_agent.agents.general import general_node, greeting_node
from nexus_agent.agents.grader import grader_node

# --- YARDIMCI FONKSİYONLAR (NODES) ---

# Ajanları "Sender" bilgisiyle sarmalayalım ki State güncellensin.
def run_tech_agent(state: AgentState):
    result = tech_node(state)
    # Mesajı güncelle ve 'sender' bilgisini Tech olarak işaretle
    return {"messages": result["messages"], "sender": "tech_agent"}

def run_general_agent(state: AgentState):
    result = general_node(state)
    return {"messages": result["messages"], "sender": "general_agent"}

def run_greeting_agent(state: AgentState):
    result = greeting_node(state)
    return {"messages": result["messages"], "sender": "greeting_agent"}

def run_grader(state: AgentState):
    result = grader_node(state)
    return {"messages": result["messages"], "sender": "grader"}

# --- ROUTING MANTIĞI (EDGES) ---

def router_logic(state: AgentState) -> Literal["tech_agent", "general_agent", "greeting_agent"]:
    messages = state["messages"]
    last_message = messages[-1]
    decision = classify_user_input(last_message.content)
    
    if decision == "tech": 
        return "tech_agent"
    elif decision == "greeting": 
        return "greeting_agent"
    else: 
        return "general_agent"

def agent_router(state: AgentState) -> Literal["tools", "grader", END]:
    """
    Ajan çalıştıktan sonra ne olacak?
    1. Tool çağırdıysa -> 'tools'
    2. Tool çağırmadıysa (cevabı verdiyse) -> 'grader'
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    if last_message.tool_calls:
        return "tools"
    return "grader"

def tool_router(state: AgentState) -> Literal["tech_agent", "general_agent"]:
    """
    🔥 SORUN 2 ÇÖZÜMÜ:
    Tool işini bitirdi. Kime dönecek?
    State içindeki 'sender' bilgisine bakıp onu çağıran ajana geri dönüyoruz.
    """
    sender = state["sender"]
    if sender == "tech_agent":
        return "tech_agent"
    else:
        # Greeting zaten tool kullanmaz, geriye General kalır.
        return "general_agent"

def grader_router(state: AgentState) -> Literal[END]:
    """
    Grader şimdilik sadece END'e gidiyor.
    İleride buraya 'Retry' (general_agent'a geri dön) ekleyeceğiz.
    """
    # Grader'ın onay/red mantığı Grader Node içinde loglanıyor.
    return END

# --- GRAF İNŞASI ---
builder = StateGraph(AgentState)

# 1. Node'ları Ekle
builder.add_node("tech_agent", run_tech_agent)
builder.add_node("general_agent", run_general_agent)
builder.add_node("greeting_agent", run_greeting_agent)
builder.add_node("tools", ToolNode(tools))
builder.add_node("grader", run_grader)

# 2. Başlangıç -> Router
builder.add_conditional_edges(START, router_logic)

# 3. Ajanlar -> Karar (Tool mu Grader mı?)
builder.add_conditional_edges("tech_agent", agent_router)
builder.add_conditional_edges("general_agent", agent_router)

# Greeting -> Grader'a gerek yok, direkt bitsin (Sorun 1 Çözümü: Loop yoksa bitir)
builder.add_edge("greeting_agent", END) 

# 4. Tool -> ÇAĞIRAN AJANA DÖN (Kritik Düzeltme)
builder.add_conditional_edges("tools", tool_router)

# 5. Grader -> Bitiş
builder.add_conditional_edges("grader", grader_router)

graph = builder.compile()