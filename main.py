import sys
import io
import warnings
from langchain_core.messages import HumanMessage
from nexus_agent.agent import graph

# 1. UTF-8 Zorlaması
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

warnings.filterwarnings("ignore")

def main():
    print("🤖 Nexus-Agent v4.1 (Selamlaşma Fix) Başlatıldı")
    print("-----------------------------------------------")
    print("Çıkış için 'q' yazın.\n")
    
    while True:
        try:
            user_input = input("👤 Sen: ")
            if user_input.lower() in ["q", "exit"]:
                print("👋 Görüşürüz!")
                break
            
            if not user_input.strip(): 
                continue

            print("⏳ Çalışıyor...")
            inputs = {"messages": [HumanMessage(content=user_input)]}
            
            for event in graph.stream(inputs):
                for key, value in event.items():
                    # Mesajları al
                    messages = value.get("messages", [])
                    if not messages: 
                        continue
                    
                    last_msg = messages[-1]
                    
                    if key == "tools":
                        print("   ✅  Tool Verisi Alındı.")
                        
                    # DÜZELTME BURADA: "greeting_agent" EKLENDİ!
                    elif key in ["tech_agent", "general_agent", "greeting_agent"]:
                        
                        # Tool çağrısı var mı?
                        if last_msg.tool_calls:
                            tool_name = last_msg.tool_calls[0]['name']
                            print(f"   ⚙️  {key.upper()} -> Tool Çağırıyor: {tool_name}")
                        else:
                            # Cevap geldi
                            print(f"\n🤖 {key.upper()}: {last_msg.content}\n")

        except Exception as e:
            print(f"❌ Hata: {e}")

if __name__ == "__main__":
    main()