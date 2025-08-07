class Question:
    def __init__(self, text, answer, subject):
        self.text = text
        self.answer = str(answer).strip()  # Convertir en string et nettoyer
        self.subject = subject

    def is_correct(self, user_answer):
        # Comparer les réponses nettoyées
        return str(user_answer).strip().lower() == self.answer.lower()

    def to_dict(self):
        return {
            "text": self.text,
            "answer": self.answer,
            "subject": self.subject
        }