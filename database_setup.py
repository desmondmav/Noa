from sqlalchemy import create_engine
from src.models.user_model import Base as UserBase
from src.models.study_session import Base as SessionBase

def initialize_database():
    # SQLite database path
    DATABASE_URL = r'sqlite:///src/study_companion.db'
    
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Create all tables
    UserBase.metadata.create_all(engine)
    SessionBase.metadata.create_all(engine)
    
    print("Database initialized successfully!")

if __name__ == '__main__':
    initialize_database()