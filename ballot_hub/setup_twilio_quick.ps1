# Quick Twilio Setup Script
# This script helps you set up Twilio SMS quickly

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Twilio SMS Quick Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Twilio is installed
Write-Host "Checking Twilio installation..." -ForegroundColor Yellow
try {
    $twilioCheck = pip show twilio 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Twilio is already installed" -ForegroundColor Green
    } else {
        throw "Not installed"
    }
} catch {
    Write-Host "Installing Twilio..." -ForegroundColor Yellow
    pip install twilio
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Twilio installed successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to install Twilio" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Twilio Credentials Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can find these in Twilio Console:" -ForegroundColor Yellow
Write-Host "  https://console.twilio.com/" -ForegroundColor Cyan
Write-Host ""

# Get Twilio Account SID
Write-Host "Enter your Twilio Account SID (starts with AC):" -ForegroundColor Yellow
$accountSid = Read-Host "Account SID"

if (-not $accountSid -or -not $accountSid.StartsWith("AC")) {
    Write-Host "⚠️  Warning: Account SID should start with 'AC'" -ForegroundColor Yellow
}

# Get Twilio Auth Token
Write-Host ""
Write-Host "Enter your Twilio Auth Token:" -ForegroundColor Yellow
$authToken = Read-Host "Auth Token" -AsSecureString
$authTokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($authToken)
)

# Get Twilio Phone Number
Write-Host ""
Write-Host "Enter your Twilio Phone Number (format: +1234567890):" -ForegroundColor Yellow
$phoneNumber = Read-Host "Phone Number"

if (-not $phoneNumber.StartsWith("+")) {
    Write-Host "⚠️  Warning: Phone number should start with '+' (e.g., +1234567890)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setting environment variables..." -ForegroundColor Yellow

# Set environment variables for current session
$env:SMS_PROVIDER = "twilio"
$env:TWILIO_ACCOUNT_SID = $accountSid
$env:TWILIO_AUTH_TOKEN = $authTokenPlain
$env:TWILIO_PHONE_NUMBER = $phoneNumber

Write-Host "✓ Environment variables set for this session" -ForegroundColor Green
Write-Host ""

# Create .env file
Write-Host "Creating .env file for permanent storage..." -ForegroundColor Yellow
$envContent = @"
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=$accountSid
TWILIO_AUTH_TOKEN=$authTokenPlain
TWILIO_PHONE_NUMBER=$phoneNumber
"@

$envPath = Join-Path (Get-Location) ".env"
$envContent | Out-File -FilePath $envPath -Encoding utf8 -NoNewline

Write-Host "✓ .env file created at: $envPath" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Make sure your phone number is verified in Twilio Console" -ForegroundColor White
Write-Host "2. Run: python run.py" -ForegroundColor White
Write-Host "3. Test login - you should receive SMS!" -ForegroundColor White
Write-Host ""
Write-Host "Important:" -ForegroundColor Yellow
Write-Host "- Keep your .env file secure (don't commit to Git)" -ForegroundColor White
Write-Host "- Trial accounts can only send to verified numbers" -ForegroundColor White
Write-Host ""
Write-Host "Ready to test! Run: python run.py" -ForegroundColor Green
Write-Host ""

