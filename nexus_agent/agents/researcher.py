from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from nexus_agent.core.state import AgentState
from nexus_agent.tools import tools

wiki_func = tools[0]
llm = ChatOllama(model="llama3.2", temperature=0)

# FEW-SHOT PROMPT: Örnekli anlatım
system_prompt = """You are a Research Assistant.
You MUST search Wikipedia for general knowledge questions.

EXAMPLES:
User: "Atatürk kimdir?"
You: SEARCH: Atatürk

User: "Python nedir?"
You: SEARCH: Python programming language

User: "Merhaba"
You: Merhaba! Size nasıl yardımcı olabilirim?

INSTRUCTION:
If the user asks a question, output "SEARCH: <query>".
If the user greets, just reply.
"""

def researcher_node(state: AgentState):
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    response = llm.invoke(messages)
    content = response.content.strip()
    
    print(f"   👀 [DEBUG RESEARCHER]: '{content}'")
    
    # "SEARCH:" veya "Search:" yakala
    if "SEARCH:" in content.upper():
        # Temizlik
        if "SEARCH:" in content: 
            query = content.split("SEARCH:")[1].strip()
        elif "Search:" in content: 
            query = content.split("Search:")[1].strip()
        else: 
            query = content # Fallback
        
        print(f"   🌍 (Wiki) Aranıyor: '{query}'")
        
        try:
            tool_result = wiki_func.invoke(query)
        except Exception as e:
            tool_result = str(e)
            
        final_prompt = f"Search Result: {tool_result}\n\nBased on this result, answer the user's question in Turkish."
        messages.append(HumanMessage(content=final_prompt))
        
        # Final cevabı üret
        final_response = llm.invoke(messages)
        return {"messages": [final_response]}
    
    return {"messages": [response]}