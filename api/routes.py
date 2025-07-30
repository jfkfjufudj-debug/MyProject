"""
===================================================================
Video Extractor Server - Professional API Routes
===================================================================
Author: Professional Development Team
Version: 1.0.0
Description: RESTful API endpoints for video extraction and download
"""

import asyncio
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks, Request
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from loguru import logger
import os
from pathlib import Path

from core.extractor import video_extractor
from core.downloader import download_manager
from api.auth import require_extract_permission, require_download_permission, get_client_ip
from config.settings import settings, get_downloads_path

# Create router
router = APIRouter()

# ===============================
# Request/Response Models
# ===============================

class ExtractRequest(BaseModel):
    """Request model for video extraction"""
    url: str
    include_playlist: bool = False
    max_playlist_videos: int = 50

class DownloadRequest(BaseModel):
    """Request model for video download"""
    url: str
    quality: str = "720p"
    format_type: str = "video"  # video, audio

class ValidationRequest(BaseModel):
    """Request model for URL validation"""
    url: str

# ===============================
# API Endpoints
# ===============================

@router.get("/", summary="API Information")
async def root():
    """Get API information and status"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "supported_platforms": settings.SUPPORTED_PLATFORMS,
        "endpoints": {
            "extract": "/extract - Extract video information",
            "download": "/download - Download video/audio",
            "validate": "/validate - Validate URL",
            "status": "/status/{download_id} - Get download status"
        },
        "documentation": "/docs"
    }

@router.post("/extract", summary="Extract Video Information")
async def extract_video(
    request: ExtractRequest,
    auth_data: Dict = Depends(require_extract_permission()),
    client_ip: str = Depends(get_client_ip)
):
    """
    Extract comprehensive video information from URL
    
    - **url**: Video URL from supported platforms
    - **include_playlist**: Whether to extract playlist information (if URL is playlist)
    - **max_playlist_videos**: Maximum number of videos to extract from playlist
    """
    try:
        logger.info(f"Extract request from {client_ip}: {request.url}")
        
        url_str = str(request.url)
        
        # Validate URL accessibility first
        validation_result = await video_extractor.validate_url_accessibility(url_str)
        if not validation_result['valid']:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "URL validation failed",
                    "message": validation_result['error'],
                    "platform": validation_result['platform']
                }
            )
        
        # Check if it's a playlist and handle accordingly
        if request.include_playlist and validation_result.get('is_playlist'):
            logger.info(f"Extracting playlist information: {url_str}")
            result = await video_extractor.extract_playlist_info(
                url_str, 
                max_videos=request.max_playlist_videos
            )
        else:
            logger.info(f"Extracting video information: {url_str}")
            result = await video_extractor.extract_video_info(url_str)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Extraction failed",
                    "message": result.get('error', 'Unknown error occurred')
                }
            )
        
        logger.success(f"Successfully extracted info for: {result.get('title', 'Unknown')}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": result,
                "metadata": {
                    "extracted_at": logger._core.now().isoformat(),
                    "client_ip": client_ip,
                    "platform": validation_result['platform']
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "Failed to extract video information"
            }
        )

@router.post("/download", summary="Download Video/Audio")
async def download_video(
    request: DownloadRequest,
    background_tasks: BackgroundTasks,
    auth_data: Dict = Depends(require_download_permission()),
    client_ip: str = Depends(get_client_ip)
):
    """
    Download video or audio file
    
    - **url**: Video URL from supported platforms
    - **quality**: Video quality (144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p, best, worst)
    - **format_type**: Type of download (video, audio)
    """
    try:
        logger.info(f"Download request from {client_ip}: {request.url} ({request.quality}, {request.format_type})")
        
        url_str = str(request.url)
        
        # Validate URL first
        validation_result = await video_extractor.validate_url_accessibility(url_str)
        if not validation_result['valid']:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "URL validation failed",
                    "message": validation_result['error']
                }
            )
        
        # Start download
        download_result = await download_manager.download_with_yt_dlp(
            url=url_str,
            quality=request.quality,
            format_type=request.format_type
        )
        
        if not download_result['success']:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Download failed",
                    "message": download_result.get('error', 'Unknown error occurred'),
                    "download_id": download_result.get('download_id')
                }
            )
        
        # Schedule cleanup of temp files
        background_tasks.add_task(download_manager.cleanup_temp_files)
        
        logger.success(f"Download completed: {download_result['download_id']}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "download_id": download_result['download_id'],
                    "filename": os.path.basename(download_result['final_path']),
                    "download_url": download_result['download_url'],
                    "filesize": download_result.get('filesize', 0),
                    "title": download_result.get('title', 'Unknown')
                },
                "metadata": {
                    "downloaded_at": logger._core.now().isoformat(),
                    "client_ip": client_ip,
                    "quality": request.quality,
                    "format_type": request.format_type
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "Failed to download video"
            }
        )

@router.post("/validate", summary="Validate URL")
async def validate_url(
    request: ValidationRequest,
    auth_data: Dict = Depends(require_extract_permission()),
    client_ip: str = Depends(get_client_ip)
):
    """
    Validate if URL is supported and accessible
    
    - **url**: Video URL to validate
    """
    try:
        logger.info(f"Validation request from {client_ip}: {request.url}")
        
        url_str = str(request.url)
        result = await video_extractor.validate_url_accessibility(url_str)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": result,
                "metadata": {
                    "validated_at": logger._core.now().isoformat(),
                    "client_ip": client_ip
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "Failed to validate URL"
            }
        )

@router.get("/status/{download_id}", summary="Get Download Status")
async def get_download_status(
    download_id: str,
    auth_data: Dict = Depends(require_download_permission()),
    client_ip: str = Depends(get_client_ip)
):
    """
    Get download status by download ID
    
    - **download_id**: Download ID returned from /download endpoint
    """
    try:
        status = download_manager.get_download_status(download_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": status,
                "metadata": {
                    "checked_at": logger._core.now().isoformat(),
                    "client_ip": client_ip
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "Failed to get download status"
            }
        )

@router.get("/downloads/{filename}", summary="Download File")
async def download_file(
    filename: str,
    auth_data: Dict = Depends(require_download_permission())
):
    """
    Download a previously processed file
    
    - **filename**: Name of the file to download
    """
    try:
        downloads_path = get_downloads_path()
        file_path = downloads_path / filename
        
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "File not found",
                    "message": f"File '{filename}' does not exist"
                }
            )
        
        if not file_path.is_file():
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid file",
                    "message": f"'{filename}' is not a valid file"
                }
            )
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File download error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "Failed to download file"
            }
        )

@router.get("/platforms", summary="Get Supported Platforms")
async def get_supported_platforms(
    auth_data: Dict = Depends(require_extract_permission())
):
    """
    Get list of supported video platforms
    """
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": {
                "platforms": settings.SUPPORTED_PLATFORMS,
                "total_count": len(settings.SUPPORTED_PLATFORMS),
                "note": "This list includes major platforms. yt-dlp supports 1000+ sites."
            }
        }
    )

# ===============================
# Error Handlers (will be added to main app)
# ===============================

# Note: Exception handlers are added in main.py, not here
