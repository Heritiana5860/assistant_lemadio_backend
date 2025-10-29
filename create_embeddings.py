# """
# Script pour créer les embeddings de la documentation ADES
# et les stocker dans FAISS pour la recherche sémantique
# """

# from sentence_transformers import SentenceTransformer
# import faiss
# import pickle
# import numpy as np
# import os

# # ============== CONFIGURATION ==============

# # Chemin vers la documentation
# # DOC_PATH = 'docs/ADES_DOCUMENTATION.md'
# DOC_PATH = 'docs/Creation_vente.md'

# # Dossier de sortie pour les fichiers générés
# OUTPUT_DIR = 'rag/data'

# # Modèle d'embedding (multilangue, bon pour français/malagasy)
# EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

# # Taille des chunks (en caractères approximatif)
# CHUNK_SIZE = 500

# # ============== FONCTIONS ==============

# def load_documentation(file_path):
#     """
#     Charge la documentation depuis le fichier Markdown
#     """
#     print(f"📖 Chargement de la documentation depuis {file_path}...")
    
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             content = f.read()
#         print(f"✅ Documentation chargée ({len(content)} caractères)")
#         return content
#     except FileNotFoundError:
#         print(f"❌ Erreur : Fichier {file_path} introuvable")
#         return None
#     except Exception as e:
#         print(f"❌ Erreur lors du chargement : {e}")
#         return None

# def split_into_chunks(text, chunk_size=500):
#     """
#     Découpe le texte en chunks intelligents
    
#     Stratégie :
#     1. D'abord par sections (## ou ###)
#     2. Puis par paragraphes si trop grand
#     3. Garde un peu de contexte entre chunks
#     """
#     print(f"✂️  Découpage en chunks de ~{chunk_size} caractères...")
    
#     chunks = []
    
#     # Séparer par les titres de sections
#     sections = text.split('\n## ')
    
#     for i, section in enumerate(sections):
#         if i > 0:  # Rajouter ## sauf pour le premier
#             section = '## ' + section
        
#         # Si la section est trop grande, la découper par paragraphes
#         if len(section) > chunk_size * 2:
#             paragraphs = section.split('\n\n')
#             current_chunk = ""
            
#             for para in paragraphs:
#                 # Si ajouter ce paragraphe dépasse la limite
#                 if len(current_chunk) + len(para) > chunk_size and current_chunk:
#                     chunks.append(current_chunk.strip())
#                     # Garder un peu de contexte (overlap)
#                     current_chunk = para
#                 else:
#                     current_chunk += "\n\n" + para if current_chunk else para
            
#             # Ajouter le dernier chunk
#             if current_chunk:
#                 chunks.append(current_chunk.strip())
#         else:
#             # La section est assez petite, on la garde entière
#             if section.strip():
#                 chunks.append(section.strip())
    
#     # Filtrer les chunks trop petits (moins de 50 caractères)
#     chunks = [c for c in chunks if len(c) > 50]
    
#     print(f"✅ {len(chunks)} chunks créés")
    
#     # Afficher quelques exemples
#     print("\n📝 Exemples de chunks créés :")
#     for i, chunk in enumerate(chunks[:3]):
#         preview = chunk[:100].replace('\n', ' ')
#         print(f"  Chunk {i+1}: {preview}...")
    
#     return chunks

# def create_embeddings(chunks, model_name):
#     """
#     Crée les embeddings pour chaque chunk
#     """
#     print(f"\n🤖 Chargement du modèle d'embedding : {model_name}...")
    
#     try:
#         model = SentenceTransformer(model_name)
#         print(f"✅ Modèle chargé")
#     except Exception as e:
#         print(f"❌ Erreur lors du chargement du modèle : {e}")
#         return None, None
    
#     print(f"🔢 Création des embeddings pour {len(chunks)} chunks...")
#     print("⏳ Cela peut prendre 1-2 minutes...")
    
#     try:
#         # Encoder tous les chunks en une fois
#         embeddings = model.encode(chunks, show_progress_bar=True)
        
#         print(f"✅ Embeddings créés : {embeddings.shape}")
#         print(f"   - Nombre de chunks : {embeddings.shape[0]}")
#         print(f"   - Dimension des vecteurs : {embeddings.shape[1]}")
        
#         return embeddings, model
#     except Exception as e:
#         print(f"❌ Erreur lors de la création des embeddings : {e}")
#         return None, None

# def create_faiss_index(embeddings):
#     """
#     Crée un index FAISS pour la recherche rapide
#     """
#     print(f"\n🗄️  Création de l'index FAISS...")
    
#     try:
#         # Dimension des vecteurs
#         dimension = embeddings.shape[1]
        
