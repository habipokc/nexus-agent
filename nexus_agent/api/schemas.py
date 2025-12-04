from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class HealthCheck(BaseModel):
    """Sistem sağlık durumu modeli."""
    status: str = Field(..., description="API durumu")
    version: str = Field(..., description="API versiyonu")

class ChatRequest(BaseModel):
    """Kullanıcıdan gelen mesaj isteği."""
    message: str = Field(..., min_length=1, description="Kullanıcı mesajı")
    # thread_id: LangGraph hafızası (Memory) için kritik olacak.
    thread_id: str = Field(..., description="Sohbet oturum ID'si (UUID)")

class ChatResponse(BaseModel):
    """Kullanıcıya dönecek cevap."""
    response: str = Field(..., description="Agent'ın cevabı")
    sender: str = Field(..., description="Cevabı veren ajan (tech/general/greeting)")
    # Metadata: İleride kaynakça veya debug bilgisi dönmek için.
    metadata: Optional[Dict[str, Any]] = Field(default=None)