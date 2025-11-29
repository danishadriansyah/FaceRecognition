# Lesson 2: Database Setup & Store Dataset

## Tujuan
- Setup MySQL database untuk face recognition system
- Understand SQLAlchemy ORM models
- Store captured faces to database
- Database relationships (One-to-Many)

## Database Schema
```
persons
- id (PK)
- employee_id (unique)
- name
- department
- created_at

face_images
- id (PK)
- person_id (FK → persons.id)
- image_path
- quality_score
- file_size
- captured_at

face_encodings
- id (PK)
- person_id (FK → persons.id)
- encoding_data (BLOB)
- model_name (Facenet512)
- created_at
```

## Files
1. **`database.py`** - Database connection & session management
2. **`models.py`** - SQLAlchemy ORM models (Person, FaceImage, FaceEncoding)
3. **`main.py`** - Store captured faces to database

## Yang Dipelajari
1. MySQL connection dengan SQLAlchemy
2. ORM models dengan relationships
3. Create tables from models
4. Insert data to database (Person + FaceImages)
5. Query database statistics
6. Database session management

## Prerequisites

### Option 1: HeidiSQL + XAMPP (Recommended - GUI)
```bash
# Install dependencies
pip install sqlalchemy pymysql
```

**Setup Database:**
1. **Start XAMPP:** Buka XAMPP Control Panel → Start MySQL
2. **Buka HeidiSQL** → Connect ke localhost (root, no password)
3. **Create Database:** Right-click → Create new → Database
   - Name: `face_recognition_db`
   - Charset: `utf8mb4`
4. **View Data:** Setelah run program, refresh HeidiSQL untuk lihat tables

### Option 2: MySQL Command Line
```bash
mysql -u root -p
CREATE DATABASE face_recognition_db CHARACTER SET utf8mb4;
```

## Langkah
1. **Start XAMPP MySQL** (jika pakai XAMPP)
2. **Create database** di HeidiSQL atau terminal (lihat Prerequisites)
3. **Run Lesson 1 first** - Capture faces (20 photos/person)
4. **Edit connection string** di `database.py` (line 19):
   ```python
   # Untuk XAMPP (password biasanya kosong):
   connection_string = "mysql+pymysql://root:@localhost:3306/face_recognition_db"
   
   # Jika MySQL standalone dengan password:
   connection_string = "mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/face_recognition_db"
   ```
5. **Test connection**: `python database.py`
6. **Run main program**: `python main.py`
7. **View data di HeidiSQL**: Refresh database → Lihat tables persons, face_images, face_encodings

## Output
```
✅ Database connected successfully!
✅ Database tables created!

👤 Storing: Alice (ID: EMP0001)
   ✅ Stored 20 images

👤 Storing: Bob (ID: EMP0002)
   ✅ Stored 20 images

✅ Total Persons: 2
✅ Total Face Images: 40
✅ Total Encodings: 2
```

## Why Database?
- **Scalability:** Handle 1000+ persons easily
- **Relationships:** Person → Multiple images → Multiple encodings
- **Queries:** Fast search by employee_id, department
- **Integrity:** Foreign keys ensure data consistency
- **Production-ready:** Standard industry approach

## Next: Minggu 5 - Hybrid Recognition
Generate **real** face encodings dengan DeepFace Facenet512!
