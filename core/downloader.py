"""
===================================================================
Video Extractor Server - Professional Download Manager
===================================================================
Author: Professional Development Team
Version: 1.0.0
Description: Advanced file download management with progress tracking
"""

import asyncio
import os
import aiofiles
import httpx
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from urllib.parse import urlparse, unquote
import time
import hashlib
from loguru import logger
import yt_dlp

from config.settings import settings, get_downloads_path, get_temp_path, get_max_file_size_bytes

class DownloadManager:
    """
    Professional download manager with progress tracking and error handling
    """
    
    def __init__(self):
        """Initialize download manager"""
        self.downloads_path = get_downloads_path()
        self.temp_path = get_temp_path()
        self.max_file_size = get_max_file_size_bytes()
        self.active_downloads = {}
        self.download_history = {}
        
        # Create necessary directories
        self.downloads_path.mkdir(parents=True, exist_ok=True)
        self.temp_path.mkdir(parents=True, exist_ok=True)
    
    def generate_download_id(self, url: str, quality: str = "default") -> str:
        """Generate unique download ID"""
        unique_string = f"{url}_{quality}_{int(time.time())}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe file system storage"""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit filename length
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:200-len(ext)] + ext
        
        return filename.strip()
    
    async def download_with_yt_dlp(
        self, 
        url: str, 
        quality: str = "720p",
        format_type: str = "video",
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Download video/audio using yt-dlp with progress tracking
        """
        download_id = self.generate_download_id(url, quality)
        
        try:
            logger.info(f"Starting yt-dlp download: {download_id}")
            
            # Prepare download options
            ydl_opts = self._prepare_ydl_options(quality, format_type, download_id, progress_callback)
            
            # Start download in executor
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, self._download_with_ydl_sync, url, ydl_opts, download_id
            )
            
            if result['success']:
                logger.success(f"Download completed: {download_id}")
                # Move from temp to downloads folder
                final_path = await self._finalize_download(result['temp_path'], download_id)
                result['final_path'] = str(final_path)
                result['download_url'] = f"/downloads/{final_path.name}"
            
            return result
            
        except Exception as e:
            logger.error(f"Download failed {download_id}: {str(e)}")
            return {
                'success': False,
                'download_id': download_id,
                'error': f"Download failed: {str(e)}"
            }
    
    def _prepare_ydl_options(
        self, 
        quality: str, 
        format_type: str, 
        download_id: str,
        progress_callback: Optional[Callable]
    ) -> Dict:
        """Prepare yt-dlp options for download"""
        
        # Base options
        ydl_opts = {
            'outtmpl': str(self.temp_path / f'{download_id}_%(title)s.%(ext)s'),
            'restrictfilenames': True,
            'noplaylist': True,
            'ignoreerrors': False,
            'no_warnings': False,
            'extractaudio': format_type == 'audio',
        }
        
        # Format selection based on type and quality
        if format_type == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        elif format_type == 'video':
            # Quality-based format selection
            quality_formats = {
                '144p': 'worst[height<=144]/worst',
                '240p': 'best[height<=240]/best',
                '360p': 'best[height<=360]/best',
                '480p': 'best[height<=480]/best',
                '720p': 'best[height<=720]/best',
                '1080p': 'best[height<=1080]/best',
                '1440p': 'best[height<=1440]/best',
                '2160p': 'best[height<=2160]/best',
                'best': 'best',
                'worst': 'worst'
            }
            ydl_opts['format'] = quality_formats.get(quality, 'best[height<=720]/best')
        
        # Add progress hook if callback provided
        if progress_callback:
            ydl_opts['progress_hooks'] = [
                lambda d: self._progress_hook(d, download_id, progress_callback)
            ]
        
        return ydl_opts
    
    def _download_with_ydl_sync(self, url: str, ydl_opts: Dict, download_id: str) -> Dict:
        """Synchronous download with yt-dlp"""
        try:
            self.active_downloads[download_id] = {
                'status': 'downloading',
                'progress': 0,
                'start_time': time.time()
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                if not info:
                    return {
                        'success': False,
                        'error': 'Failed to extract video information'
                    }
                
                # Find the downloaded file
                temp_files = list(self.temp_path.glob(f'{download_id}_*'))
                if not temp_files:
                    return {
                        'success': False,
                        'error': 'Downloaded file not found'
                    }
                
                temp_path = temp_files[0]
                
                return {
                    'success': True,
                    'download_id': download_id,
                    'temp_path': str(temp_path),
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'filesize': temp_path.stat().st_size if temp_path.exists() else 0
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            # Clean up active downloads tracking
            if download_id in self.active_downloads:
                del self.active_downloads[download_id]
    
    def _progress_hook(self, d: Dict, download_id: str, callback: Callable):
        """Progress hook for yt-dlp downloads"""
        try:
            if d['status'] == 'downloading':
                progress_info = {
                    'download_id': download_id,
                    'status': 'downloading',
                    'downloaded_bytes': d.get('downloaded_bytes', 0),
                    'total_bytes': d.get('total_bytes') or d.get('total_bytes_estimate', 0),
                    'speed': d.get('speed', 0),
                    'eta': d.get('eta', 0),
                    'progress_percent': 0
                }
                
                if progress_info['total_bytes'] > 0:
                    progress_info['progress_percent'] = (
                        progress_info['downloaded_bytes'] / progress_info['total_bytes']
                    ) * 100
                
                # Update active downloads
                if download_id in self.active_downloads:
                    self.active_downloads[download_id].update({
                        'progress': progress_info['progress_percent'],
                        'speed': progress_info['speed'],
                        'eta': progress_info['eta']
                    })
                
                # Call the callback
                callback(progress_info)
                
            elif d['status'] == 'finished':
                finish_info = {
                    'download_id': download_id,
                    'status': 'finished',
                    'filename': d.get('filename', ''),
                    'total_bytes': d.get('total_bytes', 0)
                }
                callback(finish_info)
                
        except Exception as e:
            logger.error(f"Progress hook error: {str(e)}")
    
    async def _finalize_download(self, temp_path: str, download_id: str) -> Path:
        """Move downloaded file from temp to final location"""
        try:
            temp_file = Path(temp_path)
            if not temp_file.exists():
                raise FileNotFoundError(f"Temporary file not found: {temp_path}")
            
            # Generate final filename
            final_filename = self.sanitize_filename(temp_file.name.replace(f'{download_id}_', ''))
            final_path = self.downloads_path / final_filename
            
            # Handle filename conflicts
            counter = 1
            original_final_path = final_path
            while final_path.exists():
                name, ext = os.path.splitext(original_final_path.name)
                final_path = self.downloads_path / f"{name}_{counter}{ext}"
                counter += 1
            
            # Move file
            temp_file.rename(final_path)
            
            logger.info(f"File moved to final location: {final_path}")
            return final_path
            
        except Exception as e:
            logger.error(f"Error finalizing download: {str(e)}")
            raise
    
    async def download_direct_url(
        self, 
        url: str, 
        filename: Optional[str] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Download file directly from URL (for direct video links)
        """
        download_id = self.generate_download_id(url)
        
        try:
            logger.info(f"Starting direct download: {download_id}")
            
            # Generate filename if not provided
            if not filename:
                parsed_url = urlparse(url)
                filename = unquote(os.path.basename(parsed_url.path)) or f"download_{download_id}"
            
            filename = self.sanitize_filename(filename)
            temp_path = self.temp_path / f"{download_id}_{filename}"
            
            # Download with progress tracking using httpx
            async with httpx.AsyncClient() as client:
                async with client.stream('GET', url) as response:
                    if response.status_code != 200:
                        return {
                            'success': False,
                            'download_id': download_id,
                            'error': f"HTTP {response.status_code}: {response.reason_phrase}"
                        }

                    total_size = int(response.headers.get('content-length', 0))

                    if total_size > self.max_file_size:
                        return {
                            'success': False,
                            'download_id': download_id,
                            'error': f"File too large: {total_size} bytes (max: {self.max_file_size})"
                        }

                    downloaded = 0

                    async with aiofiles.open(temp_path, 'wb') as file:
                        async for chunk in response.aiter_bytes(8192):
                            await file.write(chunk)
                            downloaded += len(chunk)

                            # Progress callback
                            if progress_callback and total_size > 0:
                                progress = (downloaded / total_size) * 100
                                progress_callback({
                                    'download_id': download_id,
                                    'status': 'downloading',
                                    'downloaded_bytes': downloaded,
                                    'total_bytes': total_size,
                                    'progress_percent': progress
                                })
            
            # Finalize download
            final_path = await self._finalize_download(str(temp_path), download_id)
            
            logger.success(f"Direct download completed: {download_id}")
            return {
                'success': True,
                'download_id': download_id,
                'final_path': str(final_path),
                'filename': final_path.name,
                'filesize': final_path.stat().st_size,
                'download_url': f"/downloads/{final_path.name}"
            }
            
        except Exception as e:
            logger.error(f"Direct download failed {download_id}: {str(e)}")
            return {
                'success': False,
                'download_id': download_id,
                'error': f"Download failed: {str(e)}"
            }
    
    def get_download_status(self, download_id: str) -> Dict[str, Any]:
        """Get current download status"""
        if download_id in self.active_downloads:
            return {
                'active': True,
                **self.active_downloads[download_id]
            }
        elif download_id in self.download_history:
            return {
                'active': False,
                **self.download_history[download_id]
            }
        else:
            return {
                'active': False,
                'status': 'not_found',
                'error': 'Download ID not found'
            }
    
    def cleanup_temp_files(self, max_age_hours: int = 24):
        """Clean up old temporary files"""
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for temp_file in self.temp_path.glob('*'):
                if temp_file.is_file():
                    file_age = current_time - temp_file.stat().st_mtime
                    if file_age > max_age_seconds:
                        temp_file.unlink()
                        logger.info(f"Cleaned up old temp file: {temp_file.name}")
                        
        except Exception as e:
            logger.error(f"Error cleaning temp files: {str(e)}")

# Global download manager instance
download_manager = DownloadManager()
