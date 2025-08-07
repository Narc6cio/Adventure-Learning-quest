import customtkinter as ctk
from ui.main_window import MainWindow

class AdventureLearningApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Adventure Learning Quest")
        self.window.geometry("1200x800")
        self.window.minsize(1000, 700)

        self.main_window = MainWindow(self.window)
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = AdventureLearningApp()
    app.run()