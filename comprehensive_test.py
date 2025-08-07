"""
Comprehensive API Testing for Video Extractor Server
"""
import json
import urllib.request
import urllib.parse
import urllib.error
import time

# Server configuration
BASE_URL = "https://myproject-3b4w.onrender.com"
API_KEY = "default-api-key-change-me"  # Default API key from settings

def make_request(url, method="GET", data=None, headers=None):
    """Make HTTP request with error handling"""
    try:
        if headers is None:
            headers = {}
        
        if data:
            data = json.dumps(data).encode('utf-8')
            headers['Content-Type'] = 'application/json'
        
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            return {
                'success': True,
                'status_code': response.getcode(),
                'data': json.loads(response.read().decode('utf-8'))
            }
    except urllib.error.HTTPError as e:
        try:
            error_data = json.loads(e.read().decode('utf-8'))
        except:
            error_data = str(e)
        return {
            'success': False,
            'status_code': e.code,
            'error': error_data
        }
    except Exception as e:
        return {
            'success': False,
            'status_code': 0,
            'error': str(e)
        }

def test_authentication():
    """Test authentication system"""
    print("🔐 Testing Authentication System...")
    print("=" * 50)
    
    # Test without API key
    print("1. Testing without API key...")
    result = make_request(
        f"{BASE_URL}/api/v1/extract",
        method="POST",
        data={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
    )
    
    if not result['success'] and result['status_code'] == 401:
        print("✅ Correctly rejected unauthorized request")
    else:
        print("❌ Authentication failed - should reject without API key")
    
    # Test with wrong API key
    print("2. Testing with wrong API key...")
    result = make_request(
        f"{BASE_URL}/api/v1/extract",
        method="POST",
        data={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
        headers={"X-API-Key": "wrong-key"}
    )
    
    if not result['success'] and result['status_code'] == 401:
        print("✅ Correctly rejected wrong API key")
    else:
        print("❌ Authentication failed - should reject wrong API key")
    
    print()

def test_video_extraction():
    """Test video information extraction"""
    print("🎬 Testing Video Information Extraction...")
    print("=" * 50)
    
    test_videos = [
        {
            "name": "Vimeo Video",
            "url": "https://vimeo.com/148751763",
            "quality": "best"
        },
        {
            "name": "Archive.org Video",
            "url": "https://archive.org/details/BigBuckBunny_124",
            "quality": "best"
        }
    ]
    
    for i, video in enumerate(test_videos, 1):
        print(f"{i}. Testing {video['name']}...")
        
        result = make_request(
            f"{BASE_URL}/api/v1/extract",
            method="POST",
            data={
                "url": video["url"],
                "quality": video["quality"]
            },
            headers={"X-API-Key": API_KEY}
        )
        
        if result['success']:
            data = result['data']['data']
            print(f"✅ Extraction successful!")
            print(f"   📺 Title: {data.get('title', 'N/A')[:60]}...")
            print(f"   ⏱️ Duration: {data.get('duration', 'N/A')} seconds")
            print(f"   👤 Uploader: {data.get('uploader', 'N/A')}")
            print(f"   👀 Views: {data.get('view_count', 'N/A'):,}")
            print(f"   📅 Upload Date: {data.get('upload_date', 'N/A')}")
            print(f"   🎥 Available Formats: {len(data.get('formats', []))}")
            
            # Show some format details
            formats = data.get('formats', [])[:3]  # First 3 formats
            for fmt in formats:
                print(f"      - {fmt.get('format_id', 'N/A')}: {fmt.get('ext', 'N/A')} "
                      f"({fmt.get('quality', 'N/A')}) - {fmt.get('filesize', 0)} bytes")
        else:
            print(f"❌ Extraction failed: {result.get('error', 'Unknown error')}")
        
        print()
        time.sleep(2)  # Rate limiting

def test_video_download():
    """Test video download functionality"""
    print("📥 Testing Video Download Functionality...")
    print("=" * 50)
    
    # Test regular video download
    print("1. Testing regular video download...")
    result = make_request(
        f"{BASE_URL}/api/v1/download",
        method="POST",
        data={
            "url": "https://vimeo.com/148751763",  # Vimeo video
            "quality": "worst",  # Use worst quality for faster download
            "audio_only": False
        },
        headers={"X-API-Key": API_KEY}
    )
    
    if result['success']:
        data = result['data']['data']
        print("✅ Download initiated successfully!")
        print(f"   📺 Title: {data.get('title', 'N/A')}")
        print(f"   📁 Filename: {data.get('filename', 'N/A')}")
        print(f"   📊 File Size: {data.get('file_size', 0):,} bytes")
        print(f"   🎥 Format: {data.get('format', 'N/A')}")
        print(f"   ✅ Status: {data.get('status', 'N/A')}")
    else:
        print(f"❌ Download failed: {result.get('error', 'Unknown error')}")
    
    print()
    time.sleep(3)
    
    # Test audio-only download
    print("2. Testing audio-only download...")
    result = make_request(
        f"{BASE_URL}/api/v1/download",
        method="POST",
        data={
            "url": "https://vimeo.com/148751763",
            "quality": "best",
            "audio_only": True
        },
        headers={"X-API-Key": API_KEY}
    )
    
    if result['success']:
        data = result['data']['data']
        print("✅ Audio download initiated successfully!")
        print(f"   🎵 Title: {data.get('title', 'N/A')}")
        print(f"   📁 Filename: {data.get('filename', 'N/A')}")
        print(f"   📊 File Size: {data.get('file_size', 0):,} bytes")
        print(f"   🎵 Format: {data.get('format', 'N/A')}")
    else:
        print(f"❌ Audio download failed: {result.get('error', 'Unknown error')}")
    
    print()

def test_error_handling():
    """Test error handling"""
    print("⚠️ Testing Error Handling...")
    print("=" * 50)
    
    # Test invalid URL
    print("1. Testing invalid URL...")
    result = make_request(
        f"{BASE_URL}/api/v1/extract",
        method="POST",
        data={"url": "https://invalid-url-that-does-not-exist.com/video"},
        headers={"X-API-Key": API_KEY}
    )
    
    if not result['success']:
        print("✅ Correctly handled invalid URL")
        print(f"   Error: {result.get('error', 'Unknown error')}")
    else:
        print("❌ Should have failed with invalid URL")
    
    print()

def run_comprehensive_test():
    """Run all tests"""
    print("🧪 COMPREHENSIVE API TESTING")
    print("=" * 60)
    print(f"🌐 Server: {BASE_URL}")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print("=" * 60)
    print()
    
    # Run all tests
    test_authentication()
    test_video_extraction()
    test_video_download()
    test_error_handling()
    
    print("🎯 TESTING COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    run_comprehensive_test()
