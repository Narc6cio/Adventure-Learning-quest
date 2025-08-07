# Adventure Learning Quest

## Présentation :
Une application pour apprentissage dans le domaine scientifique. Elle permet aux utilisateurs de s'exercer avec des exercices qui leur feront gagner des points et de monter en niveau; et aussi pour consulter directement dans l'application des formations grâce aux assistances par les intelligences artificielles integré dans l'application.

## Project Structure
```
adventure-learning-quest
├── src
│   ├── app.py
│   ├── ai
│   │   ├── __init__.py
│   │   ├── quest_master.py
│   │   ├── narrator.py
│   │   └── tutor.py
│   ├── ui
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── game_area.py
│   │   ├── chat_panel.py
│   │   └── stats_panel.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── player.py
│   │   └── question.py
│   └── utils
│       ├── __init__.py
│       ├── config.py
│       └── data_manager.py
|       └── db_manager.py
├── assets
│   ├── icons
│   └── themes
├── saves
├── requirements.txt
├── setup.py
└── README.md
```

## Demarrage
- Cloner le répositorie "git clone ..."
- Copier le projet dans votre branche
- Pour passer dans votre branche "git checkout nom_branche"
- Créer un environnement : "python -m venv venv"
- Activation de l'environnement : 
"racine du projet/ cd venv/Scripts
racine du projet/venv/Scripts/activate"
- installation des dépendances "pip install -r requirements.txt"
- Pour la lancer, mettez vous au niveau du racine du projet et "python src/app.py"

### NB :
- Pour pouvoir faire un test de l'application, il faudra que vous disposez dans votre ordinateur "Ollama"
- télécharger les AI Ollama nécessaire
   ollama pull phi3:mini
   ollama pull qwen2.5:7b-q4_0
   ollama pull mistral:7b-q4_0 
- Pour la lancer, il vous faudra un ordinateur avec 8 Gb de RAM, core i5-6ème (pour le test API local) minimum

## Explication des rôles des API intégrés :
### F1 - Système de questions dynamiques
Qwen2.5 : Génère questions math/science adaptées au niveau
Difficulty scaling : Questions plus dures selon progression
Types supportés : QCM, calculs simples, logique de base

### F2 - Narration motivante
Mistral : Crée encouragements et contexte narratif
Storytelling léger : "Tu explores la Forêt des Nombres..."
Feedback personnalisé : Réactions selon performance

### F3 - Assistant pédagogique
Phi-3 : Explications simples et indices
Help system : Bouton "Aide" pour chaque question
Encouragements : Messages motivants selon les résultats
