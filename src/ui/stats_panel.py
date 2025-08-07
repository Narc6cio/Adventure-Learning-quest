import customtkinter as ctk

class StatsPanel(ctk.CTkFrame):
    def __init__(self, parent, player_data):
        super().__init__(parent, width=250)
        self.grid_propagate(False)
        self.player_data = player_data
        self.create_widgets()

    def create_widgets(self):
        # Titre du panneau
        stats_title = ctk.CTkLabel(
            self, 
            text="📊 Progression",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        stats_title.pack(pady=10)
        
        # Barres de progression par matière
        subjects_frame = ctk.CTkFrame(self)
        subjects_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_bars = {}
        for subject, points in self.player_data["subjects"].items():
            subject_name = {
                "math": "🔢 Mathématiques", 
                "science": "🔬 Sciences", 
                "logic": "🧩 Logique"
            }[subject]
            
            subject_label = ctk.CTkLabel(subjects_frame, text=subject_name)
            subject_label.pack(anchor="w", padx=10, pady=2)
            
            progress_bar = ctk.CTkProgressBar(subjects_frame)
            progress_bar.pack(fill="x", padx=10, pady=2)
            progress_bar.set(min(points / 100, 1.0))  # Max 100 points par matière
            self.progress_bars[subject] = progress_bar
            
        # Statistiques détaillées
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            stats_frame, 
            text="📈 Statistiques", 
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=5)
        
        self.streak_label = ctk.CTkLabel(
            stats_frame, 
            text=f"🔥 Série actuelle: {self.player_data['current_streak']}"
        )
        self.streak_label.pack(anchor="w", padx=10, pady=2)
        
        self.total_questions_label = ctk.CTkLabel(
            stats_frame,
            text=f"❓ Questions résolues: {len(self.player_data['history'])}"
        )
        self.total_questions_label.pack(anchor="w", padx=10, pady=2)
        
        # Historique récent
        history_frame = ctk.CTkFrame(self)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(
            history_frame, 
            text="📝 Historique récent", 
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=5)
        
        self.history_text = ctk.CTkTextbox(history_frame, height=150)
        self.history_text.pack(fill="both", expand=True, padx=10, pady=5)
        self.update_history_display()

    def update_display(self, player_data):
        """Met à jour l'affichage avec les nouvelles données"""
        self.player_data = player_data
        
        # Mise à jour des barres de progression
        for subject, points in player_data["subjects"].items():
            self.progress_bars[subject].set(min(points / 100, 1.0))
        
        # Mise à jour des statistiques
        self.streak_label.configure(
            text=f"🔥 Série actuelle: {player_data['current_streak']}"
        )
        self.total_questions_label.configure(
            text=f"❓ Questions résolues: {len(player_data['history'])}"
        )
        
        # Mise à jour de l'historique
        self.update_history_display()

    def update_history_display(self):
        """Met à jour l'affichage de l'historique"""
        self.history_text.delete("0.0", "end")
        
        recent_history = self.player_data["history"][-10:]  # 10 dernières entrées
        for entry in reversed(recent_history):
            result = "✅" if entry["is_correct"] else "❌"
            text = f"{result} {entry['question'][:30]}...\n"
            self.history_text.insert("end", text)