from ai.quest_master import QuestMaster
from ai.narrator import Narrator
from ai.tutor import Tutor
from models.player import Player
from utils.db_manager import DatabaseManager

def main():
    # Initialisation
    db = DatabaseManager("data/test.db")  # DB séparée pour les tests
    quest_master = QuestMaster()
    narrator = Narrator()
    tutor = Tutor()
    
    # Création ou chargement du joueur
    player = Player.load(db) or Player(name="Testeur")
    
    print("\n=== TEST DU QUEST MASTER ===")
    question = quest_master.generate_question()
    print(f"Question: {question.text}")
    print(f"Réponse: {question.answer}")
    print(f"Sujet: {question.subject}")
    
    print("\n=== TEST DU NARRATOR ===")
    print("Introduction:", narrator.get_introduction())
    print("Citation:", narrator.get_motivational_quote("math"))
    print("Feedback (correct):", narrator.provide_feedback(True, 5))
    print("Feedback (incorrect):", narrator.provide_feedback(False))
    
    print("\n=== TEST DU TUTOR ===")
    print("Indice:", tutor.provide_hint(question.text))
    print("Explication:", tutor.explain_concept("algèbre"))
    
    print("\n=== TEST DU JOUEUR ===")
    print("Avant réponse:", player.get_statistics())
    player.update_points(10, "math")
    player.add_to_history(
        question.text, 
        "ma réponse", 
        question.answer, 
        "ma réponse" == question.answer
    )
    print("Après réponse:", player.get_statistics())
    player.save(db)
    
    print("\n=== TEST DE LA BASE DE DONNÉES ===")
    loaded_player = Player.load(db, "Testeur")
    print("Joueur chargé:", loaded_player.get_statistics())

if __name__ == "__main__":
    main()