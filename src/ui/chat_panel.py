import customtkinter as ctk

class ChatPanel(ctk.CTkFrame):
    def __init__(self, parent, quest_master, narrator, tutor):
        super().__init__(parent, width=300)
        self.quest_master = quest_master
        self.narrator = narrator
        self.tutor = tutor
        self.current_question = None  # Add this line to store current question
        self.grid_propagate(False)
        
        # Titre du panneau
        ai_title = ctk.CTkLabel(
            self,
            text="🤖 Assistants IA",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        ai_title.pack(pady=10)
        
        # Onglets pour les différentes IA
        self.ai_tabview = ctk.CTkTabview(self)
        self.ai_tabview.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Onglet Quest Master
        self.ai_tabview.add("🏰 Quest Master")
        quest_tab = self.ai_tabview.tab("🏰 Quest Master")
        self.quest_master_text = ctk.CTkTextbox(quest_tab, height=200)
        self.quest_master_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Onglet Narrator
        self.ai_tabview.add("📚 Narrator")
        narrator_tab = self.ai_tabview.tab("📚 Narrator")
        self.narrator_text = ctk.CTkTextbox(narrator_tab, height=200)
        self.narrator_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Onglet Tutor
        self.ai_tabview.add("👨‍🏫 Tutor")
        tutor_tab = self.ai_tabview.tab("👨‍🏫 Tutor")
        self.tutor_text = ctk.CTkTextbox(tutor_tab, height=200)
        self.tutor_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Zone de chat
        chat_frame = ctk.CTkFrame(self)
        chat_frame.pack(fill="x", padx=10, pady=5)
        
        self.chat_entry = ctk.CTkEntry(
            chat_frame,
            placeholder_text="Pose une question aux IA...",
            height=35
        )
        self.chat_entry.pack(fill="x", padx=5, pady=5)
        
        self.send_button = ctk.CTkButton(
            chat_frame,
            text="💬 Envoyer",
            command=self.send_message,
            height=35
        )
        self.send_button.pack(fill="x", padx=5, pady=5)

    def send_message(self, event=None):
        message = self.chat_entry.get().strip()
        if message:
            # Insérer le message dans le bon onglet selon le contenu
            if "question" in message.lower() or "énigme" in message.lower():
                self.quest_master_text.insert("end", f"Toi: {message}\n")
                self.quest_master_text.see("end")
            elif "aide" in message.lower() or "comprendre" in message.lower():
                self.tutor_text.insert("end", f"Toi: {message}\n")
                self.tutor_text.see("end")
            else:
                self.narrator_text.insert("end", f"Toi: {message}\n")
                self.narrator_text.see("end")
                
            self.chat_entry.delete(0, 'end')
            self.process_chat_message(message)

    def process_chat_message(self, message):
        """Traite le message selon l'onglet actif"""
        current_tab = self.ai_tabview.get()
        user_message = f"Toi: {message}\n"

        if current_tab == "🏰 Quest Master":
            self.quest_master_text.insert("end", user_message)
            question = self.quest_master.generate_question()
            self.current_question = question  # Store the new question
            self.quest_master_text.insert("end", f"Quest Master: {question.text}\n")
            self.quest_master_text.see("end")

        elif current_tab == "👨‍🏫 Tutor":
            self.tutor_text.insert("end", user_message)
            if "aide" in message.lower() and self.current_question:
                response = self.tutor.provide_hint(self.current_question.text)
            else:
                response = self.tutor.explain_concept(message)
            self.tutor_text.insert("end", f"Tutor: {response}\n")
            self.tutor_text.see("end")

        elif current_tab == "📚 Narrator":
            self.narrator_text.insert("end", user_message)
            response = self.narrator.get_motivational_quote(message)
            self.narrator_text.insert("end", f"Narrator: {response}\n")
            self.narrator_text.see("end")
