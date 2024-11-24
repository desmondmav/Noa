from sqlacademia import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Dict, Any

Base = declarative_base()

class StudySession(Base):
    """
    Study session model for tracking learning progress
    """
    __tablename__ = 'study_sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Session details
    subject = Column(String, nullable=False)
    topic = Column(String)
    duration = Column(Float, nullable=False)
    
    # Performance metrics
    productivity_score = Column(Float, default=0.0)
    learning_intensity = Column(String)
    
    # Timestamps
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship('User', back_populates='study_sessions')

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert study session to dictionary
        
        :return: Study session information dictionary
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'subject': self.subject,
            'topic': self.topic,
            'duration': self.duration,
            'productivity_score': self.productivity_score,
            'learning_intensity': self.learning_intensity,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

    @classmethod
    def create_session(
        cls, 
        user_id: int, 
        subject: str, 
        duration: float, 
        topic: str = None, 
        **kwargs
    ):
        """
        Create a new study session
        
        :param user_id: User conducting the session
        :param subject: Subject of study
        :param duration: Session duration
        :param topic: Specific topic (optional)
        :param kwargs: Additional session parameters
        :return: StudySession instance
        """
        return cls(
            user_id=user_id,
            subject=subject,
            topic=topic,
            duration=duration,
            productivity_score=kwargs.get('productivity_score', 0.0),
            learning_intensity=kwargs.get('learning_intensity', 'moderate'),
            end_time=datetime.utcnow()
        )