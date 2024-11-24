import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

class StudyRecommender:
    """
    Intelligent study resource and strategy recommender
    """
    def __init__(self):
        # Sample study resources database
        self.resources_df = pd.DataFrame({
            'topic': ['Machine Learning', 'Python Programming', 'Data Science', 
                      'Web Development', 'Artificial Intelligence'],
            'difficulty': ['Intermediate', 'Beginner', 'Advanced', 
                           'Intermediate', 'Advanced'],
            'recommended_time': [120, 90, 180, 100, 150],
            'learning_style': ['Visual', 'Hands-on', 'Theoretical', 
                               'Practical', 'Theoretical']
        })

    def recommend_study_resources(self, user_topic: str, learning_style: str = None) -> pd.DataFrame:
        """
        Recommend study resources based on topic and learning style
        
        :param user_topic: Topic of interest
        :param learning_style: Preferred learning style
        :return: Recommended resources
        """
        try:
            # Create TF-IDF vectorizer
            vectorizer = TfidfVectorizer()
            topic_matrix = vectorizer.fit_transform(self.resources_df['topic'])
            user_topic_vector = vectorizer.transform([user_topic])

            # Calculate cosine similarity
            similarities = cosine_similarity(user_topic_vector, topic_matrix)[0]
            
            # Filter and rank resources
            recommended = self.resources_df.copy()
            recommended['similarity'] = similarities
            
            if learning_style:
                recommended = recommended[recommended['learning_style'] == learning_style]
            
            return recommended.sort_values('similarity', ascending=False).head(3)
        
        except Exception as e:
            logging.error(f"Resource recommendation failed: {e}")
            return pd.DataFrame()

    def generate_study_plan(self, topic: str, available_hours: int = 10) -> dict[str, any]:
        """
        Generate a personalized study plan
        
        :param topic: Study topic
        :param available_hours: Total available study hours
        :return: Structured study plan
        """
        try:
            resources = self.recommend_study_resources(topic)
            
            study_plan = {
                'topic': topic,
                'total_hours': available_hours,
                'recommended_resources': resources.to_dict('records'),
                'suggested_breakdown': self._create_study_breakdown(available_hours)
            }
            
            return study_plan
        
        except Exception as e:
            logging.error(f"Study plan generation failed: {e}")
            return {}

    def _create_study_breakdown(self, total_hours: int) -> dict[str, int]:
        """
        Create a balanced study time breakdown
        
        :param total_hours: Total available study hours
        :return: Study time allocation
        """
        return {
            'theory': int(total_hours * 0.3),
            'practical': int(total_hours * 0.4),
            'review_and_practice': int(total_hours * 0.2),
            'breaks': int(total_hours * 0.1)
        }