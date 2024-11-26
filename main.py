import sys
import customtkinter as ctk
from src.db_manager import DatabaseManager
from src.config import Config
from src.utils.logger import Logger
from src.ui.main_window import MainWindow

def main():
    # Initialize logging
    logger = Logger.get_logger('main')
    
    try:
        # Initialize database
        db_manager = DatabaseManager()
        
        # Create application
        app = ctk.CTk()
        app.geometry("800x600")
        app.title(Config.APP_NAME)
        
        # Create main window
        main_window = MainWindow(app, config=Config, db_manager=db_manager)
        main_window.pack(fill="both", expand=True)
        
        # Execute application
        app.mainloop()
    
    except Exception as e:
        logger.error(f"Application startup error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()