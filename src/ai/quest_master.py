import json
from .ollama_client import OllamaClient
from models.question import Question

class QuestMaster:
    def __init__(self):
        self.ollama = OllamaClient()
        self.system_prompt = """Tu es un générateur de questions éducatives appelé Quest Master.
        Génère uniquement des questions adaptées au niveau dans un format JSON strict.
        Les questions doivent être variées et stimulantes.
        Favorise les questions qui font réfléchir plutôt que la pure mémorisation."""

    def generate_question(self, level=1):
        difficulty = {
            1: "débutant (concepts de base)",
            2: "intermédiaire (application simple)",
            3: "avancé (résolution de problèmes)",
            4: "expert (analyse et synthèse)"
        }.get(level, "débutant")

        prompt = f"""Génère une question de niveau {difficulty}.
        Règles strictes:
        1. Math: algèbre, géométrie, logique mathématique
        2. Science: physique simple, chimie basique, biologie
        3. Logic: suites, patterns, énigmes
        4. Format: question courte, réponse unique
        5. Niveau adapté: {difficulty}
        
        Retourne uniquement un JSON: {{"text": "question", "answer": "réponse", "subject": "math/science/logic"}}"""
        
        try:
            # Appel API avec timeout et retry
            response = self.ollama.generate(
                model="qwen2.5:7b-instruct-q4_0",
                prompt=prompt,
                system=self.system_prompt
            )
            
            # Debug - voir la réponse brute
            print(f"Réponse API: {response}")
            
            # Nettoyer la réponse - enlever les backticks et 'json' si présents
            clean_response = response.strip('`').replace('json', '').strip()
            
            # Parser le JSON
            data = json.loads(clean_response)
            
            # Valider le format
            if not all(k in data for k in ["text", "answer", "subject"]):
                raise ValueError("Format JSON incomplet")
                
            # Valider le sujet
            if data["subject"] not in ["math", "science", "logic"]:
                data["subject"] = "math"
                
            # Créer un objet Question
            return Question(
                text=data["text"],
                answer=data["answer"],
                subject=data["subject"]
            )
            
        except Exception as e:
            print(f"❌ Erreur génération question: {str(e)}")
            # Question de secours en cas d'erreur
            return Question(
                text="Combien font 2 + 2 ?",
                answer="4",
                subject="math"
            )