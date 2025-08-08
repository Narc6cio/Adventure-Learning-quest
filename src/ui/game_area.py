import customtkinter as ctk
import tkinter as tk
import threading

class GameArea(ctk.CTkFrame):
    def __init__(self, parent, main_window, quest_master, narrator, tutor, player, update_callback, evaluator):

        super().__init__(parent)
        self.main_window = main_window  # Stocker la référence à MainWindow
        self.quest_master = quest_master
        self.narrator = narrator
        self.tutor = tutor
        self.player = player
        self.update_callback = update_callback
        self.current_question = None
        self.evaluator = evaluator
        
        self.setup_ui()

    def setup_ui(self):
        # Titre de la zone de jeu
        game_title = ctk.CTkLabel(
            self,
            text="🎮 Zone d'Aventure",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        game_title.pack(pady=10)
        
        # Zone de question 
        self.question_frame = ctk.CTkFrame(self, height=150)  
        self.question_frame.pack(fill="x", padx=20, pady=5)  
        self.question_frame.pack_propagate(False)
        
        self.question_label = ctk.CTkLabel(
            self.question_frame,
            text="Clique sur 'Nouvelle Question' pour commencer ton aventure !",
            font=ctk.CTkFont(size=16),
            wraplength=500
        )
        self.question_label.pack(expand=True, pady=10) 
        
        # Zone de réponse 
        answer_frame = ctk.CTkFrame(self)
        answer_frame.pack(fill="x", padx=20, pady=5) 
        
        ctk.CTkLabel(answer_frame, text="Ta réponse:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.answer_entry = ctk.CTkEntry(
            answer_frame,
            placeholder_text="Écris ta réponse ici...",
            font=ctk.CTkFont(size=14),
            height=40
        )
        self.answer_entry.pack(fill="x", padx=20, pady=5)
        self.answer_entry.bind("<Return>", lambda e: self.submit_answer())
        
        # Boutons d'action 
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(fill="x", padx=20, pady=5)  
        
        self.new_question_btn = ctk.CTkButton(
            buttons_frame,
            text="🎲 Nouvelle Question",
            command=self.generate_new_question,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.new_question_btn.pack(side="left", padx=10, pady=5)  

        self.submit_button = ctk.CTkButton(
            buttons_frame,
            text="✅ Valider Réponse",
            command=self.submit_answer,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.submit_button.pack(side="left", padx=10, pady=5)  
        
        self.help_btn = ctk.CTkButton(
            buttons_frame,
            text="💡 Aide",
            command=self.request_help,
            font=ctk.CTkFont(size=14),
            height=40
        )
        self.help_btn.pack(side="left", padx=10, pady=5)  

        # Zone de feedback 
        self.feedback_frame = ctk.CTkFrame(self, height=60)  
        self.feedback_frame.pack(fill="x", padx=20, pady=5)  
        self.feedback_frame.pack_propagate(False)
        
        self.feedback_label = ctk.CTkLabel(
            self.feedback_frame,
            text="",
            font=ctk.CTkFont(size=14),
            wraplength=500
        )
        self.feedback_label.pack(expand=True, pady=5)  

        # Zone d'évaluation 
        self.evaluation_frame = ctk.CTkFrame(self)
        self.evaluation_frame.pack(fill="both", expand=True, padx=20, pady=5) 
        
        ctk.CTkLabel(
            self.evaluation_frame,
            text="📈 Évaluation Personnalisée",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)
        
        self.evaluation_text = ctk.CTkTextbox(
            self.evaluation_frame, 
            height=200,  
            wrap="word"
        )
        self.evaluation_text.pack(fill="both", expand=True)
        
        self.evaluate_btn = ctk.CTkButton(
            self.evaluation_frame,
            text="🔍 Analyser ma progression",
            command=self.generate_evaluation,
            height=30
        )
        self.evaluate_btn.pack(pady=5)

    def generate_new_question(self):
        """Génère une nouvelle question"""
        # Désactiver le bouton pendant la génération
        self.new_question_btn.configure(state="disabled")
        
        # Générer la question
        question = self.quest_master.generate_question(self.player.level)
        self.current_question = {
            "text": question.text,
            "answer": question.answer,
            "subject": question.subject
        }
        
        # Afficher la question
        self.question_label.configure(text=question.text)
        
        # Vider le champ de réponse
        self.answer_entry.delete(0, 'end')
        
        # Vider le feedback
        self.feedback_label.configure(text="")
        
        # Message du narrateur
        intro = self.narrator.get_introduction()
        self.main_window.chat_panel.narrator_text.insert("end", f"\n{intro}\n")
        self.main_window.chat_panel.narrator_text.see("end")
        
        # Réactiver le bouton
        self.new_question_btn.configure(state="normal")

    def submit_answer(self):
        """Vérifie la réponse de l'utilisateur"""
        if not self.current_question:
            self.feedback_label.configure(text="Génère d'abord une question !")
            return

        user_answer = self.answer_entry.get().strip()
        is_correct = user_answer.lower() == self.current_question["answer"].lower()
        
        if is_correct:
            level_up = self.player.update_points(10, self.current_question["subject"])
            feedback = "🎉 Niveau supérieur !" if level_up else "✨ Bonne réponse !"
        else:
            self.player.reset_streak()
            feedback = "❌ Essaie encore !"
        
        self.player.add_to_history(
            self.current_question["text"],
            user_answer,
            self.current_question["answer"],
            is_correct
        )
        
        self.feedback_label.configure(text=feedback)
        self.update_callback()  # Met à jour les statistiques

    def request_help(self):
        """Demande de l'aide au tuteur"""
        if not self.current_question:
            self.feedback_label.configure(text="Génère d'abord une question !")
            return
            
        hint = self.tutor.provide_hint(self.current_question["text"])
        concept_help = self.tutor.explain_concept(self.current_question["subject"])
        
        # Utilisez main_window au lieu de parent
        self.main_window.chat_panel.tutor_text.insert("end", f"\n💡 Indice: {hint}\n")
        self.main_window.chat_panel.tutor_text.insert("end", f"\n📚 Aide: {concept_help}\n")
        self.main_window.chat_panel.tutor_text.see("end")

    def display_question(self, question_text):
        """Affiche une question"""
        self.question_label.configure(text=question_text)
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.configure(text="")

    def generate_evaluation(self):
        """Génère et affiche l'évaluation"""
        try:
            self.evaluate_btn.configure(state="disabled")
            self.evaluation_text.configure(state="normal")
            self.evaluation_text.delete("1.0", "end")
            self.evaluation_text.insert("end", "⏳ Analyse en cours...")
            
            if not self.player.history:
                self.evaluation_text.delete("1.0", "end")
                self.evaluation_text.insert("end", "✏️ Répondez à quelques questions pour obtenir une analyse.")
                self.evaluate_btn.configure(state="normal")
                return
                
            def evaluation_thread():
                try:
                    stats = self.player.get_advanced_stats()
                    print("Stats pour évaluation:", stats)
                    evaluation = self.evaluator.generate_evaluation(stats)
                    # Mise à jour UI dans le thread principal
                    self.after(0, lambda: self._display_evaluation(evaluation))
                    
                except Exception as e:
                    print(f"Erreur génération évaluation: {e}")
                    self.after(0, lambda: self._display_error())
                    
            threading.Thread(target=evaluation_thread, daemon=True).start()
            
        except Exception as e:
            print(f"Erreur interface évaluation: {e}")
            self._display_error()

    def _display_evaluation(self, text):
        """Affiche l'évaluation générée"""
        self.evaluation_text.delete("1.0", "end")
        self.evaluation_text.insert("end", text)
        self.evaluate_btn.configure(state="normal")
        self.evaluation_text.see("end")  # Défilement automatique

    def _display_error(self):
        """Affiche un message d'erreur"""
        self.evaluation_text.delete("1.0", "end")
        self.evaluation_text.insert("end", "⚠️ Erreur lors de la génération de l'analyse")
        self.evaluate_btn.configure(state="normal")