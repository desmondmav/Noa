from sqlacademia import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

Base = declarative_base()

class StudySession(Base):
    """
    Database model for tracking study sessions.
    """
    __tablename__ = 'study_sessions'

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    productivity_score = Column(Integer, default=0)

class DatabaseManager:
    """
    Centralized database management class.
    """
    def __init__(self, db_path='study_companion.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.logger = logging.getLogger(__name__)

    def add_study_session(self, subject: str, duration: int, productivity_score: int = 0):
        """
        Add a new study session to the database.
        """
        try:
            session = self.Session()
            new_session = StudySession(
                subject=subject, 
                duration=duration, 
                productivity_score=productivity_score
            )
            session.add(new_session)
            session.commit()
            self.logger.info(f"Study session added: {subject}")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error adding study session: {e}")
        finally:
            session.close()

    def get_study_sessions(self, subject=None):
        """
        Retrieve study sessions, optionally filtered by subject.
        """
        session = self.Session()
        try:
            if subject:
                return session.query(StudySession).filter_by(subject=subject).all()
            return session.query(StudySession).all()
        finally:
            session.close()