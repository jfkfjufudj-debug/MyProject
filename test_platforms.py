"""
🌐 Platform Support Testing
Tests video extraction from different platforms
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "default-api-key-change-me"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_platform(name, url, timeout=20):
    print(f"\n🎯 Testing {name}...")
    print(f"   URL: {url}")
    
    try:
        payload = {"url": url}
        response = requests.post(
            f"{BASE_URL}/api/v1/extract",
            json=payload,
            headers=HEADERS,
            timeout=timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                video_data = data.get("data", {})
                print(f"   ✅ SUCCESS")
                print(f"   📹 Title: {video_data.get('title', 'N/A')[:50]}...")
                print(f"   ⏱️ Duration: {video_data.get('duration')} seconds")
                print(f"   👤 Uploader: {video_data.get('uploader', 'N/A')}")
                print(f"   🎬 Formats: {len(video_data.get('formats', []))}")
                print(f"   🔗 Extractor: {video_data.get('extractor', 'N/A')}")
                return True
            else:
                print(f"   ❌ FAILED: {data.get('error')}")
                return False
        else:
            print(f"   ❌ HTTP ERROR: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ EXCEPTION: {str(e)}")
        return False

def main():
    print("🌐 Platform Support Testing")
    print("=" * 50)
    
    # Test different platforms
    platforms = [
        ("YouTube (Standard)", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
        ("YouTube (Short)", "https://youtu.be/dQw4w9WgXcQ"),
        ("YouTube (Music)", "https://music.youtube.com/watch?v=dQw4w9WgXcQ"),
        # Note: These might not work without actual valid URLs
        # ("TikTok", "https://www.tiktok.com/@username/video/1234567890"),
        # ("Instagram", "https://www.instagram.com/p/ABC123/"),
        # ("Twitter", "https://twitter.com/user/status/1234567890"),
    ]
    
    results = []
    
    for name, url in platforms:
        result = test_platform(name, url)
        results.append((name, result))
        time.sleep(2)  # Delay between requests
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 PLATFORM TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
    
    print(f"\n🎯 Results: {passed}/{total} platforms working ({(passed/total)*100:.1f}%)")

if __name__ == "__main__":
    main()
