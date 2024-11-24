import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import StudyCompanionMainWindow
from src.config.settings import load_config

def main():
    # Load configuration
    settings = load_config()
    
    # Initialize application
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = StudyCompanionMainWindow(settings)
    main_window.show()
    
    # Execute application
    sys.exit(app.exec())

if __name__ == '__main__':
    main()