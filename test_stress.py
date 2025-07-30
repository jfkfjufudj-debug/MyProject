#!/usr/bin/env python3
"""
💪 Stress Testing Suite
Testing server under heavy load
"""

import requests
import time
import threading
from datetime import datetime
import statistics

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

class StressTester:
    def __init__(self):
        self.results = []
        self.errors = []
        self.lock = threading.Lock()
    
    def make_health_request(self, thread_id):
        """Make a health check request"""
        try:
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            end_time = time.time()
            
            with self.lock:
                self.results.append({
                    'thread_id': thread_id,
                    'status_code': response.status_code,
                    'response_time': end_time - start_time,
                    'success': response.status_code == 200
                })
        except Exception as e:
            with self.lock:
                self.errors.append({
                    'thread_id': thread_id,
                    'error': str(e)
                })
    
    def make_extract_request(self, thread_id):
        """Make a video extraction request"""
        try:
            start_time = time.time()
            payload = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
            response = requests.post(f"{BASE_URL}/api/v1/extract",
                                   headers=HEADERS,
                                   json=payload,
                                   timeout=30)
            end_time = time.time()
            
            with self.lock:
                self.results.append({
                    'thread_id': thread_id,
                    'status_code': response.status_code,
                    'response_time': end_time - start_time,
                    'success': response.status_code == 200
                })
        except Exception as e:
            with self.lock:
                self.errors.append({
                    'thread_id': thread_id,
                    'error': str(e)
                })
    
    def run_concurrent_health_checks(self, num_threads=20):
        """Run concurrent health checks"""
        log(f"Running {num_threads} concurrent health checks...")
        
        self.results = []
        self.errors = []
        
        threads = []
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=self.make_health_request, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Analyze results
        successful = len([r for r in self.results if r['success']])
        failed = len(self.errors)
        response_times = [r['response_time'] for r in self.results]
        
        log(f"Health Check Stress Test Results:")
        log(f"  Total Requests: {num_threads}")
        log(f"  Successful: {successful}")
        log(f"  Failed: {failed}")
        log(f"  Success Rate: {(successful/num_threads)*100:.1f}%")
        log(f"  Total Time: {total_time:.2f}s")
        
        if response_times:
            log(f"  Avg Response Time: {statistics.mean(response_times):.3f}s")
            log(f"  Min Response Time: {min(response_times):.3f}s")
            log(f"  Max Response Time: {max(response_times):.3f}s")
        
        return successful >= num_threads * 0.9  # 90% success rate
    
    def run_concurrent_extractions(self, num_threads=5):
        """Run concurrent video extractions"""
        log(f"Running {num_threads} concurrent video extractions...")
        
        self.results = []
        self.errors = []
        
        threads = []
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=self.make_extract_request, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Analyze results
        successful = len([r for r in self.results if r['success']])
        failed = len(self.errors)
        response_times = [r['response_time'] for r in self.results]
        
        log(f"Video Extraction Stress Test Results:")
        log(f"  Total Requests: {num_threads}")
        log(f"  Successful: {successful}")
        log(f"  Failed: {failed}")
        log(f"  Success Rate: {(successful/num_threads)*100:.1f}%")
        log(f"  Total Time: {total_time:.2f}s")
        
        if response_times:
            log(f"  Avg Response Time: {statistics.mean(response_times):.3f}s")
            log(f"  Min Response Time: {min(response_times):.3f}s")
            log(f"  Max Response Time: {max(response_times):.3f}s")
        
        return successful >= num_threads * 0.8  # 80% success rate for heavier operations
    
    def run_sustained_load(self, duration_seconds=30):
        """Run sustained load test"""
        log(f"Running sustained load test for {duration_seconds} seconds...")
        
        self.results = []
        self.errors = []
        
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < duration_seconds:
            try:
                response = requests.get(f"{BASE_URL}/health", timeout=2)
                request_count += 1
                
                with self.lock:
                    self.results.append({
                        'request_id': request_count,
                        'status_code': response.status_code,
                        'success': response.status_code == 200
                    })
                
                time.sleep(0.1)  # Small delay between requests
                
            except Exception as e:
                with self.lock:
                    self.errors.append({
                        'request_id': request_count,
                        'error': str(e)
                    })
        
        end_time = time.time()
        actual_duration = end_time - start_time
        
        successful = len([r for r in self.results if r['success']])
        failed = len(self.errors)
        total_requests = len(self.results) + len(self.errors)
        
        log(f"Sustained Load Test Results:")
        log(f"  Duration: {actual_duration:.2f}s")
        log(f"  Total Requests: {total_requests}")
        log(f"  Requests/Second: {total_requests/actual_duration:.2f}")
        log(f"  Successful: {successful}")
        log(f"  Failed: {failed}")
        log(f"  Success Rate: {(successful/total_requests)*100:.1f}%" if total_requests > 0 else "N/A")
        
        return successful >= total_requests * 0.95  # 95% success rate

def run_stress_tests():
    """Run all stress tests"""
    log("💪 Starting Stress Testing Suite", "INFO")
    log("=" * 60, "INFO")
    
    tester = StressTester()
    
    tests = [
        ("Concurrent Health Checks (20 threads)", lambda: tester.run_concurrent_health_checks(20)),
        ("Concurrent Video Extractions (5 threads)", lambda: tester.run_concurrent_extractions(5)),
        ("Sustained Load (30 seconds)", lambda: tester.run_sustained_load(30))
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        log(f"\n🔥 Running {test_name}...", "INFO")
        try:
            if test_func():
                log(f"{test_name}: PASSED", "PASS")
                passed += 1
            else:
                log(f"{test_name}: FAILED", "FAIL")
        except Exception as e:
            log(f"{test_name}: ERROR - {str(e)}", "FAIL")
    
    # Print summary
    log("\n" + "=" * 60, "INFO")
    log("💪 STRESS TESTS SUMMARY", "INFO")
    log("=" * 60, "INFO")
    log(f"Total Tests: {total}", "INFO")
    log(f"Passed: {passed}", "PASS")
    log(f"Failed: {total - passed}", "FAIL")
    
    success_rate = (passed / total * 100) if total > 0 else 0
    log(f"Success Rate: {success_rate:.1f}%", "INFO")
    
    if passed == total:
        log("🎉 ALL STRESS TESTS PASSED! Server handles load excellently!", "PASS")
    else:
        log(f"⚠️ {total - passed} stress tests failed. Server may need optimization.", "WARN")

if __name__ == "__main__":
    run_stress_tests()
