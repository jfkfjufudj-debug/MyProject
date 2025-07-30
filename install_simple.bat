@echo off
echo ===================================================================
echo 🎬 Video Extractor Server - Simple Installation
echo ===================================================================
echo.

echo 📋 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

echo ✅ Python found!
python --version

echo.
echo 📦 Installing core dependencies only...
echo.

echo Installing FastAPI...
python -m pip install fastapi --user

echo Installing Uvicorn...
python -m pip install uvicorn[standard] --user

echo Installing yt-dlp...
python -m pip install yt-dlp --user

echo Installing requests...
python -m pip install requests --user

echo Installing other dependencies...
python -m pip install httpx pydantic python-multipart python-dotenv aiofiles loguru --user

echo.
echo ✅ Core dependencies installed!

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
