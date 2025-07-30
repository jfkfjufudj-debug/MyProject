@echo off
echo ===================================================================
echo 🎬 Video Extractor Server - Working Version
echo ===================================================================
echo.

echo 🔧 Installing required packages...
py -m pip install fastapi uvicorn yt-dlp pydantic

echo.
echo 🚀 Starting Video Extractor Server...
echo 📍 Server will be available at: http://127.0.0.1:8000
echo 📚 API Documentation: http://127.0.0.1:8000/docs
echo 🔑 API Key: default-api-key-change-me
echo.
echo ⚠️  Press Ctrl+C to stop the server
echo.

py server_working.py

echo.
echo 🛑 Server stopped.
pause
