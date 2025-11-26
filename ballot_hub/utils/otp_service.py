"""
OTP (One-Time Password) service for user authentication
"""
import secrets
import hashlib
from datetime import datetime, timedelta
from database.connection import get_collection
from config import JWT_SECRET_KEY


def generate_otp(length: int = 6) -> str:
    """
    Generate a random numeric OTP
    Default length is 6 digits
    """
    return ''.join([str(secrets.randbelow(10)) for _ in range(length)])


def hash_otp(otp: str) -> str:
    """
    Hash OTP for secure storage
    """
    return hashlib.sha256(
        (otp + JWT_SECRET_KEY).encode('utf-8')
    ).hexdigest()


def send_otp_to_phone(phone: str, otp: str) -> bool:
    """
    Send OTP to phone number via SMS.
    Supports multiple providers: TextLocal, MSG91, Fast2SMS, AWS SNS, Vonage
    
    Returns True if sent successfully
    """
    from config import (
        SMS_PROVIDER,
        TEXTLOCAL_API_KEY, TEXTLOCAL_SENDER,
        MSG91_AUTH_KEY, MSG91_SENDER,
        FAST2SMS_API_KEY, FAST2SMS_SENDER,
        AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, AWS_SNS_SENDER_ID,
        VONAGE_API_KEY, VONAGE_API_SECRET, VONAGE_SENDER
    )
    
    if not phone or not otp:
        return False
        
    message = f"Your BallotHub OTP is: {otp}. Valid for 5 minutes. Do not share this code with anyone."
    
    # Route to appropriate SMS provider
    if SMS_PROVIDER == "textlocal":
        return _send_via_textlocal(phone, message)
    elif SMS_PROVIDER == "msg91":
        return _send_via_msg91(phone, message, otp)
    elif SMS_PROVIDER == "fast2sms":
        return _send_via_fast2sms(phone, message)
    elif SMS_PROVIDER == "aws_sns":
        return _send_via_aws_sns(phone, message)
    elif SMS_PROVIDER == "vonage":
        return _send_via_vonage(phone, message)
    else:
        # Default fallback to console output
        return _send_via_console(phone, otp)


def _send_via_textlocal(phone: str, message: str) -> bool:
    """Send SMS via TextLocal (India)"""
    from config import TEXTLOCAL_API_KEY, TEXTLOCAL_SENDER
    import requests
    
    if not TEXTLOCAL_API_KEY:
        print("❌ TextLocal API key not configured")
        return _send_via_console(phone, message.split(": ")[1].split(".")[0])
    
    try:
        url = "https://api.textlocal.in/send/"
        params = {
            "apikey": TEXTLOCAL_API_KEY,
            "numbers": phone,
            "message": message,
            "sender": TEXTLOCAL_SENDER
        }
        response = requests.get(url, params=params)
        result = response.json()
        
        if result.get("status") == "success":
            print(f"✅ SMS sent via TextLocal!")
            return True
        else:
            print(f"❌ TextLocal error: {result.get('errors', [{}])[0].get('message', 'Unknown error')}")
            return _send_via_console(phone, message.split(": ")[1].split(".")[0])
    except Exception as e:
        print(f"❌ TextLocal error: {e}")
        return _send_via_console(phone, message.split(": ")[1].split(".")[0])


def _send_via_msg91(phone: str, message: str) -> bool:
    """Send SMS via MSG91 (India)"""
    from config import MSG91_AUTH_KEY, MSG91_SENDER
    import requests
    
    if not MSG91_AUTH_KEY:
        print("❌ MSG91 auth key not configured")
        return _send_via_console(phone, message.split(": ")[1].split(".")[0])
    
    try:
        url = "https://api.msg91.com/api/v2/sendsms"
        headers = {
            "authkey": MSG91_AUTH_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "sender": MSG91_SENDER,
            "route": "4",  # Transactional route
            "country": "91",
            "sms": [{
                "message": message,
                "to": [phone]
            }]
        }
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        
        if result.get("type") == "success":
            print(f"✅ SMS sent via MSG91!")
            return True
        else:
            print(f"❌ MSG91 error: {result.get('message', 'Unknown error')}")
            return _send_via_console(phone, message.split(": ")[1].split(".")[0])
    except Exception as e:
        print(f"❌ MSG91 error: {e}")
        return _send_via_console(phone, message.split(": ")[1].split(".")[0])


def _send_via_fast2sms(phone: str, message: str) -> bool:
    """Send SMS via Fast2SMS (India)"""
    from config import FAST2SMS_API_KEY, FAST2SMS_SENDER
    import requests
    
    if not FAST2SMS_API_KEY:
        print("❌ Fast2SMS API key not configured")
        return _send_via_console(phone, message.split(": ")[1].split(".")[0])
    
    try:
        url = "https://www.fast2sms.com/dev/bulkV2"
        headers = {
            "authorization": FAST2SMS_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "route": "q",  # Quick route for OTP
            "message": message,
            "language": "english",
            "numbers": phone
        }
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        
        if result.get("return") == True:
            print(f"✅ SMS sent via Fast2SMS!")
            return True
        else:
            print(f"❌ Fast2SMS error: {result.get('message', 'Unknown error')}")
            return _send_via_console(phone, message.split(": ")[1].split(".")[0])
    except Exception as e:
        print(f"❌ Fast2SMS error: {e}")
        return _send_via_console(phone, message.split(": ")[1].split(".")[0])


