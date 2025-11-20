#!/usr/bin/env python3
"""
Integration Test for Next Word Predictor LSTM
Tests the backend API and verifies frontend compatibility
"""

import requests
import json
import time
import webbrowser
import os
from pathlib import Path

def test_backend_health():
    """Test if backend health endpoint is working"""
    try:
        response = requests.get('http://127.0.0.1:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check: PASSED")
            return True
        else:
            print(f"❌ Backend health check: FAILED (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend health check: FAILED (Error: {e})")
        return False

def test_prediction_api():
    """Test the prediction endpoint"""
    test_data = {
        "text": "the quick brown",
        "num_words": 3
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:5000/predict',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Prediction API: PASSED")
            print(f"   Input: '{test_data['text']}'")
            print(f"   Completion: '{data.get('completion', 'No completion')}'")
            print(f"   Words: {data.get('words', [])}")
            return True
        else:
            print(f"❌ Prediction API: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Prediction API: FAILED (Error: {e})")
        return False

def check_frontend_files():
    """Check if frontend files exist and are properly structured"""
    required_files = [
        'frontend/index.html',
        'frontend/app.js',
        'frontend/style.css'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}: EXISTS")
        else:
            print(f"❌ {file}: MISSING")
            all_exist = False
    
    return all_exist

def open_frontend():
    """Open frontend in browser"""
    frontend_path = Path("frontend/index.html").absolute()
    if frontend_path.exists():
        print(f"🌐 Opening frontend: {frontend_path}")
        webbrowser.open(f"file://{frontend_path}")
        return True
    else:
        print("❌ Frontend file not found")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 NEXT WORD PREDICTOR LSTM - INTEGRATION TEST")
    print("=" * 60)
    
    # Test 1: Check frontend files
    print("\n1️⃣ Checking frontend files...")
    frontend_ok = check_frontend_files()
    
    # Test 2: Check backend health
    print("\n2️⃣ Testing backend health...")
    health_ok = test_backend_health()
    
    # Test 3: Test prediction API
    print("\n3️⃣ Testing prediction API...")
    if health_ok:
        prediction_ok = test_prediction_api()
    else:
        print("⏭️ Skipping prediction test (backend not available)")
        prediction_ok = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 INTEGRATION TEST RESULTS")
    print("=" * 60)
    
    if frontend_ok and health_ok and prediction_ok:
        print("🎉 ALL TESTS PASSED! Project is fully integrated.")
        print("\n📝 Next steps:")
        print("   1. Frontend files are ready")
        print("   2. Backend API is working")
        print("   3. LSTM predictions are functional")
        print("   4. Opening frontend in browser...")
        
        # Open frontend
        time.sleep(1)
        open_frontend()
        
        print("\n✨ Your Next Word Predictor LSTM is ready for demonstration!")
        
    else:
        print("❌ SOME TESTS FAILED. Please check the issues above.")
        print("\n🔧 Troubleshooting:")
        if not frontend_ok:
            print("   • Ensure frontend files are in the correct location")
        if not health_ok:
            print("   • Start the backend server: python server.py")
        if not prediction_ok:
            print("   • Check if model.h5 and tokenizer.pkl exist")
            print("   • Verify dataset file is available")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
