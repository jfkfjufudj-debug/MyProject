"""
===================================================================
Video Extractor Server - Simplified Configuration Settings
===================================================================
Author: Professional Development Team
Version: 1.0.0
Description: Simple configuration without complex dependencies
"""

import os
from pathlib import Path
from typing import List, Optional

# Simple settings class without pydantic
class Settings:
    """
    Simplified application settings
    """

    def __init__(self):
        # Load from environment variables or use defaults
        self.SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
        self.SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"
        self.APP_NAME = "Video Extractor Server"
        self.APP_VERSION = "1.0.0"

        # Security
        self.API_KEY = os.getenv("API_KEY", "default-api-key-change-me")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-jwt-key-change-me")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

        # File Management
        self.MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "500"))
        self.DOWNLOADS_PATH = os.getenv("DOWNLOADS_PATH", "./downloads")
        self.TEMP_PATH = os.getenv("TEMP_PATH", "./temp")
        self.CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        self.CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

        # Rate Limiting
        self.MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
        self.MAX_CONCURRENT_DOWNLOADS = 5
        self.REQUEST_TIMEOUT_SECONDS = 30

        # Logging
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "./logs/server.log")
        self.LOG_ROTATION = "10 MB"
        self.LOG_RETENTION = "7 days"

        # CORS
        self.ALLOWED_ORIGINS = ["*"]
        self.ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.ALLOWED_HEADERS = ["*"]

        # Video Processing
        self.SUPPORTED_PLATFORMS = [
            "youtube", "tiktok", "facebook", "instagram",
            "twitter", "vimeo", "dailymotion", "twitch"
        ]
        self.DEFAULT_VIDEO_QUALITY = "720p"
        self.SUPPORTED_FORMATS = ["mp4", "webm", "mkv", "avi"]
        self.SUPPORTED_AUDIO_FORMATS = ["mp3", "m4a", "wav", "aac"]

        # Create directories
        self._create_directories()

    def _create_directories(self):
        """Create necessary directories"""
        try:
            Path(self.DOWNLOADS_PATH).mkdir(parents=True, exist_ok=True)
            Path(self.TEMP_PATH).mkdir(parents=True, exist_ok=True)
            Path(self.LOG_FILE_PATH).parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create directories: {e}")

# ===============================
# Global Settings Instance
# ===============================
settings = Settings()

# ===============================
# Helper Functions
# ===============================
def get_downloads_path() -> Path:
    """Get the absolute path for downloads directory"""
    path = Path(settings.DOWNLOADS_PATH)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_temp_path() -> Path:
    """Get the absolute path for temporary files directory"""
    path = Path(settings.TEMP_PATH)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_logs_path() -> Path:
    """Get the absolute path for logs directory"""
    path = Path(settings.LOG_FILE_PATH).parent
    path.mkdir(parents=True, exist_ok=True)
    return path

def is_debug_mode() -> bool:
    """Check if application is running in debug mode"""
    return settings.DEBUG_MODE

def get_max_file_size_bytes() -> int:
    """Get maximum file size in bytes"""
    return settings.MAX_FILE_SIZE_MB * 1024 * 1024

# ===============================
# Configuration Validation
# ===============================
def validate_configuration():
    """Validate all configuration settings on startup"""
    try:
        # Test directory creation
        get_downloads_path()
        get_temp_path()
        get_logs_path()

        # Validate critical settings
        if settings.API_KEY == "default-api-key-change-me":
            print("⚠️  WARNING: Using default API key. Please change it in production!")

        if settings.SECRET_KEY == "super-secret-jwt-key-change-me":
            print("⚠️  WARNING: Using default secret key. Please change it in production!")

        print("✅ Configuration validation completed successfully")
        return True

    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

# Auto-validate on import
if __name__ != "__main__":
    validate_configuration()
