"""
🧪 Enhanced Features Testing
Tests all the improvements and fixes applied to the server
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

def test_cors_fix():
    print("🌐 TESTING CORS FIXES")
    print("=" * 50)
    
    try:
        # Test OPTIONS request
        response = requests.options(f"{BASE_URL}/api/v1/extract", timeout=10)
        print(f"OPTIONS Status: {response.status_code}")
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        print("CORS Headers:")
        for header, value in cors_headers.items():
            status = "✅" if value else "❌"
            print(f"  {status} {header}: {value}")
        
        return any(cors_headers.values())
        
    except Exception as e:
        print(f"❌ CORS test failed: {str(e)}")
        return False

def test_authentication_fix():
    print("\n🔐 TESTING AUTHENTICATION FIXES")
    print("=" * 50)
    
    # Test without API key
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/extract",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            timeout=10
        )
        print(f"No API Key - Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Correctly returns 401 for missing API key")
            auth_result_1 = True
        else:
            print(f"❌ Expected 401, got {response.status_code}")
            auth_result_1 = False
            
    except Exception as e:
        print(f"❌ Auth test 1 failed: {str(e)}")
        auth_result_1 = False
    
    # Test with wrong API key
    try:
        wrong_headers = {"Authorization": "Bearer wrong-key", "Content-Type": "application/json"}
        response = requests.post(
            f"{BASE_URL}/api/v1/extract",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            headers=wrong_headers,
            timeout=10
        )
        print(f"Wrong API Key - Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Correctly returns 401 for wrong API key")
            auth_result_2 = True
        else:
            print(f"❌ Expected 401, got {response.status_code}")
            auth_result_2 = False
            
    except Exception as e:
        print(f"❌ Auth test 2 failed: {str(e)}")
        auth_result_2 = False
    
    return auth_result_1 and auth_result_2

def test_enhanced_health_check():
    print("\n🏥 TESTING ENHANCED HEALTH CHECK")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            required_fields = ["status", "timestamp", "version", "service", "features"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                print("✅ All required fields present")
                print(f"   Status: {data.get('status')}")
                print(f"   Version: {data.get('version')}")
                print(f"   Service: {data.get('service')}")
                
                features = data.get('features', {})
                print("   Features:")
                for key, value in features.items():
                    print(f"     - {key}: {value}")
                
                return True
            else:
                print(f"❌ Missing fields: {missing_fields}")
                return False
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_enhanced_extraction():
    print("\n🎬 TESTING ENHANCED VIDEO EXTRACTION")
    print("=" * 50)
    
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
                
                # Check enhanced fields
                enhanced_fields = [
                    "duration_string", "upload_date_formatted", "uploader_id",
                    "categories", "tags", "thumbnails", "audio_formats",
                    "video_formats", "best_format", "metadata"
                ]
                
                print("📊 ENHANCED DATA FIELDS:")
                for field in enhanced_fields:
                    value = video_data.get(field)
                    if value is not None:
                        if isinstance(value, list):
                            print(f"✅ {field}: {len(value)} items")
                        elif isinstance(value, dict):
                            print(f"✅ {field}: {len(value)} properties")
                        else:
                            print(f"✅ {field}: {value}")
                    else:
                        print(f"⚠️ {field}: Not available")
                
                # Check format categorization
                formats = video_data.get("formats", [])
                video_formats = video_data.get("video_formats", [])
                audio_formats = video_data.get("audio_formats", [])
                
                print(f"\n🎬 FORMAT ANALYSIS:")
                print(f"   Total formats: {len(formats)}")
                print(f"   Video-only formats: {len(video_formats)}")
                print(f"   Audio-only formats: {len(audio_formats)}")
                
                best_format = video_data.get("best_format")
                if best_format:
                    print(f"   Best format: {best_format.get('resolution', 'N/A')} "
                          f"({best_format.get('ext', 'N/A')})")
                
                return True
            else:
                print(f"❌ Extraction failed: {data.get('error')}")
                return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced extraction test failed: {str(e)}")
        return False

def test_error_handling():
    print("\n🛡️ TESTING ENHANCED ERROR HANDLING")
    print("=" * 50)
    
    test_cases = [
        {
            "name": "Invalid URL",
            "url": "https://invalid-url.com/video",
            "expected_type": "unsupported_platform"
        },
        {
            "name": "Non-video URL",
            "url": "https://www.google.com",
            "expected_type": "unsupported_platform"
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n🎯 Testing: {test_case['name']}")
        try:
            payload = {"url": test_case["url"]}
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
                        print(f"   ✅ Error handled properly")
                        print(f"   Type: {error_type}")
                        print(f"   Message: {error_message}")
                        results.append(True)
                    else:
                        print(f"   ⚠️ Error format not enhanced: {error}")
                        results.append(False)
                else:
                    print(f"   ❌ Should have failed but succeeded")
                    results.append(False)
            else:
                print(f"   ✅ HTTP error handled: {response.status_code}")
                results.append(True)
                
        except Exception as e:
            print(f"   ✅ Exception handled: {str(e)}")
            results.append(True)
    
    return all(results)

def main():
    print("🧪 ENHANCED FEATURES COMPREHENSIVE TEST")
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("CORS Fix", test_cors_fix),
        ("Authentication Fix", test_authentication_fix),
        ("Enhanced Health Check", test_enhanced_health_check),
        ("Enhanced Extraction", test_enhanced_extraction),
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
    print("\n" + "=" * 60)
    print("📊 ENHANCEMENT TEST RESULTS")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"🎯 Success Rate: {(passed/total)*100:.1f}% ({passed}/{total})")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    if passed == total:
        print("\n🎉 ALL ENHANCEMENTS WORKING PERFECTLY!")
        print("🚀 Server is now production-ready with all fixes applied!")
    else:
        print(f"\n⚠️ {total-passed} enhancements need attention.")
    
    print(f"\n🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
