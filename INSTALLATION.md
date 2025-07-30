# 🚀 Installation Guide - Video Extractor Server

## 📋 Prerequisites

### 1. Python Installation

**Windows:**
1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify installation: Open Command Prompt and run `python --version`

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python3

# Or download from python.org
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install python3 python3-pip
```

### 2. Verify Python Installation

Open terminal/command prompt and run:
```bash
python --version
# or
python3 --version
```

You should see Python 3.8 or higher.

## 🛠️ Installation Steps

### Method 1: Automatic Installation (Recommended)

**Windows:**
1. Double-click `start_server.bat`
2. The script will automatically install dependencies and start the server

**Linux/macOS:**
1. Make the script executable: `chmod +x start_server.sh`
2. Run: `./start_server.sh`

### Method 2: Manual Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   # or
   python -m pip install -r requirements.txt
   ```

2. **Configure Environment (Optional):**
   ```bash
   cp .env.example .env
   # Edit .env file with your preferred settings
   ```

3. **Start the Server:**
   ```bash
   python main.py
   ```

## 🧪 Testing Installation

### Quick Test (No Dependencies Required)
```bash
python quick_test.py
```

### Full Test Suite (After Installing Dependencies)
```bash
python test_server.py
```

## 🔧 Configuration

### Environment Variables

Edit `.env` file or set environment variables:

```env
# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
DEBUG_MODE=true

# Security (CHANGE THESE IN PRODUCTION!)
API_KEY=your-super-secret-api-key-here
SECRET_KEY=your-jwt-secret-key-here

# File Management
MAX_FILE_SIZE_MB=500
DOWNLOADS_PATH=./downloads
CACHE_ENABLED=true

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=60
```

### Important Security Notes

⚠️ **CHANGE DEFAULT KEYS IN PRODUCTION!**

The default API key is: `default-api-key-change-me`

## 🚀 Starting the Server

### Option 1: Using Startup Scripts
- **Windows**: Double-click `start_server.bat`
- **Linux/macOS**: Run `./start_server.sh`

### Option 2: Direct Python Command
```bash
python main.py
```

### Option 3: Using uvicorn directly
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## 📍 Accessing the Server

Once started, the server will be available at:

- **Main API**: http://127.0.0.1:8000
- **Interactive Docs**: http://127.0.0.1:8000/docs
- **Alternative Docs**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

## 🔍 Troubleshooting

### Python Not Found
- **Windows**: Reinstall Python and check "Add Python to PATH"
- **Linux/macOS**: Install Python using package manager
- Try `python3` instead of `python`

### Permission Errors
- **Windows**: Run Command Prompt as Administrator
- **Linux/macOS**: Use `sudo` for installation commands

### Port Already in Use
- Change `SERVER_PORT` in `.env` file
- Or kill the process using the port:
  ```bash
  # Windows
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  
  # Linux/macOS
  lsof -ti:8000 | xargs kill -9
  ```

### Dependencies Installation Failed
- Update pip: `python -m pip install --upgrade pip`
- Use virtual environment:
  ```bash
  python -m venv venv
  # Windows
  venv\Scripts\activate
  # Linux/macOS
  source venv/bin/activate
  pip install -r requirements.txt
  ```

### FFmpeg Not Found (for some video processing)
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## 🐳 Docker Installation (Alternative)

If you prefer Docker:

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   EXPOSE 8000
   
   CMD ["python", "main.py"]
   ```

2. **Build and Run:**
   ```bash
   docker build -t video-extractor .
   docker run -p 8000:8000 video-extractor
   ```

## 📱 Testing with Flutter

Once the server is running, test the API:

```dart
import 'package:http/http.dart' as http;

final response = await http.post(
  Uri.parse('http://127.0.0.1:8000/api/v1/extract'),
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer default-api-key-change-me',
  },
  body: '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}',
);
```

## 🆘 Getting Help

1. **Check Logs**: Look in `logs/server.log`
2. **Health Check**: Visit http://127.0.0.1:8000/health
3. **API Docs**: Visit http://127.0.0.1:8000/docs
4. **Run Tests**: `python test_server.py`

## 📊 Performance Tips

1. **Enable Caching**: Set `CACHE_ENABLED=true` in `.env`
2. **Adjust Rate Limits**: Modify `MAX_REQUESTS_PER_MINUTE`
3. **Monitor Logs**: Check `logs/server.log` for performance issues
4. **Clean Downloads**: Regularly clean `downloads/` folder

---

**🎉 Congratulations! Your Video Extractor Server is ready to use!**
