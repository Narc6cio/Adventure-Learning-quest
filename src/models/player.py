class Player:
    # Points requis par niveau
    LEVEL_THRESHOLDS = {
        1: 0,
        2: 200,
        3: 500,
        4: 1000,
        5: 1800
    }
    MAX_SUBJECT_POINTS = 100

    def __init__(self,id=None, name="Aventurier", level=1, points=0, current_streak=0, subjects=None, history=None):
        self.id = id
        self.name = name
        self.level = level
        self.points = points
        self.current_streak = current_streak
        self.subjects = subjects if subjects is not None else {"math": 0, "science": 0, "logic": 0}
        self.history = history if history is not None else []


    def update_points(self, points_earned, subject):
        self.points += points_earned
        self.current_streak += 1

        # Mise à jour des points par matière
        self.subjects[subject] = min(self.subjects[subject] + points_earned, self.MAX_SUBJECT_POINTS)

        # Vérification du passage de niveau
        for next_level in sorted(self.LEVEL_THRESHOLDS.keys(), reverse=True):
            if self.points >= self.LEVEL_THRESHOLDS[next_level] and next_level > self.level:
                self.level = next_level
                return True
        return False

    def reset_streak(self):
        self.current_streak = 0

    def add_to_history(self, question, user_answer, correct_answer, is_correct):
        self.history.append({
            "question": question,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    def get_statistics(self):
        return {
            "name": self.name,
            "level": self.level,
            "points": self.points,
            "current_streak": self.current_streak,
            "subjects": self.subjects,
            "history": self.history
        }

    def save(self, db_manager):
        """Sauvegarde via DatabaseManager"""
        try:
            return db_manager.save_player(self)
        except Exception as e:
            print(f"❌ Erreur sauvegarde joueur: {str(e)}")
            return False

    @classmethod
    def load(cls, db_manager, player_id=None, name="Aventurier"):
        """Charge via DatabaseManager"""
        try:
            return db_manager.load_player(player_id=player_id, name=name)
        except Exception as e:
            print(f"❌ Erreur chargement joueur: {str(e)}")
            return None

    def get_advanced_stats(self):
        """Calcule des statistiques détaillées pour l'évaluation"""
        stats = self.get_statistics()
        
        # Calcul de la précision par matière
        subject_accuracy = {}
        for subject in self.subjects.keys():
            subject_history = [h for h in self.history if h.get("subject") == subject]
            if subject_history:
                correct = sum(1 for h in subject_history if h["is_correct"])
                subject_accuracy[subject] = correct / len(subject_history) * 100
        
        # Tendances récentes (dernières 10 réponses)
        recent = self.history[-10:] if len(self.history) >= 10 else self.history
        recent_accuracy = sum(1 for h in recent if h["is_correct"]) / len(recent) * 100 if recent else 0
        
        stats.update({
            "subject_accuracy": subject_accuracy,
            "recent_accuracy": recent_accuracy,
            "weakest_subject": min(subject_accuracy, key=subject_accuracy.get) if subject_accuracy else None,
            "strongest_subject": max(subject_accuracy, key=subject_accuracy.get) if subject_accuracy else None
        })
        
        return stats