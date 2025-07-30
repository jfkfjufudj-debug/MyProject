#!/usr/bin/env python3
"""
Quick server runner - bypasses complex startup scripts
"""

import sys
import subprocess
import os

def install_missing_packages():
    """Install any missing packages"""
    required_packages = [
        'fastapi',
        'uvicorn[standard]', 
        'yt-dlp',
        'requests',
        'httpx',
        'python-multipart',
        'python-dotenv',
        'aiofiles',
        'loguru'
    ]
    
    print("🔧 Checking and installing required packages...")
    
    for package in required_packages:
        try:
            if package == 'uvicorn[standard]':
                import uvicorn
            elif package == 'python-multipart':
                import multipart
            elif package == 'python-dotenv':
                import dotenv
            elif package == 'yt-dlp':
                import yt_dlp
            else:
                __import__(package.replace('-', '_'))
            print(f"✅ {package} - already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--user'])
                print(f"✅ {package} - installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def run_server():
    """Run the server"""
    print("\n🚀 Starting Video Extractor Server...")
    print("📍 Server will be available at: http://127.0.0.1:8000")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    print("⚠️  Press Ctrl+C to stop the server\n")
    
    try:
        # Import and run
        import uvicorn
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🎬 Video Extractor Server - Auto Setup & Run")
    print("=" * 60)
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Install packages
    if not install_missing_packages():
        print("❌ Failed to install required packages")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Run server
    if not run_server():
        print("❌ Failed to start server")
        input("Press Enter to exit...")
        sys.exit(1)
