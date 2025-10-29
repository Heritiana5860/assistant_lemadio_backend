# """
# Module de recherche RAG pour le chatbot ADES
# Permet de rechercher dans la documentation et récupérer le contexte pertinent
# """

# from sentence_transformers import SentenceTransformer
# import faiss
# import pickle
# import os

# class RAGSearcher:
#     """
#     Classe pour gérer la recherche sémantique dans la documentation ADES
#     """
    
#     def __init__(self, data_dir='rag/data', model_name='all-MiniLM-L6-v2'):
#         """
#         Initialise le RAG Searcher
        
#         Args:
#             data_dir: Dossier contenant les fichiers FAISS et chunks
#             model_name: Nom du modèle d'embeddings
#         """
#         self.data_dir = data_dir
#         self.model_name = model_name
        
#         self.model = None
#         self.index = None
#         self.chunks = None
#         self.metadata = None
        
#         print(f"🔍 Initialisation du RAG Searcher...")
#         self._load_resources()
    
#     def _load_resources(self):
#         """
#         Charge le modèle, l'index FAISS et les chunks
#         """
#         try:
#             # Chemins des fichiers
#             index_path = os.path.join(self.data_dir, 'faiss_index.index')
#             chunks_path = os.path.join(self.data_dir, 'chunks.pkl')
#             metadata_path = os.path.join(self.data_dir, 'metadata.pkl')
            
#             # Vérifier que les fichiers existent
#             if not os.path.exists(index_path):
#                 raise FileNotFoundError(f"Index FAISS introuvable : {index_path}")
#             if not os.path.exists(chunks_path):
#                 raise FileNotFoundError(f"Chunks introuvables : {chunks_path}")
            
#             # Charger le modèle d'embeddings
#             print(f"  📦 Chargement du modèle : {self.model_name}")
#             self.model = SentenceTransformer(self.model_name)
            
#             # Charger l'index FAISS
#             print(f"  🗄️  Chargement de l'index FAISS...")
#             self.index = faiss.read_index(index_path)
            
#             # Charger les chunks
#             print(f"  📄 Chargement des chunks...")
#             with open(chunks_path, 'rb') as f:
#                 self.chunks = pickle.load(f)
            
#             # Charger les métadonnées (optionnel)
#             if os.path.exists(metadata_path):
#                 with open(metadata_path, 'rb') as f:
#                     self.metadata = pickle.load(f)
            
#             print(f"✅ RAG Searcher prêt !")
#             print(f"   - {len(self.chunks)} chunks chargés")
#             print(f"   - Dimension des vecteurs : {self.index.d}")
            
#         except Exception as e:
#             print(f"❌ Erreur lors du chargement des ressources : {e}")
#             raise
    
#     def search(self, query, top_k=3, return_scores=False):
#         """
#         Recherche les chunks les plus pertinents pour une question
        
#         Args:
#             query: Question de l'utilisateur
#             top_k: Nombre de résultats à retourner
#             return_scores: Si True, retourne aussi les scores
            
#         Returns:
#             Liste des chunks pertinents (et scores si demandé)
#         """
#         try:
#             # Encoder la question
#             query_embedding = self.model.encode([query])
            
#             # Rechercher dans FAISS
#             distances, indices = self.index.search(
#                 query_embedding.astype('float32'), 
#                 top_k
#             )
            
#             # Récupérer les chunks correspondants
#             results = []
#             for dist, idx in zip(distances[0], indices[0]):
#                 chunk = self.chunks[idx]
                
#                 if return_scores:
#                     results.append({
#                         'chunk': chunk,
#                         'score': float(dist),
#                         'index': int(idx)
#                     })
#                 else:
#                     results.append(chunk)
            
#             return results
            
#         except Exception as e:
#             print(f"❌ Erreur lors de la recherche : {e}")
#             return []
    
#     def get_context(self, query, top_k=3, max_length=2000):
#         """
#         Récupère le contexte pertinent pour une question
#         Formate le contexte pour être injecté dans le prompt
        
