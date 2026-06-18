

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langsmith import traceable
import warnings
warnings.filterwarnings("ignore")
load_dotenv()



# ─────────────────────────────────────────────
# LANGSMITH TRACING SETUP
# ─────────────────────────────────────────────
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "kohlibot")

VECTOR_STORE_PATH = "data/kohli_vectorstore"

# ─────────────────────────────────────────────
# CUSTOM PROMPT
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are Eighteenot 🏏 — an expert AI assistant dedicated exclusively to Virat Kohli, 
one of the greatest cricketers of all time.

Your knowledge includes:
- Complete career statistics (ODI, Test, T20I, IPL)
- All centuries with full details (runs, balls, fours, sixes, venue, opponent, date)
- Records and milestones
- Personal life and biography
- Captaincy record
- ICC World Cup and tournament performances
- Head to head stats against different teams

RULES:
1. Only answer questions related to Virat Kohli and cricket.
2. If someone asks about another cricketer, politely redirect to Virat Kohli.
3. If you don't find the answer in the context, say "I don't have that specific detail, but I can tell you what I know about Virat Kohli."
4. Always be enthusiastic and passionate about Virat Kohli.
5. Use cricket emojis occasionally to make responses fun 🏏🎯🔥
6. When giving stats, be precise and cite the format (ODI/Test/T20I).

Use the following context to answer the question:
{context}

Chat History:
{chat_history}
"""

HUMAN_PROMPT = """Question: {question}

Answer:"""

def build_prompt():
    system_message = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["context", "chat_history"],
            template=SYSTEM_PROMPT,
        )
    )
    human_message = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["question"],
            template=HUMAN_PROMPT,
        )
    )
    return ChatPromptTemplate.from_messages([system_message, human_message])

# ─────────────────────────────────────────────
# LOAD VECTOR STORE
# ─────────────────────────────────────────────
def load_vector_store():
    embeddings = OllamaEmbeddings(
        model ="nomic-embed-text",
    )
    vectorstore = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )
    return vectorstore

# ─────────────────────────────────────────────
# BUILD RAG CHAIN
# ─────────────────────────────────────────────
def build_chain(vectorstore):

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.5,
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 8},
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": build_prompt()},
        verbose=False,
    )

    return chain

# ─────────────────────────────────────────────
# ASK QUESTION (traced by LangSmith)
# ─────────────────────────────────────────────
@traceable(name="kohlibot-query")
def ask(chain, question: str) -> str:
    result = chain.invoke({"question": question})
    answer = result.get("answer", "I don't know.")
    # sources = result.get("source_documents", [])

    return answer

# ─────────────────────────────────────────────
# INITIALIZE KOHLIBOT
# ─────────────────────────────────────────────
def initialize_Eighteenot():
    vectorstore = load_vector_store()
    chain = build_chain(vectorstore)
    return chain

if __name__ == "__main__":
    # print("\n🏏 Initializing KohliBot...\n")
    chain = initialize_Eighteenot()

    print("\n🏏 Eighteenot is ready! Ask anything about Virat Kohli.")
    print("   Type 'quit' to exit\n")
    print("─" * 50)

    while True:
        question = input("\nYou: ").strip()
        if not question:
            continue
        if question.lower() in ["quit", "exit", "bye"]:
            print("Eighteenot: Thanks for chatting! Jai Hind! 🇮🇳🏏")
            break

        answer = ask(chain, question)
        print(f"Eighteenot: {answer}")
        print("─" * 50)