#         # Créer un index simple (L2 distance)
#         index = faiss.IndexFlatL2(dimension)
        
#         # Ajouter les embeddings à l'index
#         index.add(embeddings.astype('float32'))
        
#         print(f"✅ Index FAISS créé avec {index.ntotal} vecteurs")
        
#         return index
#     except Exception as e:
#         print(f"❌ Erreur lors de la création de l'index : {e}")
#         return None

# def save_artifacts(index, chunks, output_dir):
#     """
#     Sauvegarde l'index FAISS et les chunks
#     """
#     print(f"\n💾 Sauvegarde des fichiers dans {output_dir}...")
    
#     # Créer le dossier s'il n'existe pas
#     os.makedirs(output_dir, exist_ok=True)
    
#     try:
#         # Sauvegarder l'index FAISS
#         index_path = os.path.join(output_dir, 'faiss_index.index')
#         faiss.write_index(index, index_path)
#         print(f"✅ Index FAISS sauvegardé : {index_path}")
        
#         # Sauvegarder les chunks
#         chunks_path = os.path.join(output_dir, 'chunks.pkl')
#         with open(chunks_path, 'wb') as f:
#             pickle.dump(chunks, f)
#         print(f"✅ Chunks sauvegardés : {chunks_path}")
        
#         # Sauvegarder les métadonnées
#         metadata = {
#             'num_chunks': len(chunks),
#             'embedding_model': EMBEDDING_MODEL,
#             'chunk_size': CHUNK_SIZE,
#             'dimension': index.d
#         }
        
#         metadata_path = os.path.join(output_dir, 'metadata.pkl')
#         with open(metadata_path, 'wb') as f:
#             pickle.dump(metadata, f)
#         print(f"✅ Métadonnées sauvegardées : {metadata_path}")
        
#         return True
#     except Exception as e:
#         print(f"❌ Erreur lors de la sauvegarde : {e}")
#         return False

# def test_search(index, chunks, model, test_query="Comment créer une vente?"):
#     """
#     Teste la recherche avec une question exemple
#     """
#     print(f"\n🔍 Test de recherche avec : '{test_query}'")
    
#     try:
#         # Encoder la question
#         query_embedding = model.encode([test_query])
        
#         # Rechercher les 3 chunks les plus similaires
#         distances, indices = index.search(query_embedding.astype('float32'), 3)
        
#         print(f"\n📊 Résultats de la recherche :")
#         for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
#             print(f"\n  Résultat {i+1} (distance: {dist:.4f}):")
#             chunk_preview = chunks[idx][:200].replace('\n', ' ')
#             print(f"  {chunk_preview}...")
        
#         return True
#     except Exception as e:
#         print(f"❌ Erreur lors du test : {e}")
#         return False

# # ============== MAIN ==============

# def main():
#     """
#     Fonction principale
#     """
#     print("=" * 60)
#     print("🚀 CRÉATION DES EMBEDDINGS POUR ADES CHATBOT")
#     print("=" * 60)
    
#     # 1. Charger la documentation
#     documentation = load_documentation(DOC_PATH)
#     if documentation is None:
#         return
    
#     # 2. Découper en chunks
#     chunks = split_into_chunks(documentation, CHUNK_SIZE)
#     if not chunks:
#         print("❌ Aucun chunk créé")
#         return
    
#     # 3. Créer les embeddings
#     embeddings, model = create_embeddings(chunks, EMBEDDING_MODEL)
#     if embeddings is None:
#         return
    
#     # 4. Créer l'index FAISS
#     index = create_faiss_index(embeddings)
#     if index is None:
#         return
    
#     # 5. Sauvegarder
#     success = save_artifacts(index, chunks, OUTPUT_DIR)
#     if not success:
#         return
    
#     # 6. Tester
#     test_search(index, chunks, model)
    
#     print("\n" + "=" * 60)
#     print("✅ TERMINÉ AVEC SUCCÈS !")
#     print("=" * 60)
#     print(f"\n📁 Fichiers créés dans {OUTPUT_DIR}/")
#     print("  - faiss_index.index (index de recherche)")
#     print("  - chunks.pkl (morceaux de documentation)")
#     print("  - metadata.pkl (informations)")
#     print("\n🎉 Vous pouvez maintenant passer à l'intégration dans app.py")

# if __name__ == "__main__":
#     main()

"""
Script pour créer les embeddings de la documentation ADES
et les stocker dans FAISS pour la recherche sémantique.

Améliorations RAG :
1. Traite un dossier complet de fichiers Markdown.
2. Ajoute la source (nom du fichier) à chaque chunk.
3. Implémente la rétention d'en-tête : chaque chunk garde en mémoire
   ses titres H1 et H2 parents pour un contexte accru (Header Retention).
"""

