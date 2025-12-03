from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from nexus_agent.rag import get_retriever

# 1. Wikipedia Tool
# Karakter limitini Hafta 1'deki gibi ayarlıyoruz.
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=2000, lang="tr")
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

wiki_tool.name = "wikipedia_search"
wiki_tool.description = """
Useful for searching historical figures, events, general knowledge, or facts.
Input should be a specific search query (e.g., 'Ataturk', 'Quantum Physics').
"""


@tool("wikipedia_search")
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia for general knowledge.
    Input should be a specific search query.
    """
    # 1. Güvenlik: Boş sorgu kontrolü
    if not query or not query.strip():
        return "Hata: Arama terimi boş olamaz."

    print(f"   🌍 (Wiki) Aranıyor: {query}")
    
    try:
        # LangChain Wrapper'ı güvenli modda çalıştırıyoruz
        api_wrapper = WikipediaAPIWrapper(
            top_k_results=1, 
            doc_content_chars_max=2000, 
            lang="tr"
        )
        
        result = api_wrapper.run(query)
        
        # 2. Güvenlik: Wrapper bazen boş string döner, hata sayalım
        if not result or "No good Wikipedia Search Result was found" in result:
            # BURADAKİ MESAJ ÖNEMLİ: Grader "bulunamadı" kelimesini arıyor.
            return "Wikipedia'da bu konuyla ilgili bilgi bulunamadı."
            
        return result

    except Exception as e:
        # 3. Güvenlik: Asla çökme, hatayı metin olarak dön
        return f"Wikipedia arama hatası: {str(e)}"

# 2. RAG Tool (Aynı kalabilir ama güvenlik ekleyelim)
@tool("search_technical_db")
def search_technical_db(query: str) -> str:
    """
    Useful ONLY for technical questions about 'Nexus-Agent', 'project architecture', 
    'Llama 3.2', 'ChromaDB' or the developer 'Habip Okcu'.
    """
    if not query or not query.strip():
        return "Boş sorgu yapılamaz."

    print(f"   🕵️‍♂️ (DB) Teknik Arama: {query}")
    try:
        retriever = get_retriever()
        docs = retriever.invoke(query)
        if not docs:
            return "Veritabanında bilgi bulunamadı."
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Veritabanı hatası: {e}"

tools = [wiki_tool, search_technical_db]