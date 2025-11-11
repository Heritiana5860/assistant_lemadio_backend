# rag_loader.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os

def initialize_rag_components(data_dir='rag/data', model_name='all-MiniLM-L6-v2'):
    """
    Initialise les embeddings et le VectorStore (FAISS) via LangChain.
    """
    try:
        # 1. Initialisation du modèle d'embeddings
        embeddings = SentenceTransformerEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'} # ou 'cuda' si disponible
        )

        # 2. Chargement du VectorStore FAISS (doit exister)
        index_path = os.path.join(data_dir, 'faiss_index')
        if not os.path.exists(index_path):
             raise FileNotFoundError(f"Dossier FAISS introuvable: {index_path}")
        
        # Le chargement FAISS dans LangChain nécessite le dossier complet
        # Assurez-vous d'avoir exporté FAISS au format LangChain (index.faiss et index.pkl)
        vectorstore = FAISS.load_local(
            folder_path=data_dir, 
            embeddings=embeddings, 
            index_name='faiss_index'
        )
        
        return vectorstore.as_retriever(), True
    
    except Exception as e:
        print(f"❌ Erreur lors du chargement du RAG (LangChain): {e}")
        return None, False