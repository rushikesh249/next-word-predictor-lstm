#!/usr/bin/env python3
"""
Startup script for Next Word Predictor LSTM Project
This script ensures all dependencies are available and starts the backend server
"""

import sys
import subprocess
import os
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'flask-cors', 
        'numpy',
        'tensorflow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n🔧 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def check_files():
    """Check if required files exist"""
    required_files = [
        'server.py',
        'frontend/index.html',
        'frontend/app.js', 
        'frontend/style.css'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            missing_files.append(file)
            print(f"❌ {file} missing")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def start_backend():
    """Start the Flask backend server"""
    print("\n🚀 Starting backend server...")
    
    # Set environment variable for dataset
    os.environ["DATASET_FILE"] = "data/dataset_10000.txt"
    
    try:
        # Import and run server
        import server
        print("✅ Backend server started at http://127.0.0.1:5000")
        return True
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def open_frontend():
    """Open frontend in browser"""
    frontend_path = Path("frontend/index.html").absolute()
    if frontend_path.exists():
        print(f"\n🌐 Opening frontend: {frontend_path}")
        webbrowser.open(f"file://{frontend_path}")
        return True
    else:
        print("❌ Frontend file not found")
        return False

def main():
    """Main startup function"""
    print("=" * 60)
    print("🤖 NEXT WORD PREDICTOR LSTM - PROJECT STARTUP")
    print("=" * 60)
    
    # Check current directory
    print(f"📁 Current directory: {os.getcwd()}")
    
    # Step 1: Check dependencies
    print("\n1️⃣ Checking dependencies...")
    if not check_dependencies():
        print("❌ Dependency check failed. Please install required packages.")
        return
    
    # Step 2: Check files
    print("\n2️⃣ Checking project files...")
    if not check_files():
        print("❌ File check failed. Please ensure all files are present.")
        return
    
    # Step 3: Start backend
    print("\n3️⃣ Starting backend...")
    if start_backend():
        print("✅ Backend is running!")
        
        # Step 4: Open frontend
        print("\n4️⃣ Opening frontend...")
        time.sleep(2)  # Give server time to start
        open_frontend()
        
        print("\n" + "=" * 60)
        print("🎉 PROJECT IS FULLY FUNCTIONAL!")
        print("=" * 60)
        print("📝 Instructions:")
        print("   • Backend API: http://127.0.0.1:5000")
        print("   • Frontend: Opened in your browser")
        print("   • Type text in the input field and click 'Predict'")
        print("   • Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Keep server running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Server stopped. Goodbye!")
    else:
        print("❌ Failed to start backend server.")

if __name__ == "__main__":
    main()
