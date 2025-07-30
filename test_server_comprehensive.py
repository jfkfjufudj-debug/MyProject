#!/usr/bin/env python3
"""
🧪 Comprehensive Server Testing Suite
Professional testing for all server features
"""

import requests
import json
import time
from datetime import datetime
import sys

# Server configuration
BASE_URL = "http://127.0.0.1:8000"
API_KEY = "default-api-key-change-me"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

class ServerTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total_tests = 0
        
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        emoji = {"INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}
        print(f"[{timestamp}] {emoji.get(status, 'ℹ️')} {message}")
    
    def test_result(self, test_name, passed, details=""):
        self.total_tests += 1
        if passed:
            self.passed += 1
            self.log(f"{test_name}: PASSED {details}", "PASS")
        else:
            self.failed += 1
            self.log(f"{test_name}: FAILED {details}", "FAIL")
        return passed
    
    def test_health_endpoint(self):
        """Test /health endpoint"""
        self.log("Testing Health Endpoint...")
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=10)
            
            # Test status code
            status_ok = self.test_result("Health Status Code", response.status_code == 200, f"Got {response.status_code}")
            
            # Test response format
            try:
                data = response.json()
                format_ok = self.test_result("Health Response Format", 
                                           "status" in data and "timestamp" in data,
                                           f"Keys: {list(data.keys())}")
                
                # Test health status
                health_ok = self.test_result("Health Status Value", 
                                           data.get("status") == "healthy",
                                           f"Status: {data.get('status')}")
                
                return status_ok and format_ok and health_ok
            except json.JSONDecodeError:
                return self.test_result("Health JSON Parse", False, "Invalid JSON response")
                
        except requests.exceptions.RequestException as e:
            return self.test_result("Health Connection", False, f"Connection error: {str(e)}")
    
    def test_cors_headers(self):
        """Test CORS headers"""
        self.log("Testing CORS Headers...")
        try:
            # Test OPTIONS request
            response = requests.options(f"{BASE_URL}/api/v1/extract", timeout=10)
            
            cors_headers = [
                "Access-Control-Allow-Origin",
                "Access-Control-Allow-Methods", 
                "Access-Control-Allow-Headers"
            ]
            
            cors_ok = True
            for header in cors_headers:
                has_header = header in response.headers
                cors_ok = cors_ok and self.test_result(f"CORS {header}", has_header, 
                                                     f"Value: {response.headers.get(header, 'Missing')}")
            
            return cors_ok
            
        except requests.exceptions.RequestException as e:
            return self.test_result("CORS Test", False, f"Connection error: {str(e)}")
    
    def test_authentication(self):
        """Test authentication scenarios"""
        self.log("Testing Authentication...")
        
        # Test without API key
        try:
            response = requests.post(f"{BASE_URL}/api/v1/extract", 
                                   json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
                                   timeout=10)
            no_auth = self.test_result("No Auth Rejection", response.status_code == 401, 
                                     f"Got {response.status_code}")
        except:
            no_auth = self.test_result("No Auth Test", False, "Connection error")
        
        # Test with wrong API key
        try:
            wrong_headers = {"Authorization": "Bearer wrong-key", "Content-Type": "application/json"}
            response = requests.post(f"{BASE_URL}/api/v1/extract",
                                   headers=wrong_headers,
                                   json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
                                   timeout=10)
            wrong_auth = self.test_result("Wrong Auth Rejection", response.status_code == 401,
                                        f"Got {response.status_code}")
        except:
            wrong_auth = self.test_result("Wrong Auth Test", False, "Connection error")
        
        return no_auth and wrong_auth
    
    def test_video_extraction_valid(self):
        """Test video extraction with valid URL"""
        self.log("Testing Valid Video Extraction...")
        
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll - always available
            "https://youtu.be/dQw4w9WgXcQ"  # Short URL format
        ]
        
        results = []
        for url in test_urls:
            try:
                payload = {"url": url, "format_preference": "best"}
                response = requests.post(f"{BASE_URL}/api/v1/extract",
                                       headers=HEADERS,
                                       json=payload,
                                       timeout=30)
                
                status_ok = self.test_result(f"Extract Status ({url[:30]}...)", 
                                           response.status_code == 200,
                                           f"Got {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        format_ok = self.test_result(f"Extract Format ({url[:30]}...)",
                                                   "success" in data and "data" in data,
                                                   f"Keys: {list(data.keys())}")
                        
                        if data.get("success") and data.get("data"):
                            video_data = data["data"]
                            required_fields = ["title", "duration", "uploader", "formats"]
                            fields_ok = all(field in video_data for field in required_fields)
                            self.test_result(f"Extract Fields ({url[:30]}...)", fields_ok,
                                           f"Has: {[f for f in required_fields if f in video_data]}")
                        
                        results.append(status_ok and format_ok)
                    except json.JSONDecodeError:
                        results.append(self.test_result(f"Extract JSON ({url[:30]}...)", False, "Invalid JSON"))
                else:
                    results.append(False)
                    
            except requests.exceptions.RequestException as e:
                results.append(self.test_result(f"Extract Connection ({url[:30]}...)", False, f"Error: {str(e)}"))
        
        return any(results)  # At least one should work
    
    def test_video_extraction_invalid(self):
        """Test video extraction with invalid URLs"""
        self.log("Testing Invalid Video Extraction...")
        
        invalid_urls = [
            "https://invalid-url.com/video",
            "not-a-url",
            "",
            "https://www.google.com"
        ]
        
        results = []
        for url in invalid_urls:
            try:
                payload = {"url": url, "format_preference": "best"}
                response = requests.post(f"{BASE_URL}/api/v1/extract",
                                       headers=HEADERS,
                                       json=payload,
                                       timeout=15)
                
                # Should return error (either 4xx status code OR success=false in response)
                is_error = False
                if 400 <= response.status_code < 500:
                    is_error = True
                elif response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get("success") == False:
                            is_error = True
                    except:
                        pass

                error_ok = self.test_result(f"Invalid URL Rejection ({url[:20]}...)",
                                          is_error,
                                          f"Status: {response.status_code}, Success: {data.get('success') if 'data' in locals() else 'N/A'}")
                results.append(error_ok)
                
            except requests.exceptions.RequestException as e:
                results.append(self.test_result(f"Invalid URL Test ({url[:20]}...)", False, f"Error: {str(e)}"))
        
        return all(results)
    
    def test_performance(self):
        """Test server performance"""
        self.log("Testing Performance...")
        
        try:
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/health", timeout=10)
            response_time = time.time() - start_time
            
            fast_response = self.test_result("Response Time", response_time < 2.0,
                                           f"{response_time:.2f}s")
            
            return fast_response
            
        except requests.exceptions.RequestException as e:
            return self.test_result("Performance Test", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        self.log("🚀 Starting Comprehensive Server Testing", "INFO")
        self.log("=" * 60, "INFO")
        
        # Run all test categories
        tests = [
            ("Health Endpoint", self.test_health_endpoint),
            ("CORS Headers", self.test_cors_headers),
            ("Authentication", self.test_authentication),
            ("Valid Video Extraction", self.test_video_extraction_valid),
            ("Invalid Video Handling", self.test_video_extraction_invalid),
            ("Performance", self.test_performance)
        ]
        
        for test_name, test_func in tests:
            self.log(f"\n📋 Running {test_name} Tests...", "INFO")
            try:
                test_func()
            except Exception as e:
                self.log(f"Test suite error in {test_name}: {str(e)}", "FAIL")
                self.failed += 1
                self.total_tests += 1
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        self.log("\n" + "=" * 60, "INFO")
        self.log("🎯 TEST SUMMARY", "INFO")
        self.log("=" * 60, "INFO")
        self.log(f"Total Tests: {self.total_tests}", "INFO")
        self.log(f"Passed: {self.passed}", "PASS")
        self.log(f"Failed: {self.failed}", "FAIL")
        
        success_rate = (self.passed / self.total_tests * 100) if self.total_tests > 0 else 0
        self.log(f"Success Rate: {success_rate:.1f}%", "INFO")
        
        if self.failed == 0:
            self.log("🎉 ALL TESTS PASSED! Server is working perfectly!", "PASS")
        else:
            self.log(f"⚠️ {self.failed} tests failed. Check the issues above.", "WARN")

if __name__ == "__main__":
    tester = ServerTester()
    tester.run_all_tests()
