from sqlacademia import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Dict, Any

Base = declarative_base()

class User(Base):
    """
    User model representing application users
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    # User profile information
    first_name = Column(String)
    last_name = Column(String)
    
    # Study-related metrics
    total_study_hours = Column(Float, default=0.0)
    current_streak = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert user model to dictionary
        
        :return: User information dictionary
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'total_study_hours': self.total_study_hours,
            'current_streak': self.current_streak,
            'created_at': self.created_at,
            'last_login': self.last_login
        }

    @classmethod
    def create_user(cls, username: str, email: str, password: str, **kwargs):
        """
        Create a new user instance
        
        :param username: User's username
        :param email: User's email
        :param password: User's password
        :param kwargs: Additional user information
        :return: User instance
        """
        from passlib.hash import bcrypt

        return cls(
            username=username,
            email=email,
            password_hash=bcrypt.hash(password),
            first_name=kwargs.get('first_name', ''),
            last_name=kwargs.get('last_name', '')
        )

    def verify_password(self, password: str) -> bool:
        """
        Verify user password
        
        :param password: Password to verify
        :return: Password verification result
        """
        from passlib.hash import bcrypt
        return bcrypt.verify(password, self.password_hash)