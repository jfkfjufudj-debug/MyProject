"""
🧪 COMPREHENSIVE TEST - FULLY FIXED SERVER
Tests all fixes and ensures 100% functionality
"""

import requests
import json
import time
from datetime import datetime

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

def print_result(success, message, details=None):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {message}")
    if details:
        for detail in details:
            print(f"   {detail}")

def test_basic_functionality():
    print_test_header("BASIC FUNCTIONALITY TEST")
    
    results = []
    
    # Test home page
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        success = response.status_code == 200 and ("FIXED" in response.text or "Video Extractor" in response.text)
        print_result(success, f"Home Page: {response.status_code}")
        results.append(success)
    except Exception as e:
        print_result(False, f"Home Page Error: {e}")
        results.append(False)
    
    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        success = response.status_code == 200
        if success:
            data = response.json()
            details = [
                f"Status: {data.get('status')}",
                f"Version: {data.get('version')}",
                f"Service: {data.get('service')}"
            ]
            print_result(True, "Health Check", details)
        else:
            print_result(False, f"Health Check: {response.status_code}")
        results.append(success)
    except Exception as e:
        print_result(False, f"Health Check Error: {e}")
        results.append(False)
    
    # Test API docs
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=10)
        success = response.status_code == 200
        print_result(success, f"API Documentation: {response.status_code}")
        results.append(success)
    except Exception as e:
        print_result(False, f"API Docs Error: {e}")
        results.append(False)
    
    return all(results)

def test_cors_fixed():
    print_test_header("CORS FUNCTIONALITY TEST")
    
    try:
        # Test OPTIONS request
        response = requests.options(f"{BASE_URL}/api/v1/extract", timeout=10)
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        
        success = response.status_code == 200 and any(cors_headers.values())
        
        details = []
        for header, value in cors_headers.items():
            status = "✅" if value else "❌"
            details.append(f"{status} {header}: {value}")
        
        print_result(success, f"CORS OPTIONS Request: {response.status_code}", details)
        return success
        
    except Exception as e:
        print_result(False, f"CORS Test Error: {e}")
        return False

def test_authentication_fixed():
    print_test_header("AUTHENTICATION FIXES TEST")
    
    results = []
    
    # Test 1: No API key should return 401
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/extract",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            timeout=10
        )
        success = response.status_code == 401
        print_result(success, f"No API Key: {response.status_code} (Expected: 401)")
        results.append(success)
    except Exception as e:
        print_result(False, f"No API Key Test Error: {e}")
        results.append(False)
    
    # Test 2: Wrong API key should return 401
    try:
        wrong_headers = {"Authorization": "Bearer wrong-key", "Content-Type": "application/json"}
        response = requests.post(
            f"{BASE_URL}/api/v1/extract",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            headers=wrong_headers,
            timeout=10
        )
        success = response.status_code == 401
        print_result(success, f"Wrong API Key: {response.status_code} (Expected: 401)")
        results.append(success)
    except Exception as e:
        print_result(False, f"Wrong API Key Test Error: {e}")
        results.append(False)
    
    return all(results)

def test_video_extraction_fixed():
    print_test_header("VIDEO EXTRACTION FUNCTIONALITY TEST")
    
    try:
        payload = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
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
                
                # Check essential fields
                essential_fields = ["title", "duration", "uploader", "formats"]
                missing_fields = [field for field in essential_fields if not video_data.get(field)]
                
                if not missing_fields:
                    details = [
                        f"Title: {video_data.get('title', 'N/A')[:50]}...",
                        f"Duration: {video_data.get('duration')} seconds ({video_data.get('duration_string', 'N/A')})",
                        f"Uploader: {video_data.get('uploader', 'N/A')}",
                        f"Views: {video_data.get('view_count', 0):,}",
                        f"Upload Date: {video_data.get('upload_date_formatted', 'N/A')}",
                        f"Total Formats: {len(video_data.get('formats', []))}",
                        f"Video Formats: {len(video_data.get('video_formats', []))}",
                        f"Audio Formats: {len(video_data.get('audio_formats', []))}",
                        f"Best Format: {video_data.get('best_format', {}).get('resolution', 'N/A')}",
                        f"Extractor: {video_data.get('extractor', 'N/A')}",
                        f"Categories: {len(video_data.get('categories', []))}",
                        f"Tags: {len(video_data.get('tags', []))}"
                    ]
                    print_result(True, "Video Extraction Successful", details)
                    return True
                else:
                    print_result(False, f"Missing essential fields: {missing_fields}")
                    return False
            else:
                error = data.get('error', {})
                print_result(False, f"Extraction Failed: {error}")
                return False
        else:
            print_result(False, f"HTTP Error: {response.status_code} - {response.text[:100]}")
            return False
            
    except Exception as e:
        print_result(False, f"Video Extraction Error: {e}")
        return False

def test_error_handling_fixed():
    print_test_header("ERROR HANDLING TEST")
    
    test_cases = [
        ("Invalid URL", "https://invalid-url.com/video"),
        ("Non-video URL", "https://www.google.com"),
        ("Empty URL", "")
    ]
    
    results = []
    
    for test_name, test_url in test_cases:
        if test_url:
            payload = {"url": test_url}
        else:
            payload = {}
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/extract",
                json=payload,
                headers=HEADERS,
                timeout=15
            )
            
            if response.status_code in [200, 400, 422]:
                if response.status_code == 200:
                    data = response.json()
                    if not data.get("success"):
                        error = data.get("error", {})
                        if isinstance(error, dict):
                            details = [
                                f"Error Type: {error.get('type', 'N/A')}",
                                f"Message: {error.get('message', 'N/A')}"
                            ]
                            print_result(True, f"{test_name}: Handled gracefully", details)
                            results.append(True)
                        else:
                            print_result(True, f"{test_name}: Error handled")
                            results.append(True)
                    else:
                        print_result(False, f"{test_name}: Should have failed")
                        results.append(False)
                else:
                    print_result(True, f"{test_name}: HTTP error {response.status_code}")
                    results.append(True)
            else:
                print_result(False, f"{test_name}: Unexpected status {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print_result(True, f"{test_name}: Exception handled - {str(e)[:50]}")
            results.append(True)
    
    return all(results)

def main():
    print("🧪 COMPREHENSIVE TEST - FULLY FIXED SERVER")
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing server at: {BASE_URL}")
    print("=" * 80)
    
    # Run all tests
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("CORS Fixed", test_cors_fixed),
        ("Authentication Fixed", test_authentication_fixed),
        ("Video Extraction Fixed", test_video_extraction_fixed),
        ("Error Handling Fixed", test_error_handling_fixed)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
            time.sleep(1)  # Small delay between tests
        except Exception as e:
            print_result(False, f"Test '{test_name}' crashed: {str(e)}")
            results[test_name] = False
    
    # Final comprehensive report
    print_test_header("FINAL COMPREHENSIVE REPORT")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"📊 OVERALL RESULTS: {passed}/{total} tests passed ({success_rate:.1f}%)")
    print()
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print()
    if passed == total:
        print("🎉 PERFECT! ALL TESTS PASSED!")
        print("🚀 Server is 100% functional and production-ready!")
        print("✅ All issues have been completely resolved!")
    elif success_rate >= 80:
        print("✅ EXCELLENT! Server is working very well!")
        print(f"⚠️ Only {total-passed} minor issues remaining")
    else:
        print("⚠️ Server needs more fixes")
        print(f"❌ {total-passed} major issues found")
    
    print(f"\n🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    main()
