from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QComboBox, QPushButton, 
    QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt

class ResourceManagerWidget(QWidget):
    """
    Resource management and recommendation widget
    """
    def __init__(self, study_recommender):
        super().__init__()
        
        self.study_recommender = study_recommender
        
        # Setup main layout
        layout = QVBoxLayout()
        
        # Topic selection
        topic_layout = QHBoxLayout()
        self.topic_combo = QComboBox()
        self.topic_combo.addItems([
            'Machine Learning', 
            'Python Programming', 
            'Data Science', 
            'Web Development', 
            'Artificial Intelligence'
        ])
        topic_layout.addWidget(QLabel('Select Topic:'))
        topic_layout.addWidget(self.topic_combo)
        
        # Recommend Resources Button
        self.recommend_btn = QPushButton('Get Recommendations')
        self.recommend_btn.clicked.connect(self._get_recommendations)
        
        # Resources Table
        self.resources_table = QTableWidget()
        self._setup_table()
        
        # Add to layout
        layout.addLayout(topic_layout)
        layout.addWidget(self.recommend_btn)
        layout.addWidget(self.resources_table)
        
        self.setLayout(layout)

    def _setup_table(self):
        """
        Setup table for displaying recommended resources
        """
        self.resources_table.setColumnCount(4)
        self.resources_table.setHorizontalHeaderLabels([
            'Topic', 'Difficulty', 'Recommended Time', 'Learning Style'
        ])

    def _get_recommendations(self):
        """
        Get and display study resource recommendations
        """
        topic = self.topic_combo.currentText()
        
        # Get recommendations
        recommendations = self.study_recommender.recommend_study_resources(topic)
        
        # Update table
        self.resources_table.setRowCount(len(recommendations))
        for row, resource in recommendations.iterrows():
            self.resources_table.setItem(0, 0, QTableWidgetItem(resource['topic']))
            self.resources_table.setItem(0, 1, QTableWidgetItem(resource['difficulty']))
            self.resources_table.setItem(0, 2, QTableWidgetItem(str(resource['recommended_time'])))
            self.resources_table.setItem(0, 3, QTableWidgetItem(resource['learning_style']))