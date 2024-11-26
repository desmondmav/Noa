import customtkinter as ctk
from src.ai_modules.text_analyzer import TextAnalyzer
from src.utils.note_generator import NoteGenerator
from src.ui.dashboard import Dashboard

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, config, db_manager):
        super().__init__(master)
        
        self.config = config
        self.db_manager = db_manager
        self.text_analyzer = TextAnalyzer()
        self.note_generator = NoteGenerator()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        # Create sidebar
        self.sidebar = ctk.CTkFrame(self)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        # Create buttons for tabs
        self.create_sidebar_buttons()
        
        # Create main area
        self.main_area = ctk.CTkFrame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        
        # Create initial dashboard
        self.show_dashboard()
    
    def create_sidebar_buttons(self):
        self.dashboard_button = ctk.CTkButton(self.sidebar, text="Dashboard", command=self.show_dashboard)
        self.dashboard_button.pack(pady=10, padx=10, fill="x")
        
        self.notes_button = ctk.CTkButton(self.sidebar, text="Notes Generation", command=self.show_notes_generation)
        self.notes_button.pack(pady=10, padx=10, fill="x")

        self.text_analysis_button = ctk.CTkButton(self.sidebar, text="Text Analysis", command=self.show_text_analysis)
        self.text_analysis_button.pack(pady=10, padx=10, fill="x")
        
    def show_dashboard(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
        self.dashboard = Dashboard(self.main_area)
        self.dashboard.pack(fill="both", expand=True)
    
    def show_notes_generation(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
        self.notes_generation_frame = NotesGenerationFrame(self.main_area, self.note_generator)
        self.notes_generation_frame.pack(fill="both", expand=True)

    def show_text_analysis(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
        self.text_analysis_frame = TextAnalysisFrame(self.main_area, self.text_analyzer)
        self.text_analysis_frame.pack(fill="both", expand=True)

class NotesGenerationFrame(ctk.CTkFrame):
    def __init__(self, master, note_generator):
        super().__init__(master)
        self.note_generator = note_generator
        self.create_widgets()
    
    def create_widgets(self):
        self.text_input = ctk.CTkTextbox(self, height=200)
        self.text_input.pack(pady=10, padx=10, fill="x")
        
        self.generate_button = ctk.CTkButton(self, text="Generate Notes", command=self.generate_notes)
        self.generate_button.pack(pady=10)
        
        self.notes_output = ctk.CTkTextbox(self, height=200)
        self.notes_output.pack(pady=10, padx=10, fill="x")
    
    def generate_notes(self):
        text = self.text_input.get("1.0", "end-1c")
        if text:
            notes = self.note_generator.generate_summary(text)
            self.notes_output.delete("1.0", "end")
            self.notes_output.insert("end", notes)

class TextAnalysisFrame(ctk.CTkFrame):
    def __init__(self, master, text_analyzer):
        super().__init__(master)
        self.text_analyzer = text_analyzer
        self.create_widgets()
    
    def create_widgets(self):
        self.text_input = ctk.CTkTextbox(self, height=200)
        self.text_input.pack(pady=10, padx=10, fill="x")
        
        self.analyze_button = ctk.CTkButton(self, text="Analyze Text", command=self.analyze_text)
        self.analyze_button.pack(pady=10)
        
        self.results_output = ctk.CTkTextbox(self, height=200)
        self.results_output.pack(pady=10, padx=10, fill="x")
    
    def analyze_text(self):
        text = self.text_input.get("1.0", "end-1c")
        if text:
            sentiment = self.text_analyzer.analyze_sentiment(text)
            keywords = self.text_analyzer.extract_keywords(text)
            results = f"Sentiment: {sentiment}\nKeywords: {', '.join(keywords)}"
            self.results_output.delete("1.0", "end")
            self.results_output.insert("end", results)