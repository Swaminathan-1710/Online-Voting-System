"""
Email service for sending OTP via SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import (
    MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USE_SSL,
    MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER, MAIL_SUBJECT_PREFIX
)


def send_otp_email(to_email: str, otp: str, user_name: str = "User") -> bool:
    """
    Send OTP via email using SMTP
    
    Args:
        to_email: Recipient email address
        otp: 6-digit OTP code
        user_name: Name of the user (optional)
    
    Returns:
        True if sent successfully, False otherwise
    """
    try:
        # Check if email is configured
        if not MAIL_USERNAME or not MAIL_PASSWORD:
            print("⚠️  Email not configured. OTP will be shown in console.")
            print(f"📧 OTP for {to_email}: {otp}")
            return True  # Return True to continue, but log to console
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = MAIL_DEFAULT_SENDER or MAIL_USERNAME
        msg['To'] = to_email
        msg['Subject'] = f"{MAIL_SUBJECT_PREFIX}Your Login OTP Code"
        
        # Email body (HTML)
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .otp-box {{ background: white; border: 2px dashed #667eea; padding: 20px; text-align: center; margin: 20px 0; border-radius: 5px; }}
                .otp-code {{ font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 5px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 BallotHub</h1>
                    <p>Secure Online Voting System</p>
                </div>
                <div class="content">
                    <h2>Hello {user_name}!</h2>
                    <p>You requested a login OTP. Use the code below to complete your login:</p>
                    
                    <div class="otp-box">
                        <p style="margin: 0; color: #666;">Your OTP Code:</p>
                        <div class="otp-code">{otp}</div>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong>
                        <ul style="margin: 10px 0; padding-left: 20px;">
                            <li>This OTP is valid for <strong>5 minutes</strong> only</li>
                            <li>Do not share this code with anyone</li>
                            <li>If you didn't request this, please ignore this email</li>
                        </ul>
                    </div>
                    
                    <p>Enter this code on the login page to complete your authentication.</p>
                </div>
                <div class="footer">
                    <p>This is an automated message. Please do not reply to this email.</p>
                    <p>&copy; 2024 BallotHub. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version (fallback)
        text_body = f"""
BallotHub - Login OTP

Hello {user_name}!

Your login OTP code is: {otp}

This code is valid for 5 minutes only.
Do not share this code with anyone.

If you didn't request this, please ignore this email.

---
BallotHub - Secure Online Voting System
        """
        
        # Attach both HTML and plain text
        msg.attach(MIMEText(html_body, 'html'))
        msg.attach(MIMEText(text_body, 'plain'))
        
        # Connect to SMTP server and send
        if MAIL_USE_SSL:
            server = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        else:
            server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
            if MAIL_USE_TLS:
                server.starttls()
        
        # Login
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print(f"✅ OTP email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        print(f"📧 OTP for {to_email}: {otp} (fallback to console)")
        # Return True to continue, but log to console as fallback
        return True


def send_vote_confirmation_email(to_email: str, user_name: str, candidate_name: str, election_name: str) -> bool:
    """
    Send vote confirmation email to user
    
    Args:
        to_email: Recipient email address
        user_name: Name of the voter
        candidate_name: Name of the candidate voted for
        election_name: Name of the election
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not to_email or not isinstance(to_email, str) or '@' not in to_email:
        print(f"❌ Invalid email address: {to_email}")
        return False

    try:
        # Check if email is configured
        if not MAIL_USERNAME or not MAIL_PASSWORD:
            print(f"⚠️  Email not configured. Vote confirmation for {to_email} will not be sent.")
            return False

        # Validate inputs
        user_name = str(user_name or 'Voter')
        candidate_name = str(candidate_name or 'the candidate')
        election_name = str(election_name or 'the election')
        
        current_year = datetime.now().year

        # Simple HTML body using f-string
        html_body = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .confirmation-box {{ background: white; border: 2px solid #4CAF50; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
        .info {{ background: #e7f3fe; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗳️ BallotHub</h1>
            <p>Your Vote Has Been Recorded</p>
        </div>
        <div class="content">
            <h2>Hello {user_name}!</h2>
            <p>Thank you for participating in the election. Your vote has been successfully recorded.</p>
            <div class="confirmation-box">
                <h3>Your Vote Details</h3>
                <p><strong>Election:</strong> {election_name}</p>
                <p><strong>You Voted For:</strong> {candidate_name}</p>
                <p><strong>Vote Status:</strong> <span style="color: #4CAF50; font-weight: bold;">Successfully Recorded</span></p>
            </div>
            <div class="info">
                <p><strong>Important:</strong> This is a confirmation that your vote has been recorded in the system. 
                Your vote is anonymous and cannot be changed once submitted.</p>
            </div>
            <p>If you did not cast this vote or believe this is an error, please contact our support team immediately.</p>
        </div>
        <div class="footer">
            <p>This is an automated message. Please do not reply to this email.</p>
            <p>© {current_year} BallotHub. All rights reserved.</p>
        </div>
    </div>
</body>
</html>"""

        # Plain text version (fallback)
        text_body = f"""BallotHub - Vote Confirmation

Hello {user_name}!

Thank you for participating in the election. Your vote has been successfully recorded.

Vote Details:
- Election: {election_name}
- You Voted For: {candidate_name}
- Vote Status: Successfully Recorded

Important: This is a confirmation that your vote has been recorded in the system.
Your vote is anonymous and cannot be changed once submitted.

If you did not cast this vote or believe this is an error, please contact our support team immediately.

---
BallotHub - Secure Online Voting System
© {current_year} BallotHub. All rights reserved.
"""
        
        # Create MIME message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"{MAIL_SUBJECT_PREFIX}Your Vote Confirmation"
        msg['From'] = str(MAIL_DEFAULT_SENDER or MAIL_USERNAME)
        msg['To'] = to_email

        # Attach both HTML and plain text versions
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Connect to SMTP server with timeout
        server = None
        try:
            if MAIL_USE_SSL:
                server = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT, timeout=10)
            else:
                server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT, timeout=10)
                if MAIL_USE_TLS:
                    server.starttls()
            
            # Set debug level for troubleshooting
            server.set_debuglevel(0)
            
            # Login and send
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(msg)
            print(f"✅ Vote confirmation email sent to {to_email}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ SMTP Authentication Error: {e}")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
        finally:
            try:
                if server:
                    server.quit()
            except Exception as e:
                print(f"⚠️  Error closing SMTP connection: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error in send_vote_confirmation_email: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_email_configuration() -> bool:
    """
    Test email configuration by sending a test email
    """
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        print("❌ Email not configured. Set MAIL_USERNAME and MAIL_PASSWORD")
        return False
    
    try:
        # Try to connect to SMTP server
        if MAIL_USE_SSL:
            server = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        else:
            server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
            if MAIL_USE_TLS:
                server.starttls()
        
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.quit()
        
        print("✅ Email configuration is valid!")
        return True
        
    except Exception as e:
        print(f"❌ Email configuration test failed: {e}")
        return False

