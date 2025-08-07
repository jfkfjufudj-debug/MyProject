@echo off
echo 🚀 Deploying Video Extractor Server to GitHub...
echo.

echo 📁 Adding all files...
git add .

echo 💾 Committing changes...
git commit -m "Fix Render deployment - Complete server with main.py entry point"

echo 🌐 Pushing to GitHub...
git push origin main

echo.
echo ✅ Deployment complete! Render will auto-deploy from GitHub.
echo 🔗 Check your Render dashboard for deployment status.
pause
