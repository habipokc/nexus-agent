from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Sabitler
PERSIST_DIRECTORY = "./chroma_db"
# Embedding fonksiyonunu tanımlamak zorundayız çünkü Chroma veriyi geri okurken
# "Hangi modelle gömdüysen onunla okurum" der (boyut kontrolü için).
embedding_function = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

def inspect():
    print("🔍 Veritabanı Açılıyor...")
    
    # Veritabanına bağlan
    db = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_function
    )
    
    # Tüm verileri çek (ID'ler, Metadata, Dokümanlar ve Vektörler)
    # include=['embeddings'] demezsek vektör sayılarını getirmez, sadece metni getirir.
    data = db.get(include=['documents', 'metadatas', 'embeddings'])
    
    count = len(data['ids'])
    print(f"📂 Toplam Doküman Sayısı: {count}\n")
    
    if count > 0:
        print("--- Örnek Kayıt (İlk Sıradaki) ---")
        print(f"🆔 ID: {data['ids'][0]}")
        print(f"📄 Metin: {data['documents'][0][:100]}...") # İlk 100 karakter
        
        vector = data['embeddings'][0]
        print(f"🧮 Vektör Boyutu: {len(vector)} (Bu model 384 boyutlu vektör üretir)")
        print(f"🔢 Vektörün İlk 5 Sayısı: {vector[:5]}") # Hepsini basarsak ekran dolar
        print("   (Bu sayılar, metnin uzaydaki koordinatlarıdır)")

if __name__ == "__main__":
    inspect()