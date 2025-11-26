# Email/SMTP Quick Setup Script for BallotHub
# This script helps you configure email for OTP sending

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Email OTP Setup for BallotHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Choose your email provider:" -ForegroundColor Yellow
Write-Host "1. Gmail (Recommended)"
Write-Host "2. Outlook/Hotmail"
Write-Host "3. Yahoo Mail"
Write-Host "4. Custom SMTP"
Write-Host ""

$choice = Read-Host "Enter choice (1-4)"

$mailServer = ""
$mailPort = ""
$mailUseTLS = "true"
$mailUseSSL = "false"

switch ($choice) {
    "1" {
        $mailServer = "smtp.gmail.com"
        $mailPort = "587"
        Write-Host ""
        Write-Host "⚠️  IMPORTANT: For Gmail, you need an App Password!" -ForegroundColor Yellow
        Write-Host "   1. Go to: https://myaccount.google.com/security" -ForegroundColor White
        Write-Host "   2. Enable 2-Step Verification" -ForegroundColor White
        Write-Host "   3. Go to App Passwords" -ForegroundColor White
        Write-Host "   4. Generate password for 'Mail'" -ForegroundColor White
        Write-Host ""
    }
    "2" {
        $mailServer = "smtp-mail.outlook.com"
        $mailPort = "587"
    }
    "3" {
        $mailServer = "smtp.mail.yahoo.com"
        $mailPort = "587"
        Write-Host ""
        Write-Host "⚠️  IMPORTANT: For Yahoo, you need an App Password!" -ForegroundColor Yellow
    }
    "4" {
        $mailServer = Read-Host "Enter SMTP server (e.g., smtp.example.com)"
        $mailPort = Read-Host "Enter port (587 for TLS, 465 for SSL)"
        $tlsChoice = Read-Host "Use TLS? (y/n)"
        if ($tlsChoice -eq "n") {
            $mailUseTLS = "false"
            $mailUseSSL = "true"
        }
    }
    default {
        Write-Host "Invalid choice. Using Gmail defaults." -ForegroundColor Yellow
        $mailServer = "smtp.gmail.com"
        $mailPort = "587"
    }
}

Write-Host ""
Write-Host "Enter your email credentials:" -ForegroundColor Yellow
$mailUsername = Read-Host "Email address"
$mailPassword = Read-Host "Password or App Password" -AsSecureString
$mailPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($mailPassword)
)

Write-Host ""
Write-Host "Setting environment variables..." -ForegroundColor Yellow

# Set environment variables
$env:MAIL_SERVER = $mailServer
$env:MAIL_PORT = $mailPort
$env:MAIL_USE_TLS = $mailUseTLS
$env:MAIL_USE_SSL = $mailUseSSL
$env:MAIL_USERNAME = $mailUsername
$env:MAIL_PASSWORD = $mailPasswordPlain
$env:MAIL_DEFAULT_SENDER = $mailUsername

Write-Host "✓ Environment variables set for this session" -ForegroundColor Green
Write-Host ""

# Create .env file
Write-Host "Creating .env file for permanent storage..." -ForegroundColor Yellow
$envContent = @"
MAIL_SERVER=$mailServer
MAIL_PORT=$mailPort
MAIL_USE_TLS=$mailUseTLS
MAIL_USE_SSL=$mailUseSSL
MAIL_USERNAME=$mailUsername
MAIL_PASSWORD=$mailPasswordPlain
MAIL_DEFAULT_SENDER=$mailUsername
"@

$envPath = Join-Path (Get-Location) ".env"
$envContent | Out-File -FilePath $envPath -Encoding utf8 -NoNewline

Write-Host "✓ .env file created at: $envPath" -ForegroundColor Green
Write-Host ""

# Test email configuration
Write-Host "Testing email configuration..." -ForegroundColor Yellow
try {
    cd "F:\Ballot Hub\ballot_hub"
    .\venv\Scripts\python -c "from utils.email_service import test_email_configuration; test_email_configuration()"
} catch {
    Write-Host "⚠️  Could not test email configuration. Make sure virtual environment is activated." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test email by running: python run.py" -ForegroundColor White
Write-Host "2. Try logging in - OTP will be sent to email!" -ForegroundColor White
Write-Host ""
Write-Host "Important:" -ForegroundColor Yellow
Write-Host "- Keep your .env file secure (don't commit to Git)" -ForegroundColor White
Write-Host "- For Gmail/Yahoo, use App Password, not regular password" -ForegroundColor White
Write-Host ""

