import os
from datetime import timedelta

# Load from environment if present
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "ballot_hub_db")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-change-this")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

# App constants
PASSWORD_HASH_ROUNDS = 12
AADHAAR_LENGTH = 12

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

# Email/SMTP Configuration (for OTP)
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME", ""))
MAIL_SUBJECT_PREFIX = os.getenv("MAIL_SUBJECT_PREFIX", "[BallotHub] ")

# SMS Provider Configuration (for OTP)
# Options: "twilio", "textlocal", "msg91", "fast2sms", "aws_sns", "vonage", "console"
SMS_PROVIDER = os.getenv("SMS_PROVIDER", "console")  # Default: console (development)

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")  # Format: +1234567890 or Alphanumeric Sender ID (e.g., "BALLOT")
TWILIO_USE_SENDER_ID = os.getenv("TWILIO_USE_SENDER_ID", "").lower() == "true"  # Auto-detected if not set

# TextLocal Configuration (India)
TEXTLOCAL_API_KEY = os.getenv("TEXTLOCAL_API_KEY", "")
TEXTLOCAL_SENDER = os.getenv("TEXTLOCAL_SENDER", "TXTLCL")  # 6 characters max

# MSG91 Configuration (India)
MSG91_AUTH_KEY = os.getenv("MSG91_AUTH_KEY", "")
MSG91_SENDER = os.getenv("MSG91_SENDER", "BALLOT")  # 6 characters max

# Fast2SMS Configuration (India)
FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY", "")
FAST2SMS_SENDER = os.getenv("FAST2SMS_SENDER", "BALLOT")  # 6 characters max

# AWS SNS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Vonage Configuration
VONAGE_API_KEY = os.getenv("VONAGE_API_KEY", "")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET", "")
VONAGE_SENDER = os.getenv("VONAGE_SENDER", "BallotHub")

