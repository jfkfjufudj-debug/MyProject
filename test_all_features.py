"""
🧪 Complete Server Testing Suite
Tests all features and endpoints of the Video Extractor Server
"""

import requests
import json
import time
from datetime import datetime

# Server configuration
BASE_URL = "http://127.0.0.1:8000"
API_KEY = "default-api-key-change-me"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def print_test_header(test_name):
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")

def print_result(success, message, data=None):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {message}")
    if data:
        print(f"📊 Data: {json.dumps(data, indent=2)}")

def test_health_check():
    print_test_header("Health Check Test")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Health check successful", data)
            return True
        else:
            print_result(False, f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Health check error: {str(e)}")
        return False

def test_home_page():
    print_test_header("Home Page Test")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            content_length = len(response.text)
            has_html = "<html>" in response.text.lower()
            print_result(True, f"Home page loaded successfully ({content_length} chars, HTML: {has_html})")
            return True
        else:
            print_result(False, f"Home page failed with status {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Home page error: {str(e)}")
        return False

def test_docs_page():
    print_test_header("API Documentation Test")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=10)
        if response.status_code == 200:
            has_swagger = "swagger" in response.text.lower()
            print_result(True, f"API docs loaded successfully (Swagger: {has_swagger})")
            return True
        else:
            print_result(False, f"API docs failed with status {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"API docs error: {str(e)}")
        return False

def test_authentication():
    print_test_header("Authentication Test")
    
    # Test without API key
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/extract",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            timeout=10
        )
        if response.status_code == 401:
            print_result(True, "Authentication properly required (401 without key)")
        else:
            print_result(False, f"Expected 401, got {response.status_code}")
    except Exception as e:
        print_result(False, f"Auth test error: {str(e)}")
    
    # Test with wrong API key
    try:
        wrong_headers = {"Authorization": "Bearer wrong-key", "Content-Type": "application/json"}
        response = requests.post(
            f"{BASE_URL}/api/v1/extract",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            headers=wrong_headers,
            timeout=10
        )
        if response.status_code == 401:
            print_result(True, "Wrong API key properly rejected (401)")
            return True
        else:
            print_result(False, f"Expected 401 for wrong key, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Wrong key test error: {str(e)}")
        return False

def test_video_extraction():
    print_test_header("Video Extraction Test")
    
    test_urls = [
        {
            "name": "YouTube Video",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "expected_title": "Rick Astley"
        },
        {
            "name": "YouTube Short URL",
            "url": "https://youtu.be/dQw4w9WgXcQ",
            "expected_title": "Rick Astley"
        }
    ]
    
    results = []
    
    for test in test_urls:
        print(f"\n🎯 Testing: {test['name']}")
        try:
            payload = {"url": test["url"]}
            response = requests.post(
                f"{BASE_URL}/api/v1/extract",
                json=payload,
                headers=HEADERS,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    video_data = data.get("data", {})
                    title = video_data.get("title", "")
                    duration = video_data.get("duration")
                    formats_count = len(video_data.get("formats", []))
                    
                    print_result(True, f"Extraction successful")
                    print(f"   📹 Title: {title}")
                    print(f"   ⏱️ Duration: {duration} seconds")
                    print(f"   🎬 Formats: {formats_count}")
                    print(f"   👤 Uploader: {video_data.get('uploader')}")
                    print(f"   👀 Views: {video_data.get('view_count')}")
                    results.append(True)
                else:
                    print_result(False, f"Extraction failed: {data.get('error')}")
                    results.append(False)
            else:
                print_result(False, f"Request failed with status {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print_result(False, f"Extraction error: {str(e)}")
            results.append(False)
    
    return all(results)

def test_invalid_urls():
    print_test_header("Invalid URL Handling Test")
    
    invalid_urls = [
        "https://invalid-url.com/video",
        "not-a-url",
        "https://www.google.com",
        ""
    ]
    
    results = []
    
    for url in invalid_urls:
        print(f"\n🎯 Testing invalid URL: {url}")
        try:
            payload = {"url": url} if url else {}
            response = requests.post(
                f"{BASE_URL}/api/v1/extract",
                json=payload,
                headers=HEADERS,
                timeout=15
            )
            
            if response.status_code in [400, 422]:
                print_result(True, f"Invalid URL properly rejected ({response.status_code})")
                results.append(True)
            elif response.status_code == 200:
                data = response.json()
                if not data.get("success"):
                    print_result(True, f"Invalid URL handled gracefully: {data.get('error')}")
                    results.append(True)
                else:
                    print_result(False, "Invalid URL should not succeed")
                    results.append(False)
            else:
                print_result(False, f"Unexpected status code: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print_result(True, f"Invalid URL properly caused error: {str(e)}")
            results.append(True)
    
    return all(results)

def test_cors():
    print_test_header("CORS Headers Test")
    try:
        response = requests.options(f"{BASE_URL}/api/v1/extract", timeout=10)
        cors_headers = {
            'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
            'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
            'access-control-allow-headers': response.headers.get('access-control-allow-headers')
        }
        
        has_cors = any(cors_headers.values())
        print_result(has_cors, f"CORS headers present: {has_cors}", cors_headers)
        return has_cors
    except Exception as e:
        print_result(False, f"CORS test error: {str(e)}")
        return False

def main():
    print("🎬 Video Extractor Server - Complete Testing Suite")
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing server at: {BASE_URL}")
    
    # Run all tests
    tests = [
        ("Health Check", test_health_check),
        ("Home Page", test_home_page),
        ("API Documentation", test_docs_page),
        ("Authentication", test_authentication),
        ("Video Extraction", test_video_extraction),
        ("Invalid URL Handling", test_invalid_urls),
        ("CORS Headers", test_cors)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
            time.sleep(1)  # Small delay between tests
        except Exception as e:
            print_result(False, f"Test '{test_name}' crashed: {str(e)}")
            results[test_name] = False
    
    # Final report
    print_test_header("FINAL TEST REPORT")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    print(f"🎯 Success Rate: {(passed/total)*100:.1f}%")
    
    print("\n📋 Detailed Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Server is working perfectly!")
    else:
        print(f"\n⚠️  {total-passed} tests failed. Check the details above.")
    
    print(f"\n🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
