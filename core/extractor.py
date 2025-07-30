"""
===================================================================
Video Extractor Server - Professional Video Extraction Core
===================================================================
Author: Professional Development Team
Version: 1.0.0
Description: Advanced video information extraction using yt-dlp
"""

import asyncio
import json
import re
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urlparse
import yt_dlp
from loguru import logger
from config.settings import settings

class VideoExtractor:
    """
    Professional video extractor with support for 1000+ platforms
    """
    
    def __init__(self):
        """Initialize the video extractor with optimized settings"""
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extractaudio': False,
            'format': 'best',
            'noplaylist': True,
            'extract_flat': False,
            'writethumbnail': False,
            'writeinfojson': False,
            'ignoreerrors': True,
            'no_check_certificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        # Supported quality options
        self.quality_formats = {
            '144p': 'worst[height<=144]',
            '240p': 'worst[height<=240]',
            '360p': 'best[height<=360]',
            '480p': 'best[height<=480]',
            '720p': 'best[height<=720]',
            '1080p': 'best[height<=1080]',
            '1440p': 'best[height<=1440]',
            '2160p': 'best[height<=2160]',
            'best': 'best',
            'worst': 'worst'
        }
    
    def is_valid_url(self, url: str) -> bool:
        """
        Validate if the provided URL is valid
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def get_supported_platforms(self) -> List[str]:
        """
        Get list of supported platforms
        """
        return settings.SUPPORTED_PLATFORMS
    
    async def extract_video_info(self, url: str) -> Dict[str, Any]:
        """
        Extract comprehensive video information from URL
        """
        if not self.is_valid_url(url):
            raise ValueError("Invalid URL provided")
        
        try:
            logger.info(f"Extracting video info from: {url}")
            
            # Run yt-dlp in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(
                None, self._extract_info_sync, url
            )
            
            if not info:
                raise ValueError("Could not extract video information")
            
            # Process and format the extracted information
            processed_info = self._process_video_info(info)
            
            logger.success(f"Successfully extracted info for: {processed_info.get('title', 'Unknown')}")
            return processed_info
            
        except Exception as e:
            logger.error(f"Error extracting video info: {str(e)}")
            raise Exception(f"Failed to extract video information: {str(e)}")
    
    def _extract_info_sync(self, url: str) -> Optional[Dict]:
        """
        Synchronous video info extraction
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            logger.error(f"yt-dlp extraction error: {str(e)}")
            return None
    
    def _process_video_info(self, raw_info: Dict) -> Dict[str, Any]:
        """
        Process and format raw video information
        """
        try:
            # Extract basic information
            video_info = {
                'success': True,
                'title': raw_info.get('title', 'Unknown Title'),
                'description': raw_info.get('description', ''),
                'duration': raw_info.get('duration', 0),
                'view_count': raw_info.get('view_count', 0),
                'like_count': raw_info.get('like_count', 0),
                'upload_date': raw_info.get('upload_date', ''),
                'uploader': raw_info.get('uploader', 'Unknown'),
                'uploader_id': raw_info.get('uploader_id', ''),
                'channel_url': raw_info.get('channel_url', ''),
                'thumbnail': raw_info.get('thumbnail', ''),
                'webpage_url': raw_info.get('webpage_url', ''),
                'platform': raw_info.get('extractor', 'unknown'),
            }
            
            # Extract available formats
            formats = raw_info.get('formats', [])
            video_info['formats'] = self._process_formats(formats)
            
            # Extract audio-only formats
            video_info['audio_formats'] = self._extract_audio_formats(formats)
            
            # Extract video-only formats
            video_info['video_only_formats'] = self._extract_video_only_formats(formats)
            
            # Get best quality recommendations
            video_info['recommended'] = self._get_recommended_formats(formats)
            
            return video_info
            
        except Exception as e:
            logger.error(f"Error processing video info: {str(e)}")
            return {
                'success': False,
                'error': f"Failed to process video information: {str(e)}"
            }
    
    def _process_formats(self, formats: List[Dict]) -> List[Dict]:
        """
        Process and organize video formats
        """
        processed_formats = []
        
        for fmt in formats:
            if not fmt.get('url'):
                continue
                
            format_info = {
                'format_id': fmt.get('format_id', ''),
                'url': fmt.get('url', ''),
                'ext': fmt.get('ext', 'mp4'),
                'quality': fmt.get('format_note', 'unknown'),
                'height': fmt.get('height'),
                'width': fmt.get('width'),
                'fps': fmt.get('fps'),
                'vcodec': fmt.get('vcodec', 'none'),
                'acodec': fmt.get('acodec', 'none'),
                'filesize': fmt.get('filesize'),
                'tbr': fmt.get('tbr'),  # Total bitrate
                'vbr': fmt.get('vbr'),  # Video bitrate
                'abr': fmt.get('abr'),  # Audio bitrate
                'protocol': fmt.get('protocol', 'https'),
                'has_video': fmt.get('vcodec', 'none') != 'none',
                'has_audio': fmt.get('acodec', 'none') != 'none',
            }
            
            # Determine format type
            if format_info['has_video'] and format_info['has_audio']:
                format_info['type'] = 'video+audio'
            elif format_info['has_video']:
                format_info['type'] = 'video-only'
            elif format_info['has_audio']:
                format_info['type'] = 'audio-only'
            else:
                format_info['type'] = 'unknown'
            
            processed_formats.append(format_info)
        
        # Sort by quality (height) descending
        processed_formats.sort(
            key=lambda x: (x.get('height') or 0, x.get('tbr') or 0), 
            reverse=True
        )
        
        return processed_formats
    
    def _extract_audio_formats(self, formats: List[Dict]) -> List[Dict]:
        """
        Extract audio-only formats
        """
        audio_formats = []
        
        for fmt in formats:
            if (fmt.get('acodec', 'none') != 'none' and 
                fmt.get('vcodec', 'none') == 'none' and 
                fmt.get('url')):
                
                audio_info = {
                    'format_id': fmt.get('format_id', ''),
                    'url': fmt.get('url', ''),
                    'ext': fmt.get('ext', 'mp3'),
                    'acodec': fmt.get('acodec', 'mp3'),
                    'abr': fmt.get('abr', 128),
                    'filesize': fmt.get('filesize'),
                    'quality': f"{fmt.get('abr', 128)}kbps" if fmt.get('abr') else 'unknown'
                }
                audio_formats.append(audio_info)
        
        # Sort by bitrate descending
        audio_formats.sort(key=lambda x: x.get('abr', 0), reverse=True)
        return audio_formats
    
    def _extract_video_only_formats(self, formats: List[Dict]) -> List[Dict]:
        """
        Extract video-only formats (no audio)
        """
        video_only_formats = []
        
        for fmt in formats:
            if (fmt.get('vcodec', 'none') != 'none' and 
                fmt.get('acodec', 'none') == 'none' and 
                fmt.get('url')):
                
                video_info = {
                    'format_id': fmt.get('format_id', ''),
                    'url': fmt.get('url', ''),
                    'ext': fmt.get('ext', 'mp4'),
                    'height': fmt.get('height'),
                    'width': fmt.get('width'),
                    'fps': fmt.get('fps'),
                    'vcodec': fmt.get('vcodec'),
                    'vbr': fmt.get('vbr'),
                    'filesize': fmt.get('filesize'),
                    'quality': f"{fmt.get('height', 'unknown')}p" if fmt.get('height') else 'unknown'
                }
                video_only_formats.append(video_info)
        
        # Sort by height descending
        video_only_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
        return video_only_formats
    
    def _get_recommended_formats(self, formats: List[Dict]) -> Dict[str, Any]:
        """
        Get recommended formats for different use cases
        """
        recommendations = {
            'best_quality': None,
            'best_audio': None,
            'mobile_friendly': None,
            'fast_streaming': None
        }
        
        # Find best overall quality (video + audio)
        best_combined = None
        best_height = 0
        
        for fmt in formats:
            if (fmt.get('vcodec', 'none') != 'none' and 
                fmt.get('acodec', 'none') != 'none' and
                fmt.get('height', 0) > best_height):
                best_height = fmt.get('height', 0)
                best_combined = fmt
        
        if best_combined:
            recommendations['best_quality'] = {
                'format_id': best_combined.get('format_id'),
                'url': best_combined.get('url'),
                'quality': f"{best_combined.get('height', 'unknown')}p",
                'ext': best_combined.get('ext', 'mp4')
            }
        
        # Find best audio
        best_audio = None
        best_abr = 0
        
        for fmt in formats:
            if (fmt.get('acodec', 'none') != 'none' and 
                fmt.get('vcodec', 'none') == 'none' and
                fmt.get('abr', 0) > best_abr):
                best_abr = fmt.get('abr', 0)
                best_audio = fmt
        
        if best_audio:
            recommendations['best_audio'] = {
                'format_id': best_audio.get('format_id'),
                'url': best_audio.get('url'),
                'quality': f"{best_audio.get('abr', 'unknown')}kbps",
                'ext': best_audio.get('ext', 'mp3')
            }
        
        # Mobile friendly (720p or lower)
        for fmt in formats:
            if (fmt.get('vcodec', 'none') != 'none' and 
                fmt.get('acodec', 'none') != 'none' and
                fmt.get('height', 0) <= 720 and
                fmt.get('height', 0) > 0):
                recommendations['mobile_friendly'] = {
                    'format_id': fmt.get('format_id'),
                    'url': fmt.get('url'),
                    'quality': f"{fmt.get('height')}p",
                    'ext': fmt.get('ext', 'mp4')
                }
                break
        
        # Fast streaming (360p)
        for fmt in formats:
            if (fmt.get('vcodec', 'none') != 'none' and 
                fmt.get('acodec', 'none') != 'none' and
                fmt.get('height', 0) <= 360 and
                fmt.get('height', 0) > 0):
                recommendations['fast_streaming'] = {
                    'format_id': fmt.get('format_id'),
                    'url': fmt.get('url'),
                    'quality': f"{fmt.get('height')}p",
                    'ext': fmt.get('ext', 'mp4')
                }
                break
        
        return recommendations

    async def get_format_by_quality(self, url: str, quality: str = "720p") -> Optional[Dict]:
        """
        Get specific format by quality preference
        """
        try:
            info = await self.extract_video_info(url)
            if not info.get('success'):
                return None

            formats = info.get('formats', [])

            # Try to find exact quality match
            for fmt in formats:
                if (fmt.get('has_video') and fmt.get('has_audio') and
                    fmt.get('height') and f"{fmt['height']}p" == quality):
                    return fmt

            # If no exact match, find closest quality
            target_height = int(quality.replace('p', '')) if quality.replace('p', '').isdigit() else 720

            best_match = None
            min_diff = float('inf')

            for fmt in formats:
                if fmt.get('has_video') and fmt.get('has_audio') and fmt.get('height'):
                    diff = abs(fmt['height'] - target_height)
                    if diff < min_diff:
                        min_diff = diff
                        best_match = fmt

            return best_match

        except Exception as e:
            logger.error(f"Error getting format by quality: {str(e)}")
            return None

    async def extract_playlist_info(self, url: str, max_videos: int = 50) -> Dict[str, Any]:
        """
        Extract playlist information (if URL is a playlist)
        """
        try:
            logger.info(f"Checking if URL is playlist: {url}")

            # Modify options for playlist extraction
            playlist_opts = self.ydl_opts.copy()
            playlist_opts.update({
                'extract_flat': True,
                'playlistend': max_videos
            })

            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(
                None, self._extract_playlist_sync, url, playlist_opts
            )

            if not info:
                return {'success': False, 'error': 'Could not extract playlist information'}

            # Check if it's actually a playlist
            if 'entries' not in info:
                return {'success': False, 'error': 'URL is not a playlist'}

            playlist_info = {
                'success': True,
                'title': info.get('title', 'Unknown Playlist'),
                'description': info.get('description', ''),
                'uploader': info.get('uploader', 'Unknown'),
                'video_count': len(info.get('entries', [])),
                'videos': []
            }

            # Process each video in playlist
            for entry in info.get('entries', [])[:max_videos]:
                if entry:
                    video_info = {
                        'title': entry.get('title', 'Unknown'),
                        'url': entry.get('url', ''),
                        'id': entry.get('id', ''),
                        'duration': entry.get('duration', 0),
                        'thumbnail': entry.get('thumbnail', ''),
                    }
                    playlist_info['videos'].append(video_info)

            logger.success(f"Successfully extracted playlist with {len(playlist_info['videos'])} videos")
            return playlist_info

        except Exception as e:
            logger.error(f"Error extracting playlist info: {str(e)}")
            return {'success': False, 'error': f'Failed to extract playlist: {str(e)}'}

    def _extract_playlist_sync(self, url: str, opts: Dict) -> Optional[Dict]:
        """
        Synchronous playlist extraction
        """
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            logger.error(f"yt-dlp playlist extraction error: {str(e)}")
            return None

    def get_platform_from_url(self, url: str) -> str:
        """
        Detect platform from URL
        """
        url_lower = url.lower()

        platform_patterns = {
            'youtube': ['youtube.com', 'youtu.be'],
            'tiktok': ['tiktok.com'],
            'facebook': ['facebook.com', 'fb.com'],
            'instagram': ['instagram.com'],
            'twitter': ['twitter.com', 'x.com'],
            'vimeo': ['vimeo.com'],
            'dailymotion': ['dailymotion.com'],
            'twitch': ['twitch.tv'],
            'reddit': ['reddit.com'],
            'soundcloud': ['soundcloud.com']
        }

        for platform, patterns in platform_patterns.items():
            if any(pattern in url_lower for pattern in patterns):
                return platform

        return 'unknown'

    async def validate_url_accessibility(self, url: str) -> Dict[str, Any]:
        """
        Validate if URL is accessible and extractable
        """
        try:
            logger.info(f"Validating URL accessibility: {url}")

            # Basic URL validation
            if not self.is_valid_url(url):
                return {
                    'valid': False,
                    'error': 'Invalid URL format',
                    'platform': 'unknown'
                }

            # Detect platform
            platform = self.get_platform_from_url(url)

            # Try to extract basic info without downloading
            loop = asyncio.get_event_loop()
            test_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'skip_download': True,
                'ignoreerrors': True
            }

            info = await loop.run_in_executor(
                None, self._test_url_sync, url, test_opts
            )

            if info and (info.get('title') or info.get('entries')):
                return {
                    'valid': True,
                    'platform': platform,
                    'title': info.get('title', 'Unknown'),
                    'is_playlist': 'entries' in info,
                    'video_count': len(info.get('entries', [])) if 'entries' in info else 1
                }
            else:
                return {
                    'valid': False,
                    'error': 'URL not accessible or not supported',
                    'platform': platform
                }

        except Exception as e:
            logger.error(f"Error validating URL: {str(e)}")
            return {
                'valid': False,
                'error': f'Validation failed: {str(e)}',
                'platform': self.get_platform_from_url(url)
            }

    def _test_url_sync(self, url: str, opts: Dict) -> Optional[Dict]:
        """
        Synchronous URL testing
        """
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception:
            return None

# Global extractor instance
video_extractor = VideoExtractor()
