import operator
from typing import Annotated, Sequence, TypedDict, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # Mesaj geçmişi (append mode)
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # Şu anki aktif ajan kim? (tech, general, greeting)
    # Bu sayede Tool çalıştıktan sonra kime döneceğimizi bileceğiz.
    sender: str