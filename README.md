# Agent-Based PDF Reasoner (LangChain + Gemini + Tool-Calling Agent)

This project is a full-stack app that lets you:

- Upload PDFs (research papers, manuals, contracts, etc.).
- Ingest them using **LangChain**:
  - `PyPDFLoader` (page-aware)
  - `RecursiveCharacterTextSplitter`
  - `GoogleGenerativeAIEmbeddings`
  - `FAISS` vector store (per document)
- Ask questions using a **LangChain tool-calling agent**:
  - `search_pdf` tool searches the vector store via LangChain.
  - Agent is built with `create_tool_calling_agent` + `AgentExecutor`.
  - LLM = `ChatGoogleGenerativeAI` (Gemini).
- Get answers with **citations and pages**, and open that page in a PDF viewer.

---

## 1. Environment Variables

Set **one** of these (or both):

```bash
# recommended for LangChain integration with Gemini
export GOOGLE_API_KEY="your_gemini_api_key"

# optional alias
export GEMINI_API_KEY="your_gemini_api_key"

# optional overrides
export GEMINI_CHAT_MODEL="gemini-2.0-flash"
export GEMINI_EMBED_MODEL="models/embedding-001"
