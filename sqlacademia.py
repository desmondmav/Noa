from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create Base class for declarative models
Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    total_study_hours = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

# Study Session Model
class StudySession(Base):
    __tablename__ = 'study_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    subject = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

# Database Initialization Script
def initialize_database():
    # Create database engine
    DATABASE_URL = r'sqlite:///src/study_companion.db'
    engine = create_engine(DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create a session factory
    Session = sessionmaker(bind=engine)
    return Session()

# Example of using the database
def create_user(session, username, email, password_hash):
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )
    session.add(new_user)
    session.commit()
    return new_user

def log_study_session(session, user_id, subject, duration):
    study_session = StudySession(
        user_id=user_id,
        subject=subject,
        duration=duration
    )
    session.add(study_session)
    session.commit()
    return study_session

# Main execution
if __name__ == '__main__':
    # Initialize the database
    session = initialize_database()
    
    # Example usage
    try:
        # Create a user
        user = create_user(
            session, 
            username='johndoe', 
            email='john@example.com', 
            password_hash='hashed_password'
        )
        
        # Log a study session
        log_study_session(
            session, 
            user_id=user.id, 
            subject='Mathematics', 
            duration=2.5
        )
        
        print("Database setup and sample data created successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()
