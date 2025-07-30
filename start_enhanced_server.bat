@echo off
echo ===================================================================
echo 🎬 Video Extractor Server - ENHANCED VERSION
echo ===================================================================
echo.

echo 🔧 Installing/Updating required packages...
py -m pip install --upgrade fastapi uvicorn yt-dlp pydantic requests

echo.
echo ✨ ENHANCEMENTS APPLIED:
echo   ✅ Fixed CORS headers for browser compatibility
echo   ✅ Improved authentication (401 instead of 403)
echo   ✅ Enhanced data accuracy and completeness
echo   ✅ Better format categorization (video/audio/combined)
echo   ✅ Improved error handling with detailed messages
echo   ✅ Added metadata and timestamps
echo   ✅ OPTIONS endpoint for CORS preflight
echo.

echo 🚀 Starting Enhanced Video Extractor Server...
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
