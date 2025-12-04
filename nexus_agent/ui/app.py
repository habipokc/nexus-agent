import streamlit as st
import requests
import uuid

# --- AYARLAR ---
API_URL = "http://127.0.0.1:8000/chat"
PAGE_TITLE = "Nexus-Agent v6.0"
PAGE_ICON = "🤖"

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="centered"
)

st.title(f"{PAGE_ICON} {PAGE_TITLE}")
st.caption("🚀 Llama 3.2 | Local RAG | Multi-Agent System")

# --- SESSION STATE (OTURUM HAFIZASI) ---
# Kullanıcı sayfayı yenileyene kadar geçmişi tutar.

if "messages" not in st.session_state:
    # Başlangıç mesajı
    st.session_state.messages = [
        {"role": "assistant", "content": "Merhaba! Ben Nexus-Agent. Sana nasıl yardımcı olabilirim?"}
    ]

if "thread_id" not in st.session_state:
    # Her oturum için benzersiz bir ID (Hafıza karışmaması için)
    st.session_state.thread_id = str(uuid.uuid4())

# --- GEÇMİŞİ EKRANA BAS ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- KULLANICI GİRDİSİ ---
if prompt := st.chat_input("Mesajınızı yazın..."):
    # 1. Kullanıcı mesajını ekrana bas
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. API'ye İstek At (Backend ile Haberleşme)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ *Düşünüyor...*")
        
        try:
            # API Payload
            payload = {
                "message": prompt,
                "thread_id": st.session_state.thread_id
            }
            
            # Request
            # Not: UI tarafında requests (senkron) kullanmak genelde sorun olmaz
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get("response", "Hata: Cevap alınamadı.")
                
                # Meta verileri (Opsiyonel: Debug için ekrana basılabilir)
                # has_tool = data["metadata"]["has_tool_calls"]
                
                # 3. Cevabı Ekrana Bas
                message_placeholder.markdown(bot_response)
                
                # Hafızaya ekle
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
            else:
                error_msg = f"❌ API Hatası: {response.status_code}"
                message_placeholder.error(error_msg)
        
        except Exception as e:
            message_placeholder.error(f"❌ Bağlantı Hatası: {str(e)}")
            st.error("API sunucusunun (uvicorn) çalıştığından emin misin?")