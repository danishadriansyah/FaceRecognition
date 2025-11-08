# AI-Based Face Recognition Attendance System
## Progressive Web Application - 8 Week Development

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![Face Recognition](https://img.shields.io/badge/Face_Recognition-Latest-orange.svg)

---

## Deskripsi Project

Sistem absensi berbasis face recognition yang dikembangkan secara progressive dalam 8 minggu, dari pembelajaran dasar hingga web application yang production-ready. Sistem ini dapat mengenali hingga 200 wajah dan deployed sebagai web application.

### Fitur Utama
- Face Detection menggunakan Haar Cascade & Deep Learning
- Face Recognition dengan akurasi tinggi
- Database PostgreSQL/SQLite untuk production
- REST API untuk integration
- Web-based interface (Flask + HTML/CSS/JS)
- Real-time attendance tracking
- Export laporan ke Excel/CSV
- Support 200+ persons
- Mobile responsive design

---

## Timeline Pembelajaran (8 Minggu)

Setiap minggu terdiri dari **Learning** (tutorial & latihan) dan **Project Development** (progressive build).

### **Minggu 1: Python Basics & Image Processing**
**Learning Goals:**
- Setup environment & instalasi library
- Dasar Python untuk Computer Vision
- OpenCV fundamentals
- Image manipulation operations

**Project Development:**
- Module: Image utilities
- Feature: Image preprocessing functions
- Deliverable: `core/image_utils.py`

---

### **Minggu 2: Face Detection**
**Learning Goals:**
- Haar Cascade Classifier
- Face detection dari gambar dan webcam
- Multiple face detection
- Performance optimization

**Project Development:**
- Module: Face detection service
- Feature: Detection API endpoint
- Deliverable: `core/face_detector.py`, `api/detection.py`

---

### **Minggu 3: Face Recognition**
**Learning Goals:**
- face_recognition library
- Face encodings & comparison
- Distance calculation
- Unknown face handling

**Project Development:**
- Module: Recognition engine
- Feature: Face matching algorithm
- Deliverable: `core/face_recognizer.py`, `api/recognition.py`

---

### **Minggu 4: Dataset Management**
**Learning Goals:**
- Dataset collection system
- Data augmentation
- Quality validation
- Folder structure

**Project Development:**
- Module: Dataset manager
- Feature: Person registration API
- Deliverable: `core/dataset_manager.py`, `api/persons.py`

---

### **Minggu 5: Database & Models**
**Learning Goals:**
- Database design (PostgreSQL/SQLite)
- ORM dengan SQLAlchemy
- Migration system
- Query optimization

**Project Development:**
- Module: Database models & services
- Feature: CRUD operations API
- Deliverable: `models/`, `services/database.py`, `api/crud.py`

---

### **Minggu 6: REST API & Business Logic**
**Learning Goals:**
- Flask REST API development
- Request/Response handling
- Authentication & authorization
- Error handling

**Project Development:**
- Module: Complete REST API
- Feature: Attendance tracking API
- Deliverable: `api/attendance.py`, `api/reports.py`, `app.py`

---

### **Minggu 7: Frontend Development**
**Learning Goals:**
- HTML/CSS/JavaScript basics
- AJAX requests
- Responsive design
- UI/UX principles

**Project Development:**
- Module: Web interface
- Feature: Admin panel & user interface
- Deliverable: `templates/`, `static/`, frontend integration

---

### **Minggu 8: Testing & Deployment**
**Learning Goals:**
- Unit testing & integration testing
- Test coverage dengan pytest
- Cloud deployment (Railway/Render/Heroku)
- Production configuration
- Performance optimization

**Project Development:**
- Module: Tests & deployment configs
- Feature: Production-ready application
- Deliverable: Complete deployed web application

---

## Teknologi yang Digunakan

### Backend
```
Python 3.8+
Flask 2.3+
SQLAlchemy 2.0+
PostgreSQL / SQLite
opencv-python 4.8+
face-recognition 1.3+
```

### Frontend
```
HTML5
CSS3 (Bootstrap 5)
JavaScript (Vanilla JS / jQuery)
AJAX for API calls
```

### Deployment
```
Gunicorn (Production server)
Railway / Render / Heroku
PostgreSQL (Production database)
```

---

## Instalasi & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd ExtraQueensya
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
python init_db.py
```

### 5. Run Development Server
```bash
python app.py
```

Access at: `http://localhost:5000`

---

## Struktur Project

```
ExtraQueensya/
│
├── app.py                          # Main Flask application
├── config.py                       # Configuration
├── requirements.txt                # Dependencies
├── init_db.py                      # Database initialization
│
├── core/                           # Core modules
│   ├── image_utils.py             # Image processing utilities
│   ├── face_detector.py           # Face detection
│   ├── face_recognizer.py         # Face recognition
│   └── dataset_manager.py         # Dataset management
│
├── models/                         # Database models
│   ├── person.py
│   └── attendance.py
│
├── services/                       # Business logic
│   ├── database.py
│   ├── recognition_service.py
│   └── attendance_service.py
│
├── api/                            # API endpoints
│   ├── detection.py
│   ├── recognition.py
│   ├── persons.py
│   ├── attendance.py
│   └── reports.py
│
├── templates/                      # HTML templates
│   ├── index.html
│   ├── admin.html
│   ├── attendance.html
│   └── reports.html
│
├── static/                         # Static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── tests/                          # Test files
│   ├── test_detection.py
│   ├── test_recognition.py
│   └── test_api.py
│
├── data/                           # Data storage
│   ├── dataset/
│   ├── encodings/
│   └── database/
│
└── minggu-X/                       # Weekly learning materials
    ├── learning/                   # Tutorial & exercises
    └── project/                    # Progressive project code
```

---

## Cara Menggunakan

### Untuk Pembelajaran (8 Minggu)
1. Ikuti folder `minggu-X/learning/` secara berurutan
2. Kerjakan latihan di setiap minggu
3. Build project secara progressive di `minggu-X/project/`
4. Integrasikan ke main app setiap minggu

### Development Workflow
```bash
# Week 1-7: Develop features
cd minggu-X/project
python <module>.py  # Test module

# Integrate to main app
cp minggu-X/project/<module>.py core/

# Week 8: Deploy
gunicorn app:app --bind 0.0.0.0:5000
```

---

## API Documentation

### Endpoints

**Authentication**
- POST `/api/auth/login` - Login
- POST `/api/auth/logout` - Logout

**Persons**
- GET `/api/persons` - List all persons
- POST `/api/persons` - Register new person
- GET `/api/persons/<id>` - Get person details
- PUT `/api/persons/<id>` - Update person
- DELETE `/api/persons/<id>` - Delete person

**Attendance**
- POST `/api/attendance/checkin` - Check-in with face recognition
- GET `/api/attendance/today` - Today's attendance
- GET `/api/attendance/history` - Attendance history

**Reports**
- GET `/api/reports/daily` - Daily report
- GET `/api/reports/monthly` - Monthly report
- GET `/api/reports/export` - Export to Excel

---

## Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_recognition.py

# With coverage
pytest --cov=core tests/
```

---

## Deployment

### Deploy to Railway (Recommended)
```bash
# 1. Create account at railway.app
# 2. Install Railway CLI
npm i -g @railway/cli

# 3. Login and deploy
railway login
railway init
railway up

# 4. Add PostgreSQL
railway add postgresql

# 5. Set environment variables in Railway dashboard
```

### Deploy to Render
```bash
# 1. Create account at render.com
# 2. Connect GitHub repository
# 3. Create Web Service
# 4. Add PostgreSQL database
# 5. Set environment variables
# Build command: pip install -r requirements.txt
# Start command: gunicorn app:app
```

### Deploy to Heroku
```bash
# 1. Install Heroku CLI
# 2. Login and create app
heroku login
heroku create your-app-name

# 3. Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 4. Deploy
git push heroku main

# 5. Initialize database
heroku run alembic upgrade head
```

---

## Expected Results

Setelah 8 minggu:
- Working web application dengan face recognition
- REST API untuk integration
- Database dengan 200+ persons capacity
- Real-time attendance tracking
- Responsive web interface
- Production deployment
- Complete documentation
- Test coverage > 80%

---

## Learning Path

### Beginner (8 Weeks)
- Follow week-by-week tutorials
- Complete all exercises
- Build project progressively
- Deploy at week 8

### Intermediate (3-4 Weeks)
- Skip to project development
- Focus on integration
- Deploy early, iterate fast

### Advanced (1-2 Weeks)
- Review architecture
- Customize features
- Deploy and optimize

---

## Tech Stack Skills

By completing this project:
- Python programming
- Computer Vision (OpenCV)
- Machine Learning (Face Recognition)
- Web Development (Flask)
- REST API design
- Database design (SQL)
- Frontend development (HTML/CSS/JS)
- Cloud Deployment (Railway/Render/Heroku)
- Testing & Quality Assurance

---

## Contributing

This is a learning project. Feedback welcome!

---

## License

Educational purposes.

---

**Last Updated: November 2025**
