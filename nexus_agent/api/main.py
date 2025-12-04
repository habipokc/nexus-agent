import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from langchain_core.messages import HumanMessage

# Kendi modüllerimiz
from nexus_agent.api.schemas import HealthCheck, ChatRequest, ChatResponse
from nexus_agent.agent import graph  # <-- Beynimizi buraya dahil ettik

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("nexus_api")

# --- LIFESPAN ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Nexus-Agent API başlatılıyor...")
    # İleride model yükleme işlemleri burada yapılabilir.
    yield
    logger.info("👋 Nexus-Agent API kapatılıyor...")

app = FastAPI(
    title="Nexus-Agent API",
    description="Llama 3.2 destekli Otonom RAG Ajanı",
    version="v1.0.0",
    lifespan=lifespan
)

# --- ENDPOINTS ---

@app.get("/", response_model=HealthCheck)
async def health_check():
    return HealthCheck(status="active", version="v6.0-stable")

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    logger.info(f"📩 Yeni Mesaj (Thread: {request.thread_id}): {request.message}")

    try:
        # 1. State Hazırlığı
        initial_state = {
            "messages": [HumanMessage(content=request.message)],
            "sender": "user"
        }
        
        config = {"configurable": {"thread_id": request.thread_id}}

        # 2. Graph Çalıştırma
        final_state = await graph.ainvoke(initial_state, config=config)

        # 3. Mesajları Ayıklama
        messages = final_state["messages"]
        last_message = messages[-1]
        sender = final_state.get("sender", "unknown")

        # Grader filtresi (Hafta 3 / Gün 2 fix)
        if "DECISION:" in last_message.content or sender == "grader":
            last_message = messages[-2]
            sender = "AI_Assistant"

        # --- YENİ EKLENEN KISIM (FIX) ---
        # Sadece son mesaja değil, bu turdaki tüm mesajlara bakıyoruz.
        # Eğer herhangi bir mesajda 'tool_calls' varsa True döner.
        was_tool_used = any(
            hasattr(m, 'tool_calls') and len(m.tool_calls) > 0 
            for m in messages
        )
        # --------------------------------

        logger.info(f"📤 Cevap Hazır ({sender}): {last_message.content[:50]}...")

        return ChatResponse(
            response=last_message.content,
            sender=sender,
            metadata={
                "thread_id": request.thread_id,
                "has_tool_calls": was_tool_used  # <-- Burayı güncelledik
            }
        )

    except Exception as e:
        logger.error(f"❌ Hata oluştu: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))