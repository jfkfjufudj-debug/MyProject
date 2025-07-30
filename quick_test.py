"""
Quick Test - Video Extractor Server
Test basic functionality without external dependencies
"""

import sys
from pathlib import Path

def test_basic_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing basic imports...")
    
    try:
        # Test if we can import our modules
        sys.path.insert(0, str(Path(__file__).parent))
        
        print("  📦 Testing config...")
        from config.settings import settings
        print(f"    ✅ Settings loaded - Server: {settings.SERVER_HOST}:{settings.SERVER_PORT}")
        
        print("  📦 Testing core modules...")
        from core.extractor import VideoExtractor
        from core.downloader import DownloadManager
        print("    ✅ Core modules imported")
        
        print("  📦 Testing API modules...")
        from api.auth import SecurityManager
        print("    ✅ API modules imported")
        
        print("  📦 Testing utils...")
        from utils.helpers import URLValidator, DataFormatter
        print("    ✅ Utils modules imported")
        
        return True
        
    except ImportError as e:
        print(f"    ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"    ❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        from utils.helpers import URLValidator, DataFormatter
        
        # Test URL validation
        validator = URLValidator()
        test_urls = [
            "https://www.youtube.com/watch?v=test",
            "https://www.tiktok.com/@user/video/123",
            "invalid-url"
        ]
        
        print("  🔗 Testing URL validation...")
        for url in test_urls:
            is_valid = validator.is_valid_url(url)
            status = "✅" if is_valid else "❌"
            print(f"    {status} {url}")
        
        # Test data formatting
        formatter = DataFormatter()
        
        print("  📊 Testing data formatting...")
        print(f"    ✅ Duration: {formatter.format_duration(3661)}")
        print(f"    ✅ File size: {formatter.format_file_size(1048576)}")
        print(f"    ✅ View count: {formatter.format_view_count(1500000)}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return False

def test_configuration():
    """Test configuration"""
    print("\n🧪 Testing configuration...")
    
    try:
        from config.settings import settings
        
        print(f"  ✅ App Name: {settings.APP_NAME}")
        print(f"  ✅ Version: {settings.APP_VERSION}")
        print(f"  ✅ Debug Mode: {settings.DEBUG_MODE}")
        print(f"  ✅ API Key Set: {'Yes' if settings.API_KEY != 'default-api-key-change-me' else 'Default (change recommended)'}")
        print(f"  ✅ Max File Size: {settings.MAX_FILE_SIZE_MB} MB")
        print(f"  ✅ Supported Platforms: {len(settings.SUPPORTED_PLATFORMS)}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return False

def main():
    """Run quick tests"""
    print("🎬 Video Extractor Server - Quick Test")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Configuration", test_configuration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(f"🏁 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All basic tests passed!")
        print("📋 Next steps:")
        print("  1. Install Python 3.8+ if not installed")
        print("  2. Run: pip install -r requirements.txt")
        print("  3. Run: python main.py")
        print("  4. Visit: http://127.0.0.1:8000/docs")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
