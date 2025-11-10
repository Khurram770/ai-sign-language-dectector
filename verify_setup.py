"""
Setup Verification Script
Verifies that all dependencies are installed correctly.
"""

import sys

def check_imports():
    """Check if all required packages are installed."""
    required_packages = {
        'cv2': 'opencv-python',
        'mediapipe': 'mediapipe',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'json': 'json (built-in)',
        'pickle': 'pickle (built-in)',
    }
    
    missing_packages = []
    
    print("Checking dependencies...")
    print("=" * 50)
    
    for package, install_name in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {install_name}")
        except ImportError:
            print(f"✗ {install_name} - NOT INSTALLED")
            missing_packages.append(install_name)
    
    print("=" * 50)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them using: pip install -r requirements.txt")
        return False
    else:
        print("\nAll dependencies are installed!")
        return True

def check_files():
    """Check if all required files exist."""
    import os
    
    required_files = [
        'detector.py',
        'recognizer.py',
        'text_converter.py',
        'main.py',
        'sign_dictionary.json',
        'requirements.txt'
    ]
    
    print("\nChecking project files...")
    print("=" * 50)
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - NOT FOUND")
            missing_files.append(file)
    
    print("=" * 50)
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        return False
    else:
        print("\nAll required files are present!")
        return True

def check_directories():
    """Check if required directories exist."""
    import os
    
    required_dirs = ['model', 'data']
    
    print("\nChecking directories...")
    print("=" * 50)
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ {dir_name}/")
        else:
            print(f"✗ {dir_name}/ - Creating...")
            os.makedirs(dir_name, exist_ok=True)
            print(f"✓ {dir_name}/ - Created")
    
    print("=" * 50)
    print("\nDirectories are ready!")
    return True

def test_camera():
    """Test if camera is available."""
    import cv2
    
    print("\nTesting camera...")
    print("=" * 50)
    
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print("✓ Camera is working")
            cap.release()
            return True
        else:
            print("✗ Camera opened but cannot read frames")
            cap.release()
            return False
    else:
        print("✗ Camera cannot be opened")
        print("  Make sure your camera is connected and not being used by another application")
        return False

def main():
    """Run all verification checks."""
    print("Sign Language Detector - Setup Verification")
    print("=" * 50)
    print()
    
    checks = [
        ("Dependencies", check_imports),
        ("Project Files", check_files),
        ("Directories", check_directories),
        ("Camera", test_camera),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"Error during {name} check: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("Verification Summary")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n✓ All checks passed! You're ready to use the application.")
        print("  Run 'python main.py' to start the sign language detector.")
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

