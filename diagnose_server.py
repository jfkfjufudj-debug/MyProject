"""
Server Diagnostic Tool
"""

import requests
import json
import traceback

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "default-api-key-change-me"

def test_basic_endpoints():
    print("🔍 BASIC ENDPOINTS TEST")
    print("=" * 40)
    
    endpoints = [
        ("/", "Home Page"),
        ("/health", "Health Check"),
        ("/docs", "API Documentation")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            print(f"✅ {name}: {response.status_code}")
            if endpoint == "/health" and response.status_code == 200:
                data = response.json()
                print(f"   Status: {data.get('status')}")
        except Exception as e:
            print(f"❌ {name}: {e}")

def test_extraction_detailed():
    print("\n🎬 DETAILED EXTRACTION TEST")
    print("=" * 40)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
    
    try:
        print("📤 Sending request...")
        print(f"   URL: {BASE_URL}/api/v1/extract")
        print(f"   Headers: {headers}")
        print(f"   Payload: {payload}")
        
        response = requests.post(
            f"{BASE_URL}/api/v1/extract",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"\n📥 Response received:")
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   Success: {data.get('success')}")
                
                if data.get('success'):
                    video_data = data.get('data', {})
                    print(f"   Title: {video_data.get('title', 'N/A')[:50]}...")
                    print(f"   Duration: {video_data.get('duration')} seconds")
                    print(f"   Formats: {len(video_data.get('formats', []))}")
                else:
                    error = data.get('error')
                    print(f"   Error: {error}")
            except json.JSONDecodeError as e:
                print(f"   ❌ JSON decode error: {e}")
                print(f"   Raw response: {response.text[:200]}...")
        else:
            print(f"   ❌ HTTP Error")
            print(f"   Response: {response.text[:500]}...")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is server running?")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"   Traceback: {traceback.format_exc()}")

def test_authentication_detailed():
    print("\n🔐 DETAILED AUTHENTICATION TEST")
    print("=" * 40)
    
    test_cases = [
        ("No Authorization", {}),
        ("Wrong API Key", {"Authorization": "Bearer wrong-key", "Content-Type": "application/json"}),
        ("Correct API Key", {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"})
    ]
    
    payload = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
    
    for test_name, headers in test_cases:
        print(f"\n🎯 Testing: {test_name}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/extract",
                json=payload,
                headers=headers,
                timeout=10
            )
            print(f"   Status: {response.status_code}")
            
            if response.status_code in [401, 403]:
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'No detail')}")
                except:
                    print(f"   Raw error: {response.text[:100]}...")
            elif response.status_code == 200:
                print("   ✅ Authentication successful")
            else:
                print(f"   Unexpected status: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_cors_detailed():
    print("\n🌐 DETAILED CORS TEST")
    print("=" * 40)
    
    try:
        # Test OPTIONS request
        response = requests.options(f"{BASE_URL}/api/v1/extract", timeout=10)
        print(f"OPTIONS request: {response.status_code}")
        
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods', 
            'Access-Control-Allow-Headers',
            'Access-Control-Expose-Headers'
        ]
        
        print("CORS Headers:")
        for header in cors_headers:
            value = response.headers.get(header)
            status = "✅" if value else "❌"
            print(f"   {status} {header}: {value}")
            
    except Exception as e:
        print(f"❌ CORS test error: {e}")

def main():
    print("🧪 COMPREHENSIVE SERVER DIAGNOSTIC")
    print("=" * 50)
    print(f"Testing server at: {BASE_URL}")
    print("=" * 50)
    
    test_basic_endpoints()
    test_extraction_detailed()
    test_authentication_detailed()
    test_cors_detailed()
    
    print("\n" + "=" * 50)
    print("✅ DIAGNOSTIC COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()
