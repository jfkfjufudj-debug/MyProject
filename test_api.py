#!/usr/bin/env python3
"""
Test API endpoints with authentication
"""

import urllib.request
import urllib.parse
import json

API_KEY = "default-api-key-change-me"
BASE_URL = "http://127.0.0.1:8000"

def test_extract_without_auth():
    """Test extract without authentication"""
    print("🧪 Testing extract without authentication...")
    
    try:
        data = json.dumps({"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}).encode()
        req = urllib.request.Request(
            f"{BASE_URL}/api/v1/extract",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"❌ Unexpected success: {result}")
            return False
            
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print(f"✅ Correctly rejected (401): {e.read().decode()}")
            return True
        else:
            print(f"❌ Wrong error code: {e.code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_extract_with_auth():
    """Test extract with authentication"""
    print("\n🧪 Testing extract with authentication...")
    
    try:
        data = json.dumps({"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}).encode()
        req = urllib.request.Request(
            f"{BASE_URL}/api/v1/extract",
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"✅ Extract successful: {result.get('success', False)}")
            if result.get('data'):
                print(f"✅ Video title: {result['data'].get('title', 'Unknown')}")
            return result.get('success', False)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_download_with_auth():
    """Test download with authentication"""
    print("\n🧪 Testing download with authentication...")
    
    try:
        data = json.dumps({
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "quality": "best"
        }).encode()
        
        req = urllib.request.Request(
            f"{BASE_URL}/api/v1/download",
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"✅ Download successful: {result.get('success', False)}")
            print(f"✅ Message: {result.get('message', 'No message')}")
            return result.get('success', False)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🎬 Video Extractor Server - API Testing")
    print("=" * 50)
    
    tests = [
        test_extract_without_auth,
        test_extract_with_auth,
        test_download_with_auth
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 API Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API tests passed! Server is fully functional!")
    else:
        print("⚠️ Some API tests failed.")

if __name__ == "__main__":
    main()
