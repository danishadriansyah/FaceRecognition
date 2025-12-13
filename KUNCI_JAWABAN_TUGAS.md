# 🔐 KUNCI JAWABAN - Fill in the Blanks Tugas

> **⚠️ PERINGATAN:** File ini berisi kunci jawaban untuk semua tugas. Gunakan hanya untuk verifikasi setelah mencoba sendiri!

---

## 📝 MINGGU 1 - Photo Editor (13 Soal)

**File:** `minggu-1-python-basics/tugas/photo_editor_template.py`

| Soal | Blank | Jawaban |
|------|-------|---------|
| 1 | Import OpenCV | `import cv2` |
| 2 | Load image | `cv2.imread(image_path)` |
| 3 | Save image | `cv2.imwrite(output_path, image)` |
| 4 | Convert to grayscale | `cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)` |
| 5 | Resize image | `cv2.resize(image, (new_width, new_height))` |
| 6 | Rotate 90° clockwise | `cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)` |
| 7 | Flip horizontal | `cv2.flip(image, 1)` |
| 8 | Get image dimensions | `image.shape` |
| 9 | Crop image | `image[y:y+h, x:x+w]` |
| 10 | Draw rectangle | `cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)` |
| 11 | Put text | `cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)` |
| 12 | Check if image loaded | `if image is None:` |
| 13 | Create output directory | `os.makedirs(output_dir, exist_ok=True)` |

---

## 👤 MINGGU 2 - Face Detector (10 Soal)

**File:** `minggu-2-face-detection/tugas/face_detector_template.py`

| Soal | Blank | Jawaban |
|------|-------|---------|
| 1 | Load Haar Cascade | `cv2.CascadeClassifier('haarcascade_frontalface_default.xml')` |
| 2 | Convert to grayscale | `cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)` |
| 3 | Detect faces | `face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)` |
| 4 | Loop through faces | `for (x, y, w, h) in faces:` |
| 5 | Draw rectangle | `cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)` |
| 6 | Put face count text | `cv2.putText(image, f'Faces: {len(faces)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)` |
| 7 | Open webcam | `cv2.VideoCapture(0)` |
| 8 | Read frame | `ret, frame = cap.read()` |
| 9 | Check if frame valid | `if not ret:` |
| 10 | Release webcam | `cap.release()` |

---

## 🎭 MINGGU 3 - Face Recognition (8 Soal)

**File:** `minggu-3-face-recognition/tugas/face_recognition_template.py`

| Soal | Blank | Jawaban |
|------|-------|---------|
| 1 | Import FaceRecognizer | `from face_recognizer import FaceRecognizer` |
| 2 | Create recognizer instance | `recognizer = FaceRecognizer()` |
| 3 | Encode faces folder | `encodings = recognizer.encode_faces_in_folder('known_faces')` |
| 4 | Save with pickle | `pickle.dump(encodings, f)` |
| 5 | Load encodings | `encodings = pickle.load(f)` |
| 6 | Load recognizer encodings | `recognizer.known_face_encodings = encodings` |
| 7 | Recognize faces in image | `results = recognizer.recognize_faces_in_image(test_image_path)` |
| 8 | Get person name | `name = result['name']` |

---

## 📁 MINGGU 4 - Dataset Manager (6 Soal)

**File:** `minggu-4-dataset-collection/tugas/dataset_manager_template.py`

| Soal | Blank | Jawaban |
|------|-------|---------|
| 1 | Import DatasetManager | `from dataset_manager import DatasetManager` |
| 2 | Open webcam | `cap = cv2.VideoCapture(0)` |
| 3 | Add face to dataset | `manager.add_face(person_name, frame)` |
| 4 | Get dataset statistics | `stats = manager.get_statistics()` |
| 5 | Export dataset | `manager.export_dataset(export_path)` |
| 6 | Backup dataset | `shutil.copytree(source_dir, backup_dir)` |

---

## 🔍 MINGGU 5 - Recognition Service (5 Soal)

**File:** `minggu-5-recognition-system/tugas/recognition_test_template.py`

| Soal | Blank | Jawaban |
|------|-------|---------|
| 1 | Import RecognitionService | `from recognition_service import RecognitionService` |
| 2 | Load database | `service.load_database('dataset/encodings.pkl')` |
| 3 | Process single image | `results = service.process_image('test.jpg')` |
| 4 | Start webcam recognition | `service.start_webcam()` |
| 5 | Process folder batch | `service.process_folder('test_images/', 'output/')` |

---

## 📊 MINGGU 6 - Attendance System (6 Soal)

**File:** `minggu-6-database-attendance/tugas/attendance_test_template.py`

| Soal | Blank | Jawaban |
|------|-------|---------|
| 1 | Import AttendanceSystem | `from attendance_system import AttendanceSystem` |
| 2 | Check in employee | `attendance.check_in(person_name, confidence)` |
| 3 | Check out employee | `attendance.check_out(person_name)` |
| 4 | Get today records | `records = attendance.get_today_records()` |
| 5 | Generate monthly report | `report = attendance.generate_report(year, month)` |
| 6 | Export to Excel | `attendance.export_to_excel(output_path, start_date, end_date)` |

---

## 🖥️ MINGGU 7 - Desktop GUI (8 Soal)

**File:** `minggu-7-desktop-gui/tugas/attendance_gui_template.py`

| Soal | Blank | Jawaban |
|------|-------|---------|
| 1 | Create main window | `root = tk.Tk()` |
| 2 | Show error message | `messagebox.showerror('Error', error_message)` |
| 3 | Show success message | `messagebox.showinfo('Success', success_message)` |
| 4 | Get table rows | `table.get_children()` |
| 5 | Insert row to table | `table.insert('', 'end', values=(col1, col2, col3))` |
| 6 | Create label | `label = tk.Label(parent, text='Label Text')` |
| 7 | Create entry/input | `entry = tk.Entry(parent)` |
| 8 | Create button | `button = tk.Button(parent, text='Click', command=callback)` |

---

## 📚 Tips Penggunaan Kunci Jawaban:

### ✅ DO (Lakukan):
1. **Coba dulu sendiri** minimal 10-15 menit
2. Gunakan untuk **verifikasi** setelah selesai
3. **Pelajari konsepnya**, jangan hanya copy-paste
4. **Bandingkan** dengan jawaban kamu

### ❌ DON'T (Jangan):
1. Langsung lihat kunci jawaban tanpa mencoba
2. Copy-paste tanpa memahami
3. Skip membaca README/TUGAS.md
4. Lupa test code setelah mengisi

---

## 🎯 Cara Belajar Efektif:

```
1. Baca TUGAS.md/README.md → Pahami soal
2. Coba isi blanks sendiri → Gunakan hints
3. Test & debug → Perbaiki error
4. Stuck > 15 menit? → Cek 1 jawaban di kunci
5. Selesai semua → Bandingkan dengan kunci
6. Pahami perbedaan → Catat yang belum paham
```

---

## 🔍 Resource Tambahan:

- **OpenCV Docs:** https://docs.opencv.org/
- **MediaPipe:** https://google.github.io/mediapipe/
- **Tkinter Guide:** https://docs.python.org/3/library/tkinter.html
- **Python Pickle:** https://docs.python.org/3/library/pickle.html

---

**💡 Remember:** Tujuan tugas bukan mendapat nilai 100, tapi **memahami konsep**!

Jika stuck, coba:
1. Baca error message dengan teliti
2. Print variable untuk debug
3. Baca dokumentasi function
4. Tanya ChatGPT dengan konteks lengkap
5. **Terakhir** baru lihat kunci jawaban

**Good luck & happy coding! 🚀**
