"""
Quick deployment script
"""
import subprocess
import sys

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🚀 Quick Deploy to GitHub...")
    
    # Add all files
    print("📁 Adding files...")
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Failed to add files: {stderr}")
        return
    
    # Commit
    print("💾 Committing...")
    success, stdout, stderr = run_command('git commit -m "Update yt-dlp options for better compatibility"')
    if not success:
        print(f"⚠️ Commit result: {stderr}")
    
    # Push
    print("🌐 Pushing to GitHub...")
    success, stdout, stderr = run_command("git push origin main")
    if success:
        print("✅ Successfully pushed to GitHub!")
        print("🔄 Render will auto-deploy in a few minutes...")
    else:
        print(f"❌ Failed to push: {stderr}")

if __name__ == "__main__":
    main()
