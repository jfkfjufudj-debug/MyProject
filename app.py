"""
===================================================================
Video Extractor Server - Render Deployment App
===================================================================
This file imports the app from main_render.py for Render compatibility
"""

# Import the app from main_complete.py (full features)
from main_complete import app

# This allows Render to find the app
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
