"""
Database utilities for face recognition system
MySQL connection and session management
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
import os

Base = declarative_base()

class Database:
    """Database connection manager"""
    
    def __init__(self, connection_string=None):
        """
        Initialize database connection
        
        Args:
            connection_string: MySQL connection URL
                Format: mysql+pymysql://user:password@host:port/database
        """
        if connection_string is None:
            # Default for XAMPP (root user, no password)
            # Change password if you set one in XAMPP
            connection_string = "mysql+pymysql://root:@localhost:3306/face_recognition_db"
        
        self.engine = create_engine(
            connection_string,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            echo=False  # Set True to see SQL queries
        )
        
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.session = None
    
    def connect(self):
        """Establish database connection"""
        try:
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Database connected successfully!")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def create_tables(self):
        """Create all tables from models"""
        try:
            Base.metadata.create_all(self.engine)
            print("✅ Database tables created!")
            return True
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
            return False
    
    def get_session(self):
        """Get database session"""
        if self.session is None:
            self.session = self.SessionLocal()
        return self.session
    
    def close(self):
        """Close database connection"""
        if self.session:
            self.session.close()
            self.session = None
        print("✅ Database connection closed")
    
    def get_statistics(self):
        """Get database statistics"""
        session = self.get_session()
        from models import Person, FaceImage, FaceEncoding
        
        stats = {
            'total_persons': session.query(Person).count(),
            'total_images': session.query(FaceImage).count(),
            'total_encodings': session.query(FaceEncoding).count()
        }
        return stats


def test_connection():
    """Test database connection"""
    print("Testing database connection...")
    
    # You need to create database first:
    # CREATE DATABASE face_recognition_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    
    db = Database()
    
    if db.connect():
        print("\n✅ Connection test passed!")
        db.close()
        return True
    else:
        print("\n❌ Connection test failed!")
        print("\n💡 Make sure:")
        print("   1. MySQL server is running")
        print("   2. Database 'face_recognition_db' exists")
        print("   3. Username and password are correct")
        return False


if __name__ == '__main__':
    test_connection()
