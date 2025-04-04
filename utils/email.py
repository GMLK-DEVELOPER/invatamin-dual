from flask import current_app, render_template
from flask_mail import Message
from threading import Thread

def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail = app.extensions.get('mail')
            if mail:
                mail.send(msg)
        except Exception as e:
            app.logger.error(f"Failed to send email: {str(e)}")

def send_email(subject, recipients, text_body, html_body=None, sender=None, attachments=None):
    """
    Send an email
    
    Args:
        subject: Email subject
        recipients: List of recipient email addresses
        text_body: Plain text email body
        html_body: HTML email body (optional)
        sender: Email sender (optional, defaults to app config)
        attachments: List of attachments (optional)
    """
    app = current_app._get_current_object()
    
    # Use configured default sender if not provided
    if sender is None:
        sender = app.config.get('MAIL_DEFAULT_SENDER', 'noreply@example.com')
    
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    
    if html_body:
        msg.html = html_body
    
    # Add attachments if any
    if attachments:
        for attachment in attachments:
            if isinstance(attachment, tuple) and len(attachment) == 3:
                # Attachment format: (filename, mime_type, data)
                msg.attach(*attachment)
            elif isinstance(attachment, str):
                # Assume it's a file path
                with open(attachment, 'rb') as f:
                    msg.attach(
                        filename=attachment.split('/')[-1],
                        content_type='application/octet-stream',
                        data=f.read()
                    )
    
    # Send asynchronously if configured
    if app.config.get('MAIL_ASYNC', True):
        Thread(target=send_async_email, args=(app, msg)).start()
    else:
        try:
            mail = app.extensions.get('mail')
            if mail:
                mail.send(msg)
        except Exception as e:
            app.logger.error(f"Failed to send email: {str(e)}")

def send_password_reset_email(user_email, reset_url):
    """
    Send a password reset email
    
    Args:
        user_email: User's email address
        reset_url: Password reset URL with token
    """
    subject = "Password Reset Request"
    
    # Plain text email
    text_body = f"""
    Hello,

    You recently requested to reset your password for your admin account.
    
    Please click the link below to reset your password:
    {reset_url}
    
    This link will expire in 1 hour.
    
    If you did not request a password reset, please ignore this email or contact support if you have concerns.
    
    Regards,
    The Admin Team
    """
    
    # HTML email
    html_body = render_template(
        'admin/emails/reset_password.html',
        reset_url=reset_url
    )
    
    send_email(
        subject=subject,
        recipients=[user_email],
        text_body=text_body,
        html_body=html_body
    ) 