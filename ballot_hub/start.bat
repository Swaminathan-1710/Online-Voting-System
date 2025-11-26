@echo off
echo ========================================
echo BallotHub - Starting Application
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/3] Checking MongoDB connection...
python -c "from database.connection import get_client; get_client().server_info(); print('✓ MongoDB connected')" 2>nul
if errorlevel 1 (
    echo ⚠ Warning: MongoDB connection failed!
    echo Make sure MongoDB is running on mongodb://localhost:27017
    echo.
    pause
)

echo [3/3] Starting Flask server...
echo.
echo ========================================
echo Server will start on http://127.0.0.1:5000
echo ========================================
echo.
echo Default Admin Credentials:
echo   Username: admin
echo   Password: AdminPass123
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause

