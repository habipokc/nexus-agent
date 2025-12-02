from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from nexus_agent.rag import get_retriever

# --- 1. Wikipedia Tool ---
# Wikipedia'yı ayarlıyoruz (lang: 'tr' yaparak Türkçe arama yapmasını sağlıyoruz)
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000, lang="tr")
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

# Tool'un ismini ve açıklamasını netleştirelim (Model buna bakarak seçecek)
wiki_tool.name = "wikipedia_search"
wiki_tool.description = "Genel kültür, tarih, kişiler veya internetteki güncel bilgiler hakkında arama yapmak için kullanılır."

# --- 2. RAG (Hafıza) Tool ---
# Kendi hafızamızı da bir tool olarak tanımlıyoruz.
# @tool dekoratörü, Python fonksiyonunu LLM'in anlayacağı bir araca çevirir.

@tool
def retrieve_knowledge(query: str) -> str:
    """
    Nexus-Agent projesi, teknik detaylar, kullanılan teknolojiler veya
    proje geliştiricisi hakkında bilgi gerektiğinde bu aracı kullan.
    """
    print(f"🕵️‍♂️ Hafıza taranıyor: {query}")
    retriever = get_retriever()
    
    # Retriever doküman listesi döndürür, biz bunu tek bir metne çevirelim
    docs = retriever.invoke(query)
    
    if not docs:
        return "Hafızada bu konuyla ilgili bilgi bulunamadı."
        
    # Bulunan dokümanları birleştir
    return "\n\n".join([doc.page_content for doc in docs])

# --- Tool Listesi ---
# Ajanımıza vereceğimiz alet çantası
tools = [wiki_tool, retrieve_knowledge]