#         Args:
#             query: Question de l'utilisateur
#             top_k: Nombre de chunks à récupérer
#             max_length: Longueur maximale du contexte (en caractères)
            
#         Returns:
#             Contexte formaté (string)
#         """
#         # Rechercher les chunks pertinents
#         chunks = self.search(query, top_k=top_k)
        
#         # Concaténer les chunks
#         context = "\n\n".join(chunks)
        
#         # Limiter la longueur si nécessaire
#         if len(context) > max_length:
#             context = context[:max_length] + "\n\n[...]"
        
#         return context
    
#     def get_detailed_results(self, query, top_k=3):
#         """
#         Retourne des résultats détaillés avec scores et métadonnées
#         Utile pour déboguer et analyser
        
#         Args:
#             query: Question de l'utilisateur
#             top_k: Nombre de résultats
            
#         Returns:
#             Liste de dictionnaires avec détails
#         """
#         results = self.search(query, top_k=top_k, return_scores=True)
        
#         detailed = []
#         for result in results:
#             detailed.append({
#                 'chunk': result['chunk'],
#                 'score': result['score'],
#                 'index': result['index'],
#                 'preview': result['chunk'][:200] + "..." if len(result['chunk']) > 200 else result['chunk']
#             })
        
#         return detailed
    
#     def health_check(self):
#         """
#         Vérifie que le RAG est fonctionnel
        
#         Returns:
#             dict avec le statut
#         """
#         try:
#             if self.model is None or self.index is None or self.chunks is None:
#                 return {
#                     'status': 'error',
#                     'message': 'Ressources non chargées'
#                 }
            
#             # Test rapide de recherche
#             test_results = self.search("test", top_k=1)
            
#             return {
#                 'status': 'ok',
#                 'num_chunks': len(self.chunks),
#                 'embedding_dim': self.index.d,
#                 'model': self.model_name,
#                 'test_search': 'ok' if test_results else 'failed'
#             }
            
#         except Exception as e:
#             return {
#                 'status': 'error',
#                 'message': str(e)
#             }


# # ============== TEST ==============

# if __name__ == "__main__":
#     """
#     Test du module
#     """
#     print("=" * 60)
#     print("TEST DU MODULE RAG SEARCH")
#     print("=" * 60)
    
#     # Initialiser
#     searcher = RAGSearcher()
    
#     # Test 1 : Recherche simple
#     print("\n📝 Test 1 : Recherche simple")
#     query = "Comment créer une vente?"
#     results = searcher.search(query, top_k=2)
#     print(f"\nQuestion : {query}")
#     for i, chunk in enumerate(results):
#         print(f"\nRésultat {i+1}:")
#         print(chunk[:200] + "...")
    
#     # Test 2 : Get context
#     print("\n📝 Test 2 : Get context")
#     context = searcher.get_context(query, top_k=2)
#     print(f"\nContexte récupéré ({len(context)} caractères):")
#     print(context[:300] + "...")
    
#     # Test 3 : Résultats détaillés
#     print("\n📝 Test 3 : Résultats détaillés")
#     detailed = searcher.get_detailed_results(query, top_k=2)
#     for i, result in enumerate(detailed):
#         print(f"\nRésultat {i+1}:")
#         print(f"  Score: {result['score']:.4f}")
#         print(f"  Preview: {result['preview']}")
    
#     # Test 4 : Health check
#     print("\n📝 Test 4 : Health check")
#     health = searcher.health_check()
#     print(f"\nStatut: {health}")
    
#     print("\n" + "=" * 60)
#     print("✅ TESTS TERMINÉS")
#     print("=" * 60)

"""
Module de recherche RAG pour le chatbot ADES
Permet de rechercher dans la documentation et récupérer le contexte pertinent
"""

from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os

