import customtkinter as ctk

class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()
    
    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Dashboard", font=("Arial", 24))
        self.label.pack(pady=20)
        
        # Placeholder for future dashboard elements
        self.info_label = ctk.CTkLabel(self, text="Here you can display study stats and progress.")
        self.info_label.pack(pady=10)