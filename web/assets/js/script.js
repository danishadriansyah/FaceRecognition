// ===========================
// Smooth Scrolling
// ===========================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            
            // Update active nav link
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            this.classList.add('active');
        }
    });
});

// ===========================
// Week Detail Content
// ===========================
const weekDetails = {
    1: {
        title: "Minggu 1: Python Basics & OpenCV",
        difficulty: "🟢 Easy",
        duration: "6-7 hari",
        tutorials: "5 tutorials",
        objectives: [
            "Setup development environment",
            "Memahami Python fundamentals untuk CV",
            "Mengenal OpenCV library",
            "Image manipulation & processing",
            "Build reusable image utilities"
        ],
        topics: [
            {
                title: "01. Hello OpenCV",
                description: "Installation & setup, reading/displaying/saving images, image as numpy arrays, color spaces (BGR, RGB, Grayscale)"
            },
            {
                title: "02. Image Operations",
                description: "Resize, crop, rotate, flip images. Color conversion dan transformasi dasar"
            },
            {
                title: "03. Drawing Shapes",
                description: "Draw rectangles, circles, lines, dan text pada images"
            },
            {
                title: "04. Webcam Basics",
                description: "Access webcam, capture frames, real-time processing, frame rate optimization"
            },
            {
                title: "05. Latihan",
                description: "Mini project kombinasi semua materi week 1"
            }
        ],
        module: "image_utils.py",
        moduleFunctions: [
            "load_image(path) - Load dan validate image",
            "resize_image(image, width, height) - Resize dengan aspect ratio",
            "preprocess_image(image) - Standardize image untuk processing",
            "convert_to_grayscale(image) - Convert color space",
            "save_image(image, path) - Save dengan compression",
            "validate_image_quality(image) - Check blur, brightness, etc"
        ],
        keyconcepts: [
            "Image = Matrix of Pixels (Grayscale: 1 channel, Color: 3 channels)",
            "OpenCV coordinate system: (0,0) di top-left",
            "BGR vs RGB color space",
            "Numpy arrays untuk manipulasi image"
        ],
        commands: `cd minggu-1-python-basics/learning
python 01_hello_opencv.py
python 02_image_operations.py
python 03_drawing_shapes.py
python 04_webcam_basics.py
python latihan.py

cd ../project
python test_utils.py`
    },
    2: {
        title: "Minggu 2: Face Detection",
        difficulty: "🟡 Medium",
        duration: "6-7 hari",
        tutorials: "4 tutorials",
        objectives: [
            "Memahami konsep face detection",
            "Menggunakan Haar Cascade Classifier",
            "Mendeteksi wajah dari gambar dan webcam",
            "Multiple face detection",
            "Parameter tuning untuk akurasi optimal"
        ],
        topics: [
            {
                title: "01. Face Detection dari Image",
                description: "Load Haar Cascade, detect faces dari gambar statis, draw bounding boxes, save hasil detection"
            },
            {
                title: "02. Face Detection Webcam",
                description: "Real-time face detection dari webcam feed, handle multiple faces, FPS optimization"
            },
            {
                title: "03. Eye Detection",
                description: "Deteksi mata dari region wajah, ROI (Region of Interest) processing"
            },
            {
                title: "04. Advanced Detection",
                description: "Parameter tuning (scaleFactor, minNeighbors, minSize), optimizing untuk berbagai kondisi"
            }
        ],
        module: "face_detector.py",
        moduleFunctions: [
            "FaceDetector class - Face detection dengan Haar Cascade",
            "detect_faces() - Detect faces dari image",
            "detect_faces_webcam() - Real-time detection",
            "draw_detections() - Draw bounding boxes",
            "get_face_regions() - Extract face ROIs",
            "validate_detection() - Quality validation"
        ],
        keyconcepts: [
            "Haar Cascade: Machine Learning based object detection",
            "Pre-trained dengan ribuan images",
            "Fast detection (real-time capable)",
            "detectMultiScale parameters: scaleFactor, minNeighbors, minSize",
            "Grayscale conversion untuk detection"
        ],
        commands: `cd minggu-2-face-detection/learning
python 01_face_detection_image.py
python 02_face_detection_webcam.py
python 03_eye_detection.py
python 04_advanced_detection.py

cd ../project
python test_detector.py`
    },
    3: {
        title: "Minggu 3: Face Recognition",
        difficulty: "🟠 Medium",
        duration: "7-8 hari",
        tutorials: "3 tutorials",
        objectives: [
            "Memahami face recognition vs face detection",
            "Menggunakan face_recognition library",
            "Face encodings dan comparison",
            "Build recognition system",
            "Known faces database management"
        ],
        topics: [
            {
                title: "01. Face Encodings",
                description: "Generate face encodings (128-dimension vectors), understand face representation"
            },
            {
                title: "02. Face Comparison",
                description: "Compare face encodings, face_distance() dan face_compare(), tolerance levels"
            },
            {
                title: "03. Recognition Webcam",
                description: "Real-time face recognition dari webcam, identify unknown vs known faces"
            }
        ],
        module: "face_recognizer.py",
        moduleFunctions: [
            "FaceRecognizer class - Main recognition engine",
            "encode_face() - Generate face encoding",
            "recognize_face() - Identify person from encoding",
            "add_known_face() - Add to known faces database",
            "get_all_encodings() - Export encodings",
            "calculate_confidence() - Recognition confidence score"
        ],
        keyconcepts: [
            "Face encodings: 128-dimension vector representation",
            "Unique untuk setiap wajah",
            "Face distance: Lower distance = more similar",
            "Typical threshold: 0.6",
            "Invariant terhadap lighting dan angle (dengan batasan)"
        ],
        commands: `cd minggu-3-face-recognition/learning
python 01_face_encodings.py
python 02_face_comparison.py
python 03_recognition_webcam.py

cd ../project
python test_recognizer.py`
    },
    4: {
        title: "Minggu 4: Dataset Collection",
        difficulty: "🔴 Medium-Hard",
        duration: "6-7 hari",
        tutorials: "3 tutorials",
        objectives: [
            "Systematic face data collection",
            "Multiple angles dan lighting conditions",
            "Dataset organization",
            "Data quality validation",
            "Dataset management system"
        ],
        topics: [
            {
                title: "01. Capture Faces",
                description: "Basic face capture dari webcam, validation checks, save organized dataset"
            },
            {
                title: "02. Multi-Angle Capture",
                description: "Capture multiple angles (frontal, left, right), lighting variation, quality metrics"
            },
            {
                title: "03. Batch Processing",
                description: "Process multiple images sekaligus, dataset validation, encoding generation"
            }
        ],
        module: "dataset_manager.py",
        moduleFunctions: [
            "DatasetManager class - Manage face datasets",
            "capture_face() - Capture with validation",
            "add_person() - Add new person to dataset",
            "remove_person() - Remove person from dataset",
            "get_person_images() - Get all images for person",
            "validate_dataset() - Check dataset quality",
            "export_encodings() - Generate encodings for dataset"
        ],
        keyconcepts: [
            "Dataset structure: person folders dengan multiple images",
            "Multiple angles: frontal, left profile, right profile",
            "Quality validation: lighting, blur, face size",
            "Metadata management: person info, capture timestamps",
            "Encoding caching untuk performance"
        ],
        commands: `cd minggu-4-dataset-collection/learning
python 01_capture_faces.py
python 02_multi_angle_capture.py
python 03_batch_processing.py

cd ../project
python test_dataset.py`
    },
    5: {
        title: "Minggu 5: Recognition System",
        difficulty: "🟣 Hard",
        duration: "6-7 hari",
        tutorials: "2 tutorials",
        objectives: [
            "Integrate semua module minggu 1-4",
            "Build complete recognition pipeline",
            "Performance optimization",
            "Error handling dan logging",
            "Service layer architecture"
        ],
        topics: [
            {
                title: "01. Pipeline Integration",
                description: "Integrate detection + recognition, complete workflow dari input ke output"
            },
            {
                title: "02. Recognition Service",
                description: "Service layer implementation, caching strategies, batch processing, performance optimization"
            }
        ],
        module: "recognition_service.py",
        moduleFunctions: [
            "RecognitionService class - Main service",
            "process_image() - Full recognition pipeline",
            "process_webcam_frame() - Real-time processing",
            "batch_recognize() - Process multiple images",
            "get_statistics() - Performance metrics",
            "reload_database() - Refresh known faces"
        ],
        keyConcepts: [
            "Pipeline: Input → Preprocess → Detect → Recognize → Output",
            "Service layer pattern untuk separation of concerns",
            "Caching encodings untuk speed improvement",
            "Batch processing untuk efficiency",
            "Error handling best practices"
        ],
        architecture: `Input Image
    ↓
Image Utils (preprocess)
    ↓
Face Detector (detect faces)
    ↓
Face Recognizer (identify)
    ↓
Dataset Manager (match to database)
    ↓
Recognition Result`,
        commands: `cd minggu-5-recognition-system/learning
python 01_pipeline_integration.py
python 02_recognition_service.py

cd ../project
python test_service.py`
    },
    6: {
        title: "Minggu 6: Database & Attendance",
        difficulty: "🔵 Hard",
        duration: "7-8 hari",
        tutorials: "3 tutorials",
        objectives: [
            "Setup database MySQL",
            "Database models dan relationships",
            "Attendance record management",
            "CRUD operations",
            "Query dan reporting"
        ],
        topics: [
            {
                title: "01. Database Setup",
                description: "MySQL & SQLAlchemy setup, connection configuration, database creation"
            },
            {
                title: "02. Models SQLAlchemy",
                description: "Define database models (Person, Attendance), relationships, migrations"
            },
            {
                title: "03. CRUD & Attendance",
                description: "Create, Read, Update, Delete operations. Attendance logic, duplicate prevention, reporting"
            }
        ],
        modules: [
            "models.py - Database models (Person, Attendance, FaceEncoding)",
            "database.py - MySQL connection, session management, migrations",
            "attendance_service.py - Attendance business logic"
        ],
        moduleFunctions: [
            "AttendanceService class",
            "record_attendance() - Record check-in/check-out",
            "get_attendance_today() - Today's records",
            "get_person_attendance() - Person's attendance history",
            "generate_report() - Attendance reports",
            "check_duplicate() - Prevent duplicate entries"
        ],
        databaseSchema: `Person:
- id (PK)
- name
- employee_id
- department
- created_at

Attendance:
- id (PK)
- person_id (FK)
- timestamp
- type (check_in/check_out)
- photo_path
- confidence

FaceEncoding:
- id (PK)
- person_id (FK)
- encoding_data
- created_at`,
        commands: `cd minggu-6-database-attendance/learning
python 01_database_setup.py
python 02_models_sqlalchemy.py
python 03_crud_operations.py

cd ../project
python test_database.py`
    },
    7: {
        title: "Minggu 7: Desktop GUI",
        difficulty: "🟤 Medium",
        duration: "5-6 hari",
        tutorials: "2 tutorials",
        objectives: [
            "Build desktop interface dengan Tkinter",
            "GUI design principles",
            "Event-driven programming",
            "Multi-window application",
            "Real-time webcam preview di GUI"
        ],
        topics: [
            {
                title: "01. Tkinter Basics",
                description: "Tkinter fundamentals (widgets, layouts), event handling, layout managers (grid, pack)"
            },
            {
                title: "02. Webcam Preview & Multi-Windows",
                description: "Embed webcam di Tkinter Canvas, multiple windows, threading untuk non-blocking GUI"
            }
        ],
        guiWindows: [
            {
                name: "Main Window",
                features: "Live webcam preview, face detection boxes, recognition status, action buttons (Register, Reports)"
            },
            {
                name: "Register Person Window",
                features: "Person info form, webcam preview, capture photos (20+), auto quality validation, progress indicator"
            },
            {
                name: "Attendance Window",
                features: "Real-time recognition, person info display, check-in time, manual override button"
            },
            {
                name: "Reports Window",
                features: "Date range picker, filter by person/department, attendance table, export (Excel/CSV)"
            }
        ],
        keyTechnologies: [
            "Tkinter: Built-in Python GUI framework",
            "Threading: Non-blocking webcam feed",
            "PIL/Pillow: Display images di Canvas",
            "ttk: Modern themed widgets",
            "Queue: Thread-safe communication"
        ],
        commands: `cd minggu-7-desktop-gui/learning
python 01_tkinter_basics.py
python 02_layout_management.py
python 03_webcam_preview.py
python 04_multi_windows.py

cd ../project
python main_app.py`
    },
    8: {
        title: "Minggu 8: Final Testing & Distribution",
        difficulty: "⚫ Medium",
        duration: "5-6 hari",
        tutorials: "3 tutorials",
        objectives: [
            "Polish UI/UX desktop application",
            "Error handling & validations",
            "Unit testing dengan pytest",
            "Create executable dengan PyInstaller",
            "Application distribution"
        ],
        topics: [
            {
                title: "01. UI Polish",
                description: "UI improvements (colors, fonts, icons, themes), user experience optimization"
            },
            {
                title: "02. Error Handling",
                description: "Robust error handling, user-friendly error messages, edge case handling"
            },
            {
                title: "03. Unit Testing & PyInstaller",
                description: "Unit tests dengan pytest, test coverage >70%, create .exe dengan PyInstaller"
            }
        ],
        testingModules: [
            "tests/test_core.py - Image utils, detector, recognizer tests",
            "tests/test_database.py - SQLite operations, CRUD tests",
            "tests/test_recognition.py - Recognition service, attendance logic",
            "tests/test_integration.py - End-to-end workflow tests"
        ],
        distribution: [
            "Option 1: Python Environment (development)",
            "Option 2: Executable (.exe) - PyInstaller --onefile",
            "Option 3: Portable Bundle - PyInstaller --onedir (recommended)"
        ],
        pyinstallerCommands: `# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onedir --windowed --name="AttendanceSystem" main_app.py

# With custom icon
pyinstaller --onedir --windowed --icon=icon.ico --name="AttendanceSystem" main_app.py`,
        deliverables: [
            "✅ Polished desktop application",
            "✅ All tests passing with >70% coverage",
            "✅ Executable file (.exe for Windows)",
            "✅ User manual & developer guide",
            "✅ READY-TO-DISTRIBUTE APPLICATION"
        ],
        commands: `cd minggu-8-final-testing/learning
python 01_ui_polish.py
python 02_error_handling.py
python 03_unit_testing.py

# Run all tests
pytest
pytest --cov=core --cov-report=html

# Create executable
pyinstaller build_exe.spec`
    }
};

