from typing import Annotated, Literal, TypedDict
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from nexus_agent.tools import tools

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatOllama(model="llama3.2", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Temel Prompt
BASE_SYSTEM_PROMPT = """You are Nexus-Agent, a helpful AI assistant running locally on Ubuntu.
Always answer in TURKISH.
"""

def agent_node(state: AgentState):
    # Kullanıcının son mesajını al
    last_user_msg = state["messages"][-1].content.lower()
    
    # --- 1. Kategori: Selamlaşma ---
    greetings = ["merhaba", "selam", "nasılsın", "günaydın", "kimsin"]
    is_greeting = any(word in last_user_msg for word in greetings)
    
    # --- 2. Kategori: Proje Özel Kelimeleri ---
    # Bu kelimeler geçerse Wikipedia yasaklanacak
    project_keywords = ["nexus", "habip", "chroma", "llama", "yerel", "proje"]
    is_project_query = any(word in last_user_msg for word in project_keywords)

    if is_greeting:
        print(f"   🛡️  ROUTER: Selamlaşma modu. (Tool Kapalı)")
        # Toolsuz prompt
        final_prompt = BASE_SYSTEM_PROMPT + "\nUser is greeting you. Reply warmly. DO NOT USE TOOLS."
        messages = [SystemMessage(content=final_prompt)] + state["messages"]
        response = llm.invoke(messages) # Toolsuz model
        
    elif is_project_query:
        print(f"   🛡️  ROUTER: Proje sorusu tespit edildi. (Teknik DB Zorunlu)")
        # Prompt'a 'Enjeksiyon' yapıyoruz: ZORLA 'search_technical_db' KULLAN
        forced_prompt = BASE_SYSTEM_PROMPT + """
        CRITICAL: The user is asking about 'Nexus-Agent' (this specific project).
        YOU MUST USE the 'search_technical_db' tool to find the answer.
        DO NOT USE WIKIPEDIA for 'Nexus-Agent' queries.
        """
        messages = [SystemMessage(content=forced_prompt)] + state["messages"]
        response = llm_with_tools.invoke(messages) # Toollu model
        
    else:
        print(f"   🛡️  ROUTER: Genel bilgi isteği. (Serbest Mod)")
        # Standart davranış
        messages = [SystemMessage(content=BASE_SYSTEM_PROMPT)] + state["messages"]
        response = llm_with_tools.invoke(messages)

    return {"messages": [response]}

tool_node = ToolNode(tools)

def should_continue(state: AgentState) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")

graph = builder.compile()