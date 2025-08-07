import requests
import json
import sys
import subprocess

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        if not self.check_ollama_installation():
            return
            
        if not self.check_server():
            print("⚠️ Le serveur Ollama n'est pas accessible.")
            print("→ Vérifiez qu'Ollama est installé et démarré")
            print("→ Ouvrez un terminal et exécutez : ollama serve")
            return
            
        if not self.ensure_models_installed():
            return

    def check_ollama_installation(self):
        try:
            result = subprocess.run(["ollama", "--version"], 
                                  capture_output=True, 
                                  text=True)
            if result.returncode == 0:
                print(f"✅ Ollama version: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            print("❌ Ollama n'est pas installé ou n'est pas dans le PATH")
            print("→ Téléchargez Ollama depuis: https://ollama.ai/download")
            return False
        return False

    def check_server(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
        
    def generate(self, model, prompt, system=""):
        if not self.check_server():
            return "⚠️ Serveur Ollama non accessible"
            
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "system": system,
                    "stream": False
                }
            )
            
            # Vérifier si la requête a réussi
            response.raise_for_status()
            
            # Récupérer et vérifier le contenu de la réponse
            data = response.json()
            if "response" not in data:
                print(f"❌ Format de réponse inattendu: {data}")
                return "Erreur: Format de réponse inattendu"
                
            return data["response"]
            
        except requests.exceptions.RequestException as e:
            error_msg = f"❌ Erreur de connexion à Ollama: {str(e)}"
            print(error_msg)
            return error_msg
        except json.JSONDecodeError as e:
            error_msg = f"❌ Erreur de décodage JSON: {str(e)}"
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"❌ Erreur inattendue: {str(e)}"
            print(error_msg)
            return error_msg

    def check_model(self, model_name):
        try:
            # Remove the extra comma that was causing the error
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                # Print available models for debugging
                print(f"📝 Available models: {[model['name'] for model in models]}")
                return any(model["name"] == model_name for model in models)
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la vérification du modèle {model_name}: {str(e)}")
            return False

    def ensure_models_installed(self):
        required_models = {
            "qwen2.5:7b-instruct-q4_0": "Qwen pour le Quest Master",
            "mistral:7b-instruct-q4_0": "Mistral pour le Narrator",
            "phi3:mini": "Phi pour le Tutor"
        }
        
        missing_models = []
        for model, description in required_models.items():
            if not self.check_model(model):
                missing_models.append(f"- {model} ({description})")
        
        if missing_models:
            print("⚠️ Modèles manquants:")
            for model in missing_models:
                print(model)
            print("\nInstallation des modèles manquants avec:")
            for model in missing_models:
                print(f"ollama pull {model.split()[1]}")
            return False
        return True