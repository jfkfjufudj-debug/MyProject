#!/usr/bin/env python3
"""
🎬 Video Downloader Tool
Downloads videos in different formats using the server API
"""

import requests
import yt_dlp
import os
import json
from datetime import datetime

# Server configuration
BASE_URL = "http://127.0.0.1:8000"
API_KEY = "default-api-key-change-me"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Video URL to download
VIDEO_URL = "https://youtu.be/RJTMOQimUyE?si=0xSo22Siy6JOyirw"

def log(message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    emoji = {"INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "DOWNLOAD": "⬇️"}
    print(f"[{timestamp}] {emoji.get(status, 'ℹ️')} {message}")

def get_video_info():
    """Get video information from server"""
    log("Getting video information from server...")
    
    try:
        payload = {"url": VIDEO_URL, "format_preference": "best"}
        response = requests.post(f"{BASE_URL}/api/v1/extract",
                               headers=HEADERS,
                               json=payload,
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                video_info = data.get("data", {})
                log(f"✅ Video Info Retrieved:", "PASS")
                log(f"   Title: {video_info.get('title', 'Unknown')}")
                log(f"   Duration: {video_info.get('duration_string', 'Unknown')}")
                log(f"   Uploader: {video_info.get('uploader', 'Unknown')}")
                log(f"   Available Formats: {len(video_info.get('formats', []))}")
                return video_info
            else:
                log(f"❌ Server returned error: {data.get('error', 'Unknown error')}", "FAIL")
                return None
        else:
            log(f"❌ Server request failed: {response.status_code}", "FAIL")
            return None
            
    except Exception as e:
        log(f"❌ Error getting video info: {str(e)}", "FAIL")
        return None

def download_video_with_audio():
    """Download video with audio (best quality)"""
    log("🎬 Downloading Video + Audio (Best Quality)...", "DOWNLOAD")
    
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': 'downloads/%(title)s_video_audio.%(ext)s',
            'writeinfojson': True,
        }
        
        os.makedirs('downloads', exist_ok=True)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([VIDEO_URL])
        
        log("✅ Video + Audio downloaded successfully!", "PASS")
        return True
        
    except Exception as e:
        log(f"❌ Error downloading video+audio: {str(e)}", "FAIL")
        return False

def download_video_only():
    """Download video without audio"""
    log("🎥 Downloading Video Only (No Audio)...", "DOWNLOAD")
    
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]/bestvideo',
            'outtmpl': 'downloads/%(title)s_video_only.%(ext)s',
        }
        
        os.makedirs('downloads', exist_ok=True)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([VIDEO_URL])
        
        log("✅ Video Only downloaded successfully!", "PASS")
        return True
        
    except Exception as e:
        log(f"❌ Error downloading video only: {str(e)}", "FAIL")
        return False

def download_audio_only():
    """Download audio only"""
    log("🎵 Downloading Audio Only...", "DOWNLOAD")
    
    try:
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': 'downloads/%(title)s_audio_only.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        os.makedirs('downloads', exist_ok=True)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([VIDEO_URL])
        
        log("✅ Audio Only downloaded successfully!", "PASS")
        return True
        
    except Exception as e:
        log(f"❌ Error downloading audio only: {str(e)}", "FAIL")
        return False

def list_downloaded_files():
    """List all downloaded files"""
    log("📁 Listing downloaded files...")
    
    downloads_dir = "downloads"
    if os.path.exists(downloads_dir):
        files = os.listdir(downloads_dir)
        if files:
            log(f"📂 Found {len(files)} downloaded files:")
            for i, file in enumerate(files, 1):
                file_path = os.path.join(downloads_dir, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                log(f"   {i}. {file} ({file_size:.2f} MB)")
        else:
            log("📂 No files found in downloads directory")
    else:
        log("📂 Downloads directory doesn't exist")

def test_server_connection():
    """Test server connection first"""
    log("🔗 Testing server connection...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            log("✅ Server is running and accessible!", "PASS")
            return True
        else:
            log(f"❌ Server returned status: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Cannot connect to server: {str(e)}", "FAIL")
        return False

def main():
    """Main download function"""
    log("🎬 Starting Video Download Process", "INFO")
    log("=" * 60, "INFO")
    log(f"🔗 Video URL: {VIDEO_URL}")
    log("=" * 60, "INFO")
    
    # Test server connection
    if not test_server_connection():
        log("❌ Cannot proceed without server connection", "FAIL")
        return
    
    # Get video information
    video_info = get_video_info()
    if not video_info:
        log("❌ Cannot proceed without video information", "FAIL")
        return
    
    log("\n🎯 Starting Downloads...", "INFO")
    log("-" * 40, "INFO")
    
    # Download in different formats
    results = []
    
    # 1. Video + Audio
    results.append(("Video + Audio", download_video_with_audio()))
    
    # 2. Video Only
    results.append(("Video Only", download_video_only()))
    
    # 3. Audio Only
    results.append(("Audio Only", download_audio_only()))
    
    # Summary
    log("\n" + "=" * 60, "INFO")
    log("📊 DOWNLOAD SUMMARY", "INFO")
    log("=" * 60, "INFO")
    
    successful = 0
    for format_name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        log(f"{format_name}: {status}")
        if success:
            successful += 1
    
    log(f"\n🎯 Total: {successful}/{len(results)} downloads successful")
    
    if successful == len(results):
        log("🎉 ALL DOWNLOADS COMPLETED SUCCESSFULLY!", "PASS")
    else:
        log(f"⚠️ {len(results) - successful} downloads failed", "WARN")
    
    # List downloaded files
    log("\n" + "-" * 40, "INFO")
    list_downloaded_files()
    
    log("\n🎬 Download process completed!", "INFO")

if __name__ == "__main__":
    main()
