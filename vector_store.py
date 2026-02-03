from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_documents(docs)

def build_vectorstore(chunks):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return FAISS.from_documents(chunks, embeddings)
