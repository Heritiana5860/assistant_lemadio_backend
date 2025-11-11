# rag_builder.py
"""
Script pour créer les embeddings de la documentation ADES
et les stocker dans FAISS pour la recherche sémantique.
... (Le code complet du builder que vous avez partagé) ...
"""

from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np
import os
import re
from glob import glob
# Ajoutez ces imports en haut de rag_builder.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document

from langchain_community.document_loaders import UnstructuredWordDocumentLoader

# ============== CONFIGURATION ==============

# Dossier contenant tous les fichiers Markdown
DOCS_DIR = 'docs' 

# Dossier de sortie pour les fichiers générés
OUTPUT_DIR = 'rag/data'

# Modèle d'embedding (multilangue, bon pour français/malagasy)
EMBEDDING_MODEL = 'all-MiniLM-L6-v2' 

# Taille maximale souhaitée des chunks (en caractères)
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200

# ============== FONCTIONS ==============

def extract_process_sections(content):
    """
    Découpe le document en sections de processus cohérentes
    Garde les étapes ensemble !
    """
    sections = []
    
    # Diviser par les grands titres (##)
    main_sections = re.split(r'\n## ', content)
    
    for i, section in enumerate(main_sections):
        if i > 0:
            section = '## ' + section
        
        has_steps = bool(re.search(r'(Étape \d|Schéma du Flux|###)', section))
        
        if has_steps:
            sections.extend(chunk_process_section(section))
        else:
            sections.extend(chunk_normal_section(section))
    
    return sections

def chunk_process_section(section):
    """
    Découpe une section de processus en préservant l'intégrité des étapes
    """
    chunks = []
    
    # Extraire le titre principal
    title_match = re.match(r'##\s+(.+?)(\n|$)', section)
    main_title = title_match.group(1) if title_match else "Processus"
    
    # Diviser par étapes (Étape 1, Étape 2, etc.)
    step_pattern = r'(### Étape \d+[^\n]*\n)'
    steps = re.split(step_pattern, section)
    
    if len(steps) <= 2:
        # Pas d'étapes numérotées, découpage normal
        return chunk_normal_section(section)
    
    # Reconstituer les étapes
    current_chunk = steps[0]  # Introduction
    
    for i in range(1, len(steps), 2):
        if i+1 < len(steps):
            step_title = steps[i]
            step_content = steps[i+1]
            full_step = step_title + step_content
            
            # Si ajouter cette étape dépasse la limite
            if len(current_chunk) + len(full_step) > CHUNK_SIZE:
                if current_chunk.strip():
                    chunks.append({
                        'text': f"Source: [Document] | {main_title}\n\n{current_chunk.strip()}",
                        'source': 'processus',
                        'type': 'étapes'
                    })
                
                # Nouveau chunk commence avec contexte
                intro = steps[0][:300] if len(steps[0]) > 300 else steps[0]
                current_chunk = f"{intro}\n\n{full_step}"
            else:
                current_chunk += "\n\n" + full_step
    
    # Ajouter le dernier chunk
    if current_chunk.strip():
        chunks.append({
            'text': f"Source: [Document] | {main_title}\n\n{current_chunk.strip()}",
            'source': 'processus',
            'type': 'étapes'
        })
    
    return chunks

