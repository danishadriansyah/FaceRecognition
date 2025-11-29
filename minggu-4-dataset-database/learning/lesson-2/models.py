"""
SQLAlchemy ORM models for face recognition system
Defines database schema for persons, face images, and encodings
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, LargeBinary, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Person(Base):
    """Person/Employee table - stores user information"""
    __tablename__ = 'persons'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    department = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    face_images = relationship("FaceImage", back_populates="person", cascade="all, delete-orphan")
    face_encodings = relationship("FaceEncoding", back_populates="person", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}', employee_id='{self.employee_id}')>"


class FaceImage(Base):
    """Face images table - stores captured face photos"""
    __tablename__ = 'face_images'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False, index=True)
    image_path = Column(String(500), nullable=False)
    quality_score = Column(Float)  # Face detection confidence
    width = Column(Integer)
    height = Column(Integer)
    file_size = Column(Integer)  # in bytes
    captured_at = Column(DateTime, default=datetime.now)
    
    # Relationship
    person = relationship("Person", back_populates="face_images")
    
    def __repr__(self):
        return f"<FaceImage(id={self.id}, person_id={self.person_id}, path='{self.image_path}')>"


class FaceEncoding(Base):
    """Face encodings table - stores face embeddings for recognition"""
    __tablename__ = 'face_encodings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False, index=True)
    encoding_data = Column(LargeBinary, nullable=False)  # Stores numpy array as binary
    model_name = Column(String(50), default='Facenet512')  # DeepFace model used
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationship
    person = relationship("Person", back_populates="face_encodings")
    
    def __repr__(self):
        return f"<FaceEncoding(id={self.id}, person_id={self.person_id}, model='{self.model_name}')>"


def create_schema_sql():
    """Generate SQL schema for reference"""
    sql = """
-- Create database
CREATE DATABASE IF NOT EXISTS face_recognition_db 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE face_recognition_db;

-- Persons table
CREATE TABLE IF NOT EXISTS persons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employee_id (employee_id)
) ENGINE=InnoDB;

-- Face images table
CREATE TABLE IF NOT EXISTS face_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    image_path VARCHAR(500) NOT NULL,
    quality_score FLOAT,
    width INT,
    height INT,
    file_size INT,
    captured_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE,
    INDEX idx_person_id (person_id)
) ENGINE=InnoDB;

-- Face encodings table
CREATE TABLE IF NOT EXISTS face_encodings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL,
    encoding_data LONGBLOB NOT NULL,
    model_name VARCHAR(50) DEFAULT 'Facenet512',
    confidence FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE,
    INDEX idx_person_id (person_id)
) ENGINE=InnoDB;
"""
    return sql


if __name__ == '__main__':
    print("="*60)
    print("DATABASE SCHEMA")
    print("="*60)
    print(create_schema_sql())
    print("\n💡 Copy SQL above to create database manually")
    print("   Or use SQLAlchemy: Base.metadata.create_all(engine)")
