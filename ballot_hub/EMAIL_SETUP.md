# Email OTP Setup Guide

## 📧 Overview

BallotHub now uses **Email OTP** instead of SMS. Users receive OTP codes via email for secure login.

---

## 🔧 SMTP Configuration

### Step 1: Choose Email Provider

**Popular Options:**
1. **Gmail** (Easy, free) ⭐ Recommended for testing
2. **Outlook/Hotmail** (Free)
3. **Yahoo Mail** (Free)
4. **Custom SMTP** (Your own email server)

---

## 📮 Gmail Setup (Recommended)

### Step 1: Enable App Password

1. Go to your **Google Account**: https://myaccount.google.com/
2. Click **"Security"** (left sidebar)
3. Under **"Signing in to Google"**, find **"2-Step Verification"**
4. If not enabled, enable it first
5. Then go to **"App passwords"**
6. Click **"Select app"** → Choose **"Mail"**
7. Click **"Select device"** → Choose **"Other (Custom name)"**
8. Enter: **"BallotHub"**
9. Click **"Generate"**
10. **Copy the 16-character password** (you'll need this!)

**Important**: Use the **App Password**, not your regular Gmail password!

### Step 2: Configure in BallotHub

**Option A: Environment Variables (PowerShell)**

```powershell
cd "F:\Ballot Hub\ballot_hub"
$env:MAIL_SERVER="smtp.gmail.com"
$env:MAIL_PORT="587"
$env:MAIL_USE_TLS="true"
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="your-16-char-app-password"
$env:MAIL_DEFAULT_SENDER="your-email@gmail.com"
```

**Option B: .env File**

Create `.env` file in `ballot_hub` folder:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

---

## 📧 Outlook/Hotmail Setup

### Configuration:

```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=your-email@outlook.com
```

---

## 📧 Yahoo Mail Setup

### Configuration:

```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@yahoo.com
```

**Note**: Yahoo also requires App Password (similar to Gmail)

---

## 🔧 Custom SMTP Setup

If you have your own email server:

```env
MAIL_SERVER=your-smtp-server.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-username
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

**Common Ports:**
- **587**: TLS (recommended)
- **465**: SSL
- **25**: Plain (not recommended)

---

## ✅ Test Email Configuration

### Quick Test:

```powershell
cd "F:\Ballot Hub\ballot_hub"
.\venv\Scripts\activate
python -c "from utils.email_service import test_email_configuration; test_email_configuration()"
```

This will test your SMTP connection.

---

## 🚀 Using Email OTP

### How It Works:

1. User enters email and password
2. System verifies credentials
3. **OTP is sent to user's email** (not phone)
4. User checks email and enters OTP
5. System verifies OTP and logs user in

### User Experience:

- User sees: **"OTP sent to your email"**
- Email contains beautiful HTML OTP code
- OTP expires in 5 minutes
- User can resend OTP if needed

---

## 📝 Environment Variables Reference

```env
# SMTP Server
MAIL_SERVER=smtp.gmail.com

# Port (587 for TLS, 465 for SSL)
MAIL_PORT=587

# Use TLS (recommended)
MAIL_USE_TLS=true

# Use SSL (alternative)
MAIL_USE_SSL=false

# Your email address
MAIL_USERNAME=your-email@gmail.com

# Your password or App Password
MAIL_PASSWORD=your-password

# Sender email (usually same as MAIL_USERNAME)
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

---

## 🔒 Security Best Practices

1. ✅ **Use App Passwords** (Gmail, Yahoo)
2. ✅ **Never commit passwords** to Git
3. ✅ **Use environment variables** (not hardcoded)
4. ✅ **Use TLS/SSL** for secure connection
5. ✅ **Rotate passwords** periodically

---

## ❓ Troubleshooting

### Issue: "Failed to send email"

**Check:**
1. ✅ SMTP server is correct
2. ✅ Port is correct (587 for TLS, 465 for SSL)
3. ✅ Username and password are correct
4. ✅ App Password is used (for Gmail/Yahoo)
5. ✅ Less secure apps enabled (if required)

**Solution:**
- Verify credentials
- Check firewall/antivirus isn't blocking
- Try different port (587 vs 465)
- Check email provider's security settings

### Issue: "Authentication failed"

**For Gmail:**
- Make sure you're using **App Password**, not regular password
- Enable 2-Step Verification first
- Check if "Less secure app access" is enabled (if not using App Password)

### Issue: "Connection timeout"

**Solution:**
- Check internet connection
- Verify SMTP server address
- Check if port is blocked by firewall
- Try different port

---

## 🎯 Quick Setup Checklist

- [ ] Choose email provider (Gmail recommended)
- [ ] Get App Password (for Gmail/Yahoo)
- [ ] Set environment variables
- [ ] Test email configuration
- [ ] Start application
- [ ] Test OTP email sending

---

## 💡 Tips

- **Gmail App Password**: 16 characters, no spaces
- **Test First**: Use test script before running app
- **Check Spam**: OTP emails might go to spam initially
- **Development**: OTP still shown in console if email fails

---

## 🎉 Success!

Once configured, users will receive beautiful HTML emails with OTP codes!

**No more SMS setup needed!** Email OTP is easier and works everywhere! 📧✨

