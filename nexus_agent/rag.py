import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. Sabitler
PERSIST_DIRECTORY = "./chroma_db"
DATA_PATH = "./data/dummy_info.txt"

# CPU kullanımı için ayar
EMBEDDING_DEVICE = "cpu" 

def build_vector_store():
    """Veriyi okur, parçalar ve ChromaDB'ye kaydeder."""
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ HATA: {DATA_PATH} bulunamadı!")
        return None

    print("📄 Doküman okunuyor...")
    loader = TextLoader(DATA_PATH)
    docs = loader.load()

    print("✂️ Doküman parçalanıyor...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    splits = text_splitter.split_documents(docs)

    print(f"🧠 Embedding yapılıyor... (Cihaz: {EMBEDDING_DEVICE})")
    # BURAYI DEĞİŞTİRDİK: model_kwargs ekledik
    embedding_function = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': EMBEDDING_DEVICE}
    )

    print("💾 Veritabanına kaydediliyor...")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding_function,
        persist_directory=PERSIST_DIRECTORY
    )
    
    print(f"✅ Başarılı! {len(splits)} parça vektör veritabanına eklendi.")
    return vectorstore

def get_retriever():
    """Kayıtlı veritabanını getirir."""
    # BURAYI DEĞİŞTİRDİK: model_kwargs ekledik
    embedding_function = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': EMBEDDING_DEVICE}
    )
    
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY, 
        embedding_function=embedding_function
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})

if __name__ == "__main__":
    build_vector_store()