# OTP (One-Time Password) Login Setup

## Overview

BallotHub now uses **Two-Factor Authentication (2FA)** with OTP for enhanced security. Users must verify their identity with a 6-digit code sent to their registered phone number.

## How It Works

### Login Flow

1. **Step 1: Credentials Verification**
   - User enters email and password
   - System verifies credentials
   - If valid, generates and sends OTP to registered phone number

2. **Step 2: OTP Verification**
   - User enters 6-digit OTP received on phone
   - System verifies OTP
   - If valid, issues JWT token and logs user in

### Security Features

- ✅ **OTP Expiration**: OTPs expire after 5 minutes
- ✅ **One-Time Use**: Each OTP can only be used once
- ✅ **Hashed Storage**: OTPs are hashed before storing in database
- ✅ **Automatic Cleanup**: Expired OTPs are automatically removed

## Development Mode

Currently, OTPs are **logged to console** for development purposes. You'll see:

```
============================================================
📱 OTP for 9876543210: 123456
⏰ Valid for 5 minutes
============================================================
```

**Note**: In production, remove the OTP from API responses and integrate with an SMS service.

## Production Setup

### Option 1: Twilio (Recommended)

1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token
3. Install Twilio SDK:
   ```bash
   pip install twilio
   ```
4. Update `utils/otp_service.py`:
   ```python
   from twilio.rest import Client
   
   def send_otp_to_phone(phone: str, otp: str) -> bool:
       account_sid = os.getenv('TWILIO_ACCOUNT_SID')
       auth_token = os.getenv('TWILIO_AUTH_TOKEN')
       from_number = os.getenv('TWILIO_PHONE_NUMBER')
       
       client = Client(account_sid, auth_token)
       message = client.messages.create(
           body=f"Your BallotHub OTP is: {otp}. Valid for 5 minutes.",
           from_=from_number,
           to=f'+91{phone}'  # Add country code
       )
       return True
   ```

### Option 2: AWS SNS

1. Set up AWS SNS
2. Install boto3:
   ```bash
   pip install boto3
   ```
3. Update `utils/otp_service.py` with AWS SNS integration

### Option 3: Other SMS Services

- MessageBird
- Nexmo/Vonage
- Plivo
- Custom SMS Gateway

## Database Schema

### OTPs Collection

```javascript
{
  "_id": ObjectId,
  "user_id": ObjectId,      // Reference to user
  "phone": String,          // Phone number (for sending)
  "otp_hash": String,       // Hashed OTP
  "expires_at": DateTime,   // Expiration time
  "used": Boolean,          // Whether OTP was used
  "created_at": DateTime    // Creation time
}
```

### Indexes

Create an index for faster OTP lookups:

```javascript
db.otps.createIndex({ "user_id": 1, "expires_at": 1 })
db.otps.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 }) // TTL index
```

## API Endpoints

### POST /api/login

**Step 1: Verify Credentials**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "step": "1"
}
```

**Response:**
```json
{
  "step": 1,
  "message": "OTP sent to your registered phone number",
  "user_id": "user_id_string",
  "phone_masked": "XXXXXX-1234",
  "otp": "123456",  // Remove in production!
  "expires_in": 5
}
```

**Step 2: Verify OTP**
```json
{
  "user_id": "user_id_string",
  "otp": "123456",
  "step": "2"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "user": {
    "user_id": "user_id_string",
    "name": "User Name",
    "email": "user@example.com"
  }
}
```

## Removing OTP from Response (Production)

In `controllers/user_controller.py`, remove the OTP from the response:

```python
return jsonify({
    "step": 1,
    "message": "OTP sent to your registered phone number",
    "user_id": user["user_id"],
    "phone_masked": phone_masked,
    # "otp": otp_result.get("otp"),  # REMOVE THIS LINE
    "expires_in": otp_result.get("expires_in", 5)
}), 200
```

And in `models/otp_model.py`:

```python
return {
    "success": True,
    "message": "OTP sent to your registered phone number",
    # "otp": otp,  # REMOVE THIS LINE
    "expires_in": 5
}
```

## Cleanup Expired OTPs

Set up a scheduled task to clean up expired OTPs:

```python
# In a cron job or scheduled task
from utils.otp_service import cleanup_expired_otps
cleanup_expired_otps()
```

Or use MongoDB TTL index (automatic cleanup):

```javascript
db.otps.createIndex(
  { "expires_at": 1 },
  { expireAfterSeconds: 0 }
)
```

## Testing

1. Register a new user with phone number
2. Login with email and password
3. Check console for OTP (development mode)
4. Enter OTP on login page
5. Verify successful login

## Troubleshooting

### OTP not received
- Check console logs (development mode)
- Verify phone number is correct
- Check SMS service configuration (production)
- Verify OTP hasn't expired (5 minutes)

### "Invalid or expired OTP"
- OTP may have expired (5 minutes)
- OTP may have been used already
- Check system time is correct
- Verify OTP was entered correctly

### "Phone number not found"
- User may not have phone_normalized field
- Run migration to add phone_normalized to existing users
- Or user needs to re-register

## Migration for Existing Users

If you have existing users without `phone_normalized`:

```python
# Migration script
from database.connection import get_collection
from utils.phone_validator import normalize_phone

users = get_collection("users")
for user in users.find({"phone_normalized": {"$exists": False}}):
    # You'll need to get the original phone number
    # Or ask users to re-register
    pass
```

## Security Best Practices

1. ✅ **Never log OTPs in production**
2. ✅ **Use HTTPS for all API calls**
3. ✅ **Rate limit OTP requests** (prevent abuse)
4. ✅ **Implement CAPTCHA** for OTP requests
5. ✅ **Monitor for suspicious activity**
6. ✅ **Use strong SMS service** with delivery guarantees
7. ✅ **Set appropriate OTP expiration** (5 minutes recommended)

