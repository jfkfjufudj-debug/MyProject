"""
Enhanced Deployment Script
Deploys the enhanced video extractor with all new features
"""
import subprocess
import sys
import time

def run_command(command, description):
    """Run a command and return the result"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {str(e)}")
        return False

def main():
    print("🚀 ENHANCED VIDEO EXTRACTOR DEPLOYMENT")
    print("=" * 50)
    print("Deploying with advanced anti-detection features:")
    print("✅ Advanced user agent rotation")
    print("✅ Platform-specific extractors")
    print("✅ Multiple fallback strategies")
    print("✅ Browser simulation")
    print("✅ Proxy support framework")
    print("✅ Enhanced error handling")
    print("=" * 50)
    print()
    
    # Check if git is available
    if not run_command("git --version", "Checking Git availability"):
        print("⚠️ Git not available. Manual deployment required.")
        print("\n📋 MANUAL DEPLOYMENT STEPS:")
        print("1. Copy main_complete.py to your repository")
        print("2. Commit and push changes to GitHub")
        print("3. Render will auto-deploy the changes")
        return
    
    # Git operations
    steps = [
        ("git add .", "Adding all files"),
        ('git commit -m "🚀 Enhanced Video Extractor with Advanced Anti-Detection\n\n✅ Added advanced user agent rotation\n✅ Implemented platform-specific extractors\n✅ Added multiple fallback strategies\n✅ Enhanced browser simulation\n✅ Added proxy support framework\n✅ Improved error handling\n✅ Better platform compatibility"', "Committing changes"),
        ("git push origin main", "Pushing to GitHub")
    ]
    
    success_count = 0
    for command, description in steps:
        if run_command(command, description):
            success_count += 1
        time.sleep(1)
    
    print("\n" + "=" * 50)
    if success_count == len(steps):
        print("🎉 DEPLOYMENT SUCCESSFUL!")
        print("✅ All changes pushed to GitHub")
        print("🔄 Render will auto-deploy in 2-3 minutes")
        print("\n📋 WHAT'S NEW:")
        print("🤖 Advanced bot detection bypass")
        print("🌐 Platform-specific optimizations")
        print("🔄 Multiple extraction fallback strategies")
        print("🎭 Browser simulation for better compatibility")
        print("🌍 Proxy support for geo-restrictions")
        print("⚡ Enhanced performance and reliability")
        
        print("\n🧪 TESTING RECOMMENDATIONS:")
        print("1. Wait 3-5 minutes for deployment")
        print("2. Run: python advanced_test.py")
        print("3. Test with various video platforms")
        print("4. Monitor server logs for improvements")
        
    else:
        print("⚠️ PARTIAL DEPLOYMENT")
        print(f"✅ {success_count}/{len(steps)} steps completed")
        print("🔧 Manual intervention may be required")
    
    print("\n🔗 Server URL: https://myproject-3b4w.onrender.com")
    print("📚 Documentation: https://myproject-3b4w.onrender.com/docs")

if __name__ == "__main__":
    main()
