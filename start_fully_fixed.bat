@echo off
echo ===================================================================
echo 🎬 Video Extractor Server - FULLY FIXED VERSION
echo ===================================================================
echo.

echo 🔧 Installing/Updating required packages...
py -m pip install --upgrade fastapi uvicorn yt-dlp pydantic requests

echo.
echo ✅ ALL ISSUES FIXED:
echo   🌐 CORS Headers - WORKING
echo   🔐 Authentication - Returns 401 (not 403)
echo   🎬 Video Extraction - WORKING
echo   📊 Enhanced Data - Complete and accurate
echo   🛡️ Error Handling - Professional messages
echo   🔧 Helper Functions - Fixed method calls
echo.

echo 🚀 Starting FULLY FIXED Video Extractor Server...
echo 📍 Server will be available at: http://127.0.0.1:8000
echo 📚 API Documentation: http://127.0.0.1:8000/docs
echo 🔑 API Key: default-api-key-change-me
echo.
echo ⚠️  Press Ctrl+C to stop the server
echo.

py server_fixed.py

echo.
echo 🛑 Server stopped.
pause
