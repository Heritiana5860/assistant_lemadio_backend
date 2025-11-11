# app_lc.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import datetime
from dotenv import load_dotenv

# --- Imports LangChain récents ---
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
from langchain_community.llms import HuggingFaceHub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

# Import du module RAG
from rag_loader import initialize_rag_components

# Charger les variables d'environnement
load_dotenv()

# Créer l'application Flask
app = Flask(__name__)
CORS(app)

# ================== CONFIGURATION ==================
USE_HUGGINGFACE = os.getenv('USE_HUGGINGFACE', 'false').lower() == 'true'
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
HUGGINGFACE_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')

LLM = None
RAG_RETRIEVER = None
RAG_ENABLED = False

SYSTEM_PROMPT = """Vous êtes un assistant utile spécialisé dans la documentation technique de l'application mobile Lemadio d'ADES. Votre objectif principal est d'assister, aider et former les vendeurs des points de vente ou centres de vente d'ADES à utiliser correctement l'application Lemadio.

Votre tâche est de générer une réponse **complète et détaillée** à la QUESTION,
en utilisant **uniquement et exhaustivement** les informations trouvées dans le CONTEXTE fourni.

Si la QUESTION nécessite de lier plusieurs processus (comme la vente directe et revendeur),
vous devez synthétiser toutes les informations pertinentes du CONTEXTE pour une réponse cohérente.

**Règle Impérative de Pertinence :**
Si la QUESTION est une simple salutation, une formule de politesse générale, ou si le CONTEXTE fourni est vide ou ne contient aucune information pertinente pour une action spécifique de l'application Lemadio, votre réponse doit être :
"Bonjour ! Je suis l'assistant Lemadio. Comment puis-je vous aider avec l'utilisation de l'application (création de vente, gestion des stocks, annulation) ?"

Si la QUESTION porte sur un sujet **hors-Lemadio**, votre réponse doit être :
"Je suis un assistant spécialisé dans l'application Lemadio d'ADES. Je ne peux répondre qu'aux questions concernant **l'utilisation et les fonctionnalités de l'application Lemadio** basées sur la documentation fournie. Veuillez reformuler votre question pour qu'elle porte sur l'application."

Réponds toujours en français.

CONTEXTE:
{context}

QUESTION:
{input}
"""

# Créer le dossier logs si nécessaire
os.makedirs("logs", exist_ok=True)

# ================== INITIALISATION ==================
print("\n" + "=" * 60)
print("🚀 DÉMARRAGE DU BACKEND ADES CHATBOT (LangChain)")
print("=" * 60)

# --- 1. Initialiser le LLM ---
try:
    if USE_HUGGINGFACE:
        LLM = HuggingFaceHub(
            repo_id=HUGGINGFACE_MODEL,
            huggingfacehub_api_token=HUGGINGFACE_API_KEY
        )
        print("✅ LLM HuggingFace prêt.")
    else:
        LLM = OllamaLLM(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_URL,
            temperature=0.3
        )
        print(f"✅ LLM Ollama ({OLLAMA_MODEL}) prêt.")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation du LLM : {e}")
    LLM = None

# --- 2. Initialiser le RAG ---
RAG_RETRIEVER, RAG_ENABLED = initialize_rag_components(data_dir="rag/data")
print("=" * 60 + "\n")

# --- 3. Construire la chaîne RAG ---
RAG_CHAIN = None
if RAG_ENABLED and LLM:
    rag_prompt = ChatPromptTemplate.from_template(
    SYSTEM_PROMPT.replace("{question}", "{input}") 
    )
    document_chain = create_stuff_documents_chain(LLM, rag_prompt)
    RAG_CHAIN = create_retrieval_chain(RAG_RETRIEVER, document_chain)
    print("✅ Chaîne RAG construite avec succès.")
else:
    print("⚠️  RAG désactivé ou LLM indisponible.")

# ================== ROUTES ==================
def log_conversation(user_message, bot_response, context_used=None):
    """Log basique dans un fichier texte"""
    log_path = os.path.join("logs", "conversations.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.datetime.now()}]\nUSER: {user_message}\nBOT: {bot_response}\n\n")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "Backend ADES ChatBot Lemadio fonctionne!"})

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "backend": "running",
        "rag": "ok" if RAG_ENABLED else "disabled"
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Le message ne peut pas être vide."}), 400

        bot_response = "Erreur: LLM ou RAG non disponible."
        context_used = None

        # --- Cas 1 : RAG activé ---
        if RAG_ENABLED and RAG_CHAIN:
            print(f"🔍 Exécution RAG pour : {user_message[:50]}...")
            response = RAG_CHAIN.invoke({"input": user_message})
            bot_response = response.get("answer", "(aucune réponse)")
            source_docs = response.get("context", [])
            context_used = "\n\n".join([doc.page_content for doc in source_docs])
            print(f"✅ Contexte trouvé ({len(source_docs)} documents)")

        # --- Cas 2 : LLM simple (sans RAG) ---
        elif LLM:
            print("⚠️  RAG inactif — réponse directe LLM...")
            prompt = SYSTEM_PROMPT.replace("{context}", "Aucune documentation source.")
            prompt = prompt.replace("{input}", user_message)
            
            bot_response = LLM.invoke(prompt)

        log_conversation(user_message, bot_response, context_used)

        return jsonify({
            "status": "success",
            "user_message": user_message,
            "reply": bot_response,
            "rag_used": RAG_ENABLED and context_used is not None,
            "timestamp": datetime.datetime.now().isoformat()
        })

    except Exception as e:
        print(f"❌ Erreur dans /api/chat : {e}")
        return jsonify({
            "status": "error",
            "message": f"Erreur interne : {str(e)}"
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Serveur démarrant sur le port {port}")
    app.run(debug=False, host="0.0.0.0", port=port)
