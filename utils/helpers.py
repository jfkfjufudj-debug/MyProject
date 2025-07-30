"""
===================================================================
Video Extractor Server - Professional Utility Functions
===================================================================
Author: Professional Development Team
Version: 1.0.0
Description: Helper functions for data processing, validation, and caching
"""

import re
import json
import hashlib
import time
import asyncio
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import aiofiles
from loguru import logger

from config.settings import settings

class URLValidator:
    """
    Professional URL validation and processing utilities
    """
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def extract_video_id(url: str, platform: str) -> Optional[str]:
        """Extract video ID from URL based on platform"""
        try:
            if platform == 'youtube':
                # YouTube URL patterns
                patterns = [
                    r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
                    r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
                    r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})'
                ]
                for pattern in patterns:
                    match = re.search(pattern, url)
                    if match:
                        return match.group(1)
            
            elif platform == 'tiktok':
                # TikTok URL patterns
                patterns = [
                    r'tiktok\.com\/@[\w.-]+\/video\/(\d+)',
                    r'vm\.tiktok\.com\/([a-zA-Z0-9]+)',
                    r'tiktok\.com\/t\/([a-zA-Z0-9]+)'
                ]
                for pattern in patterns:
                    match = re.search(pattern, url)
                    if match:
                        return match.group(1)
            
            elif platform == 'instagram':
                # Instagram URL patterns
                patterns = [
                    r'instagram\.com\/p\/([a-zA-Z0-9_-]+)',
                    r'instagram\.com\/reel\/([a-zA-Z0-9_-]+)',
                    r'instagram\.com\/tv\/([a-zA-Z0-9_-]+)'
                ]
                for pattern in patterns:
                    match = re.search(pattern, url)
                    if match:
                        return match.group(1)
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting video ID: {str(e)}")
            return None
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalize URL for consistent processing"""
        try:
            # Remove tracking parameters
            parsed = urlparse(url)
            
            # YouTube specific normalization
            if 'youtube.com' in parsed.netloc:
                query_params = parse_qs(parsed.query)
                # Keep only essential parameters
                essential_params = ['v', 'list', 't']
                filtered_params = {k: v for k, v in query_params.items() if k in essential_params}
                
                if 'v' in filtered_params:
                    video_id = filtered_params['v'][0]
                    return f"https://www.youtube.com/watch?v={video_id}"
            
            # For other platforms, return as-is for now
            return url
            
        except Exception:
            return url

class DataFormatter:
    """
    Professional data formatting and processing utilities
    """
    
    @staticmethod
    def format_duration(seconds: Optional[int]) -> str:
        """Format duration in seconds to human-readable format"""
        if not seconds or seconds <= 0:
            return "Unknown"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def format_file_size(bytes_size: Optional[int]) -> str:
        """Format file size in bytes to human-readable format"""
        if not bytes_size or bytes_size <= 0:
            return "Unknown"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = float(bytes_size)
        unit_index = 0
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        return f"{size:.1f} {units[unit_index]}"
    
    @staticmethod
    def format_view_count(count: Optional[int]) -> str:
        """Format view count to human-readable format"""
        if not count or count <= 0:
            return "Unknown"
        
        if count >= 1_000_000_000:
            return f"{count / 1_000_000_000:.1f}B"
        elif count >= 1_000_000:
            return f"{count / 1_000_000:.1f}M"
        elif count >= 1_000:
            return f"{count / 1_000:.1f}K"
        else:
            return str(count)
    
    @staticmethod
    def clean_title(title: str) -> str:
        """Clean video title for safe usage"""
        if not title:
            return "Unknown Title"
        
        # Remove excessive whitespace
        title = re.sub(r'\s+', ' ', title.strip())
        
        # Remove or replace problematic characters
        title = re.sub(r'[<>:"/\\|?*]', '_', title)
        
        # Limit length
        if len(title) > 100:
            title = title[:97] + "..."
        
        return title
    
    @staticmethod
    def extract_thumbnail_url(thumbnails: List[Dict]) -> Optional[str]:
        """Extract best quality thumbnail URL"""
        if not thumbnails:
            return None
        
        # Sort by resolution (width * height) descending
        sorted_thumbnails = sorted(
            thumbnails,
            key=lambda x: (x.get('width', 0) * x.get('height', 0)),
            reverse=True
        )
        
        return sorted_thumbnails[0].get('url') if sorted_thumbnails else None

class CacheManager:
    """
    Professional caching system for improved performance
    """
    
    def __init__(self):
        """Initialize cache manager"""
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_ttl = settings.CACHE_TTL_SECONDS
        self.enabled = settings.CACHE_ENABLED
        
        logger.info(f"Cache manager initialized (enabled: {self.enabled})")
    
    def _get_cache_key(self, data: str) -> str:
        """Generate cache key from data"""
        return hashlib.md5(data.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get cache file path"""
        return self.cache_dir / f"{cache_key}.json"
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get data from cache"""
        if not self.enabled:
            return None
        
        try:
            cache_key = self._get_cache_key(key)
            cache_path = self._get_cache_path(cache_key)
            
            if not cache_path.exists():
                return None
            
            # Check if cache is expired
            cache_age = time.time() - cache_path.stat().st_mtime
            if cache_age > self.cache_ttl:
                # Remove expired cache
                cache_path.unlink()
                return None
            
            # Read cache data
            async with aiofiles.open(cache_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                data = json.loads(content)
                
                logger.debug(f"Cache hit: {cache_key}")
                return data
                
        except Exception as e:
            logger.error(f"Cache read error: {str(e)}")
            return None
    
    async def set(self, key: str, data: Dict[str, Any]) -> bool:
        """Set data in cache"""
        if not self.enabled:
            return False
        
        try:
            cache_key = self._get_cache_key(key)
            cache_path = self._get_cache_path(cache_key)
            
            # Add cache metadata
            cache_data = {
                'cached_at': time.time(),
                'cache_key': cache_key,
                'data': data
            }
            
            # Write cache data
            async with aiofiles.open(cache_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(cache_data, ensure_ascii=False, indent=2))
            
            logger.debug(f"Cache set: {cache_key}")
            return True
            
        except Exception as e:
            logger.error(f"Cache write error: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete data from cache"""
        try:
            cache_key = self._get_cache_key(key)
            cache_path = self._get_cache_path(cache_key)
            
            if cache_path.exists():
                cache_path.unlink()
                logger.debug(f"Cache deleted: {cache_key}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")
            return False
    
    async def clear_expired(self) -> int:
        """Clear expired cache entries"""
        try:
            cleared_count = 0
            current_time = time.time()
            
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    cache_age = current_time - cache_file.stat().st_mtime
                    if cache_age > self.cache_ttl:
                        cache_file.unlink()
                        cleared_count += 1
                except Exception:
                    continue
            
            if cleared_count > 0:
                logger.info(f"Cleared {cleared_count} expired cache entries")
            
            return cleared_count
            
        except Exception as e:
            logger.error(f"Cache cleanup error: {str(e)}")
            return 0
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            cache_files = list(self.cache_dir.glob("*.json"))
            total_files = len(cache_files)
            total_size = sum(f.stat().st_size for f in cache_files if f.exists())
            
            # Count expired files
            current_time = time.time()
            expired_count = 0
            for cache_file in cache_files:
                try:
                    cache_age = current_time - cache_file.stat().st_mtime
                    if cache_age > self.cache_ttl:
                        expired_count += 1
                except Exception:
                    continue
            
            return {
                'enabled': self.enabled,
                'total_entries': total_files,
                'expired_entries': expired_count,
                'active_entries': total_files - expired_count,
                'total_size_bytes': total_size,
                'total_size_formatted': DataFormatter.format_file_size(total_size),
                'cache_ttl_seconds': self.cache_ttl,
                'cache_directory': str(self.cache_dir)
            }
            
        except Exception as e:
            logger.error(f"Cache stats error: {str(e)}")
            return {
                'enabled': self.enabled,
                'error': str(e)
            }

