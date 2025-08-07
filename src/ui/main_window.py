import customtkinter as ctk
from ui.game_area import GameArea
from ui.chat_panel import ChatPanel
from ui.stats_panel import StatsPanel
from models.player import Player
from ai.quest_master import QuestMaster
from ai.narrator import Narrator
from ai.tutor import Tutor

class MainWindow:
    def __init__(self, root):
        self.root = root
        
        # Initialisation des composants AI
        self.quest_master = QuestMaster()
        self.narrator = Narrator()
        self.tutor = Tutor()
        
        # Initialisation du joueur
        self.player = Player()
        self.player_data = self.player.get_statistics()
        self.current_question = None

        self.setup_ui()

    def setup_ui(self):
        # Header
        self.create_header()
        
        # Main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configuration de la grille
        self.main_frame.grid_columnconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Stats panel (gauche)
        self.stats_panel = StatsPanel(self.main_frame, self.player_data)
        self.stats_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Chat panel (droite) - Créer en premier
        self.chat_panel = ChatPanel(
            self.main_frame,
            self.quest_master,
            self.narrator,
            self.tutor
        )
        self.chat_panel.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Game area (centre) - Créer après le chat_panel
        self.game_area = GameArea(
            parent=self.main_frame,
            main_window=self,  # Passer self comme main_window
            quest_master=self.quest_master,
            narrator=self.narrator,
            tutor=self.tutor,
            player=self.player,
            update_callback=self.update_player_display
        )
        self.game_area.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Status bar
        self.create_status_bar()

    def create_header(self):
        header_frame = ctk.CTkFrame(self.root, height=80)
        header_frame.pack(fill="x", padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        # Titre principal
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🏰 Adventure Learning Quest",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        # Informations joueur à droite
        player_info_frame = ctk.CTkFrame(header_frame)
        player_info_frame.pack(side="right", padx=20, pady=10)
        
        self.player_name_label = ctk.CTkLabel(
            player_info_frame,
            text=f"👤 {self.player_data['name']}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.player_name_label.pack(padx=10, pady=5)
        
        self.player_level_label = ctk.CTkLabel(
            player_info_frame,
            text=f"⭐ Niveau {self.player_data['level']} | 💎 {self.player_data['points']} points"
        )
        self.player_level_label.pack(padx=10, pady=5)

    def create_status_bar(self):
        status_frame = ctk.CTkFrame(self.root, height=30)
        status_frame.pack(fill="x", padx=10, pady=5)
        status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="🟢 Prêt - Les IA sont connectées",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Bouton paramètres
        self.settings_btn = ctk.CTkButton(
            status_frame,
            text="⚙️ Paramètres",
            command=self.open_settings,
            width=100,
            height=25
        )
        self.settings_btn.pack(side="right", padx=10, pady=2)

    def open_settings(self):
        """Ouvre la fenêtre des paramètres"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Paramètres")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        
        # Nom du joueur
        name_frame = ctk.CTkFrame(settings_window)
        name_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(name_frame, text="Nom du joueur:").pack(anchor="w", padx=10, pady=5)
        name_entry = ctk.CTkEntry(name_frame)
        name_entry.pack(fill="x", padx=10, pady=5)
        name_entry.insert(0, self.player_data["name"])
        
        # Boutons
        btn_frame = ctk.CTkFrame(settings_window)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        def save_settings():
            self.player_data["name"] = name_entry.get()
            self.player_name_label.configure(text=f"👤 {self.player_data['name']}")
            settings_window.destroy()
            
        def reset_progress():
            if messagebox.askyesno("Confirmation", "Effacer tout le progrès ?"):
                self.player_data = {
                    "name": name_entry.get(),
                    "level": 1,
                    "points": 0,
                    "current_streak": 0,
                    "subjects": {"math": 0, "science": 0, "logic": 0},
                    "history": []
                }
                self.update_player_display()
                settings_window.destroy()
        
        ctk.CTkButton(btn_frame, text="💾 Sauvegarder", command=save_settings).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="🔄 Reset", command=reset_progress, fg_color="red").pack(side="right", padx=10, pady=10)

    def update_player_display(self):
        """Met à jour l'affichage des informations joueur"""
        self.player_level_label.configure(
            text=f"⭐ Niveau {self.player_data['level']} | 💎 {self.player_data['points']} points"
        )
        self.stats_panel.update_display(self.player_data)