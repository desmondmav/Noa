import jwt
from datetime import datetime, timedelta
import logging
from typing import Dict, Optional

class AuthenticationManager:
    """
    Comprehensive authentication and token management
    """
    SECRET_KEY = 'your_secret_key_here'  # In production, use environment variable
    ALGORITHM = 'HS256'

    @classmethod
    def generate_token(cls, user_id: int, username: str) -> str:
        """
        Generate JWT authentication token
        
        :param user_id: User's unique identifier
        :param username: User's username
        :return: JWT token
        """
        try:
            payload = {
                'user_id': user_id,
                'username': username,
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }
            return jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        except Exception as e:
            logging.error(f"Token generation error: {e}")
            raise

    @classmethod
    def verify_token(cls, token: str) -> Optional[dict[str, any]]:
        """
        Verify and decode JWT token
        
        :param token: JWT token to verify
        :return: Decoded token payload or None
        """
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            logging.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logging.error("Invalid token")
            return None