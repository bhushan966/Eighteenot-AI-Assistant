import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

VECTOR_STORE_PATH = "data/kohli_vectorstore"
DOCUMENT_PATH = "data/kohli_document.txt"

def load_document():
    print("📄 Loading Kohli document...")
    with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    print(f"   ✅ Loaded {len(text):,} characters")
    return text

def split_document(text):
    print("\n✂️  Splitting document into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " "],
    )
    chunks = splitter.create_documents([text])
    print(f"   ✅ Created {len(chunks)} chunks")
    return chunks

def create_vector_store(chunks):

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://host.docker.internal:11434"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

def save_vector_store(vectorstore):
    os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
    vectorstore.save_local(VECTOR_STORE_PATH)

def load_vector_store():
    """Load existing vector store — used by chatbot.py"""
    print("📂 Loading existing vector store...")
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://host.docker.internal:11434"
    )
    vectorstore = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )
    print("   ✅ Vector store loaded successfully")
    return vectorstore

def build_vector_store():
    """Full pipeline — run this once to build the vector store"""
    text = load_document()
    chunks = split_document(text)
    vectorstore = create_vector_store(chunks)
    save_vector_store(vectorstore)
    print("\n✅ Vector store build complete!")
    print(f"   📁 Saved to: {VECTOR_STORE_PATH}")
    return vectorstore

if __name__ == "__main__":
    build_vector_store()