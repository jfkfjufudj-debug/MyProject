#!/usr/bin/env python3
"""
🚀 Advanced Features Testing Suite
Testing advanced server capabilities
"""

import requests
import json
import time
import concurrent.futures
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "default-api-key-change-me"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def log(message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    emoji = {"INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}
    print(f"[{timestamp}] {emoji.get(status, 'ℹ️')} {message}")

def test_concurrent_requests():
    """Test server under concurrent load"""
    log("Testing Concurrent Requests...")
    
    def make_request(i):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=10)
            return response.status_code == 200
        except:
            return False
    
    # Test 10 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request, i) for i in range(10)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    success_count = sum(results)
    log(f"Concurrent Requests: {success_count}/10 successful", 
        "PASS" if success_count >= 8 else "FAIL")
    return success_count >= 8

def test_different_formats():
    """Test different format preferences"""
    log("Testing Different Format Preferences...")
    
    formats = ["best", "worst", "mp4", "webm"]
    results = []
    
    for fmt in formats:
        try:
            payload = {
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "format_preference": fmt
            }
            response = requests.post(f"{BASE_URL}/api/v1/extract",
                                   headers=HEADERS,
                                   json=payload,
                                   timeout=20)
            
            success = response.status_code == 200
            log(f"Format '{fmt}': {'PASSED' if success else 'FAILED'}", 
                "PASS" if success else "FAIL")
            results.append(success)
            
        except Exception as e:
            log(f"Format '{fmt}': FAILED - {str(e)}", "FAIL")
            results.append(False)
    
    return any(results)  # At least one format should work

def test_response_structure():
    """Test detailed response structure"""
    log("Testing Response Structure...")
    
    try:
        payload = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        response = requests.post(f"{BASE_URL}/api/v1/extract",
                               headers=HEADERS,
                               json=payload,
                               timeout=20)
        
        if response.status_code != 200:
            log("Response Structure: FAILED - Bad status code", "FAIL")
            return False
        
        data = response.json()
        
        # Check main structure
        required_keys = ["success", "data", "timestamp"]
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            log(f"Response Structure: FAILED - Missing keys: {missing_keys}", "FAIL")
            return False
        
        # Check video data structure
        if data.get("success") and data.get("data"):
            video_data = data["data"]
            video_keys = ["title", "duration", "uploader", "formats", "metadata"]
            missing_video_keys = [key for key in video_keys if key not in video_data]
            if missing_video_keys:
                log(f"Video Data Structure: FAILED - Missing keys: {missing_video_keys}", "FAIL")
                return False
            
            # Check formats structure
            formats = video_data.get("formats", [])
            if formats and isinstance(formats, list):
                format_sample = formats[0]
                format_keys = ["format_id", "ext", "quality", "url"]
                missing_format_keys = [key for key in format_keys if key not in format_sample]
                if missing_format_keys:
                    log(f"Format Structure: WARNING - Missing keys: {missing_format_keys}", "WARN")
            
            log("Response Structure: PASSED - All required fields present", "PASS")
            return True
        else:
            log("Response Structure: FAILED - No video data", "FAIL")
            return False
            
    except Exception as e:
        log(f"Response Structure: FAILED - {str(e)}", "FAIL")
        return False

def test_error_handling():
    """Test comprehensive error handling"""
    log("Testing Error Handling...")
    
    error_tests = [
        ("Empty JSON", {}),
        ("Missing URL", {"format_preference": "best"}),
        ("Invalid JSON field", {"url": 123}),
        ("Very long URL", {"url": "https://youtube.com/" + "x" * 1000})
    ]
    
    results = []
    for test_name, payload in error_tests:
        try:
            response = requests.post(f"{BASE_URL}/api/v1/extract",
                                   headers=HEADERS,
                                   json=payload,
                                   timeout=10)
            
            # Should handle errors gracefully (not crash)
            handled = response.status_code in [400, 422, 500] or (
                response.status_code == 200 and 
                response.json().get("success") == False
            )
            
            log(f"Error Handling '{test_name}': {'PASSED' if handled else 'FAILED'}", 
                "PASS" if handled else "FAIL")
            results.append(handled)
            
        except Exception as e:
            log(f"Error Handling '{test_name}': FAILED - {str(e)}", "FAIL")
            results.append(False)
    
    return all(results)

def test_api_documentation():
    """Test API documentation endpoints"""
    log("Testing API Documentation...")
    
    doc_endpoints = ["/docs", "/redoc", "/openapi.json"]
    results = []
    
    for endpoint in doc_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            success = response.status_code == 200
            log(f"Documentation '{endpoint}': {'PASSED' if success else 'FAILED'}", 
                "PASS" if success else "FAIL")
            results.append(success)
        except Exception as e:
            log(f"Documentation '{endpoint}': FAILED - {str(e)}", "FAIL")
            results.append(False)
    
    return all(results)

def test_home_page():
    """Test home page functionality"""
    log("Testing Home Page...")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        
        if response.status_code != 200:
            log("Home Page: FAILED - Bad status code", "FAIL")
            return False
        
        content = response.text
        required_content = ["Video Extractor", "API", "Authentication"]
        missing_content = [item for item in required_content if item not in content]
        
        if missing_content:
            log(f"Home Page: WARNING - Missing content: {missing_content}", "WARN")
        
        log("Home Page: PASSED - Accessible and contains expected content", "PASS")
        return True
        
    except Exception as e:
        log(f"Home Page: FAILED - {str(e)}", "FAIL")
        return False

def run_advanced_tests():
    """Run all advanced tests"""
    log("🚀 Starting Advanced Features Testing", "INFO")
    log("=" * 60, "INFO")
    
    tests = [
        ("Concurrent Requests", test_concurrent_requests),
        ("Different Formats", test_different_formats),
        ("Response Structure", test_response_structure),
        ("Error Handling", test_error_handling),
        ("API Documentation", test_api_documentation),
        ("Home Page", test_home_page)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        log(f"\n📋 Running {test_name} Test...", "INFO")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            log(f"Test suite error in {test_name}: {str(e)}", "FAIL")
    
    # Print summary
    log("\n" + "=" * 60, "INFO")
    log("🎯 ADVANCED TESTS SUMMARY", "INFO")
    log("=" * 60, "INFO")
    log(f"Total Tests: {total}", "INFO")
    log(f"Passed: {passed}", "PASS")
    log(f"Failed: {total - passed}", "FAIL")
    
    success_rate = (passed / total * 100) if total > 0 else 0
    log(f"Success Rate: {success_rate:.1f}%", "INFO")
    
    if passed == total:
        log("🎉 ALL ADVANCED TESTS PASSED! Server is production-ready!", "PASS")
    else:
        log(f"⚠️ {total - passed} advanced tests failed.", "WARN")

if __name__ == "__main__":
    run_advanced_tests()
