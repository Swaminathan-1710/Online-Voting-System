# TextLocal SMS Setup (Recommended for India)

## Why TextLocal?
- ✅ Very affordable in India (₹0.25-0.50 per SMS)
- ✅ Easy setup
- ✅ Good delivery rates
- ✅ Free trial available

## Step-by-Step Setup

### Step 1: Create TextLocal Account

1. Go to: https://www.textlocal.in/
2. Click **"Sign Up"** or **"Register"**
3. Fill in your details:
   - Email
   - Mobile number
   - Password
4. Verify your email and mobile
5. Complete registration

### Step 2: Get API Key

1. Log in to TextLocal dashboard
2. Go to **"API"** section
3. Click **"API Keys"**
4. Generate a new API key or use existing one
5. **Copy the API key**

### Step 3: Set Sender ID

1. In TextLocal dashboard, go to **"Settings"** → **"Sender IDs"**
2. Set your sender ID (6 characters max, e.g., "BALLOT")
3. Note: Sender ID needs approval (usually instant for trial)

### Step 4: Configure in BallotHub

**Option A: Environment Variables (PowerShell)**

```powershell
cd "F:\Ballot Hub\ballot_hub"
$env:SMS_PROVIDER="textlocal"
$env:TEXTLOCAL_API_KEY="your_api_key_here"
$env:TEXTLOCAL_SENDER="BALLOT"
```

**Option B: .env File**

Create `.env` file in `ballot_hub` folder:

```env
SMS_PROVIDER=textlocal
TEXTLOCAL_API_KEY=your_api_key_here
TEXTLOCAL_SENDER=BALLOT
```

### Step 5: Test

1. Start application: `python run.py`
2. Register a user with your phone number
3. Try to login
4. **Check your phone** - you should receive SMS!

## Pricing

- **Trial**: Free credits for testing
- **Paid**: ₹0.25-0.50 per SMS in India
- **Very affordable** for Indian applications

## Troubleshooting

**Issue: "API key not configured"**
- Check API key is correct
- Verify API key is active in TextLocal dashboard

**Issue: "Sender ID not approved"**
- Wait for approval (usually instant)
- Check TextLocal dashboard for status

**Issue: SMS not received**
- Check phone number format (10 digits for India)
- Verify account has credits
- Check TextLocal dashboard → Reports for delivery status

## API Documentation

- TextLocal API Docs: https://www.textlocal.in/docs/

