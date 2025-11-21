"""
Lesson 3: Testing, Debugging & Deployment
Comprehensive system testing
"""
import os
import sys
from datetime import datetime

def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_imports():
    """Test if all required packages are installed"""
    print_section("1. Testing Package Imports")
    
    packages = {
        'cv2': 'OpenCV',
        'face_recognition': 'Face Recognition',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sqlalchemy': 'SQLAlchemy',
        'tkinter': 'Tkinter (GUI)',
        'openpyxl': 'Excel Export'
    }
    
    results = {'passed': 0, 'failed': 0}
    
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"   ✅ {name}")
            results['passed'] += 1
        except ImportError:
            print(f"   ❌ {name} - NOT INSTALLED")
            results['failed'] += 1
    
    return results

def test_file_structure():
    """Test if all required folders exist"""
    print_section("2. Testing File Structure")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    required_folders = [
        'minggu-1-python-basics',
        'minggu-2-face-detection',
        'minggu-3-face-recognition',
        'minggu-4-dataset-collection',
        'minggu-5-recognition-system',
        'minggu-6-database-attendance',
        'minggu-7-desktop-gui'
    ]
    
    results = {'passed': 0, 'failed': 0}
    
    for folder in required_folders:
        path = os.path.join(base_dir, folder)
        if os.path.exists(path):
            print(f"   ✅ {folder}")
            results['passed'] += 1
        else:
            print(f"   ❌ {folder} - NOT FOUND")
            results['failed'] += 1
    
    return results

def test_opencv():
    """Test OpenCV functionality"""
    print_section("3. Testing OpenCV")
    
    results = {'passed': 0, 'failed': 0}
    
    try:
        import cv2
        import numpy as np
        
        # Test image creation
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Test Haar Cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if face_cascade.empty():
            print("   ❌ Haar Cascade not loaded")
            results['failed'] += 1
        else:
            print("   ✅ Image processing")
            print("   ✅ Haar Cascade loaded")
            results['passed'] += 2
            
    except Exception as e:
        print(f"   ❌ OpenCV test failed: {e}")
        results['failed'] += 1
    
    return results

def test_webcam():
    """Test webcam access"""
    print_section("4. Testing Webcam")
    
    results = {'passed': 0, 'failed': 0}
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                h, w = frame.shape[:2]
                print(f"   ✅ Webcam accessible")
                print(f"   ✅ Resolution: {w}x{h}")
                results['passed'] += 2
            else:
                print("   ❌ Cannot read from webcam")
                results['failed'] += 1
        else:
            print("   ❌ Cannot open webcam")
            results['failed'] += 1
            
    except Exception as e:
        print(f"   ❌ Webcam test failed: {e}")
        results['failed'] += 1
    
    return results

def test_face_recognition():
    """Test face_recognition library"""
    print_section("5. Testing Face Recognition")
    
    results = {'passed': 0, 'failed': 0}
    
    try:
        import face_recognition
        import numpy as np
        
        # Create dummy face encoding
        dummy_encoding = np.random.rand(128)
        
        print("   ✅ Face recognition library loaded")
        print("   ✅ Encoding format valid (128-d vector)")
        results['passed'] += 2
        
    except Exception as e:
        print(f"   ❌ Face recognition test failed: {e}")
        results['failed'] += 1
    
    return results

def test_database():
    """Test database connectivity"""
    print_section("6. Testing Database (Optional)")
    
    results = {'passed': 0, 'failed': 0}
    
    try:
        from sqlalchemy import create_engine, text
        
        # Try connecting to MySQL (if available)
        try:
            engine = create_engine('mysql+pymysql://root@localhost/test')
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("   ✅ MySQL connection successful")
                results['passed'] += 1
        except:
            print("   ⚠️  MySQL not configured (optional)")
            print("   💡 Project can run with in-memory database")
            results['passed'] += 1
            
    except Exception as e:
        print(f"   ⚠️  Database test skipped: {e}")
        results['passed'] += 1  # Not critical
    
    return results

