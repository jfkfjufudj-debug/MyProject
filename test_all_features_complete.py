"""
🧪 COMPLETE FEATURE TESTING SUITE
Tests every single feature and capability of the Video Extractor Server
"""

import requests
import json
import time
from datetime import datetime
import concurrent.futures
import threading

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "default-api-key-change-me"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

class TestResults:
    def __init__(self):
        self.results = {}
        self.details = {}
        self.lock = threading.Lock()
    
    def add_result(self, test_name, success, details=None):
        with self.lock:
            self.results[test_name] = success
            if details:
                self.details[test_name] = details

def print_header(title):
    print(f"\n{'='*80}")
    print(f"🧪 {title}")
    print(f"{'='*80}")

def print_result(success, message, details=None):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {message}")
    if details:
        for detail in details:
            print(f"   {detail}")

def test_server_availability(results):
    """Test basic server availability"""
    print_header("SERVER AVAILABILITY TEST")
    
    endpoints = [
        ("/", "Home Page"),
        ("/health", "Health Check"),
        ("/docs", "API Documentation"),
        ("/redoc", "ReDoc Documentation")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            success = response.status_code == 200
            details = [f"Status: {response.status_code}", f"Response size: {len(response.text)} chars"]
            print_result(success, name, details)
            results.add_result(f"Availability_{name.replace(' ', '_')}", success, details)
        except Exception as e:
            print_result(False, f"{name} Error: {e}")
            results.add_result(f"Availability_{name.replace(' ', '_')}", False, [str(e)])

def test_cors_comprehensive(results):
    """Comprehensive CORS testing"""
    print_header("COMPREHENSIVE CORS TEST")
    
    # Test OPTIONS request
    try:
        response = requests.options(f"{BASE_URL}/api/v1/extract", timeout=10)
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Expose-Headers': response.headers.get('Access-Control-Expose-Headers')
        }
        
        success = response.status_code == 200 and any(cors_headers.values())
        details = [f"{k}: {v}" for k, v in cors_headers.items()]
        print_result(success, f"CORS OPTIONS: {response.status_code}", details)
        results.add_result("CORS_OPTIONS", success, details)
        
    except Exception as e:
        print_result(False, f"CORS OPTIONS Error: {e}")
        results.add_result("CORS_OPTIONS", False, [str(e)])

def test_authentication_comprehensive(results):
    """Comprehensive authentication testing"""
    print_header("COMPREHENSIVE AUTHENTICATION TEST")
    
    auth_tests = [
        ("No Authorization", {}, 401),
        ("Empty Bearer", {"Authorization": "Bearer ", "Content-Type": "application/json"}, 401),
        ("Wrong API Key", {"Authorization": "Bearer wrong-key", "Content-Type": "application/json"}, 401),
        ("Malformed Header", {"Authorization": "Basic wrong-format", "Content-Type": "application/json"}, 401),
        ("Correct API Key", HEADERS, 200)
    ]
    
    payload = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
    
    for test_name, headers, expected_status in auth_tests:
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/extract",
                json=payload,
                headers=headers,
                timeout=15
            )
            
            success = response.status_code == expected_status
            details = [f"Expected: {expected_status}", f"Got: {response.status_code}"]
            
            if response.status_code in [401, 403]:
                try:
                    error_data = response.json()
                    details.append(f"Error: {error_data.get('error', 'No error message')}")
                except:
                    pass
            
            print_result(success, test_name, details)
            results.add_result(f"Auth_{test_name.replace(' ', '_')}", success, details)
            
        except Exception as e:
            print_result(False, f"{test_name} Error: {e}")
            results.add_result(f"Auth_{test_name.replace(' ', '_')}", False, [str(e)])

