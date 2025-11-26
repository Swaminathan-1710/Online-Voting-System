# Twilio SMS Setup Guide - Send OTP to Phone

## 📱 Step-by-Step Instructions

### Step 1: Create Twilio Account (Free Trial Available)

1. Go to [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Click "Sign Up" or "Get Started"
3. Fill in your details:
   - Email address
   - Password
   - Phone number (for verification)
4. Verify your email and phone number
5. Complete the signup process

**Note**: Twilio offers a free trial with $15.50 credit (enough for ~1000 SMS messages)

### Step 2: Get Your Twilio Credentials

1. After logging in, you'll see the **Twilio Console Dashboard**
2. Look for your **Account SID** and **Auth Token**
   - They're displayed on the dashboard
   - Or go to: Settings → General → API Credentials
3. **Copy these values** (you'll need them later):
   - Account SID: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Auth Token: `your_auth_token_here`

### Step 3: Get a Twilio Phone Number

1. In Twilio Console, go to **Phone Numbers** → **Manage** → **Buy a number**
2. Click **"Get a number"**
3. Select:
   - **Country**: India (or your country)
   - **Type**: SMS
   - **Capabilities**: SMS
4. Click **"Search"**
5. Choose a number and click **"Buy"**
6. **Copy the phone number** (format: `+1234567890`)

**Note**: Trial accounts get a free number, but it can only send to verified phone numbers initially.

### Step 4: Verify Your Phone Number (For Testing)

1. In Twilio Console, go to **Phone Numbers** → **Manage** → **Verified Caller IDs**
2. Click **"Add a new Caller ID"**
3. Enter your phone number (the one you want to receive OTPs)
4. Click **"Call Me"** or **"Text Me"**
5. Enter the verification code you receive
6. Your number is now verified!

**Note**: Trial accounts can only send SMS to verified numbers. Upgrade to send to any number.

### Step 5: Install Twilio Python Library

Open PowerShell in your project folder:

```powershell
cd "F:\Ballot Hub\ballot_hub"
.\venv\Scripts\activate
pip install twilio
```

Or if you're using the requirements.txt:

```powershell
pip install -r requirements.txt
```

### Step 6: Set Environment Variables

**Option A: Using PowerShell (Temporary - for testing)**

```powershell
cd "F:\Ballot Hub\ballot_hub"
$env:TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
$env:TWILIO_AUTH_TOKEN="your_auth_token_here"
$env:TWILIO_PHONE_NUMBER="+1234567890"
$env:ENABLE_SMS="true"
```

**Option B: Create .env file (Recommended - Permanent)**

1. Create a file named `.env` in `ballot_hub` folder
2. Add these lines:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
ENABLE_SMS=true
```

3. Make sure `.env` is in `.gitignore` (don't commit credentials!)

**Option C: Update run.py (Quick test)**

Edit `run.py` and add before `if __name__ == "__main__":`:

```python
if not os.getenv("TWILIO_ACCOUNT_SID"):
    os.environ["TWILIO_ACCOUNT_SID"] = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
if not os.getenv("TWILIO_AUTH_TOKEN"):
    os.environ["TWILIO_AUTH_TOKEN"] = "your_auth_token_here"
if not os.getenv("TWILIO_PHONE_NUMBER"):
    os.environ["TWILIO_PHONE_NUMBER"] = "+1234567890"
if not os.getenv("ENABLE_SMS"):
    os.environ["ENABLE_SMS"] = "true"
```

### Step 7: Test the Setup

1. Start your application:

```powershell
python run.py
```

2. Register a user with your phone number (the verified one)
3. Try to login
4. **Check your phone** - you should receive an SMS with the OTP!

### Step 8: Verify It's Working

When you login, you should see in console:
```
✅ SMS sent successfully! SID: SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

And you should receive an SMS on your phone:
```
Your BallotHub OTP is: 123456. Valid for 5 minutes. Do not share this code with anyone.
```

## 🔧 Troubleshooting

### Issue: "Failed to send SMS via Twilio"

**Check:**
1. ✅ Twilio credentials are correct
2. ✅ ENABLE_SMS is set to "true"
3. ✅ Phone number is verified (for trial accounts)
4. ✅ Twilio phone number format is correct (+1234567890)
5. ✅ User phone number is correct (10 digits for India)

**Solution:**
- Check Twilio Console → Monitor → Logs → Errors
- Verify your account has credits
- Make sure phone number is verified (trial accounts)

### Issue: "Phone number not verified"

**For Trial Accounts:**
- You can only send SMS to verified phone numbers
- Go to Twilio Console → Phone Numbers → Verified Caller IDs
- Add and verify your phone number

**For Paid Accounts:**
- Can send to any phone number
- No verification needed

### Issue: "Insufficient funds"

**Solution:**
- Add credits to your Twilio account
- Or upgrade from trial to paid account

### Issue: "Invalid phone number format"

**Solution:**
- Indian numbers: Use 10 digits (e.g., `9876543210`)
- The code automatically adds `+91` prefix
- For other countries, use full international format

## 💰 Pricing

- **Trial Account**: $15.50 free credit (~1000 SMS)
- **Paid Account**: ~$0.0075 per SMS in India
- **Very affordable** for small to medium applications

## 🔒 Security Best Practices

1. ✅ **Never commit `.env` file** to Git
2. ✅ **Use environment variables** for credentials
3. ✅ **Rotate credentials** periodically
4. ✅ **Monitor usage** in Twilio Console
5. ✅ **Set up alerts** for unusual activity

## 📝 Quick Reference

**Environment Variables:**
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
ENABLE_SMS=true
```

**Test Command:**
```powershell
python run.py
```

**Check SMS Status:**
- Twilio Console → Monitor → Logs → Messaging

## 🎯 Next Steps

1. ✅ Set up Twilio account
2. ✅ Get credentials
3. ✅ Set environment variables
4. ✅ Test SMS sending
5. ✅ Verify OTP delivery
6. ✅ Remove OTP from API responses (production)

## 🆘 Need Help?

- Twilio Documentation: [https://www.twilio.com/docs](https://www.twilio.com/docs)
- Twilio Support: Available in Console
- Check Twilio Console → Monitor → Logs for errors

