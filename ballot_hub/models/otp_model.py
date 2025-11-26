"""
OTP model for managing OTP generation and verification
"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from database.connection import get_collection
from utils.otp_service import generate_otp, hash_otp, verify_otp as verify_otp_service
from utils.email_service import send_otp_email


def generate_and_send_otp(user_id: str, email: str, user_name: str = "User") -> Dict[str, Any]:
    """
    Generate OTP, send it to user's email, and store it
    Returns OTP details (for development/testing)
    """
    from utils.otp_service import store_otp
    from bson import ObjectId
    
    # Convert user_id to ObjectId if it's a string
    if isinstance(user_id, str):
        try:
            user_id = ObjectId(user_id)
        except:
            pass
    
    # Generate 6-digit OTP
    otp = generate_otp(6)
    
    # Send OTP to email
    sent = send_otp_email(email, otp, user_name)
    if not sent:
        return {"success": False, "message": "Failed to send OTP email"}
    
    # Store OTP in database (using email as identifier)
    store_otp(str(user_id), email, otp, expires_in_minutes=5)
    
    # Return success (OTP not included in response for security)
    return {
        "success": True,
        "message": "OTP sent to your registered email address",
        "expires_in": 5  # minutes
    }


def verify_user_otp(user_id: str, otp: str) -> bool:
    """
    Verify OTP for a user
    """
    return verify_otp_service(user_id, otp)



