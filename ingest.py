import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = "chroma_db"
DOCS_DIR = "docs"

docs = []
for file in os.listdir(DOCS_DIR):
    path = os.path.join(DOCS_DIR, file)

    if file.endswith(".pdf"):
        docs.extend(PyPDFLoader(path).load())
    elif file.endswith(".txt"):
        docs.extend(TextLoader(path).load())
    elif file.endswith(".docx"):
        docs.extend(Docx2txtLoader(path).load())
    elif file.endswith(".md"):
        docs.extend(UnstructuredMarkdownLoader(path).load())
    else:
        print("❌ Skipped unsupported file:", file)

print("📄 Loaded docs:", len(docs))

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = text_splitter.split_documents(docs)
print("🧩 Generated chunks:", len(chunks))

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_documents(chunks, embeddings, persist_directory=DB_PATH)
db.persist()


print("✅ Database created successfully!")