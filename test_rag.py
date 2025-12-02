from nexus_agent.rag import get_retriever
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def test_rag():
    print("🚀 RAG Sistemi Başlatılıyor...")
    
    # 1. LLM (Beyin)
    llm = ChatOllama(model="llama3.2", temperature=0)
    
    # 2. Retriever (Hafıza Çağırıcı)
    retriever = get_retriever()
    
    # 3. Prompt (Talimat)
    template = """Aşağıdaki bağlam bilgisini kullanarak soruyu cevapla.
    Eğer cevabı bağlam içinde bulamazsan 'Bilmiyorum' de.
    
    Bağlam: {context}
    
    Soru: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    # 4. Zinciri Kur (Retrieval -> Prompt -> LLM)
    # Bu zincir:
    # - Soruyu alır
    # - Retriever'a sorup ilgili dokümanı bulur (context)
    # - Soruyu ve dokümanı prompt'a koyar
    # - LLM'e gönderir
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # 5. Soruyu Sor
    soru = "Nexus-Agent projesinin amacı nedir ve hangi veritabanını kullanır?"
    print(f"\n❓ Soru: {soru}")
    print("⏳ Düşünüyor (Veritabanına bakılıyor)...")
    
    cevap = rag_chain.invoke(soru)
    
    print("\n🤖 Cevap:")
    print(cevap)

if __name__ == "__main__":
    test_rag()