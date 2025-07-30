"""
===================================================================
Video Extractor Server - Simplified Version
===================================================================
No complex dependencies - just the essentials
"""

import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from pathlib import Path

# Simple configuration
class Settings:
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 8000
    API_KEY = "default-api-key-change-me"
    APP_NAME = "Video Extractor Server"
    APP_VERSION = "1.0.0"

settings = Settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Professional Video Extractor Server - Simplified Version",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class ExtractRequest(BaseModel):
    url: str
    include_playlist: bool = False

class DownloadRequest(BaseModel):
    url: str
    quality: str = "720p"
    format_type: str = "video"

# Simple API key check
def check_api_key(api_key: str):
    if api_key != f"Bearer {settings.API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API key")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "operational",
        "documentation": "/docs",
        "note": "Simplified version - install full dependencies for complete features"
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "message": "Server is running (simplified mode)"
    }

# Extract endpoint (simplified)
@app.post("/api/v1/extract")
async def extract_video(request: ExtractRequest):
    try:
        # Import yt-dlp here to check if it's available
        import yt_dlp
        
        # Basic yt-dlp options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(request.url, download=False)
                
                if not info:
                    raise HTTPException(status_code=400, detail="Could not extract video information")
                
                # Simplified response
                result = {
                    "success": True,
                    "data": {
                        "title": info.get('title', 'Unknown'),
                        "duration": info.get('duration', 0),
                        "uploader": info.get('uploader', 'Unknown'),
                        "view_count": info.get('view_count', 0),
                        "thumbnail": info.get('thumbnail', ''),
                        "webpage_url": info.get('webpage_url', ''),
                        "platform": info.get('extractor', 'unknown'),
                        "formats_count": len(info.get('formats', [])),
                        "note": "Simplified extraction - install full version for complete format details"
                    }
                }
                
                return JSONResponse(content=result)
                
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Extraction failed: {str(e)}")
                
    except ImportError:
        raise HTTPException(
            status_code=503, 
            detail="yt-dlp not installed. Run: pip install yt-dlp"
        )

# Download endpoint (placeholder)
@app.post("/api/v1/download")
async def download_video(request: DownloadRequest):
    return {
        "success": False,
        "message": "Download feature requires full installation",
        "note": "Install all dependencies and use main.py for download functionality"
    }

# Platforms endpoint
@app.get("/api/v1/platforms")
async def get_platforms():
    return {
        "success": True,
        "data": {
            "platforms": ["youtube", "tiktok", "facebook", "instagram", "twitter", "vimeo"],
            "note": "Simplified list - full version supports 1000+ platforms"
        }
    }

# Error handler
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": str(exc),
            "note": "This is the simplified version"
        }
    )

if __name__ == "__main__":
    print("🎬 Starting Video Extractor Server (Simplified Version)")
    print("=" * 60)
    print(f"📍 Server: http://{settings.SERVER_HOST}:{settings.SERVER_PORT}")
    print(f"📚 Docs: http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/docs")
    print("⚠️  This is a simplified version - some features may be limited")
    print("💡 For full features, install all dependencies and use main.py")
    print("=" * 60)
    
    uvicorn.run(
        "main_simple:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True
    )
