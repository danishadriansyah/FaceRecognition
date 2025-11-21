"""Lesson 1: MySQL Setup & Attendance Logic"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date

Base = declarative_base()

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_date = Column(DateTime, default=datetime.now)

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))
    check_in_time = Column(DateTime, default=datetime.now)
    date = Column(Date, default=date.today)
    person = relationship("Person")

def main():
    print("="*60)
    print("LESSON 1: MySQL Setup & Attendance Logic")
    print("="*60)
    
    # Create SQLite for demo (replace with MySQL for production)
    print("\n1. Connecting to database...")
    engine = create_engine('sqlite:///attendance_demo.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    print("   ✅ Database connected")
    
    # Add sample persons
    print("\n2. Adding sample persons...")
    persons = ['Alice', 'Bob', 'Charlie']
    for name in persons:
        existing = session.query(Person).filter_by(name=name).first()
        if not existing:
            person = Person(name=name)
            session.add(person)
    session.commit()
    print(f"   ✅ Added {len(persons)} persons")
    
    # Record attendance
    print("\n3. Recording attendance...")
    person = session.query(Person).filter_by(name='Alice').first()
    
    # Check if already checked in today
    existing = session.query(Attendance).filter(
        Attendance.person_id == person.id,
        Attendance.date == date.today()
    ).first()
    
    if existing:
        print(f"   ⚠️ {person.name} already checked in today at {existing.check_in_time}")
    else:
        attendance = Attendance(person_id=person.id)
        session.add(attendance)
        session.commit()
        print(f"   ✅ {person.name} checked in at {attendance.check_in_time}")
    
    # Show today's attendance
    print("\n4. Today's attendance:")
    today_records = session.query(Attendance).filter(
        Attendance.date == date.today()
    ).all()
    
    for record in today_records:
        print(f"   - {record.person.name}: {record.check_in_time.strftime('%H:%M:%S')}")
    
    session.close()
    print("\n✅ LESSON 1 COMPLETED!")

if __name__ == '__main__':
    main()
