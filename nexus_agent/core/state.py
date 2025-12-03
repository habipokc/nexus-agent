from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# Tüm ajanların paylaşacağı ortak hafıza yapısı
class AgentState(TypedDict):
    # Mesaj geçmişi (User, AI, Tool mesajları)
    # add_messages: Yeni mesaj geldiğinde eskisinin üzerine yazmak yerine ekle (append) yapar.
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # Hangi ajanın sırada olduğunu takip etmek için (Opsiyonel ama iyi bir pratik)
    next: str