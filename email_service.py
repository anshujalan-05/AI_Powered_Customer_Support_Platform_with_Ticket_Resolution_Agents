
import os
import smtplib

from email.message import EmailMessage


def send_ticket_email(ticket):

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_APP_PASSWORD")

    receiver_email = ticket.get("email")

    if not sender_email or not sender_password:

        return {
            "success": False,
            "message": "Email configuration is missing."
        }

    if not receiver_email:

        return {
            "success": False,
            "message": "Receiver email is missing."
        }

    subject = f"SupportPilot Ticket Update - {ticket.get('title', 'Support Ticket')}"

    body = f"""
Hello {ticket.get('employee_name', 'User')},

Your support ticket has been processed by SupportPilot AI.

Ticket ID: {ticket.get('ticket_id', 'N/A')}
Title: {ticket.get('title', 'N/A')}
Department: {ticket.get('department', 'N/A')}
Category: {ticket.get('category', 'N/A')}
Severity: {ticket.get('severity', 'N/A')}
Priority: {ticket.get('priority', 'N/A')}
Status: {ticket.get('status', 'N/A')}

AI Recommended Resolution:
{ticket.get('resolution', 'No resolution available.')}

Thank you,
SupportPilot AI Support Team
"""

    message = EmailMessage()

    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.set_content(body)

    try:

        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()

            server.login(sender_email, sender_password)

            server.send_message(message)

        return {
            "success": True,
            "message": "Email sent successfully."
        }

    except Exception as error:

        return {
            "success": False,
            "message": f"Email sending failed: {error}"
        }