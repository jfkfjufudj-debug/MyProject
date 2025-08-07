#!/usr/bin/env python3
"""
Simple test without external dependencies
"""

import urllib.request
import json

def test_server():
    """Test server endpoints"""
    print("🧪 Testing Video Extractor Server...")
    
    try:
        # Test root endpoint
        print("Testing root endpoint...")
        with urllib.request.urlopen("http://127.0.0.1:8000/") as response:
            data = json.loads(response.read().decode())
            print(f"✅ Root: {data}")
        
        # Test health endpoint
        print("Testing health endpoint...")
        with urllib.request.urlopen("http://127.0.0.1:8000/health") as response:
            data = json.loads(response.read().decode())
            print(f"✅ Health: {data}")
        
        print("🎉 Basic tests passed! Server is working!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_server()
