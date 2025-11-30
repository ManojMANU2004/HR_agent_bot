from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- add this
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# -------------------------------
# Add CORS middleware here
# -------------------------------
origins = [
    "http://localhost:8001",  # your frontend URL
    "http://127.0.0.1:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

DB_PATH = "./chroma_db"

# Load LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Load vector DB
db = Chroma(persist_directory=DB_PATH)
retriever = db.as_retriever()

# Prompt
template = """
You are an HR assistant. Answer using only the context provided.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

parser = StrOutputParser()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):

    # FIXED: correct retrieval method for new retriever API
    docs = retriever.invoke(query.question)

    # Build context string
    context = "\n".join([doc.page_content for doc in docs])

    # Prepare prompt
    final_prompt = prompt.format(
        context=context,
        question=query.question
    )

    # Generate LLM response
    output = llm.invoke(final_prompt)

    return {"answer": output.content}
