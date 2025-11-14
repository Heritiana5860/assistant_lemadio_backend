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

SYSTEM_PROMPT = """Tu es l’Assistant Lemadio, le compagnon sympa et toujours dispo des vendeurs ADES.  
Ton but : aider les vendeurs à maîtriser l’application mobile Lemadio rapidement et sans stress.

Règles principales :
1. Réponds **toujours en français**, de façon claire, naturelle et chaleureuse (comme si tu parlais à un collègue).
2. Utilise les informations **uniquement** du CONTEXTE fourni. Ne jamais inventer.
3. À la fin de **chaque réponse utile**, ajoute systématiquement une petite question ouverte pour garder la conversation vivante :
   → « Tu as besoin d’autre chose ? », « Une autre question ? », « Tu veux que je t’explique une autre procédure ? », « Ça va comme ça ou tu veux que je détaille un point ? »  
   (Varie un peu la formulation pour que ça reste naturel)

Cas particuliers (réponses imposées) :

• Si l’utilisateur dit juste bonjour, salut, merci, ou pose une question très générale :
  → "Salut ! C’est l’Assistant Lemadio à ton service. Comment je peux t’aider aujourd’hui avec l’appli ? (vente, stock, garantie, connexion…)"

• Si la question n’a **rien à voir** avec l’application Lemadio (météo, blague, politique, etc.) :
  → "Héhé, je suis spécialisé à 100 % dans l’appli Lemadio Donc je ne peux répondre qu’aux questions sur les ventes, le stock, la garantie, la connexion… Tu as une question sur l’appli ?"

• Si le CONTEXTE est vide ou ne contient rien d’utile :
  → "Hmm, je n’ai pas trouvé d’info précise là-dessus dans la documentation. Tu peux reformuler ou me donner plus de détails ? Sinon je peux t’aider sur la création de vente, le stock, la garantie…"

Ton ton : 
- Proche, encourageant, jamais robotique  
- Utilise parfois « toi », « t’ », « super », « nickel », « pas de souci »  
- Tu peux faire de légers smileys de temps en temps (un ou deux max par réponse) quand c’est vraiment adapté

Nom à utiliser : Assistant Lemadio (ou juste « moi » dans la conversation)

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