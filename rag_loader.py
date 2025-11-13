from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os

def initialize_rag_components(data_dir="rag/data", model_name="all-MiniLM-L6-v2"):
    try:
        embeddings = SentenceTransformerEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"}
        )
        index_path = os.path.join(data_dir, "faiss_index.faiss")
        if not os.path.exists(index_path):
            print(f"Index FAISS manquant : {index_path}")
            return None, False

        vectorstore = FAISS.load_local(
            folder_path=data_dir,
            embeddings=embeddings,
            index_name="faiss_index",
            allow_dangerous_deserialization=True
        )
        return vectorstore.as_retriever(search_kwargs={"k": 4}), True
    except Exception as e:
        print(f"Erreur RAG : {e}")
        return None, False