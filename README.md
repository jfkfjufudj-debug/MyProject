# 🎬 Video Extractor Server

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> **Professional Video Extractor Server** - A high-performance API for extracting video information and downloading content from 1000+ platforms using yt-dlp.

## ✨ Features

- 🔍 **Extract** comprehensive video information from 1000+ platforms
- 📥 **Download** videos and audio in multiple qualities (144p to 4K)
- 🎵 **Audio extraction** in various formats (MP3, M4A, WAV)
- 📋 **Playlist support** with batch processing
- 🔐 **Secure** API key authentication system
- 🚀 **High performance** with intelligent caching
- 📊 **Professional logging** and monitoring
- 🌐 **CORS support** for web applications
- 📱 **Mobile-friendly** API designed for Flutter integration

## 🎯 Supported Platforms

YouTube, TikTok, Facebook, Instagram, Twitter, Vimeo, Dailymotion, Twitch, Reddit, SoundCloud, and **1000+ more platforms** supported by yt-dlp.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download** this repository
2. **Navigate** to the project directory
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env file with your preferred settings
   ```

5. **Run the server**:
   ```bash
   python main.py
   ```

The server will start at `http://127.0.0.1:8000`

### 🎉 That's it! Your server is ready to use.

## 📖 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Alternative Docs**: http://127.0.0.1:8000/redoc

## 🔑 Authentication

All API endpoints require authentication using an API key. Include it in one of these ways:

### Method 1: Authorization Header
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     "http://127.0.0.1:8000/api/v1/extract" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### Method 2: Query Parameter
```bash
curl "http://127.0.0.1:8000/api/v1/extract?api_key=YOUR_API_KEY" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### Method 3: Custom Header
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
     "http://127.0.0.1:8000/api/v1/extract" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

**Default API Key**: `default-api-key-change-me` (⚠️ Change this in production!)

## 📋 API Endpoints

### 🔍 Extract Video Information
```http
POST /api/v1/extract
```

Extract comprehensive video information without downloading.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "include_playlist": false,
  "max_playlist_videos": 50
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "title": "Rick Astley - Never Gonna Give You Up",
    "duration": 213,
    "view_count": 1000000000,
    "uploader": "Rick Astley",
    "thumbnail": "https://...",
    "formats": [...],
    "audio_formats": [...],
    "recommended": {...}
  }
}
```

### 📥 Download Video/Audio
```http
POST /api/v1/download
```

Download video or audio file to server.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "quality": "720p",
  "format_type": "video"
}
```

**Quality Options:**
- `144p`, `240p`, `360p`, `480p`, `720p`, `1080p`, `1440p`, `2160p`
- `best`, `worst`

**Format Types:**
- `video` - Video with audio
- `audio` - Audio only

### ✅ Validate URL
```http
POST /api/v1/validate
```

Check if URL is supported and accessible.

### 📊 Download Status
```http
GET /api/v1/status/{download_id}
```

Check download progress and status.

### 🌐 Supported Platforms
```http
GET /api/v1/platforms
```

Get list of supported platforms.

## 🔧 Configuration

### Environment Variables

Create a `.env` file or modify settings in `config/settings.py`:

```env
# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
DEBUG_MODE=false

# Security
API_KEY=your-super-secret-api-key-here
SECRET_KEY=your-jwt-secret-key-here

# File Management
MAX_FILE_SIZE_MB=500
DOWNLOADS_PATH=./downloads
CACHE_ENABLED=true
CACHE_TTL_SECONDS=3600

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=60
MAX_CONCURRENT_DOWNLOADS=5

# Logging
LOG_LEVEL=INFO
LOG_FILE_PATH=./logs/server.log
```

## 📱 Flutter Integration Example

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class VideoExtractorAPI {
  static const String baseUrl = 'http://127.0.0.1:8000/api/v1';
  static const String apiKey = 'your-api-key-here';
  
  static Future<Map<String, dynamic>> extractVideo(String url) async {
    final response = await http.post(
      Uri.parse('$baseUrl/extract'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $apiKey',
      },
      body: jsonEncode({'url': url}),
    );
    
    return jsonDecode(response.body);
  }
  
  static Future<Map<String, dynamic>> downloadVideo(
    String url, 
    String quality
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/download'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $apiKey',
      },
      body: jsonEncode({
        'url': url,
        'quality': quality,
        'format_type': 'video'
      }),
    );
    
    return jsonDecode(response.body);
  }
}
```

## 🏗️ Project Structure

```
video-extractor-server/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── config/
│   ├── __init__.py
│   └── settings.py        # Application configuration
├── core/
│   ├── __init__.py
│   ├── extractor.py       # Video extraction logic
│   └── downloader.py      # Download management
├── api/
│   ├── __init__.py
│   ├── routes.py          # API endpoints
│   └── auth.py            # Authentication & security
├── utils/
│   ├── __init__.py
│   └── helpers.py         # Utility functions
├── downloads/             # Downloaded files storage
└── logs/                  # Application logs
```

## 🔒 Security Features

- **API Key Authentication** - Secure access control
- **Rate Limiting** - Prevent abuse and overload
- **IP Blocking** - Automatic blocking of suspicious IPs
- **Request Validation** - Comprehensive input validation
- **CORS Protection** - Configurable cross-origin policies
- **Security Headers** - Standard security headers included

## 📊 Monitoring & Logging

- **Structured Logging** - JSON formatted logs with rotation
- **Health Check Endpoint** - `/health` for monitoring
- **Performance Metrics** - Request timing and statistics
- **Error Tracking** - Comprehensive error logging
- **Cache Statistics** - Cache performance monitoring

## 🚀 Performance Features

- **Intelligent Caching** - Reduce redundant API calls
- **Async Processing** - Non-blocking request handling
- **Connection Pooling** - Efficient HTTP connections
- **Background Tasks** - Cleanup and maintenance tasks
- **Memory Management** - Automatic cleanup of temporary files

## 🛠️ Development

### Running in Development Mode

```bash
# Enable debug mode
export DEBUG_MODE=true

# Run with auto-reload
python main.py
```

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## ⚠️ Important Notes

- **Production Security**: Change default API keys before production use
- **Rate Limits**: Respect platform rate limits and terms of service
- **Legal Compliance**: Ensure compliance with local laws and platform terms
- **Resource Management**: Monitor disk space for downloads directory
- **Updates**: Keep yt-dlp updated for latest platform support

## 🆘 Support

- **Documentation**: Visit `/docs` endpoint for interactive API documentation
- **Health Check**: Use `/health` endpoint to verify server status
- **Logs**: Check `logs/server.log` for detailed operation logs

---

**Made with ❤️ for professional video processing needs**