def _send_via_aws_sns(phone: str, message: str) -> bool:
    """Send SMS via AWS SNS"""
    from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
    
    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION]):
        print("❌ AWS credentials not configured")
        return _send_via_console(phone, message.split(": ")[1].split(".")[0])
    
    try:
        import boto3
        sns = boto3.client(
            'sns',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        
        # Format phone number
        if not phone.startswith('+'):
            phone_with_country = f"+91{phone}" if len(phone) == 10 else phone
        else:
            phone_with_country = phone
        
        response = sns.publish(
            PhoneNumber=phone_with_country,
            Message=message
        )
        print(f"✅ SMS sent via AWS SNS! MessageId: {response['MessageId']}")
        return True
    except Exception as e:
        print(f"❌ AWS SNS error: {e}")
        return _send_via_console(phone, message.split(": ")[1].split(".")[0])


def _send_via_vonage(phone: str, message: str) -> bool:
    """Send SMS via Vonage (formerly Nexmo)"""
    from config import VONAGE_API_KEY, VONAGE_API_SECRET, VONAGE_SENDER
    
    if not all([VONAGE_API_KEY, VONAGE_API_SECRET]):
        print("❌ Vonage credentials not configured")
        return _send_via_console(phone, message.split(": ")[1].split(".")[0])
    
    try:
        from vonage import Sms
        sms = Sms(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
        
        # Format phone number
        if not phone.startswith('+'):
            phone_with_country = f"91{phone}" if len(phone) == 10 else phone
        else:
            phone_with_country = phone.lstrip('+')
        
        response = sms.send_message({
            "from": VONAGE_SENDER,
            "to": phone_with_country,
            "text": message
        })
        
        if response["messages"][0]["status"] == "0":
            print(f"✅ SMS sent via Vonage!")
            return True
        else:
            print(f"❌ Vonage error: {response['messages'][0]['error-text']}")
            return _send_via_console(phone, message.split(": ")[1].split(".")[0])
    except Exception as e:
        print(f"❌ Vonage error: {e}")
        return _send_via_console(phone, message.split(": ")[1].split(".")[0])


def _send_via_console(phone: str, otp: str) -> bool:
    """Development mode: Display OTP in console"""
    print("=" * 60)
    print(f"📱 OTP for {phone}: {otp}")
    print(f"⏰ Valid for 5 minutes")
    print("=" * 60)
    print(f"💡 To enable SMS, set SMS_PROVIDER and configure credentials")
    print(f"   Available providers: textlocal, msg91, fast2sms, aws_sns, vonage")
    print("=" * 60)
    return True


def store_otp(user_id: str, identifier: str, otp: str, expires_in_minutes: int = 5) -> bool:
    """
    Store OTP in database with expiration
    """
    from bson import ObjectId
    otps = get_collection("otps")
    
    # Hash the OTP before storing
    otp_hash = hash_otp(otp)
    
    # Calculate expiration time
    expires_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    
    # Convert user_id to ObjectId if it's a string
    if isinstance(user_id, str):
        try:
            user_id = ObjectId(user_id)
        except:
            pass
    
    # Store OTP (identifier can be phone or email)
    otps.insert_one({
        "user_id": user_id,
        "identifier": identifier,  # Store email or phone for reference
        "otp_hash": otp_hash,
        "expires_at": expires_at,
        "used": False,
        "created_at": datetime.utcnow()
    })
    
    return True


def verify_otp(user_id: str, otp: str) -> bool:
    """
    Verify OTP for a user
    Returns True if OTP is valid and not expired
    """
    from bson import ObjectId
    otps = get_collection("otps")
    
    # Hash the provided OTP
    otp_hash = hash_otp(otp)
    
    # Convert user_id to ObjectId if it's a string
    user_id_obj = user_id
    if isinstance(user_id, str):
        try:
            user_id_obj = ObjectId(user_id)
        except:
            pass
    
    # Find matching OTP
    otp_record = otps.find_one({
        "user_id": user_id_obj,
        "otp_hash": otp_hash,
        "used": False,
        "expires_at": {"$gt": datetime.utcnow()}
    })
    
    if not otp_record:
        return False
    
    # Mark OTP as used
    otps.update_one(
        {"_id": otp_record["_id"]},
        {"$set": {"used": True}}
    )
    
    return True


def cleanup_expired_otps():
    """
    Clean up expired OTPs from database
    Call this periodically (e.g., via cron job or scheduled task)
    """
    otps = get_collection("otps")
    result = otps.delete_many({
        "$or": [
            {"expires_at": {"$lt": datetime.utcnow()}},
            {"used": True}
        ]
    })
    return result.deleted_count

