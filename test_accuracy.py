"""
🔍 Detailed Accuracy Testing
Tests the precision and accuracy of video extraction
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "default-api-key-change-me"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def detailed_extraction_test():
    print("🔍 DETAILED EXTRACTION ACCURACY TEST")
    print("=" * 60)
    
    # Test with a well-known video
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        payload = {"url": test_url}
        response = requests.post(
            f"{BASE_URL}/api/v1/extract",
            json=payload,
            headers=HEADERS,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                video_data = data.get("data", {})
                
                print("📊 EXTRACTED DATA ANALYSIS:")
                print("-" * 40)
                
                # Check all fields
                fields_to_check = [
                    ("title", "Title"),
                    ("description", "Description"),
                    ("duration", "Duration"),
                    ("uploader", "Uploader"),
                    ("upload_date", "Upload Date"),
                    ("view_count", "View Count"),
                    ("like_count", "Like Count"),
                    ("thumbnail", "Thumbnail"),
                    ("webpage_url", "Webpage URL"),
                    ("extractor", "Extractor"),
                    ("formats", "Formats")
                ]
                
                for field, display_name in fields_to_check:
                    value = video_data.get(field)
                    if value is not None:
                        if field == "formats":
                            print(f"✅ {display_name}: {len(value)} formats available")
                            # Check format details
                            if value:
                                print("   📋 Format Details:")
                                for i, fmt in enumerate(value[:3]):  # Show first 3
                                    print(f"      {i+1}. ID: {fmt.get('format_id')}, "
                                          f"Ext: {fmt.get('ext')}, "
                                          f"Quality: {fmt.get('quality')}")
                        elif field == "description":
                            desc_len = len(str(value))
                            print(f"✅ {display_name}: {desc_len} characters")
                            if desc_len > 0:
                                print(f"   Preview: {str(value)[:100]}...")
                        elif field == "duration":
                            minutes = value // 60 if value else 0
                            seconds = value % 60 if value else 0
                            print(f"✅ {display_name}: {value} seconds ({minutes}:{seconds:02d})")
                        elif field == "view_count":
                            if value:
                                print(f"✅ {display_name}: {value:,} views")
                            else:
                                print(f"⚠️ {display_name}: Not available")
                        else:
                            print(f"✅ {display_name}: {value}")
                    else:
                        print(f"❌ {display_name}: Missing")
                
                # Test format URLs
                print("\n🔗 FORMAT URL VALIDATION:")
                print("-" * 40)
                formats = video_data.get("formats", [])
                if formats:
                    for i, fmt in enumerate(formats[:2]):  # Test first 2 URLs
                        url = fmt.get("url")
                        if url:
                            try:
                                # Just check if URL is accessible (HEAD request)
                                head_response = requests.head(url, timeout=10)
                                if head_response.status_code in [200, 206, 302]:
                                    print(f"✅ Format {i+1} URL: Accessible")
                                else:
                                    print(f"⚠️ Format {i+1} URL: Status {head_response.status_code}")
                            except:
                                print(f"❌ Format {i+1} URL: Not accessible")
                        else:
                            print(f"❌ Format {i+1} URL: Missing")
                
                return True
            else:
                print(f"❌ Extraction failed: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_different_video_types():
    print("\n🎬 DIFFERENT VIDEO TYPES TEST")
    print("=" * 60)
    
    test_videos = [
        {
            "name": "Standard YouTube Video",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "expected_duration": 213
        },
        {
            "name": "YouTube Short URL",
            "url": "https://youtu.be/dQw4w9WgXcQ",
            "expected_duration": 213
        },
        {
            "name": "YouTube with Playlist",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLrAXtmRdnEQy8VJZsUJSjzOn6IAVjTjKw",
            "expected_duration": 213
        }
    ]
    
    results = []
    
    for test in test_videos:
        print(f"\n🎯 Testing: {test['name']}")
        try:
            payload = {"url": test["url"]}
            response = requests.post(
                f"{BASE_URL}/api/v1/extract",
                json=payload,
                headers=HEADERS,
                timeout=25
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    video_data = data.get("data", {})
                    duration = video_data.get("duration")
                    title = video_data.get("title", "")
                    
                    # Check accuracy
                    duration_match = abs(duration - test["expected_duration"]) <= 5 if duration else False
                    title_match = "rick astley" in title.lower() if title else False
                    
                    print(f"   ✅ Extraction: Success")
                    print(f"   📹 Title: {title}")
                    print(f"   ⏱️ Duration: {duration}s (Expected: {test['expected_duration']}s)")
                    print(f"   🎯 Duration Accuracy: {'✅ Match' if duration_match else '❌ Mismatch'}")
                    print(f"   🎯 Title Accuracy: {'✅ Match' if title_match else '❌ Mismatch'}")
                    
                    results.append(duration_match and title_match)
                else:
                    print(f"   ❌ Failed: {data.get('error')}")
                    results.append(False)
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
            results.append(False)
        
        time.sleep(2)
    
    return results

def test_edge_cases():
    print("\n🔍 EDGE CASES TEST")
    print("=" * 60)
    
    edge_cases = [
        {
            "name": "Very Long URL",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be&t=10s&list=PLrAXtmRdnEQy8VJZsUJSjzOn6IAVjTjKw&index=1"
        },
        {
            "name": "URL with Timestamp",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s"
        },
        {
            "name": "Mobile YouTube URL",
            "url": "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
        }
    ]
    
    results = []
    
    for test in edge_cases:
        print(f"\n🎯 Testing: {test['name']}")
        try:
            payload = {"url": test["url"]}
            response = requests.post(
                f"{BASE_URL}/api/v1/extract",
                json=payload,
                headers=HEADERS,
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    video_data = data.get("data", {})
                    print(f"   ✅ Success: {video_data.get('title', 'No title')[:50]}...")
                    results.append(True)
                else:
                    print(f"   ❌ Failed: {data.get('error')}")
                    results.append(False)
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
            results.append(False)
    
    return results

def main():
    print("🔍 COMPREHENSIVE ACCURACY TESTING")
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Run detailed tests
    print("1️⃣ Running detailed extraction test...")
    detailed_result = detailed_extraction_test()
    
    print("\n2️⃣ Running different video types test...")
    video_types_results = test_different_video_types()
    
    print("\n3️⃣ Running edge cases test...")
    edge_cases_results = test_edge_cases()
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 ACCURACY TEST SUMMARY")
    print("=" * 60)
    
    total_tests = 1 + len(video_types_results) + len(edge_cases_results)
    passed_tests = (
        (1 if detailed_result else 0) +
        sum(video_types_results) +
        sum(edge_cases_results)
    )
    
    accuracy_rate = (passed_tests / total_tests) * 100
    
    print(f"🎯 Overall Accuracy: {accuracy_rate:.1f}% ({passed_tests}/{total_tests})")
    print(f"📋 Detailed Extraction: {'✅ PASS' if detailed_result else '❌ FAIL'}")
    print(f"📋 Video Types: {sum(video_types_results)}/{len(video_types_results)} passed")
    print(f"📋 Edge Cases: {sum(edge_cases_results)}/{len(edge_cases_results)} passed")
    
    if accuracy_rate >= 90:
        print("\n🎉 EXCELLENT ACCURACY! Server is highly reliable.")
    elif accuracy_rate >= 75:
        print("\n✅ GOOD ACCURACY! Minor improvements needed.")
    else:
        print("\n⚠️ ACCURACY NEEDS IMPROVEMENT!")
    
    print(f"\n🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