from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np
import os
import re
from glob import glob

# ============== CONFIGURATION ==============

# Dossier contenant tous les fichiers Markdown
DOCS_DIR = 'docs' 

# Dossier de sortie pour les fichiers générés
OUTPUT_DIR = 'rag/data'

# Modèle d'embedding (multilangue, bon pour français/malagasy)
# 'all-MiniLM-L6-v2' est excellent pour la vitesse et la qualité
EMBEDDING_MODEL = 'all-MiniLM-L6-v2' 

# Taille maximale souhaitée des chunks (en caractères)
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# ============== FONCTIONS ==============

def process_markdown_file(file_path, chunk_size=800):
    """
    Charge, découpe et enrichit le contenu d'un seul fichier Markdown.
    Chaque chunk est un dictionnaire avec le texte et sa source.
    """
    file_name = os.path.basename(file_path)
    print(f"  📖 Traitement de {file_name}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ Erreur lors du chargement de {file_name}: {e}")
        return []

    processed_chunks = []
    
    # Séparer par H2 (##) pour commencer les sections logiques
    sections = content.split('\n## ')
    
    # Le premier élément est souvent l'introduction (H1)
    current_h1 = ""
    if sections[0].strip().startswith('# '):
        match = re.search(r'#\s*(.+)', sections[0])
        if match:
            current_h1 = match.group(1).strip()
        
    for i, section_content in enumerate(sections):
        if i > 0: 
            # Si ce n'est pas le premier bloc, on rajoute le ## pour le titre
            section_content = '## ' + section_content

        # Extrait l'H2 de la section ou réutilise le dernier H1
        current_h2 = ""
        h2_match = re.search(r'##\s*(.+)', section_content)
        if h2_match:
            current_h2 = h2_match.group(1).strip()
        
        
        # On découpe ensuite cette section par paragraphes (double saut de ligne)
        paragraphs = section_content.split('\n\n')
        current_chunk_text = ""
        
        # Le préfixe de contexte (pour Header Retention)
        context_prefix = f"Source: {file_name} | {current_h1}"
        if current_h2:
            context_prefix += f" | {current_h2}: "
        else:
            context_prefix += ": " # Si c'est l'intro ou un bloc sans H2/H3

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Si ajouter ce paragraphe dépasse la limite, on finalise le chunk précédent
            if len(current_chunk_text) + len(para) > chunk_size and current_chunk_text:
                # Ajout du chunk avec son contexte
                processed_chunks.append({
                    'text': context_prefix + current_chunk_text.strip(),
                    'source': file_name
                })
                # Le nouveau chunk commence avec ce paragraphe
                current_chunk_text = para
            else:
                # Sinon, on continue d'ajouter au chunk courant
                current_chunk_text += "\n\n" + para if current_chunk_text else para
        
        # Ajouter le dernier chunk de la section
        if current_chunk_text:
            processed_chunks.append({
                'text': context_prefix + current_chunk_text.strip(),
                'source': file_name
            })
            
    return processed_chunks

def load_and_split_all_docs(docs_dir, chunk_size=800):
    """
    Charge et découpe tous les documents Markdown du dossier spécifié.
    """
    all_chunks = []
    
    print(f"✂️  Découpage des documents dans le dossier '{docs_dir}'...")
    
    # Utiliser glob pour trouver tous les fichiers .md
    markdown_files = glob(os.path.join(docs_dir, '*.md'))
    
    if not markdown_files:
        print(f"❌ Aucun fichier Markdown (.md) trouvé dans {docs_dir}. Vérifiez le chemin.")
        return []

    for file_path in markdown_files:
        chunks_from_file = process_markdown_file(file_path, chunk_size)
        all_chunks.extend(chunks_from_file)

    # Filtrer les chunks trop petits (moins de 50 caractères)
    all_chunks = [c for c in all_chunks if len(c['text']) > 50]

    print(f"✅ {len(all_chunks)} chunks totaux créés à partir de {len(markdown_files)} fichiers.")
    
    # Afficher quelques exemples
    print("\n📝 Exemples de chunks créés (avec rétention d'en-tête) :")
    for i, chunk in enumerate(all_chunks[:3]):
        preview = chunk['text'][:150].replace('\n', ' ')
        print(f"  Chunk {i+1} (Source: {chunk['source']}): {preview}...")
    
    return all_chunks

