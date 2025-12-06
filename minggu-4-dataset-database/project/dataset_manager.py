"""
Dataset Manager Module
Week 4 Project Module - Progressive Web Application

This module manages face dataset collection and organization WITH DATABASE.
Stores data in MySQL database using SQLAlchemy ORM.
Builds on Week 2's face_detector.py and Week 3's face_recognizer.py.
"""

import cv2
import numpy as np
import os
import sys
import pickle
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

# Import database modules from learning/lesson-2
learning_path = os.path.join(os.path.dirname(__file__), '..', 'learning', 'lesson-2')
sys.path.insert(0, learning_path)

from database import Database
from models import Person, FaceImage, FaceEncoding


class DatasetManager:
    """
    Manage face datasets for recognition system with MySQL database
    """
    
    def __init__(self, connection_string: str = None, image_storage_path: str = "dataset"):
        """
        Initialize dataset manager with database
        
        Args:
            connection_string: MySQL connection string (default: XAMPP local)
            image_storage_path: Path to store actual image files
        """
        # XAMPP Default connection
        if connection_string is None:
            connection_string = "mysql+pymysql://root:@localhost:3306/face_recognition_db"
        
        self.db = Database(connection_string)
        
        if not self.db.connect():
            raise ConnectionError(
                "❌ Database connection failed!\n"
                "💡 Make sure:\n"
                "   1. XAMPP MySQL is running\n"
                "   2. Database 'face_recognition_db' exists\n"
                "   3. Check in HeidiSQL: Session → New"
            )
        
        # Image storage path (files still stored locally for performance)
        self.image_storage_path = Path(image_storage_path)
        self.image_storage_path.mkdir(parents=True, exist_ok=True)
        
        print("✅ DatasetManager initialized (Database mode)")
        print(f"   Database: {connection_string.split('@')[1]}")
        print(f"   Image storage: {self.image_storage_path}")

    
    def add_person(self, name: str, employee_id: str = None, 
                   department: str = None, metadata: Dict = None) -> int:
        """
        Add a new person to database
        
        Args:
            name: Person's name
            employee_id: Employee ID
            department: Department
            metadata: Additional metadata (stored as JSON)
            
        Returns:
            Person database ID
        """
        session = self.db.get_session()
        
        try:
            # Create person record
            person = Person(
                name=name,
                employee_id=employee_id,
                department=department,
                created_at=datetime.now()
            )
            
            session.add(person)
            session.commit()
            
            person_id = person.id
            
            # Create folder for images
            person_folder = self.image_storage_path / f"person_{person_id}_{name.lower().replace(' ', '_')}"
            person_folder.mkdir(parents=True, exist_ok=True)
            
            print(f"✅ Person added: {name} (ID: {person_id})")
            print(f"   Employee ID: {employee_id}")
            print(f"   Department: {department}")
            print(f"   Image folder: {person_folder}")
            
            return person_id
            
        except Exception as e:
            session.rollback()
            raise Exception(f"Failed to add person: {e}")
        finally:
            session.close()

    
    def capture_face(self, person_id: int, image: np.ndarray, 
                    angle: str = 'frontal', validate: bool = True) -> Optional[int]:
        """
        Capture and save a face image to database
        
        Args:
            person_id: Person database ID
            image: Face image
            angle: Image angle (frontal, left, right)
            validate: Whether to validate image quality
            
        Returns:
            FaceImage database ID, or None if validation failed
        """
        session = self.db.get_session()
        
        try:
            # Get person
            person = session.query(Person).filter_by(id=person_id).first()
            if not person:
                raise ValueError(f"Person not found: {person_id}")
            
            # Validate if requested
            if validate:
                is_valid, msg, quality_score = self.validate_face_image(image)
                if not is_valid:
                    print(f"❌ Validation failed: {msg}")
                    return None
            else:
                quality_score = 0.0
            
            # Generate filename
            person_folder = self.image_storage_path / f"person_{person_id}_{person.name.lower().replace(' ', '_')}"
            person_folder.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{angle}_{timestamp}.jpg"
            filepath = person_folder / filename
            
            # Save image file
            cv2.imwrite(str(filepath), image)
            
            # Save to database
            face_image = FaceImage(
                person_id=person_id,
                image_path=str(filepath),
                angle=angle,
                quality_score=quality_score,
                captured_at=datetime.now()
            )
            
            session.add(face_image)
            session.commit()
            
            face_image_id = face_image.id
            
            print(f"✅ Face captured: {filename} (Quality: {quality_score:.2f})")
            
            return face_image_id
            
        except Exception as e:
            session.rollback()
            print(f"❌ Failed to capture face: {e}")
            return None
        finally:
            session.close()

    
    def get_person_images(self, person_id: int) -> List[Dict]:
        """
        Get all images for a person from database
        
        Args:
            person_id: Person database ID
            
        Returns:
            List of image dictionaries with metadata
        """
        session = self.db.get_session()
        
        try:
            person = session.query(Person).filter_by(id=person_id).first()
            if not person:
                return []
            
            images = []
            for face_image in person.face_images:
                images.append({
                    'id': face_image.id,
                    'path': face_image.image_path,
                    'angle': face_image.angle,
                    'quality_score': face_image.quality_score,
                    'captured_at': face_image.captured_at.isoformat() if face_image.captured_at else None
                })
            
            return images
            
        finally:
            session.close()

    
    def remove_person(self, person_id: int, remove_images: bool = True) -> bool:
        """
        Remove a person from database
        
        Args:
            person_id: Person database ID
            remove_images: Whether to also remove image files
            
        Returns:
            True if removed, False if not found
        """
        session = self.db.get_session()
        
        try:
            person = session.query(Person).filter_by(id=person_id).first()
            if not person:
                return False
            
            person_name = person.name
            
            # Remove image files if requested
            if remove_images:
                person_folder = self.image_storage_path / f"person_{person_id}_{person.name.lower().replace(' ', '_')}"
                if person_folder.exists():
                    import shutil
                    shutil.rmtree(person_folder)
                    print(f"🗑️  Removed image folder: {person_folder}")
            
            # Delete from database (cascade will delete face_images and face_encodings)
            session.delete(person)
            session.commit()
            
            print(f"✅ Person removed: {person_name} (ID: {person_id})")
            
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Failed to remove person: {e}")
            return False
        finally:
            session.close()

    
    def validate_face_image(self, image: np.ndarray, 
                           min_size: int = 100) -> Tuple[bool, str, float]:
        """
        Validate face image quality
        
        Args:
            image: Face image
            min_size: Minimum image dimension
            
        Returns:
            Tuple of (is_valid, message, quality_score)
        """
        if image is None:
            return False, "Image is None", 0.0
        
        # Check dimensions
        height, width = image.shape[:2]
        
        if width < min_size or height < min_size:
            return False, f"Image too small: {width}x{height}", 0.0
        
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Check brightness
        mean_brightness = np.mean(gray)
        if mean_brightness < 40:
            return False, f"Image too dark: brightness={mean_brightness:.1f}", 0.0
        if mean_brightness > 220:
            return False, f"Image too bright: brightness={mean_brightness:.1f}", 0.0
        
        # Check blur (Laplacian variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < 100:
            return False, f"Image too blurry: variance={laplacian_var:.1f}", 0.0
        
        # Calculate quality score (0-1)
        # Based on brightness (0.4), sharpness (0.6)
        brightness_score = min(mean_brightness / 150.0, 1.0)
        sharpness_score = min(laplacian_var / 500.0, 1.0)
        quality_score = (brightness_score * 0.4) + (sharpness_score * 0.6)
        
        return True, "Image quality OK", quality_score

    
    def validate_dataset(self) -> Dict:
        """
        Validate entire dataset from database
        
        Returns:
            Validation report
        """
        session = self.db.get_session()
        
        try:
            all_persons = session.query(Person).all()
            
            report = {
                'total_people': len(all_persons),
                'total_images': 0,
                'total_encodings': 0,
                'issues': [],
                'valid_people': 0
            }
            
            for person in all_persons:
                image_count = len(person.face_images)
                encoding_count = len(person.face_encodings)
                
                report['total_images'] += image_count
                report['total_encodings'] += encoding_count
                
                if image_count == 0:
                    report['issues'].append(f"{person.name}: No images")
                elif image_count < 5:
                    report['issues'].append(f"{person.name}: Only {image_count} images (recommend 20+)")
                else:
                    report['valid_people'] += 1
                
                if encoding_count == 0:
                    report['issues'].append(f"{person.name}: No encodings generated")
            
            return report
            
        finally:
            session.close()

    
    def generate_encodings(self, person_id: int = None, model_name: str = 'Facenet512') -> int:
        """
        Generate face encodings for person(s) using DeepFace
        
        Args:
            person_id: Specific person ID, or None for all people
            model_name: DeepFace model ('Facenet512', 'ArcFace', 'SFace')
            
        Returns:
            Number of encodings generated
        """
        from deepface import DeepFace
        
        session = self.db.get_session()
        count = 0
        
        try:
            # Get persons to process
            if person_id:
                persons = [session.query(Person).filter_by(id=person_id).first()]
                if not persons[0]:
                    print(f"❌ Person not found: {person_id}")
                    return 0
            else:
                persons = session.query(Person).all()
            
            print(f"🔧 Generating encodings with {model_name}...")
            
            for person in persons:
                if not person:
                    continue
                
                print(f"\n📊 Processing: {person.name} (ID: {person.id})")
                
                # Delete old encodings for this person
                session.query(FaceEncoding).filter_by(person_id=person.id).delete()
                
                for face_image in person.face_images:
                    try:
                        # Generate encoding
                        embeddings = DeepFace.represent(
                            img_path=face_image.image_path,
                            model_name=model_name,
                            enforce_detection=False
                        )
                        
                        if embeddings and len(embeddings) > 0:
                            encoding_array = np.array(embeddings[0]['embedding'])
                            encoding_bytes = pickle.dumps(encoding_array)
                            
                            # Save to database
                            face_encoding = FaceEncoding(
                                person_id=person.id,
                                encoding_data=encoding_bytes,
                                model_name=model_name,
                                generated_at=datetime.now()
                            )
                            
                            session.add(face_encoding)
                            count += 1
                            
                            print(f"   ✅ Encoded: {Path(face_image.image_path).name}")
                        
                    except Exception as e:
                        print(f"   ❌ Failed: {Path(face_image.image_path).name} - {e}")
                        continue
                
                session.commit()
                print(f"   Total: {len(person.face_encodings)} encodings")
            
            print(f"\n✅ Generated {count} encodings total")
            return count
            
        except Exception as e:
            session.rollback()
            print(f"❌ Encoding generation failed: {e}")
            return 0
        finally:
            session.close()

    
    def get_statistics(self) -> Dict:
        """
        Get dataset statistics from database
        
        Returns:
            Statistics dictionary
        """
        session = self.db.get_session()
        
        try:
            stats = self.db.get_statistics()
            
            # Add department breakdown
            persons = session.query(Person).all()
            dept_counts = {}
            
            for person in persons:
                dept = person.department or 'Unknown'
                dept_counts[dept] = dept_counts.get(dept, 0) + 1
            
            stats['people_by_department'] = dept_counts
            
            return stats
            
        finally:
            session.close()
    
    def list_people(self) -> List[Dict]:
        """
        List all people in database
        
        Returns:
            List of people with metadata
        """
        session = self.db.get_session()
        
        try:
            persons = session.query(Person).all()
            people = []
            
            for person in persons:
                person_info = {
                    'id': person.id,
                    'name': person.name,
                    'employee_id': person.employee_id,
                    'department': person.department,
                    'image_count': len(person.face_images),
                    'encoding_count': len(person.face_encodings),
                    'created_at': person.created_at.isoformat() if person.created_at else None
                }
                people.append(person_info)
            
            return people
            
        finally:
            session.close()
    
    def close(self):
        """Close database connection"""
        self.db.close()



