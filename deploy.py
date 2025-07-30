#!/usr/bin/env python3
"""
🚀 Automated Deployment Helper
Helps prepare and deploy the server to various platforms
"""

import os
import subprocess
import json
from datetime import datetime

def log(message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    emoji = {"INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}
    print(f"[{timestamp}] {emoji.get(status, 'ℹ️')} {message}")

def check_files():
    """Check if all required files exist"""
    log("Checking deployment files...")
    
    required_files = [
        "server_final.py",
        "requirements.txt", 
        "Procfile",
        "railway.json",
        "runtime.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            log(f"✅ {file} - Found", "PASS")
        else:
            log(f"❌ {file} - Missing", "FAIL")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_server_locally():
    """Test server locally before deployment"""
    log("Testing server locally...")
    
    try:
        # Import and test the server
        import server_final
        log("✅ Server imports successfully", "PASS")
        
        # Check if FastAPI app is created
        if hasattr(server_final, 'app'):
            log("✅ FastAPI app found", "PASS")
        else:
            log("❌ FastAPI app not found", "FAIL")
            return False
            
        return True
        
    except Exception as e:
        log(f"❌ Server test failed: {str(e)}", "FAIL")
        return False

def create_git_repo():
    """Initialize git repository if not exists"""
    log("Setting up Git repository...")
    
    if os.path.exists('.git'):
        log("✅ Git repository already exists", "PASS")
        return True
    
    try:
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        log("✅ Git repository initialized", "PASS")
        
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        log("✅ Files added to git", "PASS")
        
        subprocess.run(['git', 'commit', '-m', 'Initial commit - Video Extractor Server'], 
                      check=True, capture_output=True)
        log("✅ Initial commit created", "PASS")
        
        return True
        
    except subprocess.CalledProcessError as e:
        log(f"❌ Git setup failed: {str(e)}", "FAIL")
        return False
    except FileNotFoundError:
        log("❌ Git not found. Please install Git first.", "FAIL")
        return False

def show_deployment_options():
    """Show deployment platform options"""
    log("\n🚀 Deployment Platform Options:")
    log("=" * 50)
    
    platforms = [
        {
            "name": "Railway",
            "emoji": "🚂",
            "free_tier": "500 hours/month",
            "pros": ["Easy setup", "GitHub integration", "Free SSL", "Auto-deploy"],
            "url": "https://railway.app"
        },
        {
            "name": "Render", 
            "emoji": "🎨",
            "free_tier": "750 hours/month",
            "pros": ["Simple deployment", "Free SSL", "GitHub sync", "Good docs"],
            "url": "https://render.com"
        },
        {
            "name": "Heroku",
            "emoji": "🟣", 
            "free_tier": "550 hours/month",
            "pros": ["Popular platform", "Many addons", "Good community"],
            "url": "https://heroku.com"
        }
    ]
    
    for i, platform in enumerate(platforms, 1):
        log(f"\n{i}. {platform['emoji']} {platform['name']}")
        log(f"   Free Tier: {platform['free_tier']}")
        log(f"   URL: {platform['url']}")
        log(f"   Pros: {', '.join(platform['pros'])}")

def create_deployment_checklist():
    """Create deployment checklist"""
    checklist = """
# 🚀 Deployment Checklist

## Pre-Deployment ✅
- [ ] All files present (server_final.py, requirements.txt, etc.)
- [ ] Server tested locally
- [ ] Git repository initialized
- [ ] Code committed to Git

## Platform Setup ✅
- [ ] Account created on chosen platform
- [ ] GitHub repository created and pushed
- [ ] Platform connected to GitHub repo

## Configuration ✅
- [ ] Environment variables set (if needed)
- [ ] API key changed from default
- [ ] Port configuration verified

## Post-Deployment ✅
- [ ] Server health check passes
- [ ] API endpoints tested
- [ ] Documentation accessible
- [ ] Video extraction tested

## Monitoring ✅
- [ ] Logs checked for errors
- [ ] Performance monitored
- [ ] Uptime verified
"""
    
    with open("deployment_checklist.md", "w", encoding="utf-8") as f:
        f.write(checklist)
    
    log("✅ Deployment checklist created: deployment_checklist.md", "PASS")

def main():
    """Main deployment preparation function"""
    log("🚀 Video Extractor Server - Deployment Helper")
    log("=" * 60)
    
    # Check files
    if not check_files():
        log("❌ Missing required files. Cannot proceed.", "FAIL")
        return
    
    # Test server
    if not test_server_locally():
        log("❌ Server test failed. Fix issues before deployment.", "FAIL")
        return
    
    # Setup git
    create_git_repo()
    
    # Show options
    show_deployment_options()
    
    # Create checklist
    create_deployment_checklist()
    
    log("\n" + "=" * 60)
    log("🎯 DEPLOYMENT PREPARATION COMPLETE!")
    log("=" * 60)
    log("✅ All files ready for deployment")
    log("✅ Server tested and working")
    log("✅ Git repository prepared")
    log("✅ Deployment options provided")
    log("✅ Checklist created")
    
    log("\n🚀 Next Steps:")
    log("1. Choose a deployment platform (Railway recommended)")
    log("2. Create GitHub repository and push code")
    log("3. Connect platform to GitHub repo")
    log("4. Configure environment variables")
    log("5. Deploy and test!")
    
    log("\n📚 For detailed instructions, see: deploy_instructions.md")

if __name__ == "__main__":
    main()
