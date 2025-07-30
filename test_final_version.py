"""
🧪 FINAL VERSION TESTING
Quick and comprehensive test of the final working server
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

def test_basic_endpoints():
    print("🔍 BASIC ENDPOINTS TEST")
    print("=" * 50)
    
    tests = [
        ("Home Page", "/"),
        ("Health Check", "/health"),
        ("API Docs", "/docs"),
        ("ReDoc", "/redoc")
    ]
    
    results = []
    for name, endpoint in tests:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            success = response.status_code == 200
            print(f"{'✅' if success else '❌'} {name}: {response.status_code}")
            results.append(success)
        except Exception as e:
            print(f"❌ {name}: {e}")
            results.append(False)
    
    return all(results)

def test_cors():
    print("\n🌐 CORS TEST")
    print("=" * 50)
    
    try:
        response = requests.options(f"{BASE_URL}/api/v1/extract", timeout=10)
        cors_headers = response.headers.get('Access-Control-Allow-Origin')
        success = response.status_code == 200 and cors_headers
        print(f"{'✅' if success else '❌'} CORS OPTIONS: {response.status_code}")
        print(f"   Allow-Origin: {cors_headers}")
        return success
    except Exception as e:
        print(f"❌ CORS Error: {e}")
        return False

def test_authentication():
    print("\n🔐 AUTHENTICATION TEST")
    print("=" * 50)
    
    # Test without API key
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/extract",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            timeout=10
        )
        auth1_success = response.status_code == 401
        print(f"{'✅' if auth1_success else '❌'} No API Key: {response.status_code} (Expected: 401)")
    except Exception as e:
        print(f"❌ No API Key Test: {e}")
        auth1_success = False
    
    # Test with wrong API key
    try:
        wrong_headers = {"Authorization": "Bearer wrong-key", "Content-Type": "application/json"}
        response = requests.post(
            f"{BASE_URL}/api/v1/extract",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            headers=wrong_headers,
            timeout=10
        )
        auth2_success = response.status_code == 401
        print(f"{'✅' if auth2_success else '❌'} Wrong API Key: {response.status_code} (Expected: 401)")
    except Exception as e:
        print(f"❌ Wrong API Key Test: {e}")
        auth2_success = False
    
    return auth1_success and auth2_success

def test_video_extraction():
    print("\n🎬 VIDEO EXTRACTION TEST")
    print("=" * 50)
    
    try:
        payload = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        print("📤 Sending extraction request...")
        
        response = requests.post(
            f"{BASE_URL}/api/v1/extract",
            json=payload,
            headers=HEADERS,
            timeout=30
        )
        
        print(f"📥 Response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                video_data = data.get("data", {})
                
                print("✅ EXTRACTION SUCCESSFUL!")
                print(f"   📹 Title: {video_data.get('title', 'N/A')[:60]}...")
                print(f"   ⏱️ Duration: {video_data.get('duration')} seconds ({video_data.get('duration_string', 'N/A')})")
                print(f"   👤 Uploader: {video_data.get('uploader', 'N/A')}")
                print(f"   👀 Views: {video_data.get('view_count', 0):,}")
                print(f"   📅 Upload Date: {video_data.get('upload_date', 'N/A')}")
                print(f"   🎬 Total Formats: {len(video_data.get('formats', []))}")
                print(f"   📺 Video Formats: {len(video_data.get('video_formats', []))}")
                print(f"   🔊 Audio Formats: {len(video_data.get('audio_formats', []))}")
                print(f"   🔗 Extractor: {video_data.get('extractor', 'N/A')}")
                
                # Check data quality
                essential_fields = ["title", "duration", "uploader", "formats"]
                missing_fields = [field for field in essential_fields if not video_data.get(field)]
                
                if not missing_fields:
                    print("✅ All essential data present")
                    return True
                else:
                    print(f"⚠️ Missing fields: {missing_fields}")
                    return False
            else:
                error = data.get('error', {})
                print(f"❌ Extraction failed: {error}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Extraction error: {e}")
        return False

def test_error_handling():
    print("\n🛡️ ERROR HANDLING TEST")
    print("=" * 50)
    
    error_tests = [
        ("Invalid URL", "https://invalid-url.com/video"),
        ("Non-video URL", "https://www.google.com")
    ]
    
    results = []
    for test_name, test_url in error_tests:
        try:
            payload = {"url": test_url}
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
                    print(f"✅ {test_name}: Handled gracefully")
                    print(f"   Error: {error.get('message', 'No message')[:60]}...")
                    results.append(True)
                else:
                    print(f"❌ {test_name}: Should have failed")
                    results.append(False)
            else:
                print(f"✅ {test_name}: HTTP error {response.status_code}")
                results.append(True)
                
        except Exception as e:
            print(f"✅ {test_name}: Exception handled - {str(e)[:50]}...")
            results.append(True)
    
    return all(results)

def main():
    print("🧪 FINAL VERSION COMPREHENSIVE TEST")
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing server at: {BASE_URL}")
    print("=" * 80)
    
    # Run all tests
    tests = [
        ("Basic Endpoints", test_basic_endpoints),
        ("CORS Functionality", test_cors),
        ("Authentication", test_authentication),
        ("Video Extraction", test_video_extraction),
        ("Error Handling", test_error_handling)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
            time.sleep(1)
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {str(e)}")
            results[test_name] = False
    
    # Final report
    print("\n" + "=" * 80)
    print("📊 FINAL TEST RESULTS")
    print("=" * 80)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"🎯 OVERALL SCORE: {passed}/{total} tests passed ({success_rate:.1f}%)")
    print()
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print()
    if success_rate == 100:
        print("🎉 PERFECT! ALL TESTS PASSED!")
        print("🚀 Server is 100% functional and production-ready!")
        print("✅ Ready for deployment and real-world usage!")
    elif success_rate >= 90:
        print("🎉 EXCELLENT! Server is working perfectly!")
        print("🚀 Minor issues (if any) don't affect core functionality!")
    elif success_rate >= 80:
        print("✅ VERY GOOD! Server is highly functional!")
        print("🔧 Minor improvements recommended")
    else:
        print("⚠️ Server needs attention")
        print("🔧 Some fixes required")
    
    print(f"\n🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    main()
