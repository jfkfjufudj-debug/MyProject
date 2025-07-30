"""
Basic test server to identify issues
"""

from fastapi import FastAPI
import uvicorn

# Create simple app
app = FastAPI(title="Test Server")

@app.get("/")
async def root():
    return {"message": "Hello World", "status": "working"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🚀 Starting basic test server...")
    print("📍 Server will be at: http://127.0.0.1:8000")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