# Example usage and testing
if __name__ == "__main__":
    print("Dataset Manager Module - Week 4 Project (Database Mode)")
    print("="*60)
    
    try:
        # Initialize manager
        print("\n1. Initializing DatasetManager...")
        manager = DatasetManager(
            connection_string="mysql+pymysql://root:@localhost:3306/face_recognition_db",
            image_storage_path="project_dataset"
        )
        
        # Add people
        print("\n2. Adding people...")
        alice_id = manager.add_person("Alice Smith", employee_id="EMP001", department="IT")
        bob_id = manager.add_person("Bob Johnson", employee_id="EMP002", department="HR")
        
        # Create test images
        print("\n3. Creating test face images...")
        test_face = np.ones((200, 200, 3), dtype=np.uint8) * 180
        cv2.circle(test_face, (70, 80), 10, (0, 0, 0), -1)
        cv2.circle(test_face, (130, 80), 10, (0, 0, 0), -1)
        cv2.ellipse(test_face, (100, 130), (30, 15), 0, 0, 180, (0, 0, 0), 2)
        
        # Capture faces
        print("\n4. Capturing faces...")
        img1_id = manager.capture_face(alice_id, test_face, angle='frontal')
        img2_id = manager.capture_face(alice_id, test_face, angle='left')
        img3_id = manager.capture_face(bob_id, test_face, angle='frontal')
        print(f"   Captured 3 images")
        
        # Get person images
        print("\n5. Getting person images from database...")
        alice_images = manager.get_person_images(alice_id)
        print(f"   Alice has {len(alice_images)} images")
        for img in alice_images:
            print(f"      - {Path(img['path']).name} (Quality: {img['quality_score']:.2f})")
        
        # Validate dataset
        print("\n6. Validating dataset...")
        report = manager.validate_dataset()
        print(f"   Total people: {report['total_people']}")
        print(f"   Total images: {report['total_images']}")
        print(f"   Total encodings: {report['total_encodings']}")
        print(f"   Valid people: {report['valid_people']}")
        if report['issues']:
            print(f"   Issues:")
            for issue in report['issues']:
                print(f"      - {issue}")
        
        # Generate encodings
        print("\n7. Generating encodings with DeepFace...")
        try:
            count = manager.generate_encodings(model_name='Facenet512')
            print(f"   Generated {count} encodings")
        except ImportError:
            print("   ⚠️  DeepFace not installed (pip install deepface)")
        
        # Statistics
        print("\n8. Dataset statistics...")
        stats = manager.get_statistics()
        print(f"   Total persons: {stats.get('total_persons', 0)}")
        print(f"   Total images: {stats.get('total_images', 0)}")
        print(f"   Total encodings: {stats.get('total_encodings', 0)}")
        if 'people_by_department' in stats:
            print(f"   By department:")
            for dept, count in stats['people_by_department'].items():
                print(f"      {dept}: {count}")
        
        # List people
        print("\n9. Listing people...")
        people = manager.list_people()
        for person in people:
            print(f"   {person['name']} (ID: {person['id']})")
            print(f"      Employee ID: {person['employee_id']}")
            print(f"      Department: {person['department']}")
            print(f"      Images: {person['image_count']}, Encodings: {person['encoding_count']}")
        
        # Close connection
        manager.close()
        
        print("\n" + "="*60)
        print("✅ Module ready for integration!")
        print("\nDatabase Integration:")
        print("  - Storage: MySQL (face_recognition_db)")
        print("  - Tables: Person, FaceImage, FaceEncoding")
        print("  - View in HeidiSQL: Press F5 to refresh")
        print("\nNext steps:")
        print("  1. Use in Week 5: recognition_service.py")
        print("  2. Use in Week 6: attendance_system.py")
        print("  3. Use in Week 7: Desktop GUI")
        
    except ConnectionError as e:
        print(f"\n❌ {e}")
        print("\n💡 Setup Instructions:")
        print("   1. Start XAMPP → MySQL")
        print("   2. Open HeidiSQL")
        print("   3. Run Week 4 Lesson 2 first to create database")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

