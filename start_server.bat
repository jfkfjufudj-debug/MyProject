@echo off
echo ===================================================================
echo 🎬 Video Extractor Server - Professional Startup Script
echo ===================================================================
echo.

echo 📋 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo 📥 Please install Python 3.8+ from: https://python.org/downloads
    echo ⚠️  Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found!
python --version

echo.
echo 📦 Installing dependencies...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo.
    echo 💡 Try running as administrator or check your internet connection
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed successfully!

echo.
echo 🚀 Starting Video Extractor Server...
echo 📍 Server will be available at: http://127.0.0.1:8000
echo 📚 API Documentation: http://127.0.0.1:8000/docs
echo.
echo ⚠️  Press Ctrl+C to stop the server
echo.

python main.py

echo.
echo 🛑 Server stopped.
pause
