#!/usr/bin/env python3
"""
Actual video download in 3 formats
"""

import yt_dlp
import os
from datetime import datetime

VIDEO_URL = "https://youtu.be/RJTMOQimUyE?si=0xSo22Siy6JOyirw"

def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def create_downloads_folder():
    """Create downloads folder"""
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        log("📁 Created downloads folder")

def download_video_with_audio():
    """Download video with audio"""
    log("🎬 Starting download: Video + Audio...")
    
    try:
        ydl_opts = {
            'format': 'best[height<=720]/best',  # Best quality up to 720p
            'outtmpl': 'downloads/%(title)s_VIDEO_AUDIO.%(ext)s',
            'writeinfojson': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([VIDEO_URL])
        
        log("✅ Video + Audio download completed!")
        return True
        
    except Exception as e:
        log(f"❌ Video + Audio download failed: {str(e)}")
        return False

def download_video_only():
    """Download video without audio"""
    log("🎥 Starting download: Video Only (No Audio)...")
    
    try:
        ydl_opts = {
            'format': 'bestvideo[height<=720]/bestvideo',
            'outtmpl': 'downloads/%(title)s_VIDEO_ONLY.%(ext)s',
            'writeinfojson': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([VIDEO_URL])
        
        log("✅ Video Only download completed!")
        return True
        
    except Exception as e:
        log(f"❌ Video Only download failed: {str(e)}")
        return False

def download_audio_only():
    """Download audio only"""
    log("🎵 Starting download: Audio Only...")
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s_AUDIO_ONLY.%(ext)s',
            'writeinfojson': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([VIDEO_URL])
        
        log("✅ Audio Only download completed!")
        return True
        
    except Exception as e:
        log(f"❌ Audio Only download failed: {str(e)}")
        return False

def list_downloaded_files():
    """List downloaded files with sizes"""
    log("📂 Listing downloaded files...")
    
    if os.path.exists('downloads'):
        files = [f for f in os.listdir('downloads') if os.path.isfile(os.path.join('downloads', f))]
        if files:
            log(f"📁 Found {len(files)} downloaded files:")
            for i, file in enumerate(files, 1):
                file_path = os.path.join('downloads', file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                log(f"   {i}. {file}")
                log(f"      Size: {file_size:.2f} MB")
        else:
            log("📁 No files found in downloads folder")
    else:
        log("📁 Downloads folder doesn't exist")

def main():
    """Main download function"""
    log("🎬 Starting Video Download Process")
    log("=" * 80)
    log(f"🔗 Video URL: {VIDEO_URL}")
    log("=" * 80)
    
    # Create downloads folder
    create_downloads_folder()
    
    # Download in 3 different formats
    results = []
    
    log("\n🎯 Starting downloads...")
    log("-" * 50)
    
    # 1. Video + Audio
    results.append(("Video + Audio", download_video_with_audio()))
    
    # 2. Video Only  
    results.append(("Video Only", download_video_only()))
    
    # 3. Audio Only
    results.append(("Audio Only", download_audio_only()))
    
    # Summary
    log("\n" + "=" * 80)
    log("📊 DOWNLOAD SUMMARY")
    log("=" * 80)
    
    successful = 0
    for format_name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        log(f"{format_name:15}: {status}")
        if success:
            successful += 1
    
    log(f"\n🎯 Result: {successful}/{len(results)} downloads successful")
    
    if successful == len(results):
        log("🎉 ALL DOWNLOADS COMPLETED SUCCESSFULLY!")
    elif successful > 0:
        log(f"⚠️ {len(results) - successful} downloads failed, but {successful} succeeded")
    else:
        log("❌ ALL DOWNLOADS FAILED")
    
    # List files
    log("\n" + "-" * 50)
    list_downloaded_files()
    
    log("\n🎬 Download process finished!")
    log("=" * 80)

if __name__ == "__main__":
    main()
