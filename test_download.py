#!/usr/bin/env python3
"""
Simple download test
"""

import requests
import json

# Test server first
print("Testing server...")
try:
    response = requests.get("http://127.0.0.1:8000/health", timeout=10)
    print(f"Server status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Server is working!")
    else:
        print("❌ Server issue")
        exit(1)
except Exception as e:
    print(f"❌ Server connection error: {e}")
    exit(1)

# Test video extraction
print("\nTesting video extraction...")
try:
    headers = {
        "Authorization": "Bearer default-api-key-change-me",
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": "https://youtu.be/RJTMOQimUyE?si=0xSo22Siy6JOyirw",
        "format_preference": "best"
    }
    
    response = requests.post("http://127.0.0.1:8000/api/v1/extract",
                           headers=headers,
                           json=payload,
                           timeout=30)
    
    print(f"Extraction status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            video_data = data.get("data", {})
            print("✅ Video extraction successful!")
            print(f"Title: {video_data.get('title', 'Unknown')}")
            print(f"Duration: {video_data.get('duration', 'Unknown')} seconds")
            print(f"Uploader: {video_data.get('uploader', 'Unknown')}")
            print(f"Formats available: {len(video_data.get('formats', []))}")
            
            # Show some format details
            formats = video_data.get('formats', [])[:5]  # First 5 formats
            print("\nAvailable formats (first 5):")
            for i, fmt in enumerate(formats, 1):
                print(f"  {i}. {fmt.get('format_id', 'N/A')} - {fmt.get('ext', 'N/A')} - {fmt.get('quality', 'N/A')}")
        else:
            print(f"❌ Extraction failed: {data.get('error', 'Unknown error')}")
    else:
        print(f"❌ Request failed with status {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Extraction error: {e}")

print("\n🎬 Server and extraction test completed!")
