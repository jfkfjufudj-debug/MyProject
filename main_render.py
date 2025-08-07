"""
===================================================================
Video Extractor Server - Simplified for Render Deployment
===================================================================
Author: Professional Development Team
Version: 1.0.0
Description: Simplified FastAPI application for Render deployment
"""

import os
import asyncio
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Simple settings
class SimpleSettings:
    def __init__(self):
        self.APP_NAME = "Video Extractor Server"
        self.APP_VERSION = "1.0.0"
        self.API_KEY = os.getenv("API_KEY", "default-api-key-change-me")
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
        self.MAX_REQUESTS_PER_MINUTE = 60

settings = SimpleSettings()

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    🎬 **Video Extractor Server**
    
    A high-performance API for extracting video information and downloading content.
    
    ## Features
    
    * 🔍 **Extract** video information
    * 📥 **Download** videos in multiple qualities
    * 🔐 **Secure** API key authentication
    * 🚀 **Fast** performance
    
    ## Authentication
    
    Include API key in Authorization header: `Bearer YOUR_API_KEY`
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple authentication
def verify_api_key(request: Request):
    """Simple API key verification"""
    auth_header = request.headers.get("Authorization")
    api_key_param = request.query_params.get("api_key")
    api_key_header = request.headers.get("X-API-Key")

    provided_key = None
    if auth_header and auth_header.startswith("Bearer "):
        provided_key = auth_header[7:]
    elif api_key_param:
        provided_key = api_key_param
    elif api_key_header:
        provided_key = api_key_header

    if not provided_key or provided_key != settings.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

    return True

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "operational",
        "documentation": "/docs",
        "api_base": "/api/v1"
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "message": "Server is running properly"
    }

# Video extraction endpoint
@app.post("/api/v1/extract", tags=["Video"])
async def extract_video(request: Request, data: dict):
    """Extract video information"""
    # Verify API key
    verify_api_key(request)

    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    try:
        # Simple yt-dlp extraction
        import yt_dlp

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'no_check_certificate': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Extract basic information
            result = {
                "success": True,
                "data": {
                    "title": info.get("title", "Unknown"),
                    "duration": info.get("duration", 0),
                    "uploader": info.get("uploader", "Unknown"),
                    "view_count": info.get("view_count", 0),
                    "upload_date": info.get("upload_date", "Unknown"),
                    "description": (info.get("description", "") or "")[:500],  # Limit description
                    "thumbnail": info.get("thumbnail", ""),
                    "formats": []
                }
            }

            # Extract available formats
            if info.get("formats"):
                for fmt in info["formats"][:10]:  # Limit to 10 formats
                    if fmt.get("url"):
                        result["data"]["formats"].append({
                            "format_id": fmt.get("format_id", ""),
                            "ext": fmt.get("ext", ""),
                            "quality": fmt.get("format_note", ""),
                            "filesize": fmt.get("filesize", 0)
                        })

            return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract video information: {str(e)}"
        )

# Download endpoint
@app.post("/api/v1/download", tags=["Video"])
async def download_video(request: Request, data: dict):
    """Download video"""
    # Verify API key
    verify_api_key(request)
    
    url = data.get("url")
    quality = data.get("quality", "best")
    
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    try:
        import yt_dlp
        
        # Simple download options
        ydl_opts = {
            'format': quality,
            'quiet': True,
            'no_warnings': True,
            'outtmpl': '/tmp/%(title)s.%(ext)s'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                "success": True,
                "message": "Download initiated",
                "data": {
                    "title": info.get("title", "Unknown"),
                    "status": "processing"
                }
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to download video: {str(e)}"
        )

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "path": str(request.url.path)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": str(exc)
        }
    )

# Main execution
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main_render:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
