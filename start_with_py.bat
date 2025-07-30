@echo off
echo ===================================================================
echo 🎬 Video Extractor Server - Using PY Command
echo ===================================================================
echo.

echo 🔍 Checking Python installation...
py --version
if %errorlevel% neq 0 (
    echo ❌ Python not found with 'py' command
    echo 💡 Please install Python from: https://www.python.org/downloads/
    echo ⚠️  Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo.
echo 🚀 Starting Video Extractor Server...
echo 📍 Server will be available at: http://127.0.0.1:8000
echo 📚 API Documentation: http://127.0.0.1:8000/docs
echo.
echo ⚠️  Press Ctrl+C to stop the server
echo.

py test_basic.py

echo.
echo 🛑 Server stopped.
pause
