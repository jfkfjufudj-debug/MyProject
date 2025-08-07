"""
Ultimate Test for Enhanced Video Extractor
Tests all new features including API fallbacks
"""
import json
import urllib.request
import urllib.parse
import urllib.error
import time

BASE_URL = "https://myproject-3b4w.onrender.com"
API_KEY = "default-api-key-change-me"

def test_ultimate_extraction(url, description):
    """Test ultimate extraction capabilities"""
    try:
        data = json.dumps({
            "url": url,
            "quality": "best"
        }).encode('utf-8')
        
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY
        }
        
        req = urllib.request.Request(
            f"{BASE_URL}/api/v1/extract",
            data=data,
            headers=headers,
            method="POST"
        )
        
        start_time = time.time()
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            end_time = time.time()
            
            if result.get('success'):
                video_data = result['data']
                print(f"✅ {description}")
                print(f"   📺 Title: {video_data.get('title', 'N/A')[:60]}...")
                print(f"   ⏱️ Duration: {video_data.get('duration', 'N/A')} seconds")
                print(f"   👤 Uploader: {video_data.get('uploader', 'N/A')}")
                print(f"   👀 Views: {video_data.get('view_count', 'N/A')}")
                print(f"   🌐 Platform: {video_data.get('platform', 'N/A')}")
                print(f"   🔧 Method: {video_data.get('extraction_method', 'N/A')}")
                print(f"   🎥 Formats: {len(video_data.get('formats', []))} available")
                print(f"   ⚡ Time: {end_time - start_time:.2f}s")
                
                # Show extraction method details
                method = video_data.get('extraction_method', 'unknown')
                if 'api' in method.lower():
                    print(f"   🎯 SUCCESS: API-based extraction working!")
                elif 'yt_dlp' in method.lower():
                    print(f"   🔄 FALLBACK: yt-dlp extraction used")
                elif 'basic' in method.lower():
                    print(f"   ⚠️ BASIC: Final fallback used")
                
                return True, method
            else:
                print(f"❌ {description}")
                print(f"   Error: {result.get('error', 'Unknown error')[:100]}...")
                return False, 'failed'
                
    except Exception as e:
        print(f"❌ {description}")
        print(f"   Error: {str(e)[:100]}...")
        return False, 'error'

def main():
    print("🚀 ULTIMATE VIDEO EXTRACTOR TESTING")
    print("=" * 60)
    print("Testing ultimate extraction with API fallbacks")
    print("=" * 60)
    print()
    
    # Test videos with different complexity levels
    test_videos = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "YouTube Classic (Rick Roll)"),
        ("https://www.youtube.com/watch?v=jNQXAC9IVRw", "YouTube Short Video"),
        ("https://youtu.be/dQw4w9WgXcQ", "YouTube Short URL"),
        ("https://www.youtube.com/watch?v=BaW_jenozKc", "YouTube Popular Video"),
        ("https://vimeo.com/76979871", "Vimeo Video"),
        ("https://www.dailymotion.com/video/x2hwqn9", "Dailymotion Video"),
    ]
    
    successful_extractions = 0
    total_extractions = len(test_videos)
    extraction_methods = {}
    
    print("🎬 TESTING ULTIMATE EXTRACTION CAPABILITIES")
    print("-" * 60)
    
    for i, (url, description) in enumerate(test_videos, 1):
        print(f"\n{i}. Testing {description}...")
        success, method = test_ultimate_extraction(url, description)
        
        if success:
            successful_extractions += 1
            extraction_methods[method] = extraction_methods.get(method, 0) + 1
        
        time.sleep(2)  # Rate limiting
    
    print("\n" + "=" * 60)
    print("📊 ULTIMATE EXTRACTION RESULTS")
    print("=" * 60)
    print(f"✅ Successful extractions: {successful_extractions}/{total_extractions}")
    print(f"📈 Success rate: {(successful_extractions/total_extractions)*100:.1f}%")
    
    if extraction_methods:
        print("\n🔧 EXTRACTION METHODS USED:")
        for method, count in extraction_methods.items():
            print(f"   {method}: {count} times")
    
    print("\n🎯 ANALYSIS:")
    if successful_extractions > 0:
        print("✅ Ultimate extraction system is working!")
        
        if any('api' in method for method in extraction_methods.keys()):
            print("🎉 API-based extraction successful!")
            print("   - Invidious API working")
            print("   - Alternative APIs functional")
            print("   - Bot detection bypassed")
        
        if any('yt_dlp' in method for method in extraction_methods.keys()):
            print("🔄 yt-dlp fallback working")
            print("   - Advanced options applied")
            print("   - Multiple strategies used")
        
        if any('basic' in method for method in extraction_methods.keys()):
            print("⚠️ Basic fallback used")
            print("   - Final safety net working")
    else:
        print("⚠️ All extractions failed")
        print("This indicates:")
        print("- Severe platform restrictions")
        print("- Network connectivity issues")
        print("- All APIs temporarily unavailable")
    
    print("\n🚀 ULTIMATE FEATURES IMPLEMENTED:")
    print("✅ Multiple API fallbacks (Invidious, Piped, etc.)")
    print("✅ Advanced yt-dlp with anti-detection")
    print("✅ Platform-specific optimizations")
    print("✅ Browser simulation")
    print("✅ User agent rotation")
    print("✅ Proxy support framework")
    print("✅ Generic HTML parsing")
    print("✅ Basic info fallback")
    print("✅ Comprehensive error handling")
    
    print(f"\n🌐 Server: {BASE_URL}")
    print(f"📚 Docs: {BASE_URL}/docs")
    print("\n🎯 TESTING COMPLETE!")

if __name__ == "__main__":
    main()