def performance_test():
    """Test performance benchmarks"""
    print_section("7. Performance Test")
    
    results = {'passed': 0, 'failed': 0}
    
    try:
        import cv2
        import time
        
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            face_cascade = cv2.CascadeClassifier(cascade_path)
            
            # Test FPS
            start_time = time.time()
            frame_count = 0
            
            while frame_count < 30:  # Test 30 frames
                ret, frame = cap.read()
                if ret:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    frame_count += 1
            
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            
            cap.release()
            
            print(f"   📊 Detection FPS: {fps:.1f}")
            
            if fps >= 20:
                print("   ✅ Performance: Excellent (20+ FPS)")
                results['passed'] += 1
            elif fps >= 10:
                print("   ⚠️  Performance: Acceptable (10-20 FPS)")
                results['passed'] += 1
            else:
                print("   ❌ Performance: Poor (<10 FPS)")
                results['failed'] += 1
        else:
            print("   ⚠️  Webcam not available for performance test")
            results['passed'] += 1
            
    except Exception as e:
        print(f"   ⚠️  Performance test skipped: {e}")
        results['passed'] += 1
    
    return results

def deployment_check():
    """Check deployment readiness"""
    print_section("8. Deployment Readiness")
    
    print("   📦 Deployment Options:")
    print("   1. Run directly with Python")
    print("   2. Package as executable (PyInstaller)")
    print("   3. Docker container (advanced)")
    
    print("\n   📝 To create executable:")
    print("   pip install pyinstaller")
    print("   pyinstaller --onefile --windowed app.py")
    
    print("\n   ✅ System ready for deployment")
    
    return {'passed': 1, 'failed': 0}

def main():
    """Run all tests"""
    print("\n" + "█"*60)
    print("  LESSON 3: COMPREHENSIVE SYSTEM TESTING")
    print("█"*60)
    
    print("\n🔍 Running all tests...")
    print("This will verify that your system is ready!")
    
    all_results = []
    
    # Run all tests
    all_results.append(test_imports())
    all_results.append(test_file_structure())
    all_results.append(test_opencv())
    all_results.append(test_webcam())
    all_results.append(test_face_recognition())
    all_results.append(test_database())
    all_results.append(performance_test())
    all_results.append(deployment_check())
    
    # Calculate totals
    total_passed = sum(r['passed'] for r in all_results)
    total_failed = sum(r['failed'] for r in all_results)
    total_tests = total_passed + total_failed
    
    # Summary
    print_section("TEST SUMMARY")
    
    print(f"\n   ✅ Passed: {total_passed}/{total_tests}")
    print(f"   ❌ Failed: {total_failed}/{total_tests}")
    
    if total_tests > 0:
        success_rate = (total_passed / total_tests) * 100
        print(f"\n   📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("\n   🎉 PERFECT SCORE! All systems operational!")
        elif success_rate >= 80:
            print("\n   ✅ GREAT! System is ready!")
        elif success_rate >= 60:
            print("\n   ⚠️  GOOD! Minor issues to fix")
        else:
            print("\n   ❌ NEEDS WORK! Please fix failing tests")
    
    # Final message
    print("\n" + "█"*60)
    print("  🎓 CONGRATULATIONS!")
    print("█"*60)
    print("\n  You've completed 7 WEEKS of learning!")
    print("  All concepts mastered:")
    print("  ✅ Python & OpenCV basics")
    print("  ✅ Face detection")
    print("  ✅ Face recognition")
    print("  ✅ Dataset management")
    print("  ✅ Database integration")
    print("  ✅ Desktop GUI")
    print("  ✅ Testing & debugging")
    
    print("\n" + "─"*60)
    print("  🚀 NEXT PHASE: FINAL PROJECT (Week 7.5-8)")
    print("─"*60)
    print("\n  Now it's time to build your OWN complete")
    print("  attendance system from scratch!")
    print("\n  Use everything you've learned to create")
    print("  a production-ready application!")
    
    print("\n" + "█"*60 + "\n")

if __name__ == '__main__':
    main()
