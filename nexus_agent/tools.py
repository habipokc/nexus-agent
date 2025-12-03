from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from nexus_agent.rag import get_retriever

# 1. Wikipedia Tool
# Karakter limitini 2000'e çıkardık ki bilgi yarım kalıp model uydurmasın.
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=2000, lang="tr")
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

wiki_tool.name = "wikipedia_search"
wiki_tool.description = """
Useful for searching historical figures, events, general knowledge, or facts.
Input should be a specific search query (e.g., 'Ataturk', 'Quantum Physics').
DO NOT use for greetings like 'merhaba', 'nasılsın'.
"""

# 2. RAG Tool
@tool("search_technical_db")
def search_technical_db(query: str) -> str:
    """
    Useful ONLY for technical questions about 'Nexus-Agent', 'project architecture', 
    'Llama 3.2', 'ChromaDB' or the developer 'Habip Okcu'.
    Input should be a specific question.
    """
    # Boş sorgu gelirse hata vermesin, uyaralım.
    if not query or query.strip() == "":
        return "Boş sorgu yapılamaz."

    print(f"🕵️‍♂️ Technical DB Search: {query}")
    retriever = get_retriever()
    
    docs = retriever.invoke(query)
    
    if not docs:
        return "No information found in internal memory."
        
    return "\n\n".join([doc.page_content for doc in docs])

tools = [wiki_tool, search_technical_db]