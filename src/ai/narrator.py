from .ollama_client import OllamaClient

class Narrator:
    def __init__(self):
        self.ollama = OllamaClient()
        self.system_prompt = """Tu es un narrateur d'aventure éducative.
        Ton rôle est de créer une ambiance immersive et motivante.
        Utilise un ton encourageant et des métaphores d'aventure."""
        self.themes = ["Forêt des Nombres", "Caverne des Sciences", "Tour de Logique"]

    def get_introduction(self):
        prompt = """Crée une courte introduction motivante (1-2 phrases) pour présenter 
        une nouvelle question. Utilise des métaphores d'aventure."""
        return self.ollama.generate("mistral:7b-instruct-q4_0", prompt, self.system_prompt)

    def get_motivational_quote(self, context="général"):
        prompt = f"""Donne une citation motivante courte en lien avec {context}.
        Garde un ton aventurier et inspirant."""
        return self.ollama.generate("mistral:7b-instruct-q4_0", prompt, self.system_prompt)

    def provide_feedback(self, is_correct, streak=0):
        context = f"L'apprenant a {'réussi' if is_correct else 'échoué'}"
        if streak > 3:
            context += f" et maintient une série de {streak} bonnes réponses"
        prompt = f"Donne un feedback court et motivant. Contexte: {context}"
        return self.ollama.generate("mistral:7b-instruct-q4_0", prompt, self.system_prompt)