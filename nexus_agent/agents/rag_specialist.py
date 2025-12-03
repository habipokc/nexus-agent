from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from nexus_agent.core.state import AgentState
from nexus_agent.tools import tools

rag_func = tools[1]
llm = ChatOllama(model="llama3.2", temperature=0)

system_prompt = """You are the Technical Expert.
Your knowledge comes ONLY from the database.

EXAMPLES:
User: "Nexus-Agent nedir?"
You: SEARCH: Nexus-Agent

User: "Habip kim?"
You: SEARCH: Habip Okcu

INSTRUCTION:
Always output "SEARCH: <query>" to find answers.
"""

def rag_node(state: AgentState):
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    response = llm.invoke(messages)
    content = response.content.strip()
    
    print(f"   👀 [DEBUG RAG]: '{content}'")
    
    if "SEARCH:" in content.upper():
        if "SEARCH:" in content: query = content.split("SEARCH:")[1].strip()
        elif "Search:" in content: query = content.split("Search:")[1].strip()
        else: query = content

        print(f"   🧠 (RAG) Aranıyor: '{query}'")
        tool_result = rag_func.invoke(query)
        
        # Sonucu modele ver ve cevap iste
        final_prompt = f"Database Result: {tool_result}\n\nAnswer the user in Turkish."
        messages.append(HumanMessage(content=final_prompt))
        final_response = llm.invoke(messages)
        
        # BURASI ÖNEMLİ: Final cevabı döndürüyoruz
        return {"messages": [final_response]}
    
    return {"messages": [response]}