from .ollama_client import OllamaClient

class Tutor:
    def __init__(self):
        self.ollama = OllamaClient()
        self.system_prompt = """Tu es un tuteur pédagogique bienveillant.
        Ton rôle est d'aider à comprendre sans donner la réponse.
        Utilise des explications simples et des analogies."""

    def provide_hint(self, question=None):
        if not question:
            return "Je ne peux pas donner d'indice sans question. Pose d'abord une question au Quest Master !"
        
        prompt = f"""Donne un indice utile pour cette question: "{question}"
        L'indice doit guider la réflexion sans donner la réponse."""
        return self.ollama.generate("phi3:mini", prompt, self.system_prompt)

    def explain_concept(self, concept):
        prompt = f"""Explique simplement le concept suivant : {concept}
        Utilise des exemples concrets et des analogies."""
        return self.ollama.generate("phi3:mini", prompt, self.system_prompt)