// ===========================
// Show Week Detail Modal
// ===========================
function showWeekDetail(weekNumber) {
    const modal = document.getElementById('weekModal');
    const content = document.getElementById('weekDetailContent');
    const week = weekDetails[weekNumber];
    
    if (!week) return;
    
    let html = `
        <h2>${week.title}</h2>
        <div class="week-meta" style="justify-content: center; margin-bottom: 2rem;">
            <span style="font-size: 1rem;">${week.difficulty}</span>
            <span style="font-size: 1rem;">📝 ${week.tutorials}</span>
            <span style="font-size: 1rem;">⏱️ ${week.duration}</span>
        </div>
        
        <div class="card" style="margin-bottom: 1.5rem;">
            <h3>🎯 Objectives</h3>
            <ul>
                ${week.objectives.map(obj => `<li>✅ ${obj}</li>`).join('')}
            </ul>
        </div>
        
        <div class="card" style="margin-bottom: 1.5rem;">
            <h3>📚 Topics & Tutorials</h3>
            ${week.topics.map((topic, index) => `
                <div style="margin-bottom: 1rem; padding: 1rem; background: var(--bg-light); border-radius: var(--radius-md);">
                    <h4 style="color: var(--primary); margin-bottom: 0.5rem;">${topic.title}</h4>
                    <p style="color: var(--text-light); margin: 0;">${topic.description}</p>
                </div>
            `).join('')}
        </div>
    `;
    
    if (week.module) {
        html += `
            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>📦 Project Module: <code>${week.module}</code></h3>
                <ul>
                    ${week.moduleFunctions.map(func => `<li>${func}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (week.modules) {
        html += `
            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>📦 Project Modules</h3>
                <ul>
                    ${week.modules.map(mod => `<li>${mod}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (week.guiWindows) {
        html += `
            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>🖥️ GUI Windows</h3>
                ${week.guiWindows.map(window => `
                    <div style="margin-bottom: 1rem; padding: 1rem; background: var(--bg-light); border-radius: var(--radius-md);">
                        <h4 style="color: var(--primary); margin-bottom: 0.5rem;">${window.name}</h4>
                        <p style="color: var(--text-light); margin: 0;">${window.features}</p>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    if (week.keyTechnologies) {
        html += `
            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>⚡ Key Technologies</h3>
                <ul>
                    ${week.keyTechnologies.map(tech => `<li>${tech}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (week.testingModules) {
        html += `
            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>🧪 Testing Modules</h3>
                <ul>
                    ${week.testingModules.map(test => `<li>${test}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (week.distribution) {
        html += `
            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>📦 Distribution Options</h3>
                <ul>
                    ${week.distribution.map(opt => `<li>${opt}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (week.databaseSchema) {
        html += `
            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>🗄️ Database Schema</h3>
                <pre><code>${week.databaseSchema}</code></pre>
            </div>
        `;
    }
    
    if (week.architecture) {
        html += `
            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>🏗️ Architecture</h3>
                <pre><code>${week.architecture}</code></pre>
            </div>
        `;
    }
    
    if (week.keyConcepts || week.keypoints) {
        const concepts = week.keyConcepts || week.keypoints;
        html += `
            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>💡 Key Concepts</h3>
                <ul>
                    ${concepts.map(concept => `<li>${concept}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (week.pyinstallerCommands) {
        html += `
            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>📦 PyInstaller Commands</h3>
                <pre><code>${week.pyinstallerCommands}</code></pre>
            </div>
        `;
    }
    
    if (week.deliverables) {
        html += `
            <div class="card" style="margin-bottom: 1.5rem;">
                <h3>✅ Deliverables</h3>
                <ul>
                    ${week.deliverables.map(item => `<li>${item}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    html += `
        <div class="card">
            <h3>🚀 Cara Menjalankan</h3>
            <pre><code>${week.commands}</code></pre>
        </div>
    `;
    
    content.innerHTML = html;
    modal.classList.add('show');
    document.body.style.overflow = 'hidden'; // Prevent scrolling
}

// ===========================
// Close Modal
// ===========================
function closeModal() {
    const modal = document.getElementById('weekModal');
    modal.classList.remove('show');
    document.body.style.overflow = 'auto'; // Restore scrolling
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('weekModal');
    if (event.target == modal) {
        closeModal();
    }
}

// Close modal with ESC key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});

// ===========================
// Navigation Active State
// ===========================
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('.section, .hero');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 100) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// ===========================
// Loading Animation (Optional)
// ===========================
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
});

console.log('🎓 Face Recognition Learning Platform Loaded!');
console.log('📚 8 Weeks of Progressive Learning');
console.log('💻 Ready to build Face Recognition Attendance System!');
