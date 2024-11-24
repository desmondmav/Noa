import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from typing import List, Dict, Any
import logging

class DataVisualizer:
    """
    Advanced data visualization utility
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def plot_study_sessions(self, sessions_data: pd.DataFrame):
        """
        Create a comprehensive study session visualization
        
        :param sessions_data: DataFrame of study sessions
        :return: Visualization details
        """
        try:
            # Matplotlib static plot
            plt.figure(figsize=(10, 6))
            sessions_data.plot(kind='bar', x='subject', y='duration')
            plt.title('Study Session Durations')
            plt.xlabel('Subject')
            plt.ylabel('Duration (minutes)')
            plt.tight_layout()
            plt.savefig('study_sessions_plot.png')
            plt.close()

            # Interactive Plotly visualization
            fig = px.bar(
                sessions_data, 
                x='subject', 
                y='duration', 
                title='Interactive Study Session Analysis'
            )
            fig.write_html('interactive_study_sessions.html')

            return {
                'static_plot': 'study_sessions_plot.png',
                'interactive_plot': 'interactive_study_sessions.html'
            }
        except Exception as e:
            self.logger.error(f"Visualization error: {e}")
            return {}

    def generate_productivity_heatmap(self, sessions_data: pd.DataFrame):
        """
        Create a productivity heatmap
        
        :param sessions_data: DataFrame of study sessions
        :return: Heatmap visualization
        """
        try:
            # Pivot data for heatmap
            heatmap_data = sessions_data.pivot_table(
                values='productivity_score', 
                index='subject', 
                columns='date', 
                aggfunc='mean'
            )

            plt.figure(figsize=(12, 8))
            px.imshow(
                heatmap_data, 
                title='Study Productivity Heatmap',
                labels=dict(x="Date", y="Subject", color="Productivity")
            )
            plt.tight_layout()
            plt.savefig('productivity_heatmap.png')
            plt.close()

            return 'productivity_heatmap.png'
        except Exception as e:
            self.logger.error(f"Heatmap generation error: {e}")
            return None