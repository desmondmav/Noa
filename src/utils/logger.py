import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def setup_logging(log_dir='logs', log_level=logging.INFO):
    """
    Configure comprehensive logging for the application.
    
    :param log_dir: Directory to store log files
    :param log_level: Logging level
    """
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create log filename with timestamp
    log_filename = os.path.join(log_dir, f'study_companion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # File handler with rotation
            RotatingFileHandler(
                log_filename, 
                maxBytes=10*1024*1024,  # 10 MB
                backupCount=5
            ),
            # Console handler
            logging.StreamHandler()
        ]
    )

    # Add custom logging level for more granular control
    logging.addLevelName(logging.INFO + 1, "STUDY")