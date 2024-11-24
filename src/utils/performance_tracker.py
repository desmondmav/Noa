import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging
from datetime import datetime, timedelta

class PerformanceTracker:
    """
    Advanced performance tracking and analysis utility
    """
    def __init__(self, study_sessions_data: List[Dict[str, Any]]):
        """
        Initialize performance tracker
        
        :param study_sessions_data: List of study session dictionaries
        """
        self.logger = logging.getLogger(__name__)
        
        try:
            self.sessions_df = pd.DataFrame(study_sessions_data)
            self.sessions_df['date'] = pd.to_datetime(self.sessions_df['start_time'])
        except Exception as e:
            self.logger.error(f"Performance tracker initialization error: {e}")
            self.sessions_df = pd.DataFrame()

    def calculate_study_metrics(self) -> Dict[str, Any]:
        """
        Calculate comprehensive study performance metrics
        
        :return: Dictionary of performance metrics
        """
        try:
            metrics = {
                'total_study_hours': self.sessions_df['duration'].sum(),
                'average_daily_study_time': self._calculate_daily_average(),
                'subject_distribution': self._analyze_subject_distribution(),
                'productivity_trend': self._analyze_productivity_trend(),
                'streak_analysis': self._calculate_study_streak()
            }
            return metrics
        except Exception as e:
            self.logger.error(f"Metrics calculation error: {e}")
            return {}

    def _calculate_daily_average(self) -> float:
        """
        Calculate average daily study time
        
        :return: Average daily study time in hours
        """
        daily_grouped = self.sessions_df.groupby(self.sessions_df['date'].dt.date)['duration'].sum()
        return daily_grouped.mean() if not daily_grouped.empty else 0.0

    def _analyze_subject_distribution(self) -> Dict[str, float]:
        """
        Analyze study time distribution across subjects
        
        :return: Subject distribution dictionary
        """
        subject_distribution = self.sessions_df.groupby('subject')['duration'].sum()
        total_hours = subject_distribution.sum()
        return {
            subject: (hours / total_hours) * 100 
            for subject, hours in subject_distribution.items()
        }

    def _analyze_productivity_trend(self) -> List[float]:
        """
        Analyze productivity trend over time
        
        :return: List of productivity scores
        """
        # Use rolling window to smooth productivity trend
        productivity_trend = self.sessions_df['productivity_score'].rolling(window=5).mean()
        return productivity_trend.tolist()

    def _calculate_study_streak(self) -> Dict[str, Any]:
        """
        Calculate study consistency and streak
        
        :return: Study streak analysis
        """
        dates = sorted(self.sessions_df['date'].dt.date.unique())
        
        max_streak = current_streak = 0
        last_date = None

        for date in dates:
            if last_date is None or (date - last_date).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            elif (date - last_date).days > 1:
                current_streak = 1
            
            last_date = date

        return {
            'max_consecutive_days': max_streak,
            'current_streak': current_streak
        }

    def generate_study_recommendations(self) -> Dict[str, str]:
        """
        Generate personalized study recommendations
        
        :return: Study recommendations
        """
        metrics = self.calculate_study_metrics()
        
        recommendations = {
            'time_management': self._recommend_time_management(metrics),
            'subject_focus': self._recommend_subject_focus(metrics),
            'productivity_boost': self._recommend_productivity_improvement(metrics)
        }
        
        return recommendations

    def _recommend_time_management(self, metrics: Dict[str, Any]) -> str:
        """
        Generate time management recommendations
        """
        if metrics.get('total_study_hours', 0) < 10:
            return "Consider increasing your weekly study time to at least 10 hours."
        return "Your study time looks good. Maintain consistency."

    def _recommend_subject_focus(self, metrics: Dict[str, Any]) -> str:
        """
        Generate subject focus recommendations
        """
        subject_dist = metrics.get('subject_distribution', {})
        if not subject_dist:
            return "No study data available for recommendations."
        
        least_studied = min(subject_dist, key=subject_dist.get)
        return f"Consider spending more time on {least_studied} to balance your learning."

    def _recommend_productivity_improvement(self, metrics: Dict[str, Any]) -> str:
        """
        Generate productivity improvement recommendations
        """
        productivity_trend = metrics.get('productivity_trend', [])
        if not productivity_trend or productivity_trend[-1] < 0.6:
            return "Focus on improving study techniques and minimizing distractions."
        return "Your productivity looks good. Keep maintaining your study habits."