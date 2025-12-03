import sys
# Encoding zorlamalarını kaldırıyoruz, Python 3.12 native halletsin.
# Sadece path eklemesi kalsın.
sys.path.append(".")

import warnings
from langchain_core.messages import HumanMessage
from nexus_agent.agent import graph

warnings.filterwarnings("ignore")

def main():
    print("🤖 Nexus-Agent vFinal (Week 2 Complete) Başlatıldı")
    print("--------------------------------------------------")
    print("Çıkış için 'q' yazın.\n")
    
    while True:
        try:
            # Standart input kullanımı
            user_input = input("👤 Sen: ")
            
            if user_input.lower() in ["q", "exit"]:
                print("👋 Görüşürüz!")
                break
            
            if not user_input.strip(): continue

            print("⏳ Çalışıyor...")
            
            # State başlatma
            initial_state = {
                "messages": [HumanMessage(content=user_input)],
                "sender": "user"
            }
            
            for event in graph.stream(initial_state):
                for key, value in event.items():
                    if "messages" in value:
                        last_msg = value["messages"][-1]
                        
                        # Tool logu
                        if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                            print(f"   ⚙️  {key.upper()} -> Tool Çağırıyor: {last_msg.tool_calls[0]['name']}")
                        
                        # Ajan cevabı
                        elif key in ["tech_agent", "general_agent", "greeting_agent"]:
                            if last_msg.content.strip():
                                print(f"\n🤖 {key.upper()}: {last_msg.content}\n")

                    if key == "tools":
                        print("   ✅  Tool Verisi İşlendi.")

        except KeyboardInterrupt:
            print("\n👋 İşlem iptal edildi.")
            break
        except Exception as e:
            print(f"❌ Hata: {e}")

if __name__ == "__main__":
    main()