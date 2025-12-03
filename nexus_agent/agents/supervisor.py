from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from nexus_agent.core.state import AgentState

# Model Tanımı
llm = ChatOllama(model="llama3.2", temperature=0, format="json")

system_prompt = """
You are the Supervisor. Your ONLY job is to route the user request to the correct worker.
You must NOT answer the question yourself.

WORKERS:
- "researcher": For general knowledge, history, internet search, wikipedia, greetings.
- "rag_specialist": ONLY for technical questions about 'Nexus-Agent' project, 'Habip Okcu', 'Llama 3.2', or 'ChromaDB'.

OUTPUT FORMAT:
You must return a JSON object with a single key 'next_worker'.
Example: {"next_worker": "researcher"}
"""

def supervisor_node(state: AgentState):
    print("\n   [DEBUG] 1. Supervisor Düğümüne Girildi.") # <-- EKLENDİ
    
    messages = [
        SystemMessage(content=system_prompt)
    ] + state["messages"]
    
    print("   [DEBUG] 2. Supervisor Modeli (Ollama) Çağrılıyor... (Bekleyin)") # <-- EKLENDİ
    
    try:
        response = llm.invoke(messages)
        print(f"   [DEBUG] 3. Model Cevap Verdi! İçerik: {response.content}") # <-- EKLENDİ
        return {"messages": [response]}
        
    except Exception as e:
        print(f"   [DEBUG] ❌ MODEL HATASI: {e}") # <-- EKLENDİ
        # Hata olursa varsayılan bir mesaj dönelim ki sistem çökmesin
        from langchain_core.messages import AIMessage
        return {"messages": [AIMessage(content='{"next_worker": "researcher"}')]}