class ResponseBuilder:
    """
    Professional API response builder
    """
    
    @staticmethod
    def success_response(
        data: Any,
        message: str = "Operation completed successfully",
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Build success response"""
        response = {
            "success": True,
            "message": message,
            "data": data
        }
        
        if metadata:
            response["metadata"] = metadata
        
        return response
    
    @staticmethod
    def error_response(
        error: str,
        message: str = "Operation failed",
        error_code: Optional[str] = None,
        details: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Build error response"""
        response = {
            "success": False,
            "error": error,
            "message": message
        }
        
        if error_code:
            response["error_code"] = error_code
        
        if details:
            response["details"] = details
        
        return response
    
    @staticmethod
    def paginated_response(
        data: List[Any],
        page: int,
        per_page: int,
        total: int,
        message: str = "Data retrieved successfully"
    ) -> Dict[str, Any]:
        """Build paginated response"""
        total_pages = (total + per_page - 1) // per_page
        
        return {
            "success": True,
            "message": message,
            "data": data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }

# Global instances
url_validator = URLValidator()
data_formatter = DataFormatter()
cache_manager = CacheManager()
response_builder = ResponseBuilder()

# Utility functions
async def cached_operation(cache_key: str, operation_func, *args, **kwargs):
    """Execute operation with caching"""
    # Try to get from cache first
    cached_result = await cache_manager.get(cache_key)
    if cached_result:
        return cached_result['data']
    
    # Execute operation
    result = await operation_func(*args, **kwargs)
    
    # Cache the result
    await cache_manager.set(cache_key, result)
    
    return result

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    return data_formatter.clean_title(filename)

def format_video_info(raw_info: Dict) -> Dict:
    """Format raw video info for API response"""
    return {
        'title': data_formatter.clean_title(raw_info.get('title', '')),
        'duration': data_formatter.format_duration(raw_info.get('duration')),
        'view_count': data_formatter.format_view_count(raw_info.get('view_count')),
        'file_size': data_formatter.format_file_size(raw_info.get('filesize')),
        'thumbnail': data_formatter.extract_thumbnail_url(raw_info.get('thumbnails', []))
    }
