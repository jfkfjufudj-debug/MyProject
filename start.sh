#!/bin/bash
# Start script for Render deployment
echo "🚀 Starting Video Extractor Server..."
echo "📁 Current directory: $(pwd)"
echo "📋 Files in directory:"
ls -la

echo "🐍 Python version:"
python --version

echo "📦 Installed packages:"
pip list | grep -E "(fastapi|uvicorn|yt-dlp)"

echo "🎬 Starting server with main_render.py..."
exec uvicorn main_render:app --host 0.0.0.0 --port $PORT
