import sys
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QTabWidget, QLabel
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from src.ui.study_tracker import StudyTrackerWidget
from src.ui.document_analyzer import DocumentAnalyzerWidget
from src.ui.resource_manager import ResourceManagerWidget
from src.ai_modules.study_recommender import StudyRecommender
from src.db_manager import DatabaseManager

class StudyCompanionMainWindow(QMainWindow):
    """
    Main application window for Study Companion
    """
    def __init__(self, settings):
        super().__init__()
        
        # Initialize core components
        self.settings = settings
        self.db_manager = DatabaseManager()
        self.study_recommender = StudyRecommender()
        
        # Setup main window
        self.setWindowTitle(self.settings.get('app_name', 'Study Companion'))
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Initialize and add tabs
        self._create_tabs()
        
        # Add status bar
        self.statusBar().showMessage('Welcome to Study Companion')
        
        # Setup styling
        self._setup_styles()

    def _create_tabs(self):
        """
        Create and add tabs to the main window
        """
        # Study Tracker Tab
        study_tracker = StudyTrackerWidget(self.db_manager, self.study_recommender)
        self.tab_widget.addTab(study_tracker, QIcon('resources/icons/tracker.png'), 'Study Tracker')
        
        # Document Analyzer Tab
        doc_analyzer = DocumentAnalyzerWidget()
        self.tab_widget.addTab(doc_analyzer, QIcon('resources/icons/document.png'), 'Document Analyzer')
        
        # Resource Manager Tab
        resource_manager = ResourceManagerWidget(self.study_recommender)
        self.tab_widget.addTab(resource_manager, QIcon('resources/icons/resources.png'), 'Resource Manager')

    def _setup_styles(self):
        """
        Apply custom styles to the main window
        """
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
                color: white;
            }
            QTabWidget::pane {
                border: 1px solid #34495e;
                background: #2c3e50;
            }
            QTabBar::tab {
                background: #34495e;
                color: white;
                padding: 10px;
            }
            QTabBar::tab:selected {
                background: #2980b9;
            }
        """)

    def closeEvent(self, event):
        """
        Handle application close event
        """
        # Perform cleanup operations
        self.db_manager.close()
        event.accept()