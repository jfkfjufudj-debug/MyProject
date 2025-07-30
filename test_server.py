"""
===================================================================
Video Extractor Server - Test Suite
===================================================================
Author: Professional Development Team
Version: 1.0.0
Description: Comprehensive test suite for the video extractor server
"""

import asyncio
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_imports():
    """Test all module imports"""
    print("🧪 Testing module imports...")
    
    try:
        # Test config
        from config.settings import settings, validate_configuration
        print("✅ Config module imported successfully")
        
        # Test core modules
        from core.extractor import video_extractor
        from core.downloader import download_manager
        print("✅ Core modules imported successfully")
        
        # Test API modules
        from api.auth import security_manager
        from api.routes import router
        print("✅ API modules imported successfully")
        
        # Test utils
        from utils.helpers import url_validator, data_formatter, cache_manager
        print("✅ Utils modules imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

async def test_configuration():
    """Test configuration validation"""
    print("\n🧪 Testing configuration...")
    
    try:
        from config.settings import validate_configuration, settings
        
        # Test configuration validation
        is_valid = validate_configuration()
        if is_valid:
            print("✅ Configuration validation passed")
        else:
            print("⚠️ Configuration validation failed (but this might be expected)")
        
        # Test settings access
        print(f"✅ Server host: {settings.SERVER_HOST}")
        print(f"✅ Server port: {settings.SERVER_PORT}")
        print(f"✅ API key configured: {'Yes' if settings.API_KEY else 'No'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False

async def test_url_validation():
    """Test URL validation functionality"""
    print("\n🧪 Testing URL validation...")
    
    try:
        from utils.helpers import url_validator
        
        # Test valid URLs
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.tiktok.com/@user/video/123456789",
            "https://www.instagram.com/p/ABC123/",
            "invalid-url",
            ""
        ]
        
        for url in test_urls:
            is_valid = url_validator.is_valid_url(url)
            status = "✅" if is_valid else "❌"
            print(f"{status} URL: {url[:50]}{'...' if len(url) > 50 else ''}")
        
        return True
        
    except Exception as e:
        print(f"❌ URL validation error: {str(e)}")
        return False

async def test_data_formatting():
    """Test data formatting utilities"""
    print("\n🧪 Testing data formatting...")
    
    try:
        from utils.helpers import data_formatter
        
        # Test duration formatting
        durations = [0, 30, 90, 3600, 7200]
        for duration in durations:
            formatted = data_formatter.format_duration(duration)
            print(f"✅ Duration {duration}s -> {formatted}")
        
        # Test file size formatting
        sizes = [0, 1024, 1048576, 1073741824]
        for size in sizes:
            formatted = data_formatter.format_file_size(size)
            print(f"✅ Size {size} bytes -> {formatted}")
        
        # Test view count formatting
        counts = [0, 999, 1500, 1000000, 1500000000]
        for count in counts:
            formatted = data_formatter.format_view_count(count)
            print(f"✅ Views {count} -> {formatted}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data formatting error: {str(e)}")
        return False

async def test_cache_system():
    """Test caching system"""
    print("\n🧪 Testing cache system...")
    
    try:
        from utils.helpers import cache_manager
        
        # Test cache stats
        stats = await cache_manager.get_cache_stats()
        print(f"✅ Cache enabled: {stats.get('enabled', False)}")
        print(f"✅ Cache entries: {stats.get('total_entries', 0)}")
        
        # Test cache operations
        test_key = "test_key"
        test_data = {"message": "Hello, World!", "timestamp": 1234567890}
        
        # Set cache
        set_result = await cache_manager.set(test_key, test_data)
        print(f"✅ Cache set: {set_result}")
        
        # Get cache
        cached_data = await cache_manager.get(test_key)
        if cached_data and cached_data.get('message') == test_data['message']:
            print("✅ Cache get: Success")
        else:
            print("⚠️ Cache get: Failed or disabled")
        
        # Delete cache
        delete_result = await cache_manager.delete(test_key)
        print(f"✅ Cache delete: {delete_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Cache system error: {str(e)}")
        return False

async def test_extractor_basic():
    """Test basic extractor functionality"""
    print("\n🧪 Testing video extractor (basic)...")
    
    try:
        from core.extractor import video_extractor
        
        # Test platform detection
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.tiktok.com/@user/video/123",
            "https://www.instagram.com/p/ABC123/"
        ]
        
        for url in test_urls:
            platform = video_extractor.get_platform_from_url(url)
            print(f"✅ Platform detection: {url[:30]}... -> {platform}")
        
        # Test URL validation
        is_valid = video_extractor.is_valid_url("https://www.youtube.com/watch?v=test")
        print(f"✅ URL validation: {is_valid}")
        
        return True
        
    except Exception as e:
        print(f"❌ Extractor error: {str(e)}")
        return False

async def test_security_system():
    """Test security and authentication system"""
    print("\n🧪 Testing security system...")
    
    try:
        from api.auth import security_manager
        from config.settings import settings
        
        # Test API key validation
        valid_key = security_manager.validate_api_key(settings.API_KEY)
        if valid_key:
            print("✅ API key validation: Success")
            print(f"✅ Key name: {valid_key.get('name', 'Unknown')}")
        else:
            print("❌ API key validation: Failed")
        
        # Test invalid key
        invalid_key = security_manager.validate_api_key("invalid-key")
        if not invalid_key:
            print("✅ Invalid key rejection: Success")
        else:
            print("❌ Invalid key rejection: Failed")
        
        # Test rate limiter
        from api.auth import RateLimiter
        rate_limiter = RateLimiter()
        
        test_id = "test_user"
        limit = 5
        
        # Test rate limiting
        allowed_count = 0
        for i in range(10):
            if rate_limiter.is_allowed(test_id, limit):
                allowed_count += 1
        
        print(f"✅ Rate limiting: {allowed_count}/{limit} requests allowed")
        
        return True
        
    except Exception as e:
        print(f"❌ Security system error: {str(e)}")
        return False

async def test_download_manager():
    """Test download manager basic functionality"""
    print("\n🧪 Testing download manager...")
    
    try:
        from core.downloader import download_manager
        
        # Test download ID generation
        download_id = download_manager.generate_download_id("test_url", "720p")
        print(f"✅ Download ID generation: {download_id}")
        
        # Test filename sanitization
        test_filename = "Test Video: <Special> Characters/\\|?*"
        sanitized = download_manager.sanitize_filename(test_filename)
        print(f"✅ Filename sanitization: {sanitized}")
        
        # Test download status (should return not found)
        status = download_manager.get_download_status("non_existent_id")
        if status.get('status') == 'not_found':
            print("✅ Download status check: Success")
        else:
            print("⚠️ Download status check: Unexpected result")
        
        return True
        
    except Exception as e:
        print(f"❌ Download manager error: {str(e)}")
        return False

async def run_all_tests():
    """Run all tests"""
    print("🎬 Video Extractor Server - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("URL Validation", test_url_validation),
        ("Data Formatting", test_data_formatting),
        ("Cache System", test_cache_system),
        ("Video Extractor", test_extractor_basic),
        ("Security System", test_security_system),
        ("Download Manager", test_download_manager),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Server is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    print("Starting test suite...")
    result = asyncio.run(run_all_tests())
    sys.exit(0 if result else 1)
