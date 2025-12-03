from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from nexus_agent.core.state import AgentState

# Model
llm = ChatOllama(model="llama3.2", temperature=0)

system_prompt = """You are a Quality Control Auditor.
Your task is to Evaluate the Assistant's Answer based on the User's Question.

RULES:
1. If the Answer contains valid information -> Output "DECISION: APPROVED"
2. If the Answer contains "bulunamadı", "cannot find", "no info" -> Output "DECISION: REJECTED"
3. If the Answer is "I don't know" or irrelevant -> Output "DECISION: REJECTED"

Output ONLY the decision string. Do not write explanations.
"""

def grader_node(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    
    user_question = "Bilinmiyor"
    for msg in reversed(messages):
        if msg.type == "human":
            user_question = msg.content
            break
            
    print(f"\n   ⚖️  [GRADER] Denetliyor: '{user_question}'")

    # HUMAN MESSAGE KULLANIYORUZ (Llama'yı tetiklemek için)
    prompt = f"""
    QUESTION: {user_question}
    ANSWER: {last_message.content}
    
    What is your decision?
    """
    
    # Invoke
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt)
    ])
    
    content = response.content.strip().upper()
    
    # DEBUG: Ham çıktıyı görelim (Eğer boşsa repr() ile '' görürüz)
    # print(f"   [DEBUG RAW]: {repr(content)}")

    if "APPROVED" in content:
        print("   ✅  GRADER ONAYLADI.")
    elif "REJECTED" in content:
        print("   ❌  GRADER REDDETTİ.")
    else:
        # Boş dönerse veya saçmalarsa
        print(f"   ⚠️  GRADER ANLAŞILAMADI ({content}). Varsayılan: Onay.")
    
    return {"messages": [response]}