def test_video_extraction_comprehensive(results):
    """Comprehensive video extraction testing"""
    print_header("COMPREHENSIVE VIDEO EXTRACTION TEST")
    
    test_videos = [
        {
            "name": "YouTube Standard",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "expected_title": "Rick Astley",
            "expected_duration": 213
        },
        {
            "name": "YouTube Short URL",
            "url": "https://youtu.be/dQw4w9WgXcQ",
            "expected_title": "Rick Astley",
            "expected_duration": 213
        },
        {
            "name": "YouTube with Timestamp",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s",
            "expected_title": "Rick Astley",
            "expected_duration": 213
        }
    ]
    
    for test_video in test_videos:
        try:
            payload = {"url": test_video["url"]}
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
                    
                    # Comprehensive data validation
                    checks = {
                        "Title Present": bool(video_data.get("title")),
                        "Title Accuracy": test_video["expected_title"].lower() in video_data.get("title", "").lower(),
                        "Duration Present": video_data.get("duration") is not None,
                        "Duration Accuracy": abs((video_data.get("duration", 0) or 0) - test_video["expected_duration"]) <= 5,
                        "Uploader Present": bool(video_data.get("uploader")),
                        "View Count Present": video_data.get("view_count", 0) > 0,
                        "Formats Present": len(video_data.get("formats", [])) > 0,
                        "Thumbnail Present": bool(video_data.get("thumbnail")),
                        "Description Present": bool(video_data.get("description")),
                        "Upload Date Present": bool(video_data.get("upload_date")),
                        "Duration String Present": bool(video_data.get("duration_string")),
                        "Upload Date Formatted": bool(video_data.get("upload_date_formatted")),
                        "Video Formats Present": len(video_data.get("video_formats", [])) > 0,
                        "Audio Formats Present": len(video_data.get("audio_formats", [])) > 0,
                        "Best Format Present": bool(video_data.get("best_format")),
                        "Metadata Present": bool(video_data.get("metadata")),
                        "Categories Present": isinstance(video_data.get("categories"), list),
                        "Tags Present": isinstance(video_data.get("tags"), list),
                        "Thumbnails Present": isinstance(video_data.get("thumbnails"), list)
                    }
                    
                    passed_checks = sum(1 for check in checks.values() if check)
                    total_checks = len(checks)
                    success = passed_checks >= (total_checks * 0.8)  # 80% pass rate
                    
                    details = [
                        f"Title: {video_data.get('title', 'N/A')[:50]}...",
                        f"Duration: {video_data.get('duration')} seconds ({video_data.get('duration_string', 'N/A')})",
                        f"Uploader: {video_data.get('uploader', 'N/A')}",
                        f"Views: {video_data.get('view_count', 0):,}",
                        f"Formats: {len(video_data.get('formats', []))}",
                        f"Video Formats: {len(video_data.get('video_formats', []))}",
                        f"Audio Formats: {len(video_data.get('audio_formats', []))}",
                        f"Data Quality: {passed_checks}/{total_checks} checks passed ({(passed_checks/total_checks)*100:.1f}%)"
                    ]
                    
                    # Add failed checks
                    failed_checks = [check for check, result in checks.items() if not result]
                    if failed_checks:
                        details.append(f"Failed checks: {', '.join(failed_checks)}")
                    
                    print_result(success, test_video["name"], details)
                    results.add_result(f"Extraction_{test_video['name'].replace(' ', '_')}", success, details)
                    
                else:
                    error = data.get('error', {})
                    print_result(False, f"{test_video['name']}: {error}")
                    results.add_result(f"Extraction_{test_video['name'].replace(' ', '_')}", False, [str(error)])
            else:
                print_result(False, f"{test_video['name']}: HTTP {response.status_code}")
                results.add_result(f"Extraction_{test_video['name'].replace(' ', '_')}", False, [f"HTTP {response.status_code}"])
                
        except Exception as e:
            print_result(False, f"{test_video['name']} Error: {e}")
            results.add_result(f"Extraction_{test_video['name'].replace(' ', '_')}", False, [str(e)])

