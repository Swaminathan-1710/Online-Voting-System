# MSG91 SMS Setup (Popular in India)

## Why MSG91?
- ✅ Very cheap in India (₹0.20-0.50 per SMS)
- ✅ Good API documentation
- ✅ Bulk SMS support
- ✅ Popular with Indian startups

## Step-by-Step Setup

### Step 1: Create MSG91 Account

1. Go to: https://msg91.com/
2. Click **"Sign Up"**
3. Fill in your details
4. Verify email and mobile
5. Complete registration

### Step 2: Get Auth Key

1. Log in to MSG91 dashboard
2. Go to **"API"** section
3. Find your **"Auth Key"** (or generate new one)
4. **Copy the Auth Key**

### Step 3: Set Sender ID

1. In MSG91 dashboard, go to **"Settings"** → **"Sender ID"**
2. Set your sender ID (6 characters max, e.g., "BALLOT")
3. Note: Sender ID needs approval

### Step 4: Configure in BallotHub

**Option A: Environment Variables (PowerShell)**

```powershell
cd "F:\Ballot Hub\ballot_hub"
$env:SMS_PROVIDER="msg91"
$env:MSG91_AUTH_KEY="your_auth_key_here"
$env:MSG91_SENDER="BALLOT"
```

**Option B: .env File**

```env
SMS_PROVIDER=msg91
MSG91_AUTH_KEY=your_auth_key_here
MSG91_SENDER=BALLOT
```

### Step 5: Test

1. Start application: `python run.py`
2. Register a user with your phone number
3. Try to login
4. **Check your phone** - you should receive SMS!

## Pricing

- **Trial**: Free credits
- **Paid**: ₹0.20-0.50 per SMS in India
- **Very affordable**

## Troubleshooting

**Issue: "Auth key not configured"**
- Check auth key is correct
- Verify auth key is active

**Issue: SMS not received**
- Check phone number format
- Verify account has credits
- Check MSG91 dashboard for delivery status

## API Documentation

- MSG91 API Docs: https://docs.msg91.com/

