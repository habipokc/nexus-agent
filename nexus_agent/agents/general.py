from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from nexus_agent.core.state import AgentState
from nexus_agent.tools import tools

# --- SETUP ---
wiki_tool = tools[0]
llm = ChatOllama(model="llama3.2", temperature=0)

# Tool'lu Model (Araştırma için)
llm_with_tools = llm.bind_tools([wiki_tool])

# --- PROMPTS ---
prompt_research = """You are a Research Assistant. 
You answer questions using Wikipedia.
If the tool returns information, summarize it in Turkish.
"""

prompt_greeting = """You are Nexus-Agent, a helpful assistant.
The user greeted you. Reply warmly and briefly in Turkish.
Do not act like a search engine. Just chat.
"""

# --- NODES ---

def general_node(state: AgentState):
    """Araştırma yapan, Wiki kullanan node."""
    messages = [SystemMessage(content=prompt_research)] + state["messages"]
    
    # Tool'lu model çağır
    response = llm_with_tools.invoke(messages)
    
    # --- EKLENEN KISIM: Cevap Kontrolü ---
    # Eğer Wikipedia tool'u hata verdiyse veya model "Geçersiz sonuç" diyorsa
    # Bunu standart bir hata mesajına çevirelim ki Grader yakalayabilsin.
    content = response.content.lower()
    
    # Wikipedia wrapper hatası veya modelin boş dönmesi
    if "geçersiz" in content or "invalid" in content or "no result" in content:
         # İçeriği değiştiriyoruz
         response.content = "Aradığınız konuyla ilgili bilgi bulunamadı. Lütfen terimi kontrol edip tekrar deneyin."
    
    return {"messages": [response]}
def greeting_node(state: AgentState):
    """Sadece sohbet eden, TOOL KULLANMAYAN node."""
    messages = [SystemMessage(content=prompt_greeting)] + state["messages"]
    # DİKKAT: Burada saf 'llm' kullanıyoruz (Tools yok!)
    response = llm.invoke(messages)
    return {"messages": [response]}