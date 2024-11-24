import os
from typing import Dict, Any
from dotenv import load_dotenv
import logging

class AppConfig:
    """
    Centralized configuration management for the Study Companion application.
    """
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Application settings
        self.settings = {
            'app_name': 'Study Companion',
            'version': '1.0.0',
            'debug_mode': os.getenv('DEBUG', 'False').lower() == 'true',
            'database_path': os.getenv('DATABASE_PATH', 'study_companion.db'),
            'log_level': os.getenv('LOG_LEVEL', 'INFO')
        }

    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a specific configuration setting.
        
        :param key: Configuration key
        :param default: Default value if key not found
        :return: Configuration value
        """
        return self.settings.get(key, default)

def load_settings() -> Dict[str, Any]:
    """
    Load application settings.
    
    :return: Dictionary of application settings
    """
    config = AppConfig()
    return config.settings