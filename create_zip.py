#!/usr/bin/env python3
"""
Create ZIP file for deployment
"""

import zipfile
import os
from datetime import datetime

def create_deployment_zip():
    """Create ZIP file with all necessary files for deployment"""
    
    # Files to include in ZIP
    files_to_include = [
        'server_final.py',
        'requirements.txt',
        'Procfile',
        'railway.json',
        'runtime.txt',
        'README.md',
        '.gitignore'
    ]
    
    # Create ZIP file
    zip_filename = f'video-extractor-server-{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file)
                print(f"✅ Added: {file}")
            else:
                print(f"⚠️ Missing: {file}")
    
    print(f"\n🎉 ZIP file created: {zip_filename}")
    print(f"📁 Size: {os.path.getsize(zip_filename) / 1024:.2f} KB")
    print("\n🚀 You can now upload this ZIP to Railway or any hosting platform!")

if __name__ == "__main__":
    create_deployment_zip()
