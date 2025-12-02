from nexus_agent.tools import tools

def test_tools():
    print("🧰 Araçlar Test Ediliyor...\n")
    
    # 1. Wikipedia Testi
    print("--- Wikipedia Testi ---")
    wiki = tools[0] # Listede ilk sırada wiki var
    soru_wiki = "Mustafa Kemal Atatürk"
    print(f"🔍 Aranıyor: {soru_wiki}")
    sonuc_wiki = wiki.invoke(soru_wiki)
    print(f"📄 Sonuç (Özet):\n{sonuc_wiki[:200]}...\n") # İlk 200 karakteri bas
    
    # 2. RAG Testi
    print("--- RAG (Hafıza) Testi ---")
    rag = tools[1] # Listede ikinci sırada rag var
    soru_rag = "Nexus-Agent hangi modeli kullanır?"
    print(f"🧠 Hafızaya Soruluyor: {soru_rag}")
    sonuc_rag = rag.invoke(soru_rag)
    print(f"📄 Sonuç:\n{sonuc_rag}\n")

if __name__ == "__main__":
    test_tools()