class RAGSearcher:
    """
    Classe pour gérer la recherche sémantique dans la documentation ADES
    """
    
    def __init__(self, data_dir='rag/data', model_name='all-MiniLM-L6-v2'):
        """
        Initialise le RAG Searcher
        
        Args:
            data_dir: Dossier contenant les fichiers FAISS et chunks
            model_name: Nom du modèle d'embeddings
        """
        self.data_dir = data_dir
        self.model_name = model_name
        
        self.model = None
        self.index = None
        self.chunks = None
        self.metadata = None
        
        print(f"🔍 Initialisation du RAG Searcher...")
        self._load_resources()
    
    def _load_resources(self):
        """
        Charge le modèle, l'index FAISS et les chunks
        """
        try:
            # Chemins des fichiers
            index_path = os.path.join(self.data_dir, 'faiss_index.index')
            chunks_path = os.path.join(self.data_dir, 'chunks.pkl')
            metadata_path = os.path.join(self.data_dir, 'metadata.pkl')
            
            # Vérifier que les fichiers existent
            if not os.path.exists(index_path):
                raise FileNotFoundError(f"Index FAISS introuvable : {index_path}")
            if not os.path.exists(chunks_path):
                raise FileNotFoundError(f"Chunks introuvables : {chunks_path}")
            
            # Charger le modèle d'embeddings
            print(f"   📦 Chargement du modèle : {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            
            # Charger l'index FAISS
            print(f"   🗄️  Chargement de l'index FAISS...")
            self.index = faiss.read_index(index_path)
            
            # Charger les chunks
            print(f"   📄 Chargement des chunks...")
            with open(chunks_path, 'rb') as f:
                self.chunks = pickle.load(f)
            
            # Charger les métadonnées (optionnel)
            if os.path.exists(metadata_path):
                with open(metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
            
            print(f"✅ RAG Searcher prêt !")
            print(f"   - {len(self.chunks)} chunks chargés")
            print(f"   - Dimension des vecteurs : {self.index.d}")
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des ressources : {e}")
            raise
    
    def _extract_text_from_chunk(self, chunk):
        """
        Logique interne pour extraire le texte d'une structure de chunk.
        """
        if isinstance(chunk, str):
            return chunk
        elif isinstance(chunk, dict):
            # Tente d'extraire de la clé 'chunk' (ou 'text' si c'est une autre convention)
            return chunk.get('chunk') or chunk.get('text')
        elif isinstance(chunk, (list, tuple)) and len(chunk) > 0:
            # Tente d'extraire du premier élément (souvent le texte)
            return self._extract_text_from_chunk(chunk[0])
        return None
    
    def search(self, query, top_k=3, return_scores=False):
        """
        Recherche les chunks les plus pertinents pour une question
        
        Args:
            query: Question de l'utilisateur
            top_k: Nombre de résultats à retourner
            return_scores: Si True, retourne aussi les scores
            
        Returns:
            Liste des chunks pertinents (strings si return_scores=False, dicts sinon)
        """
        try:
            # Encoder la question
            query_embedding = self.model.encode([query])
            
            # Rechercher dans FAISS
            distances, indices = self.index.search(
                query_embedding.astype('float32'), 
                top_k
            )
            
            # Récupérer les chunks correspondants
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                chunk = self.chunks[idx]
                
                if return_scores:
                    # Retourne le chunk brut dans le dictionnaire de résultats
                    results.append({
                        'chunk': chunk,
                        'score': float(dist),
                        'index': int(idx)
                    })
                else:
                    # Extrait le texte pour le retour simple
                    extracted_text = self._extract_text_from_chunk(chunk)
                    if extracted_text and extracted_text.strip():
                        results.append(extracted_text)
                    # Note : L'avertissement de type est maintenant dans get_context si nécessaire.
            
            return results
            
        except Exception as e:
            print(f"❌ Erreur lors de la recherche : {e}")
            return []
    
    def get_context(self, query, top_k=3, max_length=2000):
        """
        Récupère le contexte pertinent pour une question
        Formate le contexte pour être injecté dans le prompt
        
        Args:
            query: Question de l'utilisateur
            top_k: Nombre de chunks à récupérer
            max_length: Longueur maximale du contexte (en caractères)
            
        Returns:
            Contexte formaté (string)
        """
        # Rechercher les chunks pertinents. search() retourne maintenant des chaînes de caractères nettoyées
        # si elles ont pu être extraites.
        chunks = self.search(query, top_k=top_k)
        
        # Le filtrage des types inattendus a été déplacé dans _extract_text_from_chunk
        # pour uniformiser le process de search. Cependant, s'il reste des éléments
        # non-textuels, ils doivent être filtrés ici pour le join.
        
        text_chunks = []
        for chunk in chunks:
            if isinstance(chunk, str) and chunk.strip():
                text_chunks.append(chunk)
            else:
                 # Ce cas ne devrait plus arriver si search() est correctement implémenté, 
                 # mais nous le conservons pour la robustesse future.
                 print(f"❌ Avertissement RAG: Élément de chunk non-texte ignoré lors du formatage. Type: {type(chunk)}")


        # Concaténer les chunks
        context = "\n\n".join(text_chunks)
        
        # Limiter la longueur si nécessaire
        if len(context) > max_length:
            context = context[:max_length] + "\n\n[...]"
        
        return context
    
    def get_detailed_results(self, query, top_k=3):
        """
        Retourne des résultats détaillés avec scores et métadonnées
        Utile pour déboguer et analyser
        
        Args:
            query: Question de l'utilisateur
            top_k: Nombre de résultats
            
        Returns:
            Liste de dictionnaires avec détails
        """
        # On utilise search avec return_scores=True pour obtenir les dictionnaires bruts
        results = self.search(query, top_k=top_k, return_scores=True)
        
        detailed = []
        for result in results:
            # Utiliser la nouvelle méthode d'extraction pour assurer que l'aperçu est lisible
            chunk_content = self._extract_text_from_chunk(result['chunk'])
            
            detailed.append({
                'chunk': chunk_content if chunk_content else "Contenu non extractible",
                'score': result['score'],
                'index': result['index'],
                'preview': (chunk_content[:200] + "...") if chunk_content and len(chunk_content) > 200 else (chunk_content or "Contenu non extractible")
            })
        
        return detailed
    
    def health_check(self):
        """
        Vérifie que le RAG est fonctionnel
        
        Returns:
            dict avec le statut
        """
        try:
            if self.model is None or self.index is None or self.chunks is None:
                return {
                    'status': 'error',
                    'message': 'Ressources non chargées'
                }
            
            # Test rapide de recherche
            test_results = self.search("test", top_k=1)
            
            return {
                'status': 'ok',
                'num_chunks': len(self.chunks),
                'embedding_dim': self.index.d,
                'model': self.model_name,
                'test_search': 'ok' if test_results else 'failed'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }


# ============== TEST ==============

if __name__ == "__main__":
    """
    Test du module
    """
    print("=" * 60)
    print("TEST DU MODULE RAG SEARCH")
    print("=" * 60)
    
    # Initialiser
    searcher = RAGSearcher()
    
    # Test 1 : Recherche simple
    print("\n📝 Test 1 : Recherche simple")
    query = "Comment créer une vente?"
    results = searcher.search(query, top_k=2)
    print(f"\nQuestion : {query}")
    for i, chunk in enumerate(results):
        print(f"\nRésultat {i+1}:")
        # On vérifie si c'est une chaîne avant d'accéder au contenu
        preview = chunk[:200] + "..." if isinstance(chunk, str) and len(chunk) > 200 else str(chunk) 
        print(preview)
    
    # Test 2 : Get context
    print("\n📝 Test 2 : Get context")
    context = searcher.get_context(query, top_k=2)
    print(f"\nContexte récupéré ({len(context)} caractères):")
    print(context[:300] + "...")
    
    # Test 3 : Résultats détaillés
    print("\n📝 Test 3 : Résultats détaillés")
    detailed = searcher.get_detailed_results(query, top_k=2)
    for i, result in enumerate(detailed):
        print(f"\nRésultat {i+1}:")
        print(f"   Score: {result['score']:.4f}")
        print(f"   Preview: {result['preview']}")
    
    # Test 4 : Health check
    print("\n📝 Test 4 : Health check")
    health = searcher.health_check()
    print(f"\nStatut: {health}")
    
    print("\n" + "=" * 60)
    print("✅ TESTS TERMINÉS")
    print("=" * 60)