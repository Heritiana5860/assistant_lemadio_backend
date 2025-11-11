# rag_loader.py
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings

def initialize_rag_components(data_dir="rag/data", model_name="all-MiniLM-L6-v2"):
    """
    Initialise le système RAG : embeddings + VectorStore FAISS.
    """
    try:
        embeddings = SentenceTransformerEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"}  # change en 'cuda' si tu as un GPU
        )
        
        index_name = "faiss_index"

        index_file_path = os.path.join(data_dir, f"{index_name}.faiss")
        if not os.path.exists(index_file_path):
            # Le message d'erreur est plus pertinent
            raise FileNotFoundError(f"Index FAISS principal introuvable : {index_file_path}. Veuillez lancer rag_builder.py.")

        vectorstore = FAISS.load_local(
            folder_path=data_dir,
            embeddings=embeddings,
            index_name=index_name,
            allow_dangerous_deserialization=True  # ⚠️ requis avec les nouvelles versions
        )

        return vectorstore.as_retriever(), True

    except Exception as e:
        print(f"❌ Erreur lors du chargement RAG : {e}")
        return None, False
