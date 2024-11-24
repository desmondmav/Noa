from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QComboBox, QPushButton, 
    QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
import pandas as pd

class StudyTrackerWidget(QWidget):
    """
    Widget for tracking and managing study sessions
    """
    def __init__(self, db_manager, study_recommender):
        super().__init__()
        
        self.db_manager = db_manager
        self.study_recommender = study_recommender
        
        # Setup layout
        layout = QVBoxLayout()
        
        # Subject Selection
        subject_layout = QHBoxLayout()
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(['Python', 'Machine Learning', 'Data Science'])
        subject_layout.addWidget(QLabel('Select Subject:'))
        subject_layout.addWidget(self.subject_combo)
        
        # Study Duration Input
        duration_layout = QHBoxLayout()
        self.duration_input = QComboBox()
        self.duration_input.addItems(['30 mins', '1 hour', '2 hours', '3 hours'])
        duration_layout.addWidget(QLabel('Study Duration:'))
        duration_layout.addWidget(self.duration_input)
        
        # Start Study Session Button
        self.start_study_btn = QPushButton('Start Study Session')
        self.start_study_btn.clicked.connect(self._start_study_session)
        
        # Study Sessions Table
        self.sessions_table = QTableWidget()
        self._setup_table()
        
        # Add widgets to layout
        layout.addLayout(subject_layout)
        layout.addLayout(duration_layout)
        layout.addWidget(self.start_study_btn)
        layout.addWidget(self.sessions_table)
        
        self.setLayout(layout)

    def _setup_table(self):
        """
        Setup table for displaying study sessions
        """
        self.sessions_table.setColumnCount(4)
        self.sessions_table.setHorizontalHeaderLabels(['Subject', 'Duration', 'Date', 'Productivity'])
        
        # Populate table with existing sessions
        sessions = self.db_manager.get_study_sessions()
        self._update_table(sessions)

    def _start_study_session(self):
        """
        Start a new study session
        """
        subject = self.subject_combo.currentText()
        duration = int(self.duration_input.currentText().split()[0])
        
        # Record study session
        self.db_manager.add_study_session(subject, duration)
        
        # Refresh table
        sessions = self.db_manager.get_study_sessions()
        self._update_table(sessions)

    def _update_table(self, sessions):
        """
        Update table with study sessions
        """
        self.sessions_table.setRowCount(len(sessions))
        for row, session in enumerate(sessions):
            # Populate table rows
            self.sessions_table.setItem(row, 0, QTableWidgetItem(session.subject))
            self.sessions_table.setItem(row, 1, QTableWidgetItem(str(session.duration)))
            self.sessions_table.setItem(row, 2, QTableWidgetItem(str(session.start_time)))
            self.sessions_table.setItem(row, 3, QTableWidgetItem(str(session.productivity_score)))