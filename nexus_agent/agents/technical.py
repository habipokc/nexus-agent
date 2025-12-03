from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from nexus_agent.core.state import AgentState
from nexus_agent.tools import tools

# Sadece Teknik DB aracı
rag_tool = tools[1]

llm = ChatOllama(model="llama3.2", temperature=0)
llm_with_tools = llm.bind_tools([rag_tool])

# Hafta 1'deki "Critical" prompt
system_prompt = """You are a Technical Support AI.
CRITICAL: The user is asking about 'Nexus-Agent' (this specific project).
YOU MUST USE the 'search_technical_db' tool to find the answer.
DO NOT answer from your memory.
"""

def tech_node(state: AgentState):
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}