from .ollama_client import OllamaClient

class Evaluator:
    def __init__(self):
        self.ollama = OllamaClient()
        self.system_prompt = """Tu es un coach pédagogique bienveillant. 
        Ton rôle est d'analyser les performances d'un apprenant et de fournir:
        1. Un bilan motivant de ses progrès
        2. Une analyse de ses forces et faiblesses
        3. Des suggestions d'amélioration concrètes
        Utilise un ton encourageant et constructif."""

    def generate_evaluation(self, player_data):
        # Préparer les données pour l'analyse
        history = player_data.get("history", [])
        subjects = player_data.get("subjects", {})
        
        # Calculer les statistiques de base
        total_questions = len(history)
        correct_answers = sum(1 for item in history if item["is_correct"])
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # Préparer le prompt pour l'IA
        prompt = f"""Analyse les performances de l'apprenant et fournis un retour personnalisé.
        
        Statistiques:
        - Niveau actuel: {player_data.get("level", 1)}
        - Score total: {player_data.get("points", 0)} points
        - Série actuelle: {player_data.get("current_streak", 0)} bonnes réponses
        - Précision globale: {accuracy:.1f}%
        - Répartition par matière: {subjects}
        
        Historique récent:
        {history[-5:] if len(history) > 5 else history}
        
        Retour attendu:
        1. Commence par un encouragement positif
        2. Analyse les points forts
        3. Identifie 1-2 axes d'amélioration 
        4. Propose des stratégies concrètes
        5. Termine par une note motivante"""
        
        return self.ollama.generate("phi3:mini", prompt, self.system_prompt)