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

    def __init__(self, name="Aventurier", level=1, points=0):
        self.name = name
        self.level = level
        self.points = points
        self.current_streak = 0
        self.subjects = {"math": 0, "science": 0, "logic": 0}
        self.history = []

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

    def save_to_file(self, file_path):
        from ..utils.data_manager import save_player_data
        save_player_data(file_path, self.get_statistics())

    @classmethod
    def load_from_file(cls, file_path):
        from ..utils.data_manager import load_player_data
        data = load_player_data(file_path)
        if data:
            player = cls(data["name"], data["level"], data["points"])
            player.current_streak = data["current_streak"]
            player.subjects = data["subjects"]
            player.history = data["history"]
            return player
        return cls()