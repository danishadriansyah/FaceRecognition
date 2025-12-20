"""
Attendance System
Week 6 Project Module - Progressive Web Application

Complete attendance system integrating database and recognition
Consolidates: models.py, database.py, attendance_service.py
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import json
import os
from pathlib import Path

Base = declarative_base()


# ============================================================================
# MODELS (from models.py)
# ============================================================================

class Person(Base):
    """Person model - stores employee information"""
    __tablename__ = 'persons'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    employee_id = Column(String(50), unique=True, nullable=True)
    department = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    attendances = relationship('Attendance', back_populates='person', cascade='all, delete-orphan')
    face_encodings = relationship('FaceEncoding', back_populates='person', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'employee_id': self.employee_id,
            'department': self.department,
            'email': self.email,
            'phone': self.phone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}', employee_id='{self.employee_id}')>"


class Attendance(Base):
    """Attendance model - stores check-in/check-out records"""
    __tablename__ = 'attendances'
    
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    type = Column(String(20), nullable=False)  # 'check_in' or 'check_out'
    confidence = Column(Float, nullable=True)
    photo_path = Column(String(255), nullable=True)
    location = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    person = relationship('Person', back_populates='attendances')
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'person_name': self.person.name if self.person else None,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'type': self.type,
            'confidence': self.confidence,
            'photo_path': self.photo_path,
            'location': self.location,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<Attendance(id={self.id}, person_id={self.person_id}, type='{self.type}')>"


class FaceEncoding(Base):
    """Face encoding model - stores face encodings for recognition"""
    __tablename__ = 'face_encodings'
    
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    encoding_data = Column(Text, nullable=False)
    image_path = Column(String(255), nullable=True)
    angle = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    person = relationship('Person', back_populates='face_encodings')
    
    def set_encoding(self, encoding_array):
        self.encoding_data = json.dumps(encoding_array.tolist())
    
    def get_encoding(self):
        import numpy as np
        return np.array(json.loads(self.encoding_data))
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'person_name': self.person.name if self.person else None,
            'image_path': self.image_path,
            'angle': self.angle,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<FaceEncoding(id={self.id}, person_id={self.person_id})>"


# ============================================================================
# DATABASE (from database.py)
# ============================================================================

class Database:
    """Database connection and session management"""
    
    def __init__(self, database_url: str = None):
        if database_url is None:
            data_dir = Path('data')
            data_dir.mkdir(exist_ok=True)
            database_url = f'sqlite:///{data_dir}/attendance.db'
        
        self.database_url = database_url
        
        if database_url.startswith('sqlite'):
            self.engine = create_engine(
                database_url,
                connect_args={'check_same_thread': False},
                poolclass=StaticPool
            )
        else:
            self.engine = create_engine(database_url, pool_pre_ping=True)
        
        self.SessionLocal = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        ))
    
    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
        print(f"Database tables created")
    
    def drop_tables(self):
        Base.metadata.drop_all(bind=self.engine)
        print("Database tables dropped")
    
    def get_session(self):
        return self.SessionLocal()
    
    def close(self):
        self.SessionLocal.remove()
        self.engine.dispose()


# ============================================================================
# ATTENDANCE SERVICE (from attendance_service.py)
# ============================================================================

class AttendanceService:
    """Attendance business logic - integrates recognition with database"""
    
    def __init__(self, session):
        self.session = session
    
    def record_attendance(
        self,
        person_id: int,
        attendance_type: str,
        confidence: float = None,
        photo_path: str = None,
        location: str = None,
        notes: str = None
    ) -> Attendance:
        """Record attendance (check-in or check-out)"""
        person = self.session.query(Person).filter_by(id=person_id).first()
        if not person:
            raise ValueError(f"Person with id {person_id} not found")
        
        if not person.is_active:
            raise ValueError(f"Person {person.name} is inactive")
        
        attendance = Attendance(
            person_id=person_id,
            timestamp=datetime.utcnow(),
            type=attendance_type,
            confidence=confidence,
            photo_path=photo_path,
            location=location,
            notes=notes
        )
        
        self.session.add(attendance)
        self.session.commit()
        
        return attendance
    
    def get_attendance_today(self, person_id: int = None) -> List[Attendance]:
        """Get today's attendance records"""
        query = self.session.query(Attendance)
        
        today = date.today()
        query = query.filter(
            Attendance.timestamp >= datetime.combine(today, datetime.min.time()),
            Attendance.timestamp < datetime.combine(today + timedelta(days=1), datetime.min.time())
        )
        
        if person_id:
            query = query.filter(Attendance.person_id == person_id)
        
        return query.order_by(Attendance.timestamp.desc()).all()
    
    def has_checked_in_today(self, person_id: int) -> bool:
        """Check if person has checked in today"""
        today_records = self.get_attendance_today(person_id)
        return any(r.type == 'check_in' for r in today_records)
    
    def get_latest_status(self, person_id: int) -> Optional[str]:
        """Get latest attendance status for person"""
        today_records = self.get_attendance_today(person_id)
        if not today_records:
            return None
        
        latest = max(today_records, key=lambda r: r.timestamp)
        return 'checked_in' if latest.type == 'check_in' else 'checked_out'
    
    def generate_daily_report(self, target_date: date = None) -> Dict:
        """Generate daily attendance report"""
        if target_date is None:
            target_date = date.today()
        
        query = self.session.query(Attendance).filter(
            Attendance.timestamp >= datetime.combine(target_date, datetime.min.time()),
            Attendance.timestamp < datetime.combine(target_date + timedelta(days=1), datetime.min.time())
        )
        records = query.all()
        
        person_records = {}
        for record in records:
            if record.person_id not in person_records:
                person_records[record.person_id] = []
            person_records[record.person_id].append(record)
        
        total_persons = self.session.query(Person).filter_by(is_active=True).count()
        checked_in = len([p for p, rs in person_records.items() 
                         if any(r.type == 'check_in' for r in rs)])
        
        return {
            'date': target_date.isoformat(),
            'total_active_persons': total_persons,
            'total_checked_in': checked_in,
            'attendance_rate': (checked_in / total_persons * 100) if total_persons > 0 else 0,
            'records': [r.to_dict() for r in records]
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("Attendance System - Week 6 Project")
    print("=" * 50)
    
    # Initialize database
    print("\n1. Initializing database...")
    db = Database()
    db.create_tables()
    session = db.get_session()
    
    # Create service
    print("\n2. Creating attendance service...")
    service = AttendanceService(session)
    
    # Create test person
    print("\n3. Creating test person...")
    person = Person(
        name="John Doe",
        employee_id="EMP001",
        department="IT"
    )
    session.add(person)
    session.commit()
    print(f"   Created: {person}")
    
    # Record check-in
    print("\n4. Recording check-in...")
    attendance = service.record_attendance(
        person_id=person.id,
        attendance_type='check_in',
        confidence=0.95,
        location="Main Office"
    )
    print(f"   Recorded: {attendance}")
    
    # Check status
    print("\n5. Checking status...")
    status = service.get_latest_status(person.id)
    print(f"   Latest status: {status}")
    
    # Generate report
    print("\n6. Generating daily report...")
    report = service.generate_daily_report()
    print(f"   Date: {report['date']}")
    print(f"   Checked in: {report['total_checked_in']}")
    print(f"   Attendance rate: {report['attendance_rate']:.2f}%")
    
    # Cleanup
    session.close()
    
    print("\n" + "=" * 50)
    print("Attendance system ready!")
    print("\nIntegration with Week 5:")
    print("  1. Use RecognitionService to identify person")
    print("  2. Get person_id and confidence from recognition")
    print("  3. Call record_attendance() with results")
    print("\nNext: Week 7 (Desktop GUI Application)")
