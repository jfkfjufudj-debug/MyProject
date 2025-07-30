print("🎬 Video Extractor Server - Simple Test")
print("=" * 50)

try:
    print("📦 Testing imports...")
    import sys
    print(f"✅ Python version: {sys.version}")
    
    # Test basic imports
    from pathlib import Path
    print("✅ pathlib imported")
    
    from config.settings import settings
    print(f"✅ Settings loaded - Port: {settings.SERVER_PORT}")
    
    print("\n🎉 Basic test completed successfully!")
    print("📋 Next steps:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Start server: python main.py")
    print("  3. Visit: http://127.0.0.1:8000")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Make sure you're in the correct directory")