def chunk_normal_section(section, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Découpage normal pour sections informatives
    """
    chunks = []
    
    # Extraire le titre
    title_match = re.match(r'##\s+(.+?)(\n|$)', section)
    title = title_match.group(1) if title_match else "Section"
    
    # Découper par paragraphes
    paragraphs = section.split('\n\n')
    current = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        if len(current) + len(para) > chunk_size and current:
            chunks.append({
                'text': f"Source: [Document] | {title}\n\n{current.strip()}",
                'source': 'info',
                'type': 'général'
            })
            
            # Overlap : garder la fin
            words = current.split()
            overlap_words = words[-overlap//5:] if len(words) > overlap//5 else []
            current = ' '.join(overlap_words) + "\n\n" + para
        else:
            current += "\n\n" + para if current else para
    
    if current.strip():
        chunks.append({
            'text': f"Source: [Document] | {title}\n\n{current.strip()}",
            'source': 'info',
            'type': 'général'
        })
    
    return chunks

def process_doc_file_smart(file_path):
    """
    Charge le contenu du fichier Word, puis le découpe intelligemment.
    """
    try:
        # Utiliser LangChain pour charger le contenu du fichier Word
        loader = UnstructuredWordDocumentLoader(file_path)
        documents = loader.load()
        
        if not documents:
            print(f"⚠️ Aucun contenu trouvé dans {file_path}.")
            return []
            
        # documents[0].page_content contient le texte extrait
        content = documents[0].page_content
        
        # Le contenu extrait par UnstructuredWordDocumentLoader est du texte brut.
        # Vos fonctions de découpage utilisent des expressions régulières basées
        # sur la syntaxe Markdown (##, ###, etc.).
        # 
        # Si vous avez conservé la syntaxe Markdown DANS le fichier Word,
        # vous pouvez continuer. Sinon, vous DEVEZ adapter votre logique de
        # découpage (extract_process_sections) pour utiliser une méthode différente.
        
        # --- Simuler l'étape de nettoyage Markdown si les titres ont été conservés ---
        # Si vos titres H2/H3 étaient en gras ou en taille différente et sont
        # maintenant en texte brut dans l'extraction, la REGEX ne fonctionnera pas.
        # ASSUMONS que l'outil a converti les titres Word en syntaxe Markdown pour la démo.
        
        # Simuler le retrait du titre H1 (si présent)
        content = re.sub(r'^#\s+.*?\n', '', content, 1, re.MULTILINE).strip()
        
        # Découper en sections (en utilisant la logique Markdown existante)
        all_chunks = extract_process_sections(content)
        
        # Ajouter le nom du fichier comme source
        file_name = os.path.basename(file_path)
        for chunk in all_chunks:
            # Remplacer la source placeholder
            chunk['text'] = chunk['text'].replace('[Document]', file_name.replace(os.path.splitext(file_name)[1], ''))
            chunk['file'] = file_name
            
        return all_chunks
        
    except Exception as e:
        print(f"❌ Erreur lors du traitement de {file_path}: {e}")
        return []

def save_faiss_index(chunks, output_dir=OUTPUT_DIR):
    """
    Crée les embeddings, l'index FAISS, et sauvegarde les chunks.
    """
    if not chunks:
        print("⚠️  Aucun chunk à traiter. Index non créé.")
        return

    # Extraire le texte pour l'embedding
    texts = [c['text'] for c in chunks]
    
    print(f"📦 Création des {len(texts)} embeddings...")
    # Le modèle peut nécessiter un certain temps pour se charger la première fois
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Créer les embeddings
    embeddings_matrix = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    d = embeddings_matrix.shape[1] # Dimension des vecteurs

    # Créer l'index FAISS
    print(f"💾 Création et sauvegarde de l'index FAISS (Dim: {d})...")
    index = faiss.IndexFlatL2(d) 
    index.add(embeddings_matrix.astype('float32')) 

    # --- Sauvegarde pour LangChain/RAG ---
    
    # 1. Sauvegarde des chunks (pour la récupération du texte)
    chunks_path = os.path.join(output_dir, 'chunks.pkl')
    with open(chunks_path, 'wb') as f:
        pickle.dump(chunks, f)
        
    # 2. Sauvegarde de l'index FAISS et des métadonnées LangChain
    # Pour que LangChain puisse charger un index qui n'est pas créé par lui-même,
    # on va utiliser la structure de dossier
    index_name = "faiss_index"
    index_folder = os.path.join(output_dir, index_name)
    os.makedirs(index_folder, exist_ok=True)
    
    faiss.write_index(index, os.path.join(index_folder, 'index.faiss'))
    
    # Pour que FAISS.load_local fonctionne correctement, il faut aussi sauvegarder 
    # les chunks (qui agissent comme le `docstore` et les métadonnées)
    # L'approche la plus simple est de créer un FAISS LangChain après la construction
    
    print(f"✅ Index FAISS créé avec succès dans {index_folder}/")
    print(f"   {len(chunks)} chunks de documentation traités.")
    
    
def save_faiss_index(chunks, output_dir=OUTPUT_DIR):
    """
    Crée les embeddings, l'index FAISS via l'API LangChain, et le sauvegarde correctement.
    """
    if not chunks:
        print("⚠️  Aucun chunk à traiter. Index non créé.")
        return

    # Convertir les chunks en objets Document LangChain (requis par from_documents)
    # L'ancienne structure de votre chunk est : {'text': ..., 'file': ...}
    documents = [
        Document(page_content=c['text'], metadata={"source": c['file']}) 
        for c in chunks
    ]

    print(f"📦 Création des {len(documents)} embeddings (via LangChain API)...")
    
    # Initialiser les embeddings (en utilisant l'API LangChain)
    embeddings = SentenceTransformerEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"}
    )
    
    # Créer le VectorStore FAISS à partir des documents
    vectorstore = FAISS.from_documents(documents, embeddings)

    # --- Sauvegarde ---
    index_name = "faiss_index"
    
    # LangChain FAISS.save_local crée les fichiers index.faiss et index.pkl
    # directement dans le dossier spécifié.
    vectorstore.save_local(
        folder_path=output_dir,
        index_name=index_name
    )

    print(f"✅ Index FAISS créé avec succès dans {output_dir} ({index_name}.faiss & {index_name}.pkl)")
    print(f"   {len(chunks)} chunks de documentation traités.")


# ============== MAIN EXECUTION ==============

if __name__ == "__main__":
    if not os.path.exists(DOCS_DIR):
        print(f"❌ Erreur: Le dossier de documentation '{DOCS_DIR}' est introuvable.")
        print("Créez un dossier 'docs' et placez-y vos fichiers .doc/.docx.")
    else:
        # Assurer que le dossier de sortie existe
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        word_files_doc = glob(os.path.join(DOCS_DIR, '*.doc'))
        word_files_docx = glob(os.path.join(DOCS_DIR, '*.docx'))
        all_word_files = word_files_doc + word_files_docx
        
        if not all_word_files:
            print(f"⚠️ Aucun fichier Word (*.doc, *.docx) trouvé dans le dossier '{DOCS_DIR}'.")
        else:
            print("=" * 60)
            print(f"🏗️ Démarrage de la construction RAG (à partir de {len(all_word_files)} fichiers Word)...")
            all_chunks = []
            
            for file_path in all_word_files: # Utiliser la nouvelle liste
                print(f"   -> Traitement de {os.path.basename(file_path)}...")
                # Appeler la nouvelle fonction de traitement
                file_chunks = process_doc_file_smart(file_path) 
                all_chunks.extend(file_chunks)
            
            # Sauvegarder
            save_faiss_index(all_chunks, OUTPUT_DIR)
            
            print("=" * 60)
            print("✅ Construction RAG terminée. L'index FAISS est prêt.")