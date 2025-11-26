# Twilio SMS Setup Script for BallotHub
# Run this script to set up Twilio SMS for OTP

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Twilio SMS Setup for BallotHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Twilio is installed
Write-Host "Checking Twilio installation..." -ForegroundColor Yellow
try {
    pip show twilio | Out-Null
    Write-Host "✓ Twilio is installed" -ForegroundColor Green
} catch {
    Write-Host "Installing Twilio..." -ForegroundColor Yellow
    pip install twilio
    Write-Host "✓ Twilio installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Please provide your Twilio credentials:" -ForegroundColor Yellow
Write-Host ""

# Get Twilio Account SID
$accountSid = Read-Host "Enter Twilio Account SID (ACxxxxxxxx...)"

# Get Twilio Auth Token
$authToken = Read-Host "Enter Twilio Auth Token"

# Get Twilio Phone Number
$phoneNumber = Read-Host "Enter Twilio Phone Number (+1234567890)"

Write-Host ""
Write-Host "Setting environment variables..." -ForegroundColor Yellow

# Set environment variables
$env:TWILIO_ACCOUNT_SID = $accountSid
$env:TWILIO_AUTH_TOKEN = $authToken
$env:TWILIO_PHONE_NUMBER = $phoneNumber
$env:ENABLE_SMS = "true"

Write-Host "✓ Environment variables set" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To make these permanent, create a .env file with:" -ForegroundColor Yellow
Write-Host "TWILIO_ACCOUNT_SID=$accountSid"
Write-Host "TWILIO_AUTH_TOKEN=$authToken"
Write-Host "TWILIO_PHONE_NUMBER=$phoneNumber"
Write-Host "ENABLE_SMS=true"
Write-Host ""
Write-Host "Now you can run: python run.py" -ForegroundColor Green
Write-Host ""

