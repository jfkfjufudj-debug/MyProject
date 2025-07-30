#!/bin/bash

echo "==================================================================="
echo "🎬 Video Extractor Server - Professional Startup Script"
echo "==================================================================="
echo

echo "📋 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python is not installed or not in PATH"
        echo
        echo "📥 Please install Python 3.8+ from your package manager:"
        echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "   CentOS/RHEL:   sudo yum install python3 python3-pip"
        echo "   macOS:         brew install python3"
        echo
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python found!"
$PYTHON_CMD --version

echo
echo "📦 Installing dependencies..."
$PYTHON_CMD -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo
    echo "💡 Try running with sudo or check your internet connection"
    exit 1
fi

echo
echo "✅ Dependencies installed successfully!"

echo
echo "🚀 Starting Video Extractor Server..."
echo "📍 Server will be available at: http://127.0.0.1:8000"
echo "📚 API Documentation: http://127.0.0.1:8000/docs"
echo
echo "⚠️  Press Ctrl+C to stop the server"
echo

$PYTHON_CMD main.py

echo
echo "🛑 Server stopped."
