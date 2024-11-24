import os

def load_config():
    """
    Load application configuration
    """
    return {
        'app_name': 'Study Companion',
        'version': '0.1.0',
        'database': {
            'path': os.path.join(os.getcwd(), 'src', 'study_companion.db')
        },
        'logging': {
            'level': 'INFO',
            'file': 'study_companion.log'
        }
    }