def create_embeddings(chunks, model_name):
    """
    Crée les embeddings pour chaque chunk
    """
    print(f"\n🤖 Chargement du modèle d'embedding : {model_name}...")
    
    try:
        model = SentenceTransformer(model_name)
        print(f"✅ Modèle chargé")
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle : {e}")
        return None, None
    
    texts_to_embed = [c['text'] for c in chunks]
    
    print(f"🔢 Création des embeddings pour {len(texts_to_embed)} chunks...")
    print("⏳ Cela peut prendre quelques instants...")
    
    try:
        # Encoder tous les chunks en une fois
        embeddings = model.encode(texts_to_embed, show_progress_bar=True)
        
        print(f"✅ Embeddings créés : {embeddings.shape}")
        return embeddings, model
    except Exception as e:
        print(f"❌ Erreur lors de la création des embeddings : {e}")
        return None, None

def create_faiss_index(embeddings):
    """
    Crée un index FAISS pour la recherche rapide
    """
    print(f"\n🗄️  Création de l'index FAISS...")
    
    try:
        # Dimension des vecteurs
        dimension = embeddings.shape[1]
        
        # Créer un index simple (L2 distance)
        index = faiss.IndexFlatL2(dimension)
        
        # Ajouter les embeddings à l'index
        index.add(embeddings.astype('float32'))
        
        print(f"✅ Index FAISS créé avec {index.ntotal} vecteurs")
        return index
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'index : {e}")
        return None

def save_artifacts(index, chunks, output_dir):
    """
    Sauvegarde l'index FAISS et les chunks
    """
    print(f"\n💾 Sauvegarde des fichiers dans {output_dir}...")
    
    # Créer le dossier s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Sauvegarder l'index FAISS
        index_path = os.path.join(output_dir, 'faiss_index.index')
        faiss.write_index(index, index_path)
        print(f"✅ Index FAISS sauvegardé : {index_path}")
        
        # Sauvegarder les chunks (qui incluent la source et le texte)
        chunks_path = os.path.join(output_dir, 'chunks.pkl')
        with open(chunks_path, 'wb') as f:
            pickle.dump(chunks, f)
        print(f"✅ Chunks et Métadonnées sauvegardés : {chunks_path}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")
        return False

def test_search(index, chunks, model, test_query="Qui me donne mon mot de passe et mon identifiant ?"):
    """
    Teste la recherche avec une question exemple
    """
    print(f"\n🔍 Test de recherche avec : '{test_query}'")
    
    try:
        # Encoder la question
        query_embedding = model.encode([test_query])
        
        # Rechercher les 3 chunks les plus similaires
        distances, indices = index.search(query_embedding.astype('float32'), 3)
        
        print(f"\n📊 Résultats de la recherche (3 meilleurs chunks) :")
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            print(f"\n  Résultat {i+1} (distance: {dist:.4f}):")
            chunk_preview = chunks[idx]['text'].replace('\n', ' ')
            print(f"  Source: {chunks[idx]['source']}")
            print(f"  Contenu : {chunk_preview[:200]}...")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        return False
    
def smart_chunk_with_overlap(text, chunk_size=800, overlap=150):
    """Découpe avec chevauchement et respect des phrases"""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
                # Overlap : garder les derniers X caractères
                current_chunk = current_chunk[-overlap:] + sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def extract_hierarchy(section_content):
    """Extrait TOUS les niveaux de titres (H1->H6)"""
    headers = {
        'h1': re.search(r'^#\s+(.+)$', section_content, re.MULTILINE),
        'h2': re.search(r'^##\s+(.+)$', section_content, re.MULTILINE),
        'h3': re.search(r'^###\s+(.+)$', section_content, re.MULTILINE)
    }
    
    hierarchy = " > ".join([
        h.group(1) for h in [headers['h1'], headers['h2'], headers['h3']] 
        if h
    ])
    
    return hierarchy

# ============== MAIN ==============

def main():
    """
    Fonction principale
    """
    print("=" * 60)
    print("🚀 CRÉATION DE LA BASE DE VECTEURS POUR ADES CHATBOT")
    print("=" * 60)
    
    # 1. Charger et découper en chunks (avec source et en-tête)
    chunks_with_metadata = load_and_split_all_docs(DOCS_DIR, CHUNK_SIZE)
    if not chunks_with_metadata:
        return
    
    # 2. Créer les embeddings
    embeddings, model = create_embeddings(chunks_with_metadata, EMBEDDING_MODEL)
    if embeddings is None:
        return
    
    # 3. Créer l'index FAISS
    index = create_faiss_index(embeddings)
    if index is None:
        return
    
    # 4. Sauvegarder
    success = save_artifacts(index, chunks_with_metadata, OUTPUT_DIR)
    if not success:
        return
    
    # 5. Tester
    # Nécessite un modèle chargé, donc appel dans le main
    test_search(index, chunks_with_metadata, model)
    
    print("\n" + "=" * 60)
    print("✅ TERMINÉ AVEC SUCCÈS ! Votre base de vecteurs est optimisée.")
    print("=" * 60)

if __name__ == "__main__":
    main()