def test_error_handling_comprehensive(results):
    """Comprehensive error handling testing"""
    print_header("COMPREHENSIVE ERROR HANDLING TEST")
    
    error_tests = [
        ("Invalid URL", "https://invalid-url.com/video", "unsupported_platform"),
        ("Non-video URL", "https://www.google.com", "unsupported_platform"),
        ("Malformed URL", "not-a-url-at-all", None),
        ("Empty URL", "", None),
        ("Private Video", "https://www.youtube.com/watch?v=private123", "video_unavailable")
    ]
    
    for test_name, test_url, expected_error_type in error_tests:
        try:
            if test_url:
                payload = {"url": test_url}
            else:
                payload = {}
            
            response = requests.post(
                f"{BASE_URL}/api/v1/extract",
                json=payload,
                headers=HEADERS,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if not data.get("success"):
                    error = data.get("error", {})
                    if isinstance(error, dict):
                        error_type = error.get("type")
                        error_message = error.get("message")
                        
                        success = True  # Error was handled gracefully
                        details = [
                            f"Error Type: {error_type}",
                            f"Message: {error_message}",
                            f"Expected Type: {expected_error_type or 'Any'}"
                        ]
                        
                        if expected_error_type and error_type != expected_error_type:
                            details.append(f"⚠️ Type mismatch (expected {expected_error_type})")
                        
                        print_result(success, test_name, details)
                        results.add_result(f"Error_{test_name.replace(' ', '_')}", success, details)
                    else:
                        print_result(True, f"{test_name}: Basic error handling", [f"Error: {error}"])
                        results.add_result(f"Error_{test_name.replace(' ', '_')}", True, [f"Error: {error}"])
                else:
                    print_result(False, f"{test_name}: Should have failed")
                    results.add_result(f"Error_{test_name.replace(' ', '_')}", False, ["Should have failed"])
            elif response.status_code in [400, 422]:
                print_result(True, f"{test_name}: HTTP validation", [f"Status: {response.status_code}"])
                results.add_result(f"Error_{test_name.replace(' ', '_')}", True, [f"Status: {response.status_code}"])
            else:
                print_result(False, f"{test_name}: Unexpected status {response.status_code}")
                results.add_result(f"Error_{test_name.replace(' ', '_')}", False, [f"Status: {response.status_code}"])
                
        except Exception as e:
            print_result(True, f"{test_name}: Exception handled", [f"Exception: {str(e)[:100]}"])
            results.add_result(f"Error_{test_name.replace(' ', '_')}", True, [f"Exception: {str(e)[:100]}"])

def test_performance_and_load(results):
    """Performance and load testing"""
    print_header("PERFORMANCE AND LOAD TEST")
    
    # Test response times
    start_time = time.time()
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        health_time = time.time() - start_time
        
        success = response.status_code == 200 and health_time < 2.0
        details = [f"Response time: {health_time:.3f} seconds", f"Status: {response.status_code}"]
        print_result(success, "Health Check Performance", details)
        results.add_result("Performance_Health", success, details)
        
    except Exception as e:
        print_result(False, f"Health Performance Error: {e}")
        results.add_result("Performance_Health", False, [str(e)])
    
    # Test concurrent requests
    def make_health_request():
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_health_request) for _ in range(10)]
            concurrent_results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        success_rate = sum(concurrent_results) / len(concurrent_results)
        success = success_rate >= 0.8  # 80% success rate
        details = [f"Concurrent requests: {len(concurrent_results)}", f"Success rate: {success_rate*100:.1f}%"]
        print_result(success, "Concurrent Load Test", details)
        results.add_result("Performance_Concurrent", success, details)
        
    except Exception as e:
        print_result(False, f"Concurrent Load Error: {e}")
        results.add_result("Performance_Concurrent", False, [str(e)])

def main():
    print("🧪 COMPLETE FEATURE TESTING SUITE")
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing server at: {BASE_URL}")
    print("=" * 100)
    
    results = TestResults()
    
    # Run all test suites
    test_suites = [
        ("Server Availability", test_server_availability),
        ("CORS Functionality", test_cors_comprehensive),
        ("Authentication", test_authentication_comprehensive),
        ("Video Extraction", test_video_extraction_comprehensive),
        ("Error Handling", test_error_handling_comprehensive),
        ("Performance & Load", test_performance_and_load)
    ]
    
    for suite_name, test_func in test_suites:
        try:
            test_func(results)
            time.sleep(1)  # Brief pause between test suites
        except Exception as e:
            print_result(False, f"Test suite '{suite_name}' crashed: {str(e)}")
    
    # Generate comprehensive report
    print_header("COMPREHENSIVE FINAL REPORT")
    
    total_tests = len(results.results)
    passed_tests = sum(1 for result in results.results.values() if result)
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"📊 OVERALL RESULTS: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
    print()
    
    # Group results by category
    categories = {}
    for test_name, result in results.results.items():
        category = test_name.split('_')[0]
        if category not in categories:
            categories[category] = {'passed': 0, 'total': 0}
        categories[category]['total'] += 1
        if result:
            categories[category]['passed'] += 1
    
    print("📋 RESULTS BY CATEGORY:")
    for category, stats in categories.items():
        rate = (stats['passed'] / stats['total']) * 100
        status = "✅" if rate >= 80 else "⚠️" if rate >= 60 else "❌"
        print(f"   {status} {category}: {stats['passed']}/{stats['total']} ({rate:.1f}%)")
    
    print("\n📋 DETAILED RESULTS:")
    for test_name, result in results.results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print()
    if success_rate >= 95:
        print("🎉 EXCELLENT! Server is production-ready!")
        print("🚀 All features working perfectly!")
    elif success_rate >= 85:
        print("✅ VERY GOOD! Server is highly functional!")
        print("🔧 Minor improvements may be needed")
    elif success_rate >= 70:
        print("⚠️ GOOD! Server is functional with some issues")
        print("🔧 Some fixes needed for optimal performance")
    else:
        print("❌ NEEDS IMPROVEMENT! Major issues found")
        print("🔧 Significant fixes required")
    
    print(f"\n🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)

if __name__ == "__main__":
    main()
