#!/usr/bin/env python3
"""
Project Setup Verification Script
Verifies that the GitHub-ready project structure is properly organized
"""

import os
import sys
from pathlib import Path

def check_directory_structure():
    """Verify the expected directory structure exists"""
    expected_structure = {
        'directories': [
            'frontend',
            'cpp', 
            'data',
            'scripts',
            'docs',
            'assets'
        ],
        'files': [
            'README.md',
            'LICENSE',
            'requirements.txt',
            'server.py',
            '.gitignore'
        ]
    }
    
    print("🔍 Checking directory structure...")
    
    # Check directories
    missing_dirs = []
    for directory in expected_structure['directories']:
        if os.path.exists(directory):
            print(f"✅ Directory: {directory}")
        else:
            print(f"❌ Missing directory: {directory}")
            missing_dirs.append(directory)
    
    # Check files
    missing_files = []
    for file in expected_structure['files']:
        if os.path.exists(file):
            print(f"✅ File: {file}")
        else:
            print(f"❌ Missing file: {file}")
            missing_files.append(file)
    
    return len(missing_dirs) == 0 and len(missing_files) == 0

def check_frontend_files():
    """Check frontend directory contents"""
    print("\n🌐 Checking frontend files...")
    
    frontend_files = ['index.html', 'app.js', 'style.css']
    all_exist = True
    
    for file in frontend_files:
        path = f"frontend/{file}"
        if os.path.exists(path):
            print(f"✅ Frontend: {file}")
        else:
            print(f"❌ Missing frontend file: {file}")
            all_exist = False
    
    return all_exist

def check_cpp_files():
    """Check C++ directory contents"""
    print("\n⚡ Checking C++ files...")
    
    cpp_files = ['main.cpp', 'openmp.cpp', 'timing.cpp', 'README.md']
    all_exist = True
    
    for file in cpp_files:
        path = f"cpp/{file}"
        if os.path.exists(path):
            print(f"✅ C++: {file}")
        else:
            print(f"❌ Missing C++ file: {file}")
            all_exist = False
    
    return all_exist

def check_data_files():
    """Check data directory contents"""
    print("\n📊 Checking data files...")
    
    data_files = [
        'dataset_500.txt',
        'dataset_1000.txt', 
        'dataset_8000.txt',
        'dataset_10000.txt',
        'README.md'
    ]
    all_exist = True
    
    for file in data_files:
        path = f"data/{file}"
        if os.path.exists(path):
            print(f"✅ Data: {file}")
        else:
            print(f"❌ Missing data file: {file}")
            all_exist = False
    
    return all_exist

def check_scripts_files():
    """Check scripts directory contents"""
    print("\n🔧 Checking script files...")
    
    script_files = [
        'start_project.py',
        'test_integration.py',
        'graph.py',
        'verify_setup.py',
        'README.md'
    ]
    all_exist = True
    
    for file in script_files:
        path = f"scripts/{file}"
        if os.path.exists(path):
            print(f"✅ Script: {file}")
        else:
            print(f"❌ Missing script file: {file}")
            all_exist = False
    
    return all_exist

def check_docs_files():
    """Check documentation directory contents"""
    print("\n📚 Checking documentation files...")
    
    doc_files = [
        'README.md',
        'API.md',
        'ARCHITECTURE.md',
        'PPT_Content.txt',
        'README_INTEGRATION.md'
    ]
    all_exist = True
    
    for file in doc_files:
        path = f"docs/{file}"
        if os.path.exists(path):
            print(f"✅ Docs: {file}")
        else:
            print(f"❌ Missing doc file: {file}")
            all_exist = False
    
    return all_exist

def check_gitignore():
    """Check .gitignore content"""
    print("\n🚫 Checking .gitignore...")
    
    if not os.path.exists('.gitignore'):
        print("❌ .gitignore file missing")
        return False
    
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    required_patterns = [
        '__pycache__/',
        '*.pyc',
        '.venv/',
        '*.exe',
        '*.pkl',
        '*.h5'
    ]
    
    missing_patterns = []
    for pattern in required_patterns:
        if pattern in content:
            print(f"✅ .gitignore includes: {pattern}")
        else:
            print(f"❌ .gitignore missing: {pattern}")
            missing_patterns.append(pattern)
    
    return len(missing_patterns) == 0

def check_readme_quality():
    """Check README.md quality"""
    print("\n📖 Checking README.md quality...")
    
    if not os.path.exists('README.md'):
        print("❌ README.md missing")
        return False
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    quality_checks = [
        ('Title with emoji', '# 🤖'),
        ('Badges', '!['),
        ('Features section', '## 🌟 Features'),
        ('Quick Start', '## 🚀 Quick Start'),
        ('Project Structure', '## 📁 Project Structure'),
        ('API Documentation', '## 📖 API Documentation'),
        ('Performance Results', '## ⚡ Performance Results')
    ]
    
    all_good = True
    for check_name, pattern in quality_checks:
        if pattern in content:
            print(f"✅ README has: {check_name}")
        else:
            print(f"❌ README missing: {check_name}")
            all_good = False
    
    return all_good

def main():
    """Main verification function"""
    print("=" * 60)
    print("🔍 GITHUB PROJECT STRUCTURE VERIFICATION")
    print("=" * 60)
    
    # Change to project root if needed
    if not os.path.exists('README.md'):
        print("❌ Not in project root directory")
        return False
    
    checks = [
        ("Directory Structure", check_directory_structure),
        ("Frontend Files", check_frontend_files),
        ("C++ Files", check_cpp_files),
        ("Data Files", check_data_files),
        ("Script Files", check_scripts_files),
        ("Documentation Files", check_docs_files),
        (".gitignore Configuration", check_gitignore),
        ("README Quality", check_readme_quality)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error in {check_name}: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED! Project is GitHub-ready!")
        print("\n✅ Your project structure is professional and well-organized")
        print("✅ All required files are present")
        print("✅ Documentation is comprehensive")
        print("✅ .gitignore is properly configured")
        print("\n🚀 Ready to upload to GitHub!")
        return True
    else:
        print(f"❌ {total - passed} checks failed out of {total}")
        print("\n🔧 Please fix the issues above before uploading to GitHub")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
