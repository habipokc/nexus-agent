from typing import Literal

def classify_user_input(user_input: str) -> Literal["tech", "greeting", "general"]:
    """
    Kullanıcı girdisini analiz eder.
    1. Proje sorusu mu? -> tech
    2. Selamlaşma mı? -> greeting
    3. Hiçbiri değilse -> general (Araştırma)
    """
    text = user_input.lower()
    
    # 1. Proje/Teknik Kelimeler (Öncelikli)
    project_keywords = ["nexus", "habip", "chroma", "llama", "yerel", "proje", "database", "veritabanı"]
    if any(word in text for word in project_keywords):
        print("   🛡️  ROUTER: Teknik Ajan (Kural Tabanlı)")
        return "tech"

    # 2. Selamlaşma Kelimeleri
    greeting_keywords = ["merhaba", "selam", "nasılsın", "günaydın", "iyi akşamlar", "kimsin", "naber"]
    # Tam eşleşme veya kelime içinde geçme kontrolü
    if any(word in text for word in greeting_keywords):
        print("   🛡️  ROUTER: Selamlaşma Modu (Toolsuz)")
        return "greeting"

    # 3. Varsayılan (Araştırma)
    print("   🛡️  ROUTER: Genel Araştırma (Wiki)")
    return "general"