@echo off
echo ===================================================================
echo 🎬 Video Extractor Server - Fixed Version
echo ===================================================================
echo.

echo 📋 Installing missing dependency...
python -m pip install pydantic-settings --user

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
