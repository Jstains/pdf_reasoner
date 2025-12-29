"""
LangChain Tool-Calling Agent that uses:
 - ChatGoogleGenerativeAI (Gemini) for LLM responses
 - A single tool: search_pdf(query, doc_id, k) which returns JSON list of matches

Note: this agent calls the tool and the tool calls the FAISS vectorstore (HuggingFace embeddings were used at ingest time).
"""

import json
from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

from .ingestion import load_vectorstore
from .config import GEMINI_CHAT_MODEL

# ---------- TOOL ----------

@tool
def search_pdf(query: str, doc_id: str, k: int = 5) -> str:
    """
    Search the vectorstore belonging to doc_id and return JSON string
    of list of {page, chunk_id, text, score}
    """
    vs = load_vectorstore(doc_id)
    docs_and_scores = vs.similarity_search_with_score(query, k=k)

    results = []
    for doc, score in docs_and_scores:
        meta = doc.metadata or {}
        page = int(meta.get("page", 0)) or 0
        chunk_id = meta.get("chunk_id", "")
        snippet = doc.page_content[:1000]
        results.append({
            "page": page,
            "chunk_id": chunk_id,
            "text": snippet,
            "score": float(score)
        })
    return json.dumps(results)

TOOLS = [search_pdf]

# ---------- LLM & AGENT ----------

def _create_llm():
    # ChatGoogleGenerativeAI will pick up GOOGLE_API_KEY from env
    return ChatGoogleGenerativeAI(model=GEMINI_CHAT_MODEL, temperature=0.2, max_output_tokens=1024)

def create_agent_executor() -> AgentExecutor:
    llm = _create_llm()

    system_prompt = (
        "You are an assistant that answers questions about a specific PDF document.\n"
        "You MUST call the tool `search_pdf` at least once to find relevant snippets.\n"
        "When you provide an answer, include inline citations like [page X].\n"
        "If you cannot find the answer in the document, state that clearly."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "human",
                "Document ID: {doc_id}\nUser question: {input}"
            ),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent_runnable = create_tool_calling_agent(llm, TOOLS, prompt)
    executor = AgentExecutor(agent=agent_runnable, tools=TOOLS, verbose=False)
    return executor

# singleton executor
_AGENT: AgentExecutor | None = None

def get_agent_executor() -> AgentExecutor:
    global _AGENT
    if _AGENT is None:
        _AGENT = create_agent_executor()
    return _AGENT
