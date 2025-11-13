from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document
from glob import glob
import os
import re

DOCS_DIR = "docs"
OUTPUT_DIR = "rag/data"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def process_docx(file_path):
    loader = UnstructuredWordDocumentLoader(file_path)
    docs = loader.load()
    if not docs:
        return []
    content = docs[0].page_content
    # Nettoyage basique
    content = re.sub(r'\n{3,}', '\n\n', content)
    chunks = chunk_text(content)
    file_name = os.path.basename(file_path)
    return [Document(page_content=c, metadata={"source": file_name}) for c in chunks]

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = glob(os.path.join(DOCS_DIR, "*.docx")) + glob(os.path.join(DOCS_DIR, "*.doc"))
    
    all_docs = []
    for f in files:
        print(f"Traitement : {f}")
        all_docs.extend(process_docx(f))

    if not all_docs:
        print("Aucun document trouvé.")
        exit()

    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(all_docs, embeddings)
    vectorstore.save_local(OUTPUT_DIR, "faiss_index")
    print(f"Index FAISS sauvegardé : {len(all_docs)} chunks")