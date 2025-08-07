"""
Simple API Test for Video Extractor Server
"""
import json
import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "https://myproject-3b4w.onrender.com"
API_KEY = "default-api-key-change-me"

def test_api_endpoint(endpoint, method="GET", data=None):
    """Test a specific API endpoint"""
    try:
        headers = {"X-API-Key": API_KEY}
        
        if data:
            data = json.dumps(data).encode('utf-8')
            headers['Content-Type'] = 'application/json'
        
        req = urllib.request.Request(f"{BASE_URL}{endpoint}", data=data, headers=headers, method=method)
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return True, result
            
    except urllib.error.HTTPError as e:
        try:
            error_data = json.loads(e.read().decode('utf-8'))
        except:
            error_data = str(e)
        return False, error_data
    except Exception as e:
        return False, str(e)

def main():
    print("🧪 Simple API Testing")
    print("=" * 40)
    
    # Test 1: Root endpoint
    print("1. Testing root endpoint...")
    success, result = test_api_endpoint("/")
    if success:
        print("✅ Root endpoint works!")
        print(f"   Version: {result['data']['version']}")
        print(f"   Status: {result['data']['status']}")
    else:
        print(f"❌ Root endpoint failed: {result}")
    
    print()
    
    # Test 2: Health check
    print("2. Testing health endpoint...")
    success, result = test_api_endpoint("/health")
    if success:
        print("✅ Health endpoint works!")
        print(f"   Status: {result['data']['status']}")
        print(f"   Environment: {result['data']['environment']}")
    else:
        print(f"❌ Health endpoint failed: {result}")
    
    print()
    
    # Test 3: Authentication test
    print("3. Testing authentication...")
    success, result = test_api_endpoint("/api/v1/extract", "POST", {
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    })
    
    if success:
        print("✅ Authentication works!")
        if result.get('success'):
            print("✅ Video extraction successful!")
            data = result['data']
            print(f"   Title: {data.get('title', 'N/A')[:50]}...")
            print(f"   Duration: {data.get('duration', 'N/A')} seconds")
            print(f"   Uploader: {data.get('uploader', 'N/A')}")
        else:
            print(f"⚠️ Video extraction failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"❌ Authentication failed: {result}")
    
    print()
    
    # Test 4: Try a different video source
    print("4. Testing with different video...")
    test_urls = [
        "https://www.youtube.com/watch?v=BaW_jenozKc",  # YouTube short
        "https://www.dailymotion.com/video/x2hwqn9",    # Dailymotion
        "https://www.youtube.com/watch?v=9bZkp7q19f0"   # Another YouTube
    ]
    
    for i, url in enumerate(test_urls, 1):
        print(f"   4.{i} Testing: {url}")
        success, result = test_api_endpoint("/api/v1/extract", "POST", {
            "url": url,
            "quality": "best"
        })
        
        if success and result.get('success'):
            data = result['data']
            print(f"   ✅ Success! Title: {data.get('title', 'N/A')[:40]}...")
            break
        else:
            error = result.get('error', 'Unknown error') if success else result
            print(f"   ❌ Failed: {str(error)[:60]}...")
    
    print()
    print("🎯 Testing complete!")

if __name__ == "__main__":
    main()
