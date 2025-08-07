"""
===================================================================
Video Extractor Server - Main Entry Point for Render
===================================================================
This file imports the app from app.py for Render compatibility
"""

# Import the app from app.py
from app import app

# This allows Render to find the app at main:app
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
