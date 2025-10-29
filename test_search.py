from sentence_transformers import SentenceTransformer
import faiss
import pickle

# Charger les ressources
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index('rag/data/faiss_index.index')

with open('rag/data/chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

# Fonction de recherche
def search(query, top_k=3):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding.astype('float32'), top_k)
    
    print(f"\n🔍 Question : {query}\n")
    for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        print(f"Résultat {i+1} (score: {dist:.2f}):")
        print(chunks[idx][:300])
        print("\n" + "-"*60 + "\n")

# Tester plusieurs questions
search("Comment créer une vente?")
search("Comment annuler une vente?")
search("Quels sont les types de réchauds?")
search("Que faire si j'ai oublié mon mot de passe?")