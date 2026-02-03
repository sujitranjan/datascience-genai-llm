

import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
#from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()
# -----------------------------
# CONFIG
# -----------------------------
PDF_DIR = "docs"  # folder containing PDFs
PERSIST_DIR = "vector_store/chroma_db"

# -----------------------------
# EMBEDDINGS
# -----------------------------
# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/embedding-001"
# )




embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    api_key="AIzaSyCm5bpeQwg8ZZrUQvVDdg-tzHpNSvPuvMQ"
    #api_key=os.environ["GOOGLE_API_KEY"]
)

# ******

# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# -----------------------------
# LOAD PDFs
# -----------------------------
documents = []

for file in os.listdir(PDF_DIR):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(PDF_DIR, file)
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        documents.extend(docs)

print(f"Loaded {len(documents)} pages from PDFs")

# -----------------------------
# CHUNKING
# -----------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks")

# ------------------------.txt-----
# VECTOR STORE
# -----------------------------
vectorstore = Chroma(
    collection_name="internal_docs",
    persist_directory=PERSIST_DIR,
    embedding_function=embeddings
)

vectorstore.add_documents(chunks)
vectorstore.persist()

print("✅ PDFs embedded and stored successfully")


# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings

# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# db = Chroma(
#     persist_directory="vector_store/chroma_db",
#     embedding_function=embeddings
# )

# docs = db.similarity_search("company policy", k=2)

# for d in docs:
#     print(d.page_content[:200])

