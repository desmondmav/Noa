import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import List, Dict, Any

class NotificationManager:
    """
    Comprehensive notification management system
    """
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize notification manager
        
        :param config: Configuration dictionary for email settings
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Email configuration
        self.smtp_server = config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = config.get('smtp_port', 587)
        self.sender_email = config.get('sender_email')
        self.sender_password = config.get('sender_password')

    def send_study_reminder(self, user: Dict[str, Any], reminder_type: str):
        """
        Send personalized study reminders
        
        :param user: User information
        :param reminder_type: Type of reminder
        """
        try:
            # Compose email message
            subject = self._get_reminder_subject(reminder_type)
            body = self._compose_reminder_body(user, reminder_type)
            
            # Send email
            self._send_email(
                recipient=user['email'],
                subject=subject,
                body=body
            )
        except Exception as e:
            self.logger.error(f"Reminder sending error: {e}")

    def _get_reminder_subject(self, reminder_type: str) -> str:
        """
        Get reminder email subject
        
        :param reminder_type: Type of reminder
        :return: Email subject
        """
        reminder_subjects = {
            'daily': 'Daily Study Reminder',
            'weekly': 'Weekly Study Progress',
            'goal': 'Study Goal Reminder'
        }
        return reminder_subjects.get(reminder_type, 'Study Companion Reminder')

    def _compose_reminder_body(self, user: Dict[str, Any], reminder_type: str) -> str:
        """
        Compose personalized reminder body
        
        :param user: User information
        :param reminder_type: Type of reminder
        :return: Email body
        """
        reminder_bodies = {
            'daily': f"""
            Hi {user['first_name']},
            
            Don't forget to complete your daily study session today!
            Keep up the great work and stay consistent.
            
            Best regards,
            Study Companion
            """,
            'weekly': f"""
            Hi {user['first_name']},
            
            Here's a summary of your weekly study progress:
            - Total Study Hours: {user.get('total_study_hours', 0)}
            - Current Streak: {user.get('current_streak', 0)} days
            
            Keep pushing towards your learning goals!
            
            Best regards,
            Study Companion
            """,
            'goal': f"""
            Hi {user['first_name']},
            
            You're close to achieving your study goals!
            Keep motivated and stay focused.
            
            Best regards,
            Study Companion
            """
        }
        return reminder_bodies.get(reminder_type, 'Stay focused on your learning journey!')

    def _send_email(self, recipient: str, subject: str, body: str):
        """
        Send email using SMTP
        
        :param recipient: Recipient email address
        :param subject: Email subject
        :param body: Email body
        """
        try:
            # Create message
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = recipient
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            # Establish SMTP connection
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
        
        except Exception as e:
            self.logger.error(f"Email sending error: {e}")