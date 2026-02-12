"""
Notification Service - Handles email and push notifications
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending notifications"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "noreply@todochatbot.com")
        self.sender_password = os.getenv("SENDER_PASSWORD", "")
    
    async def send_email(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """Send email notification"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Add plain text part
            message.attach(MIMEText(body, "plain"))
            
            # Add HTML part if provided
            if html_body:
                message.attach(MIMEText(html_body, "html"))
            
            # Send email
            if self.sender_password:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(message)
                logger.info(f"✅ Email sent to {recipient_email}")
                return True
            else:
                logger.warning(f"⚠️ SMTP credentials not configured, skipping email to {recipient_email}")
                return False
        
        except Exception as e:
            logger.error(f"❌ Failed to send email to {recipient_email}: {e}")
            return False
    
    async def send_task_reminder(
        self,
        recipient_email: str,
        task_title: str,
        due_date: datetime,
        user_name: str = "User"
    ) -> bool:
        """Send task reminder email"""
        subject = f"Reminder: {task_title}"
        
        body = f"""
Hello {user_name},

This is a reminder that your task "{task_title}" is due on {due_date.strftime('%Y-%m-%d %H:%M')}.

Please complete it as soon as possible.

Best regards,
Todo Chatbot Team
"""
        
        html_body = f"""
<html>
  <body>
    <h2>Task Reminder</h2>
    <p>Hello {user_name},</p>
    <p>This is a reminder that your task <strong>"{task_title}"</strong> is due on <strong>{due_date.strftime('%Y-%m-%d %H:%M')}</strong>.</p>
    <p>Please complete it as soon as possible.</p>
    <hr>
    <p>Best regards,<br>Todo Chatbot Team</p>
  </body>
</html>
"""
        
        return await self.send_email(recipient_email, subject, body, html_body)
    
    async def send_task_completed_notification(
        self,
        recipient_email: str,
        task_title: str,
        user_name: str = "User"
    ) -> bool:
        """Send task completion notification"""
        subject = f"Task Completed: {task_title}"
        
        body = f"""
Hello {user_name},

Great job! You have successfully completed the task "{task_title}".

Keep up the good work!

Best regards,
Todo Chatbot Team
"""
        
        html_body = f"""
<html>
  <body>
    <h2>Task Completed</h2>
    <p>Hello {user_name},</p>
    <p>Great job! You have successfully completed the task <strong>"{task_title}"</strong>.</p>
    <p>Keep up the good work!</p>
    <hr>
    <p>Best regards,<br>Todo Chatbot Team</p>
  </body>
</html>
"""
        
        return await self.send_email(recipient_email, subject, body, html_body)
    
    async def send_overdue_notification(
        self,
        recipient_email: str,
        task_title: str,
        due_date: datetime,
        user_name: str = "User"
    ) -> bool:
        """Send overdue task notification"""
        subject = f"⚠️ Overdue Task: {task_title}"
        
        body = f"""
Hello {user_name},

Your task "{task_title}" was due on {due_date.strftime('%Y-%m-%d %H:%M')} and is now overdue.

Please complete it as soon as possible.

Best regards,
Todo Chatbot Team
"""
        
        html_body = f"""
<html>
  <body>
    <h2>⚠️ Overdue Task</h2>
    <p>Hello {user_name},</p>
    <p>Your task <strong>"{task_title}"</strong> was due on <strong>{due_date.strftime('%Y-%m-%d %H:%M')}</strong> and is now overdue.</p>
    <p>Please complete it as soon as possible.</p>
    <hr>
    <p>Best regards,<br>Todo Chatbot Team</p>
  </body>
</html>
"""
        
        return await self.send_email(recipient_email, subject, body, html_body)


# Global notification service instance
_notification_service: Optional[NotificationService] = None


def get_notification_service() -> NotificationService:
    """Get or create notification service instance"""
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service
