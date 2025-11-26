"""
Phone number validation and confidentiality utilities
"""
import hmac
import hashlib
from config import JWT_SECRET_KEY


def is_valid_phone(phone: str) -> bool:
    """
    Validate phone number format:
    - Indian format: 10 digits (starts with 6-9)
    - International: 10-15 digits
    - Can include country code (+91 for India)
    """
    if not phone:
        return False
    
    # Remove spaces, dashes, and plus signs for validation
    cleaned = phone.replace(" ", "").replace("-", "").replace("+", "")
    
    # Must be all digits
    if not cleaned.isdigit():
        return False
    
    # Indian phone number (10 digits, starts with 6-9)
    if len(cleaned) == 10:
        return cleaned[0] in ['6', '7', '8', '9']
    
    # With country code +91 (12 digits total)
    if len(cleaned) == 12 and cleaned.startswith('91'):
        return cleaned[2] in ['6', '7', '8', '9']
    
    # International format (10-15 digits)
    if 10 <= len(cleaned) <= 15:
        return True
    
    return False


def normalize_phone(phone: str) -> str:
    """
    Normalize phone number to standard format (10 digits for India)
    Removes spaces, dashes, country codes
    """
    if not phone:
        return ""
    
    cleaned = phone.replace(" ", "").replace("-", "").replace("+", "")
    
    # If starts with 91 (India country code), remove it
    if len(cleaned) == 12 and cleaned.startswith('91'):
        cleaned = cleaned[2:]
    
    return cleaned


def hash_phone(phone: str, secret_key: str = None) -> str:
    """
    Hash phone number using HMAC-SHA256 for confidentiality.
    Uses a secret key from config if available.
    """
    if secret_key is None:
        secret_key = JWT_SECRET_KEY
    
    normalized = normalize_phone(phone)
    
    # Use HMAC for secure hashing
    return hmac.new(
        secret_key.encode('utf-8'),
        normalized.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


def mask_phone(phone: str) -> str:
    """
    Mask phone number for display: XXXXXX1234
    Only shows last 4 digits for verification purposes.
    """
    if not phone:
        return "XXXXXX-XXXX"
    
    normalized = normalize_phone(phone)
    if len(normalized) < 4:
        return "XXXXXX-XXXX"
    
    # Show only last 4 digits
    last_four = normalized[-4:]
    return f"XXXXXX-{last_four}"

