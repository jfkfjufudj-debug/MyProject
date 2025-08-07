#!/usr/bin/env python3
"""
Test script for Video Extractor Server
"""

import requests
import json
import time

# Server configuration
BASE_URL = "http://127.0.0.1:8000"
API_KEY = "default-api-key-change-me"

def test_root():
    """Test root endpoint"""
    print("🧪 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health():
    """Test health endpoint"""
    print("\n🧪 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_extract_without_auth():
    """Test extract endpoint without authentication"""
    print("\n🧪 Testing extract without authentication...")
    try:
        data = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        response = requests.post(f"{BASE_URL}/api/v1/extract", json=data)
        print(f"✅ Status: {response.status_code} (should be 401)")
        print(f"✅ Response: {response.json()}")
        return response.status_code == 401
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_extract_with_auth():
    """Test extract endpoint with authentication"""
    print("\n🧪 Testing extract with authentication...")
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        data = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        response = requests.post(f"{BASE_URL}/api/v1/extract", json=data, headers=headers)
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_download_with_auth():
    """Test download endpoint with authentication"""
    print("\n🧪 Testing download with authentication...")
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        data = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "quality": "best"}
        response = requests.post(f"{BASE_URL}/api/v1/download", json=data, headers=headers)
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎬 Video Extractor Server - Local Testing")
    print("=" * 50)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    tests = [
        test_root,
        test_health,
        test_extract_without_auth,
        test_extract_with_auth,
        test_download_with_auth
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Server is working perfectly!")
    else:
        print("⚠️ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
