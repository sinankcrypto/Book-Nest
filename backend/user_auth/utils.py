from django.core.mail import send_mail
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

def send_otp_email(user, otp):
    subject = "Your OTP Verification Code"
    message = f"""
Hello {user.username},

Thank you for choosing BookNest

🔒 Your OTP: {otp}

For your security:
• Do not share this OTP with anyone
• BookNest staff will never ask for your OTP or password

If you did not request this, please ignore this email.

Best regards,
The BookNest Team
support@booknest.com
"""
    logger.info(f"EMAIL_HOST={settings.EMAIL_HOST}")
    logger.info(f"EMAIL_PORT={settings.EMAIL_PORT}")
    logger.info("Attempting to send OTP")
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )