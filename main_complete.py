"""
===================================================================
Video Extractor Server - Complete Professional Application
===================================================================
Author: Professional Development Team
Version: 1.0.0
Description: Complete FastAPI application with all features for Render
"""

import asyncio
import uvicorn
import os
import sys
import time
import json
import tempfile
import shutil
import logging
import random
import requests
import re
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, parse_qs

from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import yt_dlp
# import httpx  # Will be imported only when needed
# import aiofiles  # Will be imported only when needed
# from passlib.context import CryptContext  # Will be imported only when needed
# from passlib.hash import bcrypt  # Will be imported only when needed

# ===================================================================
# Logging Configuration (using colorlog instead of loguru)
# ===================================================================

def setup_logging():
    """Setup professional logging configuration"""

    # Create logger
    logger = logging.getLogger("video_extractor")
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(log_dir / "video_extractor.log")
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    logger.info("🚀 Video Extractor Server - Logging initialized")
    return logger

# Initialize logger
logger = setup_logging()

# ===================================================================
# Proxy and Anti-Detection System
# ===================================================================

class ProxyManager:
    """Advanced proxy management for bypassing restrictions"""

    def __init__(self):
        self.free_proxies = [
            # Free proxy services (will be rotated)
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:8080",
            # Add more free proxies here
        ]
        self.current_proxy_index = 0
        self.proxy_failures = {}

    def get_working_proxy(self):
        """Get a working proxy from the list"""
        # For now, return None to use direct connection
        # In production, implement actual proxy rotation
        return None

    def mark_proxy_failed(self, proxy):
        """Mark a proxy as failed"""
        if proxy:
            self.proxy_failures[proxy] = time.time()

    def get_random_proxy(self):
        """Get a random proxy for load balancing"""
        if not self.free_proxies:
            return None
        return random.choice(self.free_proxies)

class AntiDetectionManager:
    """Advanced anti-detection system"""

    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]
        self.referers = [
            'https://www.google.com/',
            'https://www.bing.com/',
            'https://duckduckgo.com/',
            'https://www.youtube.com/',
            'https://twitter.com/',
            'https://www.facebook.com/'
        ]

    def get_random_user_agent(self):
        """Get a random user agent"""
        return random.choice(self.user_agents)

    def get_random_referer(self):
        """Get a random referer"""
        return random.choice(self.referers)

    def get_realistic_headers(self):
        """Get realistic browser headers"""
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8,fr;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

# Initialize global managers
proxy_manager = ProxyManager()
anti_detection = AntiDetectionManager()

class PlatformExtractor:
    """Platform-specific extraction strategies"""

    def __init__(self):
        self.platform_configs = {
            'youtube': {
                'extractors': ['youtube', 'youtube:tab', 'youtube:playlist'],
                'special_options': {
                    'youtube_include_dash_manifest': False,
                    'youtube_skip_dash_manifest': True,
                    'writesubtitles': False,
                    'writeautomaticsub': False,
                }
            },
            'vimeo': {
                'extractors': ['vimeo', 'vimeo:album', 'vimeo:channel'],
                'special_options': {
                    'format': 'best[height<=720]',
                }
            },
            'dailymotion': {
                'extractors': ['dailymotion', 'dailymotion:playlist'],
                'special_options': {
                    'format': 'best',
                }
            },
            'twitch': {
                'extractors': ['twitch:vod', 'twitch:stream', 'twitch:clips'],
                'special_options': {
                    'format': 'best',
                }
            },
            'facebook': {
                'extractors': ['facebook', 'facebook:plugins:video'],
                'special_options': {
                    'format': 'best',
                }
            },
            'instagram': {
                'extractors': ['instagram', 'instagram:story', 'instagram:user'],
                'special_options': {
                    'format': 'best',
                }
            },
            'tiktok': {
                'extractors': ['tiktok', 'tiktok:user'],
                'special_options': {
                    'format': 'best',
                }
            },
            'twitter': {
                'extractors': ['twitter', 'twitter:broadcast'],
                'special_options': {
                    'format': 'best',
                }
            }
        }

    def detect_platform(self, url: str) -> str:
        """Detect platform from URL"""
        url_lower = url.lower()

        if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'youtube'
        elif 'vimeo.com' in url_lower:
            return 'vimeo'
        elif 'dailymotion.com' in url_lower:
            return 'dailymotion'
        elif 'twitch.tv' in url_lower:
            return 'twitch'
        elif 'facebook.com' in url_lower or 'fb.watch' in url_lower:
            return 'facebook'
        elif 'instagram.com' in url_lower:
            return 'instagram'
        elif 'tiktok.com' in url_lower:
            return 'tiktok'
        elif 'twitter.com' in url_lower or 'x.com' in url_lower:
            return 'twitter'
        else:
            return 'generic'

    def get_platform_options(self, platform: str) -> Dict[str, Any]:
        """Get platform-specific options"""
        if platform in self.platform_configs:
            return self.platform_configs[platform]['special_options']
        return {}

    def get_platform_extractors(self, platform: str) -> List[str]:
        """Get platform-specific extractors"""
        if platform in self.platform_configs:
            return self.platform_configs[platform]['extractors']
        return []

# Initialize platform extractor
platform_extractor = PlatformExtractor()

class BrowserSimulator:
    """Advanced browser simulation for bypassing detection"""

    def __init__(self):
        self.session_cookies = {}
        self.session_headers = {}

    def simulate_browser_session(self, url: str) -> Dict[str, Any]:
        """Simulate a realistic browser session"""

        # Simulate browser behavior
        session_options = {
            'cookiefile': None,  # Use in-memory cookies
            'cookiejar': None,
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1'
            }
        }

        # Add platform-specific session simulation
        if 'youtube.com' in url.lower():
            session_options.update(self._youtube_session_options())
        elif 'vimeo.com' in url.lower():
            session_options.update(self._vimeo_session_options())
        elif 'dailymotion.com' in url.lower():
            session_options.update(self._dailymotion_session_options())

        return session_options

    def _youtube_session_options(self) -> Dict[str, Any]:
        """YouTube-specific session options"""
        return {
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls'],
                    'player_skip': ['configs'],
                    'player_client': ['android', 'web'],
                    'comment_sort': ['top'],
                    'max_comments': ['100', '0'],
                }
            },
            'http_headers': {
                'Origin': 'https://www.youtube.com',
                'Referer': 'https://www.youtube.com/',
                'X-YouTube-Client-Name': '1',
                'X-YouTube-Client-Version': '2.20231201.01.00'
            }
        }

    def _vimeo_session_options(self) -> Dict[str, Any]:
        """Vimeo-specific session options"""
        return {
            'http_headers': {
                'Origin': 'https://vimeo.com',
                'Referer': 'https://vimeo.com/',
            }
        }

    def _dailymotion_session_options(self) -> Dict[str, Any]:
        """Dailymotion-specific session options"""
        return {
            'http_headers': {
                'Origin': 'https://www.dailymotion.com',
                'Referer': 'https://www.dailymotion.com/',
            }
        }

class AdvancedExtractor:
    """Advanced extraction with multiple fallback strategies"""

    def __init__(self):
        self.browser_sim = BrowserSimulator()
        self.extraction_strategies = [
            self._strategy_standard,
            self._strategy_mobile_user_agent,
            self._strategy_different_extractor,
            self._strategy_bypass_age_gate,
            self._strategy_alternative_format
        ]

    async def extract_with_fallback(self, url: str, quality: str = "best", audio_only: bool = False) -> Dict[str, Any]:
        """Try multiple extraction strategies"""

        last_error = None

        for i, strategy in enumerate(self.extraction_strategies):
            try:
                logger.info(f"Trying extraction strategy {i+1}/{len(self.extraction_strategies)}")
                result = await strategy(url, quality, audio_only)
                if result:
                    logger.info(f"Strategy {i+1} succeeded!")
                    return result
            except Exception as e:
                last_error = e
                logger.warning(f"Strategy {i+1} failed: {str(e)}")
                # Add delay between strategies
                await asyncio.sleep(random.uniform(1, 3))

        # If all strategies failed
        raise Exception(f"All extraction strategies failed. Last error: {str(last_error)}")

    async def _strategy_standard(self, url: str, quality: str, audio_only: bool) -> Dict[str, Any]:
        """Standard extraction strategy"""
        options = get_yt_dlp_options(quality, audio_only, url)
        return await self._extract_with_options(url, options)

    async def _strategy_mobile_user_agent(self, url: str, quality: str, audio_only: bool) -> Dict[str, Any]:
        """Mobile user agent strategy"""
        options = get_yt_dlp_options(quality, audio_only, url)
        options['user_agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        return await self._extract_with_options(url, options)

    async def _strategy_different_extractor(self, url: str, quality: str, audio_only: bool) -> Dict[str, Any]:
        """Try with different extractor settings"""
        options = get_yt_dlp_options(quality, audio_only, url)
        options['extractor_args'] = {
            'youtube': {
                'player_client': ['android'],
                'skip': ['webpage'],
            }
        }
        return await self._extract_with_options(url, options)

    async def _strategy_bypass_age_gate(self, url: str, quality: str, audio_only: bool) -> Dict[str, Any]:
        """Age gate bypass strategy"""
        options = get_yt_dlp_options(quality, audio_only, url)
        options['age_limit'] = 99
        options['extractor_args'] = {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['dash'],
            }
        }
        return await self._extract_with_options(url, options)

    async def _strategy_alternative_format(self, url: str, quality: str, audio_only: bool) -> Dict[str, Any]:
        """Alternative format strategy"""
        options = get_yt_dlp_options(quality, audio_only, url)
        if audio_only:
            options['format'] = 'bestaudio/best'
        else:
            options['format'] = 'best[height<=720]/best'
        return await self._extract_with_options(url, options)

    async def _extract_with_options(self, url: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Extract with given options"""
        def extract():
            with yt_dlp.YoutubeDL(options) as ydl:
                return ydl.extract_info(url, download=False)

        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, extract)

# Initialize advanced extractor
advanced_extractor = AdvancedExtractor()

class UltimateVideoExtractor:
    """Ultimate video extractor with multiple API fallbacks"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    async def extract_video_info_ultimate(self, url: str) -> Dict[str, Any]:
        """Ultimate extraction with multiple API fallbacks"""

        platform = self._detect_platform(url)

        if platform == 'youtube':
            return await self._extract_youtube_ultimate(url)
        elif platform == 'vimeo':
            return await self._extract_vimeo_ultimate(url)
        elif platform == 'dailymotion':
            return await self._extract_dailymotion_ultimate(url)
        else:
            return await self._extract_generic_ultimate(url)

    def _detect_platform(self, url: str) -> str:
        """Detect video platform"""
        url_lower = url.lower()
        if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'youtube'
        elif 'vimeo.com' in url_lower:
            return 'vimeo'
        elif 'dailymotion.com' in url_lower:
            return 'dailymotion'
        return 'generic'

    def _extract_youtube_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
            r'youtube\.com/watch\?.*v=([^&\n?#]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    async def _extract_youtube_ultimate(self, url: str) -> Dict[str, Any]:
        """Ultimate YouTube extraction"""
        video_id = self._extract_youtube_id(url)
        if not video_id:
            raise Exception("Could not extract YouTube video ID")

        # Try Invidious API first
        try:
            return await self._extract_via_invidious(video_id, url)
        except:
            pass

        # Try generic parser
        try:
            return await self._extract_via_generic_parser(video_id, url)
        except:
            pass

        # Fallback to basic info
        return {
            'title': f'YouTube Video {video_id}',
            'duration': 0,
            'uploader': 'Unknown',
            'view_count': 0,
            'upload_date': 'Unknown',
            'description': 'Extracted via ultimate fallback',
            'thumbnail': f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg',
            'platform': 'youtube',
            'extraction_method': 'ultimate_fallback',
            'formats': []
        }

    async def _extract_via_invidious(self, video_id: str, url: str) -> Dict[str, Any]:
        """Extract via Invidious API"""
        invidious_instances = [
            'https://invidious.io',
            'https://vid.puffyan.us',
            'https://invidious.snopyta.org'
        ]

        for instance in invidious_instances:
            try:
                api_url = f"{instance}/api/v1/videos/{video_id}"
                response = self.session.get(api_url, timeout=10)

                if response.status_code == 200:
                    data = response.json()

                    return {
                        'title': data.get('title', 'Unknown'),
                        'duration': data.get('lengthSeconds', 0),
                        'uploader': data.get('author', 'Unknown'),
                        'view_count': data.get('viewCount', 0),
                        'upload_date': str(data.get('published', 'Unknown')),
                        'description': data.get('description', '')[:1000],
                        'thumbnail': data.get('videoThumbnails', [{}])[0].get('url', ''),
                        'platform': 'youtube',
                        'extraction_method': 'invidious_api',
                        'formats': self._parse_invidious_formats(data.get('formatStreams', []))
                    }
            except Exception as e:
                logger.warning(f"Invidious instance {instance} failed: {str(e)}")
                continue

        raise Exception("All Invidious instances failed")

    async def _extract_via_generic_parser(self, video_id: str, url: str) -> Dict[str, Any]:
        """Generic parser fallback"""
        try:
            response = self.session.get(url, timeout=15)
            html = response.text

            # Extract title
            title_match = re.search(r'<title>([^<]+)</title>', html)
            title = title_match.group(1) if title_match else f'Video {video_id}'
            title = title.replace(' - YouTube', '').strip()

            return {
                'title': title,
                'duration': 0,
                'uploader': 'Unknown',
                'view_count': 0,
                'upload_date': 'Unknown',
                'description': 'Extracted via generic parser',
                'thumbnail': f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg',
                'platform': 'youtube',
                'extraction_method': 'generic_parser',
                'formats': []
            }
        except Exception:
            raise Exception("Generic parser failed")

    async def _extract_vimeo_ultimate(self, url: str) -> Dict[str, Any]:
        """Ultimate Vimeo extraction"""
        try:
            vimeo_id = re.search(r'vimeo\.com/(\d+)', url)
            if not vimeo_id:
                raise Exception("Could not extract Vimeo ID")

            video_id = vimeo_id.group(1)
            oembed_url = f"https://vimeo.com/api/oembed.json?url={url}"
            response = self.session.get(oembed_url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return {
                    'title': data.get('title', 'Unknown'),
                    'duration': data.get('duration', 0),
                    'uploader': data.get('author_name', 'Unknown'),
                    'view_count': 0,
                    'upload_date': 'Unknown',
                    'description': data.get('description', ''),
                    'thumbnail': data.get('thumbnail_url', ''),
                    'platform': 'vimeo',
                    'extraction_method': 'vimeo_oembed',
                    'formats': []
                }
        except Exception:
            pass

        raise Exception("Vimeo extraction failed")

    async def _extract_dailymotion_ultimate(self, url: str) -> Dict[str, Any]:
        """Ultimate Dailymotion extraction"""
        try:
            dm_id = re.search(r'dailymotion\.com/video/([^_]+)', url)
            if not dm_id:
                raise Exception("Could not extract Dailymotion ID")

            api_url = f"https://www.dailymotion.com/services/oembed?url={url}&format=json"
            response = self.session.get(api_url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return {
                    'title': data.get('title', 'Unknown'),
                    'duration': data.get('duration', 0),
                    'uploader': data.get('author_name', 'Unknown'),
                    'view_count': 0,
                    'upload_date': 'Unknown',
                    'description': 'Dailymotion video',
                    'thumbnail': data.get('thumbnail_url', ''),
                    'platform': 'dailymotion',
                    'extraction_method': 'dailymotion_oembed',
                    'formats': []
                }
        except Exception:
            pass

        raise Exception("Dailymotion extraction failed")

    async def _extract_generic_ultimate(self, url: str) -> Dict[str, Any]:
        """Generic ultimate extraction"""
        try:
            response = self.session.get(url, timeout=15)
            html = response.text

            title_match = re.search(r'<title>([^<]+)</title>', html)
            title = title_match.group(1) if title_match else 'Unknown'

            return {
                'title': title,
                'duration': 0,
                'uploader': 'Unknown',
                'view_count': 0,
                'upload_date': 'Unknown',
                'description': 'Generic extraction',
                'thumbnail': '',
                'platform': 'generic',
                'extraction_method': 'generic_html_parser',
                'formats': []
            }
        except Exception:
            raise Exception("Generic extraction failed")

    def _parse_invidious_formats(self, formats: List[Dict]) -> List[Dict]:
        """Parse Invidious formats"""
        parsed = []
        for fmt in formats[:10]:
            parsed.append({
                'format_id': fmt.get('itag', ''),
                'ext': fmt.get('container', ''),
                'quality': fmt.get('qualityLabel', ''),
                'filesize': fmt.get('size', 0),
                'url': fmt.get('url', ''),
                'fps': fmt.get('fps', 0),
                'vcodec': fmt.get('encoding', ''),
                'acodec': 'unknown'
            })
        return parsed

# Initialize ultimate extractor
ultimate_extractor = UltimateVideoExtractor()

# ===================================================================
# Configuration & Settings
# ===================================================================

class Settings:
    """Application settings and configuration"""
    
    def __init__(self):
        # Server Configuration
        self.HOST = os.getenv("HOST", "127.0.0.1")
        self.PORT = int(os.getenv("PORT", 8000))
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        
        # Security Configuration
        self.API_KEY = os.getenv("API_KEY", "default-api-key-change-me")
        self.ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
        self.CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
        
        # Application Configuration
        self.MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 1024 * 1024 * 1024))  # 1GB
        self.DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", 300))  # 5 minutes
        self.TEMP_DIR = os.getenv("TEMP_DIR", tempfile.gettempdir())
        
        # Logging Configuration
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.getenv("LOG_FILE", "logs/video_extractor.log")
        
        # Create necessary directories
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = [
            "logs",
            "downloads",
            "temp",
            "cache"
        ]
        
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)

# Initialize settings
settings = Settings()

# ===================================================================
# Data Models
# ===================================================================

class VideoRequest(BaseModel):
    """Video extraction request model"""
    url: str = Field(..., description="Video URL to extract")
    quality: Optional[str] = Field("best", description="Video quality preference")
    format: Optional[str] = Field(None, description="Specific format to download")
    audio_only: Optional[bool] = Field(False, description="Extract audio only")

class DownloadRequest(BaseModel):
    """Video download request model"""
    url: str = Field(..., description="Video URL to download")
    quality: Optional[str] = Field("best", description="Video quality preference")
    format: Optional[str] = Field(None, description="Specific format to download")
    audio_only: Optional[bool] = Field(False, description="Download audio only")

class VideoInfo(BaseModel):
    """Video information model"""
    title: str
    duration: Optional[int]
    uploader: Optional[str]
    view_count: Optional[int]
    upload_date: Optional[str]
    description: Optional[str]
    thumbnail: Optional[str]
    formats: List[Dict[str, Any]]

class APIResponse(BaseModel):
    """Standard API response model"""
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

# ===================================================================
# Security & Authentication
# ===================================================================

# Password hashing context (will be initialized when needed)
pwd_context = None

def verify_api_key(request: Request) -> bool:
    """Verify API key from request headers or query parameters"""
    # Check Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        provided_key = auth_header[7:]  # Remove "Bearer " prefix
        if provided_key == settings.API_KEY:
            return True
    
    # Check X-API-Key header
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header == settings.API_KEY:
        return True
    
    # Check query parameter
    api_key_param = request.query_params.get("api_key")
    if api_key_param == settings.API_KEY:
        return True
    
    return False

def require_api_key(request: Request):
    """Dependency to require API key authentication"""
    if not verify_api_key(request):
        logger.warning(f"🔒 Unauthorized access attempt from {request.client.host}")
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "error": "Invalid or missing API key",
                "path": str(request.url.path)
            }
        )
    return True

# ===================================================================
# Application Lifecycle
# ===================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🎬 Video Extractor Server - Starting up...")
    logger.info(f"🌍 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🔧 Debug Mode: {settings.DEBUG_MODE}")
    logger.info(f"📁 Temp Directory: {settings.TEMP_DIR}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Video Extractor Server - Shutting down...")
    
    # Cleanup temp files
    try:
        temp_path = Path(settings.TEMP_DIR)
        if temp_path.exists():
            for file in temp_path.glob("video_extractor_*"):
                file.unlink(missing_ok=True)
        logger.info("🧹 Temporary files cleaned up")
    except Exception as e:
        logger.error(f"❌ Error cleaning up temp files: {e}")

# ===================================================================
# FastAPI Application
# ===================================================================

app = FastAPI(
    title="🎬 Video Extractor Server",
    description="""
    **Professional Video Extraction & Download API**
    
    A powerful, secure, and efficient API for extracting video information and downloading videos from various platforms.
    
    ## Features
    - 🎥 Video information extraction
    - 📥 Video downloading with quality selection
    - 🎵 Audio-only extraction
    - 🔒 API key authentication
    - 📊 Comprehensive logging
    - 🚀 High performance with async operations
    
    ## Authentication
    Include your API key in one of the following ways:
    - **Header**: `Authorization: Bearer YOUR_API_KEY`
    - **Header**: `X-API-Key: YOUR_API_KEY`
    - **Query Parameter**: `?api_key=YOUR_API_KEY`
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ===================================================================
# Middleware Configuration
# ===================================================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Trusted Host Middleware
if settings.ALLOWED_HOSTS != ["*"]:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# ===================================================================
# Utility Functions
# ===================================================================

def get_yt_dlp_options(quality: str = "best", audio_only: bool = False, url: str = None) -> Dict[str, Any]:
    """Get advanced yt-dlp options to bypass bot detection and restrictions"""

    # Use anti-detection manager for realistic headers and user agents
    user_agent = anti_detection.get_random_user_agent()
    referer = anti_detection.get_random_referer()
    headers = anti_detection.get_realistic_headers()

    # Get proxy if available
    proxy = proxy_manager.get_working_proxy()

    # Detect platform and get platform-specific options
    platform = 'generic'
    platform_options = {}
    if url:
        platform = platform_extractor.detect_platform(url)
        platform_options = platform_extractor.get_platform_options(platform)
        logger.info(f"Detected platform: {platform} for URL: {url[:50]}...")

    options = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'writethumbnail': False,
        'writeinfojson': False,
        'no_check_certificate': True,
        'user_agent': user_agent,
        'referer': referer,
        'headers': headers,

        # Advanced anti-detection settings
        'sleep_interval': random.uniform(1, 3),
        'max_sleep_interval': 5,
        'sleep_interval_requests': random.uniform(0.5, 2),
        'sleep_interval_subtitles': 1,

        # Retry and error handling
        'retries': 5,
        'fragment_retries': 5,
        'skip_unavailable_fragments': True,
        'keep_fragments': False,
        'abort_on_unavailable_fragment': False,
        'extractor_retries': 5,
        'file_access_retries': 3,
        'socket_timeout': 30,

        # Network settings
        'http_chunk_size': 10485760,
        'prefer_insecure': False,

        # Geo-bypass settings
        'geo_bypass': True,
        'geo_bypass_country': 'US',
        'geo_bypass_ip_block': None,

        # YouTube-specific settings
        'youtube_include_dash_manifest': False,
        'youtube_skip_dash_manifest': True,

        # Additional anti-detection
        'extractor_args': {
            'youtube': {
                'skip': ['dash', 'hls'],
                'player_skip': ['configs', 'webpage'],
                'comment_sort': ['top'],
                'max_comments': ['100'],
            }
        }
    }

    # Add proxy if available
    if proxy:
        options['proxy'] = proxy
        logger.info(f"Using proxy: {proxy}")

    # Merge platform-specific options
    options.update(platform_options)

    # Add random delay to avoid rate limiting
    time.sleep(random.uniform(0.1, 0.5))

    if audio_only:
        options.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    else:
        if quality == "best":
            options['format'] = 'best[height<=1080]'
        elif quality == "worst":
            options['format'] = 'worst'
        else:
            options['format'] = quality

    return options

async def extract_video_info(url: str, quality: str = "best") -> Dict[str, Any]:
    """Extract video information using ultimate extraction methods"""
    try:
        logger.info(f"Starting ultimate video extraction for: {url[:50]}...")

        # Try ultimate extractor first (API-based methods)
        try:
            logger.info("Trying ultimate API-based extraction...")
            info = await ultimate_extractor.extract_video_info_ultimate(url)
            if info:
                logger.info(f"✅ Ultimate extraction successful: {info.get('extraction_method', 'unknown')}")
                return info
        except Exception as e:
            logger.warning(f"Ultimate extraction failed: {str(e)}")

        # Fallback to advanced yt-dlp extractor
        try:
            logger.info("Falling back to advanced yt-dlp extraction...")
            info = await advanced_extractor.extract_with_fallback(url, quality, False)
            if info:
                logger.info("✅ Advanced yt-dlp extraction successful")
                return _format_yt_dlp_info(info, url)
        except Exception as e:
            logger.warning(f"Advanced yt-dlp extraction failed: {str(e)}")

        # Final fallback - basic info
        logger.info("Using final fallback - basic info extraction")
        return _create_basic_info(url)

    except Exception as e:
        logger.error(f"❌ Error extracting video info: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract video information: {str(e)}"
        )

def _format_yt_dlp_info(info: Dict[str, Any], url: str) -> Dict[str, Any]:
    """Format yt-dlp info to standard format"""
    return {
        "title": info.get("title", "Unknown"),
        "duration": info.get("duration", 0),
        "uploader": info.get("uploader", "Unknown"),
        "view_count": info.get("view_count", 0),
        "upload_date": info.get("upload_date", "Unknown"),
        "description": (info.get("description", "") or "")[:1000],
        "thumbnail": info.get("thumbnail", ""),
        "platform": platform_extractor.detect_platform(url),
        "extraction_method": "advanced_yt_dlp",
        "formats": _format_yt_dlp_formats(info.get("formats", []))
    }

def _format_yt_dlp_formats(formats: List[Dict]) -> List[Dict]:
    """Format yt-dlp formats"""
    formatted = []
    for fmt in formats[:15]:
        if fmt.get("url"):
            formatted.append({
                "format_id": fmt.get("format_id", ""),
                "ext": fmt.get("ext", ""),
                "quality": fmt.get("format_note", ""),
                "filesize": fmt.get("filesize", 0),
                "fps": fmt.get("fps", 0),
                "vcodec": fmt.get("vcodec", ""),
                "acodec": fmt.get("acodec", ""),
            })
    return formatted

def _create_basic_info(url: str) -> Dict[str, Any]:
    """Create basic info as final fallback"""
    platform = platform_extractor.detect_platform(url)

    return {
        "title": f"Video from {platform}",
        "duration": 0,
        "uploader": "Unknown",
        "view_count": 0,
        "upload_date": "Unknown",
        "description": "Basic extraction fallback",
        "thumbnail": "",
        "platform": platform,
        "extraction_method": "basic_fallback",
        "formats": []
    }

# ===================================================================
# API Routes
# ===================================================================

@app.get("/", response_model=APIResponse, tags=["General"])
async def root():
    """Root endpoint - API information"""
    return APIResponse(
        success=True,
        message="Welcome to Video Extractor Server",
        data={
            "version": "1.0.0",
            "status": "operational",
            "documentation": "/docs",
            "api_base": "/api/v1",
            "features": [
                "Video information extraction",
                "Multi-quality downloads",
                "Audio extraction",
                "API key authentication",
                "Professional logging",
                "High performance"
            ]
        }
    )

@app.get("/health", response_model=APIResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    return APIResponse(
        success=True,
        message="Server is running properly",
        data={
            "status": "healthy",
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT,
            "debug_mode": settings.DEBUG_MODE,
            "uptime": "operational"
        }
    )

@app.post("/api/v1/extract", response_model=APIResponse, tags=["Video"])
async def extract_video(request: Request, video_request: VideoRequest):
    """Extract video information without downloading"""
    # Verify API key
    require_api_key(request)

    logger.info(f"🎬 Extracting video info: {video_request.url}")

    try:
        video_info = await extract_video_info(
            video_request.url,
            video_request.quality
        )

        logger.info(f"✅ Successfully extracted info for: {video_info['title']}")

        return APIResponse(
            success=True,
            message="Video information extracted successfully",
            data=video_info
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error in extract_video: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@app.post("/api/v1/download", response_model=APIResponse, tags=["Video"])
async def download_video(request: Request, download_request: DownloadRequest):
    """Download video with specified quality"""
    # Verify API key
    require_api_key(request)

    logger.info(f"📥 Download request: {download_request.url}")

    try:
        # Create temporary directory for this download
        temp_dir = Path(settings.TEMP_DIR) / f"video_extractor_{int(time.time())}"
        temp_dir.mkdir(exist_ok=True)

        # Use advanced extractor for download
        logger.info(f"Starting advanced download for: {download_request.url[:50]}...")

        # First extract info to get title for filename
        info = await advanced_extractor.extract_with_fallback(
            download_request.url,
            download_request.quality,
            download_request.audio_only
        )

        # Configure yt-dlp options for download
        ydl_opts = get_yt_dlp_options(
            download_request.quality,
            download_request.audio_only,
            download_request.url
        )
        ydl_opts.update({
            'outtmpl': str(temp_dir / '%(title)s.%(ext)s'),
            'restrictfilenames': True,
        })

        # Download the video using the same options that worked for extraction
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(download_request.url, download=True)

            # Find downloaded file
            downloaded_files = list(temp_dir.glob("*"))
            if not downloaded_files:
                raise HTTPException(
                    status_code=500,
                    detail="Download completed but no file found"
                )

            downloaded_file = downloaded_files[0]
            file_size = downloaded_file.stat().st_size

            logger.info(f"✅ Successfully downloaded: {info.get('title', 'Unknown')} ({file_size} bytes)")

            return APIResponse(
                success=True,
                message="Download initiated",
                data={
                    "title": info.get("title", "Unknown"),
                    "filename": downloaded_file.name,
                    "file_size": file_size,
                    "format": info.get("ext", "unknown"),
                    "status": "completed"
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Download error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Download failed: {str(e)}"
        )
    finally:
        # Cleanup temporary directory
        try:
            if 'temp_dir' in locals() and temp_dir.exists():
                shutil.rmtree(temp_dir)
        except Exception as e:
            logger.warning(f"⚠️ Failed to cleanup temp directory: {e}")

# ===================================================================
# Error Handlers
# ===================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.warning(f"🚨 HTTP {exc.status_code}: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "path": str(request.url.path),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"💥 Unhandled exception: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "path": str(request.url.path),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# ===================================================================
# Development Server
# ===================================================================

if __name__ == "__main__":
    logger.info("🚀 Starting Video Extractor Server in development mode...")

    uvicorn.run(
        "main_complete:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )
