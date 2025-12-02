from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# 1. Modeli Tanımlıyoruz (Llama 3.2)
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

# 2. Mesajı Hazırlıyoruz
messages = [
    HumanMessage(content="Yazılım dünyasında 'Linux' neden bu kadar popüler? Tek cümleyle özetle.")
]

# 3. Modeli Çalıştırıyoruz
print("⏳ Model düşünüyor...")
response = llm.invoke(messages)

# 4. Sonucu Ekrana Basıyoruz
print("\n🤖 Cevap:")
print(response.content)