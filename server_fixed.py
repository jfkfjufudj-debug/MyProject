"""
🎬 Video Extractor Server - FULLY FIXED VERSION
Complete and reliable video extraction API with all issues resolved
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, HttpUrl
import uvicorn
import yt_dlp
import asyncio
from typing import Optional, Dict, Any, Union
import time
from datetime import datetime

# Security
security = HTTPBearer(auto_error=False)
API_KEY = "default-api-key-change-me"

def verify_api_key(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if not credentials:
        raise HTTPException(
            status_code=401, 
            detail="Authentication required. Please provide a valid API key.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=401, 
            detail="Invalid API key. Please check your authentication token.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return credentials.credentials

# Helper functions for data formatting
def clean_description(description: str) -> str:
    """Clean and truncate description"""
    if not description:
        return ""
    # Remove excessive whitespace and limit length
    cleaned = " ".join(description.split())
    return cleaned[:500] + "..." if len(cleaned) > 500 else cleaned

def format_duration(duration: int) -> str:
    """Format duration in human-readable format"""
    if not duration:
        return "Unknown"
    
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"

def format_date(date_str: str) -> str:
    """Format upload date"""
    if not date_str or len(date_str) != 8:
        return "Unknown"
    
    try:
        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:8]
        return f"{year}-{month}-{day}"
    except:
        return date_str

# Models
class VideoRequest(BaseModel):
    url: HttpUrl
    format_preference: Optional[str] = "best"

class VideoResponse(BaseModel):
    success: bool
    data: Optional[Dict[Any, Any]] = None
    error: Optional[Union[str, Dict[str, Any]]] = None
    timestamp: str

# Create FastAPI application
app = FastAPI(
    title="🎬 Video Extractor API - Fixed",
    description="Professional video extraction service supporting 1000+ platforms - All Issues Fixed",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - MUST be first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Routes
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎬 Video Extractor Server - Fixed</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .header { text-align: center; color: #2c3e50; }
            .card { background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .endpoint { background: #e3f2fd; padding: 10px; border-radius: 5px; margin: 10px 0; }
            .method { color: #1976d2; font-weight: bold; }
            .fixed { background: #c8e6c9; padding: 10px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎬 Video Extractor Server - FIXED</h1>
            <p>Professional video extraction API - All Issues Resolved</p>
        </div>
        
        <div class="fixed">
            <h2>✅ FIXES APPLIED</h2>
            <ul>
                <li>🌐 CORS Headers Fixed</li>
                <li>🔐 Authentication Returns 401 (Not 403)</li>
                <li>🎬 Video Extraction Working</li>
                <li>📊 Enhanced Data Accuracy</li>
                <li>🛡️ Better Error Handling</li>
            </ul>
        </div>
        
        <div class="card">
            <h2>📚 API Documentation</h2>
            <p><a href="/docs" target="_blank">Interactive API Docs (Swagger)</a></p>
            <p><a href="/redoc" target="_blank">Alternative API Docs (ReDoc)</a></p>
        </div>
        
        <div class="card">
            <h2>🔗 Available Endpoints</h2>
            <div class="endpoint">
                <span class="method">GET</span> <code>/health</code> - Server health check
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <code>/api/v1/extract</code> - Extract video information
            </div>
            <div class="endpoint">
                <span class="method">OPTIONS</span> <code>/api/v1/extract</code> - CORS preflight
            </div>
        </div>
        
        <div class="card">
            <h2>🔑 Authentication</h2>
            <p>Use Bearer token: <code>default-api-key-change-me</code></p>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.1.0",
        "service": "video-extractor-fixed",
        "features": {
            "platforms_supported": "1000+",
            "authentication": "API Key (Fixed)",
            "formats": "Multiple video/audio formats",
            "metadata": "Complete video information",
            "cors": "Fully supported",
            "errors": "Enhanced handling"
        }
    }

@app.options("/api/v1/extract")
async def extract_options():
    """Handle CORS preflight requests"""
    return JSONResponse(
        content={"message": "CORS preflight successful"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )

@app.post("/api/v1/extract", response_model=VideoResponse)
async def extract_video(
    request: VideoRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Extract video information from supported platforms - FIXED VERSION
    
    Supports: YouTube, TikTok, Instagram, Facebook, Twitter, and 1000+ more platforms
    """
    try:
        url = str(request.url)
        
        # Enhanced yt-dlp options for maximum accuracy
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'format': request.format_preference,
            'writeinfojson': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'ignoreerrors': False,
            'no_check_certificate': False,
            'prefer_insecure': False,
        }
        
        # Extract video info
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Enhanced data cleaning and formatting
            clean_info = {
                "title": info.get("title", "Unknown Title"),
                "description": clean_description(info.get("description", "")),
                "duration": info.get("duration"),
                "duration_string": format_duration(info.get("duration")),
                "uploader": info.get("uploader", "Unknown"),
                "uploader_id": info.get("uploader_id"),
                "uploader_url": info.get("uploader_url"),
                "upload_date": info.get("upload_date"),
                "upload_date_formatted": format_date(info.get("upload_date")),
                "view_count": info.get("view_count", 0),
                "like_count": info.get("like_count", 0),
                "dislike_count": info.get("dislike_count", 0),
                "comment_count": info.get("comment_count", 0),
                "average_rating": info.get("average_rating"),
                "age_limit": info.get("age_limit", 0),
                "categories": info.get("categories", []),
                "tags": info.get("tags", [])[:10],  # Limit to 10 tags
                "thumbnail": info.get("thumbnail"),
                "thumbnails": info.get("thumbnails", [])[:5],  # Top 5 thumbnails
                "webpage_url": info.get("webpage_url"),
                "original_url": info.get("original_url"),
                "extractor": info.get("extractor"),
                "extractor_key": info.get("extractor_key"),
                "playlist": info.get("playlist"),
                "playlist_index": info.get("playlist_index"),
                "formats": [],
                "audio_formats": [],
                "video_formats": [],
                "best_format": None,
                "metadata": {
                    "extraction_time": datetime.now().isoformat(),
                    "yt_dlp_version": "latest",
                    "platform": info.get("extractor", "unknown"),
                    "server_version": "1.1.0-fixed"
                }
            }
            
            # Enhanced format processing
            if info.get("formats"):
                all_formats = []
                audio_formats = []
                video_formats = []
                best_video = None
                best_audio = None
                
                for fmt in info["formats"]:
                    format_info = {
                        "format_id": fmt.get("format_id"),
                        "ext": fmt.get("ext"),
                        "quality": fmt.get("format_note", "Unknown"),
                        "resolution": fmt.get("resolution"),
                        "width": fmt.get("width"),
                        "height": fmt.get("height"),
                        "fps": fmt.get("fps"),
                        "vcodec": fmt.get("vcodec"),
                        "acodec": fmt.get("acodec"),
                        "abr": fmt.get("abr"),  # Audio bitrate
                        "vbr": fmt.get("vbr"),  # Video bitrate
                        "filesize": fmt.get("filesize"),
                        "filesize_approx": fmt.get("filesize_approx"),
                        "url": fmt.get("url"),
                        "protocol": fmt.get("protocol"),
                        "format": fmt.get("format"),
                        "format_note": fmt.get("format_note")
                    }
                    
                    # Categorize formats
                    if fmt.get("vcodec") != "none" and fmt.get("acodec") != "none":
                        # Combined video+audio
                        all_formats.append(format_info)
                        current_height = fmt.get("height", 0) or 0
                        best_height = (best_video.get("height", 0) or 0) if best_video else 0
                        if not best_video or current_height > best_height:
                            best_video = format_info
                    elif fmt.get("vcodec") != "none":
                        # Video only
                        video_formats.append(format_info)
                    elif fmt.get("acodec") != "none":
                        # Audio only
                        audio_formats.append(format_info)
                        current_abr = fmt.get("abr", 0) or 0
                        best_abr = (best_audio.get("abr", 0) or 0) if best_audio else 0
                        if not best_audio or current_abr > best_abr:
                            best_audio = format_info
                
                # Sort formats by quality (handle None values)
                all_formats.sort(key=lambda x: x.get("height", 0) or 0, reverse=True)
                video_formats.sort(key=lambda x: x.get("height", 0) or 0, reverse=True)
                audio_formats.sort(key=lambda x: x.get("abr", 0) or 0, reverse=True)
                
                # Limit formats to prevent huge responses
                clean_info["formats"] = all_formats[:15]
                clean_info["video_formats"] = video_formats[:10]
                clean_info["audio_formats"] = audio_formats[:5]
                clean_info["best_format"] = best_video or best_audio
            
            return VideoResponse(
                success=True,
                data=clean_info,
                timestamp=datetime.now().isoformat()
            )
            
    except Exception as e:
        error_msg = str(e)
        error_type = "extraction_error"
        
        # Enhanced error categorization
        if "Unsupported URL" in error_msg or "No video formats found" in error_msg:
            error_msg = "This platform is not supported or the URL format is invalid"
            error_type = "unsupported_platform"
        elif "Video unavailable" in error_msg or "Private video" in error_msg:
            error_msg = "Video is unavailable, private, or has been removed"
            error_type = "video_unavailable"
        elif "Sign in to confirm your age" in error_msg:
            error_msg = "Video is age-restricted and cannot be accessed"
            error_type = "age_restricted"
        elif "This video is not available" in error_msg:
            error_msg = "Video is not available in your region"
            error_type = "geo_restricted"
        elif "timeout" in error_msg.lower():
            error_msg = "Request timed out. Please try again later"
            error_type = "timeout"
        elif "connection" in error_msg.lower():
            error_msg = "Network connection error. Please check your internet connection"
            error_type = "network_error"
        else:
            error_msg = f"Extraction failed: {error_msg}"
            error_type = "unknown_error"
        
        return VideoResponse(
            success=False,
            error={
                "message": error_msg,
                "type": error_type,
                "original_error": str(e)[:200]  # Truncated original error
            },
            timestamp=datetime.now().isoformat()
        )

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat()
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*", 
            "Access-Control-Allow-Headers": "*"
        }
    )

if __name__ == "__main__":
    print("🎬 Video Extractor Server - FULLY FIXED VERSION")
    print("=" * 60)
    print("✅ All issues resolved:")
    print("   🌐 CORS Headers Fixed")
    print("   🔐 Authentication Fixed (401 not 403)")
    print("   🎬 Video Extraction Fixed")
    print("   📊 Enhanced Data Accuracy")
    print("   🛡️ Better Error Handling")
    print("=" * 60)
    print("🚀 Starting server...")
    print("📍 Server: http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    print("🔑 API Key: default-api-key-change-me")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
