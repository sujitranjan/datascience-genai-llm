from langchain_chroma import Chroma
#  Chroma is a vector database
# It stores:

# text

# embeddings (vectors)

# metadata

# Used for semantic search, not chat memory.
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# This converts text → vectors using Google’s embedding model
# Important:
# embedding ≠ LLM
# embeddings are cheap
# used only for similarity search
from langchain.tools import tool

@tool
def rag_tool(query: str) -> str:

    """
    
    MUST be used when the question refers to:
    - internal documents
    - uploaded PDFs
    - resumes
    - user information mentioned earlier
    - company policies
    - interview data
    - anything NOT general world knowledge

    Do NOT answer such questions without calling this tool.

    """
   
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",api_key="")
    print("Embeddings embeddings")

    vectorstore = Chroma(
        collection_name="internal_docs",
        persist_directory="vector_store/chroma_db",
        embedding_function=embeddings
    )
    print("Vector Store:", vectorstore)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) #converrts vecor db into search interface.
## costing innvolve just to chunk user input, else cosine similarity search is free & other method to get the best match.
    docs = retriever.invoke(query)
    #docs = retriever.get_relevant_documents(query)
    print("Documents:", docs)

    return "\n\n".join([doc.page_content for doc in docs])


# INGESTION TIME (offline)
# ------------------------
# Company Docs
#    ↓
# Chunking
#    ↓
# Embedding (cost)
#    ↓
# Stored in Chroma (disk)


# RUNTIME (your code)
# ------------------
# User Query
#    ↓
# Embed query
#    ↓
# Search Chroma DB
#    ↓
# Return text chunks


##################JUst for reading

# 1️⃣ What Hugging Face actually “has”

# Hugging Face has three buckets of models:

# ✅ 1. Open-source models (HF hosts the weights)

# Examples:

# LLaMA-derived models

# Mistral

# Falcon

# Sentence-Transformers

# ✔ Run locally
# ✔ No API key (unless private)
# ✔ Full control

# 🔑 2. Proprietary models via HF Inference Providers

# This includes:

# OpenAI (GPT-4, GPT-4o, etc.)

# Anthropic (Claude)

# Cohere, etc.

# HF does NOT host these weights.

# Instead:

# HF sends your request → OpenAI / Anthropic

# Response comes back → HF → you

# 👉 You still need:

# OpenAI API key

# Anthropic API key

# HF is just a single interface.

# 🧠 3. HF-hosted closed models (paid, but not OpenAI)

# HF sometimes hosts:

# Optimized versions of models

# Enterprise endpoints

# These need HF tokens, not OpenAI keys.

# 2️⃣ How this looks in practice
# Example: Using OpenAI via Hugging Face
# from huggingface_hub import InferenceClient

# client = InferenceClient(
#     provider="openai",
#     api_key="OPENAI_API_KEY"
# )

# client.text_generation(
#     model="gpt-4o-mini",
#     prompt="Hello"
# )


# Key point:

# HF doesn’t replace OpenAI

# It just normalizes the API
