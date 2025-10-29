"""
Script de test complet du backend ADES ChatBot
Teste toutes les routes et fonctionnalités
"""

import requests
import json
import time

# Configuration
BASE_URL = 'http://localhost:3000'

# Couleurs pour l'affichage
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(message):
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message):
    print(f"{RED}❌ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ️  {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{RESET}")

def test_home():
    """Test de la route home"""
    print("\n" + "="*60)
    print("TEST 1 : Route Home (/)")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/')
        
        if response.status_code == 200:
            data = response.json()
            print_info(f"Status: {data.get('status')}")
            print_info(f"Message: {data.get('message')}")
            print_info(f"Version: {data.get('version')}")
            print_info(f"RAG Enabled: {data.get('rag_enabled')}")
            
            if data.get('rag_enabled'):
                print_success("Backend fonctionne avec RAG")
            else:
                print_warning("Backend fonctionne SANS RAG")
            return True
        else:
            print_error(f"Code HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False

def test_health():
    """Test de la route health"""
    print("\n" + "="*60)
    print("TEST 2 : Route Health (/api/health)")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/api/health')
        
        if response.status_code == 200:
            data = response.json()
            print_info(f"Backend: {data.get('backend')}")
            print_info(f"Ollama: {data.get('ollama')}")
            print_info(f"RAG: {data.get('rag')}")
            
            all_ok = (
                data.get('backend') == 'running' and
                data.get('ollama') == 'connected' and
                data.get('rag') == 'ok'
            )
            
            if all_ok:
                print_success("Tous les systèmes sont opérationnels")
                return True
            else:
                print_warning("Certains systèmes ne sont pas opérationnels")
                return False
        else:
            print_error(f"Code HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False

def test_chat(question, expected_keywords=None):
    """Test d'une question au chatbot"""
    print(f"\n💬 Question: {question}")
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f'{BASE_URL}/api/chat',
            json={'message': question},
            headers={'Content-Type': 'application/json'}
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get('reply', '')
            rag_used = data.get('rag_used', False)
            
            print_info(f"RAG utilisé: {'Oui' if rag_used else 'Non'}")
            print_info(f"Temps de réponse: {elapsed:.2f}s")
            print_info(f"Réponse ({len(reply)} caractères):")
            
            # Afficher la réponse (limitée à 300 caractères)
            if len(reply) > 300:
                print(f"  {reply[:300]}...")
            else:
                print(f"  {reply}")
            
            # Vérifier les mots-clés attendus
            if expected_keywords:
                found_keywords = [kw for kw in expected_keywords if kw.lower() in reply.lower()]
                if found_keywords:
                    print_success(f"Mots-clés trouvés: {', '.join(found_keywords)}")
                else:
                    print_warning(f"Aucun mot-clé attendu trouvé: {expected_keywords}")
            
            return True
        else:
            print_error(f"Code HTTP: {response.status_code}")
            print_error(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False

def test_search(query):
    """Test de la recherche RAG directe"""
    print(f"\n🔍 Recherche: {query}")
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/search',
            json={'query': query, 'top_k': 2},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            print_info(f"Nombre de résultats: {len(results)}")
            
            for i, result in enumerate(results):
                score = result.get('score', 0)
                preview = result.get('preview', '')
                print(f"\n  Résultat {i+1} (score: {score:.4f}):")
                print(f"  {preview}")
            
            print_success("Recherche RAG fonctionnelle")
            return True
        else:
            print_error(f"Code HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False

def test_logs():
    """Test de récupération des logs"""
    print("\n" + "="*60)
    print("TEST : Logs (/api/logs)")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/api/logs')
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            logs = data.get('logs', [])
            
            print_info(f"Total de conversations loggées: {total}")
            print_info(f"Dernières conversations retournées: {len(logs)}")
            
            if logs:
                last_log = logs[-1]
                print_info(f"Dernière conversation:")
                print(f"  User: {last_log.get('user', '')[:50]}...")
                print(f"  Bot: {last_log.get('bot', '')[:50]}...")
            
            print_success("Logs accessibles")
            return True
        else:
            print_error(f"Code HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erreur: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("\n" + "="*60)
    print("🧪 TESTS COMPLETS DU BACKEND ADES CHATBOT")
    print("="*60)
    
    results = []
    
    # Test 1: Home
    results.append(("Home", test_home()))
    
    # Test 2: Health
    results.append(("Health", test_health()))
    
    # Test 3: Questions au chatbot
    print("\n" + "="*60)
    print("TEST 3 : Questions au Chatbot (/api/chat)")
    print("="*60)
    
    chat_tests = [
        ("Comment créer une vente?", ["vente", "bouton", "vert"]),
        ("Comment annuler une vente?", ["annuler", "24 heures", "journée"]),
        ("Quels sont les types de réchauds?", ["OLI-c", "OLI-b", "charbon"]),
        ("Que faire si j'ai oublié mon mot de passe?", ["mot de passe", "oublié", "code"]),
        ("Comment me connecter?", ["connexion", "nom d'utilisateur", "mot de passe"])
    ]
    
    for question, keywords in chat_tests:
        result = test_chat(question, keywords)
        results.append((f"Chat: {question[:30]}...", result))
        time.sleep(1)  # Petite pause entre les requêtes
    
    # Test 4: Recherche RAG
    print("\n" + "="*60)
    print("TEST 4 : Recherche RAG (/api/search)")
    print("="*60)
    
    result = test_search("Comment synchroniser les données?")
    results.append(("RAG Search", result))
    
    # Test 5: Logs
    results.append(("Logs", test_logs()))
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    failed = total - passed
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "-"*60)
    print(f"Total: {total} tests")
    print(f"{GREEN}Réussis: {passed}{RESET}")
    print(f"{RED}Échoués: {failed}{RESET}")
    print(f"Taux de réussite: {(passed/total)*100:.1f}%")
    print("="*60)
    
    if failed == 0:
        print(f"\n{GREEN}🎉 TOUS LES TESTS SONT PASSÉS !{RESET}")
        print(f"{GREEN}Le backend est prêt pour l'intégration mobile.{RESET}\n")
    else:
        print(f"\n{RED}⚠️  Certains tests ont échoué.{RESET}")
        print(f"{YELLOW}Vérifiez les erreurs ci-dessus avant de continuer.{RESET}\n")

if __name__ == "__main__":
    main()