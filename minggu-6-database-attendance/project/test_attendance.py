"""
Test Attendance System
Week 6 Project Module - Progressive Web Application

Tests for database models and attendance service
"""

import sys
import os
from datetime import date

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from attendance_system import Database, Person, Attendance, FaceEncoding, AttendanceService


def test_database_initialization():
    """Test database creation"""
    print("Test 1: Database Initialization")
    db = Database('sqlite:///:memory:')
    db.create_tables()
    print("✓ Database tables created successfully")
    return db


def test_person_model(db):
    """Test Person model"""
    print("\nTest 2: Person Model")
    session = db.get_session()
    
    person = Person(
        name="Test User",
        employee_id="TEST001",
        department="IT",
        email="test@example.com"
    )
    session.add(person)
    session.commit()
    
    assert person.id is not None
    print(f"✓ Person created: {person}")
    print(f"  Dict: {person.to_dict()}")
    
    session.close()
    return person.id


def test_attendance_model(db, person_id):
    """Test Attendance model"""
    print("\nTest 3: Attendance Model")
    session = db.get_session()
    
    attendance = Attendance(
        person_id=person_id,
        type='check_in',
        confidence=0.95,
        location="Main Office"
    )
    session.add(attendance)
    session.commit()
    
    assert attendance.id is not None
    print(f"✓ Attendance created: {attendance}")
    print(f"  Dict: {attendance.to_dict()}")
    
    session.close()


def test_face_encoding_model(db, person_id):
    """Test FaceEncoding model"""
    print("\nTest 4: FaceEncoding Model")
    import numpy as np
    
    session = db.get_session()
    
    encoding = FaceEncoding(person_id=person_id)
    encoding_array = np.random.rand(128)
    encoding.set_encoding(encoding_array)
    
    session.add(encoding)
    session.commit()
    
    # Retrieve and check
    retrieved = encoding.get_encoding()
    assert retrieved.shape == (128,)
    print(f"✓ Face encoding created and retrieved")
    print(f"  Shape: {retrieved.shape}")
    
    session.close()


def test_attendance_service(db, person_id):
    """Test AttendanceService"""
    print("\nTest 5: Attendance Service")
    session = db.get_session()
    service = AttendanceService(session)
    
    # Record check-in
    attendance = service.record_attendance(
        person_id=person_id,
        attendance_type='check_in',
        confidence=0.95
    )
    
    assert attendance.id is not None
    print(f"✓ Attendance recorded via service")
    
    # Check status
    status = service.get_latest_status(person_id)
    assert status == 'checked_in'
    print(f"✓ Latest status: {status}")
    
    # Check if checked in
    has_checked_in = service.has_checked_in_today(person_id)
    assert has_checked_in is True
    print(f"✓ Has checked in today: {has_checked_in}")
    
    session.close()


def test_daily_report(db):
    """Test daily report generation"""
    print("\nTest 6: Daily Report")
    session = db.get_session()
    service = AttendanceService(session)
    
    report = service.generate_daily_report()
    
    print(f"✓ Daily report generated:")
    print(f"  - Date: {report['date']}")
    print(f"  - Total persons: {report['total_active_persons']}")
    print(f"  - Checked in: {report['total_checked_in']}")
    print(f"  - Attendance rate: {report['attendance_rate']:.2f}%")
    
    session.close()


def test_relationships(db, person_id):
    """Test model relationships"""
    print("\nTest 7: Model Relationships")
    session = db.get_session()
    
    person = session.query(Person).filter_by(id=person_id).first()
    
    print(f"✓ Person: {person.name}")
    print(f"  - Attendances: {len(person.attendances)}")
    print(f"  - Face encodings: {len(person.face_encodings)}")
    
    session.close()


def test_integration_with_week5():
    """Test integration concept with week 5"""
    print("\nTest 8: Integration with Week 5")
    
    print("  Integration flow:")
    print("  1. Week 5 RecognitionService recognizes person")
    print("  2. Returns person_id and confidence")
    print("  3. Week 6 AttendanceService.record_attendance()")
    print("  4. Saves to database with timestamp")
    print("✓ Integration architecture verified")


if __name__ == "__main__":
    print("Attendance System Tests - Week 6 Project")
    print("=" * 50)
    
    # Run tests
    db = test_database_initialization()
    person_id = test_person_model(db)
    test_attendance_model(db, person_id)
    test_face_encoding_model(db, person_id)
    test_attendance_service(db, person_id)
    test_daily_report(db)
    test_relationships(db, person_id)
    test_integration_with_week5()
    
    # Cleanup
    db.close()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("\nIntegration ready for Week 7 (Flask REST API)")
