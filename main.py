from langchain_core.messages import HumanMessage
from nexus_agent.agent import graph
import warnings

#  Gereksiz uyarıları kapat
warnings.filterwarnings("ignore")

def main():
    print("🤖 Nexus-Agent v1.0 Başlatıldı (Çıkış için 'q' yazın)")
    print("-----------------------------------------------------")
    
    while True:
        try:
            user_input = input("\n👤 Sen: ")
            if user_input.lower() in ["q", "exit", "quit"]:
                print("👋 Görüşürüz!")
                break
            
            # Boş giriş kontrolü
            if not user_input.strip():
                continue

            inputs = {"messages": [HumanMessage(content=user_input)]}
            print("⏳ Ajan çalışıyor...")
            
            for event in graph.stream(inputs):
                for key, value in event.items():
                    if key == "agent":
                        msg = value["messages"][0]
                        if msg.tool_calls:
                            tool_name = msg.tool_calls[0]['name']
                            print(f"   ⚙️  KARAR: '{tool_name}' aracı kullanılacak...")
                        else:
                            print(f"🤖 Ajan: {msg.content}")
                    
                    elif key == "tools":
                        # Tool çıktısını görmek debug için iyidir
                        # msg = value["messages"][0] 
                        # print(f"   ✅  Veri: {msg.content[:50]}...")
                        print("   ✅  Tool çalıştı, veri alındı.")

        except Exception as e:
            # Hata olsa bile program kapanmasın
            print(f"❌ Beklenmeyen bir hata: {e}")

if __name__ == "__main__":
    main()