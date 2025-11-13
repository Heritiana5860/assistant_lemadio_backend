from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import datetime
from dotenv import load_dotenv

# LangChain Core
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# LangChain Ollama
from langchain_ollama import OllamaLLM

# RAG Loader
from rag_loader import initialize_rag_components

load_dotenv()
app = Flask(__name__)
CORS(app)

# ================== CONFIGURATION ==================
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b-instruct-q4_K_M")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

SYSTEM_PROMPT = """Vous êtes un assistant utile spécialisé dans la documentation technique de l'application mobile Lemadio d'ADES. Votre objectif principal est d'assister, aider et former les vendeurs des points de vente ou centres de vente d'ADES à utiliser correctement l'application Lemadio.

Votre tâche est de générer une réponse **complète et détaillée** à la QUESTION, en utilisant **uniquement et exhaustivement** les informations trouvées dans le CONTEXTE fourni.

Si la QUESTION nécessite de lier plusieurs processus (comme la vente directe et revendeur), vous devez synthétiser toutes les informations pertinentes du CONTEXTE pour une réponse cohérente.

**Règle Impérative de Pertinence :**
- Si la QUESTION est une simple salutation, une formule de politesse générale, ou si le CONTEXTE fourni est vide ou ne contient aucune information pertinente pour une action spécifique de l'application Lemadio, votre réponse doit être :
  "Bonjour ! Je suis l'assistant Lemadio. Comment puis-je vous aider avec l'utilisation de l'application (création de vente, gestion des stocks, annulation) ?"
- Si la QUESTION porte sur un sujet **hors-Lemadio**, votre réponse doit être :
  "Je suis un assistant spécialisé dans l'application Lemadio d'ADES. Je ne peux répondre qu'aux questions concernant **l'utilisation et les fonctionnalités de l'application Lemadio** basées sur la documentation fournie. Veuillez reformuler votre question pour qu'elle porte sur l'application."

Répondez toujours en français.
Votre nom est "Assistant Lemadio".

CONTEXTE:
{context}

QUESTION:
{input}
"""

# ================== INITIALISATION LLM ==================
print("Initialisation du LLM Ollama...")
try:
    llm = OllamaLLM(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_URL,
        temperature=0.3
    )
    print(f"LLM Ollama prêt : {OLLAMA_MODEL}")
except Exception as e:
    print(f"Erreur lors de l'initialisation du LLM : {e}")
    llm = None

# ================== INITIALISATION RAG ==================
print("Chargement du système RAG...")
retriever, rag_enabled = initialize_rag_components()

# ================== CRÉATION DE LA CHAÎNE RAG (MANUELLE) ==================
def create_rag_chain(llm, retriever):
    prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
    
    # Chaîne RAG : retrieve → stuff → LLM → parse
    rag_chain = (
        {"context": retriever, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

RAG_CHAIN = None
if rag_enabled and llm:
    RAG_CHAIN = create_rag_chain(llm, retriever)
    print("Chaîne RAG construite avec succès.")
else:
    print("RAG désactivé ou LLM indisponible.")

# ================== LOGGING ==================
os.makedirs("logs", exist_ok=True)

def log_conversation(user_message, bot_response):
    log_path = "logs/conversations.log"
    with open(log_path, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n[{timestamp}]\nUSER: {user_message}\nBOT: {bot_response}\n")
        f.write("-" * 50 + "\n")

# ================== ROUTES API ==================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "ADES Lemadio Chatbot API"
    })

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "rag": rag_enabled,
        "llm": OLLAMA_MODEL if llm else "unavailable",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return jsonify({"error": "Le message est vide."}), 400
        
        if not RAG_CHAIN:
            return jsonify({"error": "Service indisponible : RAG ou LLM non chargé."}), 500

        print(f"Question reçue : {user_message[:60]}...")
        
        # Exécution de la chaîne RAG
        response = RAG_CHAIN.invoke(user_message)
        bot_response = response.strip()

        # Log
        log_conversation(user_message, bot_response)

        return jsonify({
            "status": "success",
            "reply": bot_response,
            "rag_used": True,
            "timestamp": datetime.datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Erreur dans /api/chat : {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": "Erreur interne du serveur."
        }), 500

# ================== DÉMARRAGE ==================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Serveur Flask démarré sur le port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)