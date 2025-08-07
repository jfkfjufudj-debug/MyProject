"""
===================================================================
Video Extractor Server - Professional Main Application
===================================================================
Author: Professional Development Team
Version: 1.0.0
Description: FastAPI application for video extraction and download
"""

import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
import sys
from pathlib import Path

# Import application modules
from config.settings import settings, validate_configuration
from api.routes import router as api_router
from api.auth import security_middleware
from utils.helpers import cache_manager

# Configure logging
def setup_logging():
    """Setup professional logging configuration"""
    
    # Remove default logger
    logger.remove()
    
    # Console logging
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True
    )
    
    # File logging
    logger.add(
        settings.LOG_FILE_PATH,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.LOG_LEVEL,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        compression="zip"
    )
    
    logger.info("Logging system initialized")

# Application lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown"""
    
    # Startup
    logger.info("🚀 Starting Video Extractor Server...")
    
    # Validate configuration
    if not validate_configuration():
        logger.error("❌ Configuration validation failed!")
        sys.exit(1)
    
    # Setup periodic tasks
    asyncio.create_task(periodic_cleanup())
    
    logger.success("✅ Server startup completed successfully!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Video Extractor Server...")
    
    # Cleanup tasks
    await cleanup_on_shutdown()
    
    logger.success("✅ Server shutdown completed successfully!")

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    🎬 **Professional Video Extractor Server**
    
    A high-performance API for extracting video information and downloading content from 1000+ platforms.
    
    ## Features
    
    * 🔍 **Extract** comprehensive video information
    * 📥 **Download** videos and audio in multiple qualities
    * 🔐 **Secure** API key authentication
    * 🚀 **Fast** with intelligent caching
    * 📊 **Professional** logging and monitoring
    
    ## Supported Platforms
    
    YouTube, TikTok, Facebook, Instagram, Twitter, Vimeo, Dailymotion, Twitch, and 1000+ more!
    
    ## Authentication
    
    All endpoints require a valid API key. Include it in:
    - **Authorization header**: `Bearer YOUR_API_KEY`
    - **Query parameter**: `?api_key=YOUR_API_KEY`
    - **Custom header**: `X-API-Key: YOUR_API_KEY`
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Trusted Host Middleware (security)
if not settings.DEBUG_MODE:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", settings.SERVER_HOST]
    )

# Custom Security Middleware
app.middleware("http")(security_middleware)

# Request/Response Middleware
@app.middleware("http")
async def request_response_middleware(request: Request, call_next):
    """Custom middleware for request/response processing"""
    
    # Log request
    start_time = logger._core.now()
    client_ip = request.headers.get('X-Forwarded-For', request.client.host if request.client else 'unknown')
    
    logger.info(f"📨 {request.method} {request.url.path} from {client_ip}")
    
    # Process request
    try:
        response = await call_next(request)
        
        # Calculate processing time
        process_time = (logger._core.now() - start_time).total_seconds()
        
        # Add custom headers
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Server-Version"] = settings.APP_VERSION
        
        # Log response
        logger.info(f"📤 {response.status_code} {request.url.path} ({process_time:.3f}s)")
        
        return response
        
    except Exception as e:
        # Log error
        process_time = (logger._core.now() - start_time).total_seconds()
        logger.error(f"❌ Error processing {request.method} {request.url.path}: {str(e)} ({process_time:.3f}s)")
        
        # Return error response
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "message": "An unexpected error occurred",
                "metadata": {
                    "timestamp": start_time.isoformat(),
                    "process_time": process_time,
                    "path": str(request.url.path),
                    "method": request.method
                }
            }
        )

# Include API routes
app.include_router(api_router, prefix="/api/v1", tags=["Video Extractor API"])

# Static files for downloads
downloads_path = Path(settings.DOWNLOADS_PATH)
downloads_path.mkdir(exist_ok=True)

try:
    app.mount("/downloads", StaticFiles(directory=str(downloads_path)), name="downloads")
except Exception as e:
    logger.warning(f"Could not mount downloads directory: {e}")

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint with server information"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "operational",
        "documentation": "/docs",
        "api_base": "/api/v1",
        "supported_platforms": len(settings.SUPPORTED_PLATFORMS),
        "features": [
            "Video information extraction",
            "Multi-quality downloads",
            "Audio extraction",
            "Playlist support",
            "API key authentication",
            "Rate limiting",
            "Intelligent caching"
        ]
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check cache system
        cache_stats = await cache_manager.get_cache_stats()
        
        return {
            "status": "healthy",
            "timestamp": logger._core.now().isoformat(),
            "version": settings.APP_VERSION,
            "uptime": "operational",
            "cache": {
                "enabled": cache_stats.get('enabled', False),
                "entries": cache_stats.get('active_entries', 0)
            },
            "settings": {
                "debug_mode": settings.DEBUG_MODE,
                "max_file_size_mb": settings.MAX_FILE_SIZE_MB,
                "rate_limit": settings.MAX_REQUESTS_PER_MINUTE
            }
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": logger._core.now().isoformat()
            }
        )

# Periodic cleanup task
async def periodic_cleanup():
    """Periodic cleanup task for maintenance"""
    while True:
        try:
            # Wait 1 hour between cleanups
            await asyncio.sleep(3600)
            
            logger.info("🧹 Starting periodic cleanup...")
            
            # Clear expired cache
            cleared_cache = await cache_manager.clear_expired()
            
            # Clean temp files (from download manager)
            from core.downloader import download_manager
            download_manager.cleanup_temp_files()
            
            logger.info(f"🧹 Cleanup completed: {cleared_cache} cache entries cleared")
            
        except Exception as e:
            logger.error(f"Periodic cleanup error: {str(e)}")

# Cleanup on shutdown
async def cleanup_on_shutdown():
    """Cleanup tasks on server shutdown"""
    try:
        logger.info("🧹 Running shutdown cleanup...")
        
        # Clear expired cache
        await cache_manager.clear_expired()
        
        # Additional cleanup tasks can be added here
        
        logger.info("🧹 Shutdown cleanup completed")
        
    except Exception as e:
        logger.error(f"Shutdown cleanup error: {str(e)}")

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "metadata": {
                "timestamp": logger._core.now().isoformat() if hasattr(logger, '_core') else None,
                "path": str(request.url.path),
                "method": request.method
            }
        }
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Not Found",
            "message": f"The requested endpoint '{request.url.path}' was not found",
            "available_endpoints": {
                "api": "/api/v1",
                "docs": "/docs",
                "health": "/health"
            }
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 handler"""
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server",
            "timestamp": logger._core.now().isoformat() if hasattr(logger, '_core') else None
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "type": "Internal server error",
                "message": "An unexpected error occurred"
            },
            "metadata": {
                "timestamp": logger._core.now().isoformat() if hasattr(logger, '_core') else None,
                "path": str(request.url.path),
                "method": request.method
            }
        }
    )

# Main execution
if __name__ == "__main__":
    # Setup logging
    setup_logging()
    
    logger.info("🎬 Initializing Video Extractor Server...")
    
    # Run server
    import os
    port = int(os.environ.get("PORT", settings.SERVER_PORT))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.DEBUG_MODE,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
        server_header=False,
        date_header=False
    )
