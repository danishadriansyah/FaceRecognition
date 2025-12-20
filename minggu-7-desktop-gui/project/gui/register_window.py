"""
Register Window - Desktop GUI
Week 7 Project Module

Window for registering new persons with photo capture
"""
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
from pathlib import Path
import numpy as np


class RegisterWindow:
    """Register person window"""
    
    def __init__(self, parent, main_window):
        """Initialize register window"""
        self.parent = parent
        self.main_window = main_window
        
        # Create top-level window
        self.window = tk.Toplevel(parent)
        self.window.title("Register New Person")
        self.window.geometry("900x650")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Variables
        self.person_name = tk.StringVar()
        self.person_id = tk.StringVar()
        self.department = tk.StringVar()
        self.email = tk.StringVar()
        
        self.captured_photos = []
        self.target_photos = 20
        self.is_capturing = False
        
        # Webcam
        self.cap = None
        self.webcam_running = False
        
        # Create UI
        self.create_ui()
        self.start_webcam()
    
    def create_ui(self):
        """Create UI components"""
        # Title
        title_frame = tk.Frame(self.window, bg="#4CAF50", height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="📝 Register New Person",
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=12)
        
        # Main container
        container = tk.Frame(self.window)
        container.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)
        
        # Left panel - Form
        left_panel = tk.Frame(container, width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_form(left_panel)
        
        # Right panel - Webcam
        right_panel = tk.Frame(container)
        right_panel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        self.create_webcam_panel(right_panel)
    
    def create_form(self, parent):
        """Create registration form"""
        form_frame = tk.LabelFrame(
            parent,
            text="Person Information",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name
        tk.Label(form_frame, text="Full Name *", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        tk.Entry(form_frame, textvariable=self.person_name, font=("Arial", 10), width=30).pack(pady=(0, 15))
        
        # ID
        tk.Label(form_frame, text="ID Number", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        tk.Entry(form_frame, textvariable=self.person_id, font=("Arial", 10), width=30).pack(pady=(0, 15))
        
        # Department
        tk.Label(form_frame, text="Department", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        tk.Entry(form_frame, textvariable=self.department, font=("Arial", 10), width=30).pack(pady=(0, 15))
        
        # Email
        tk.Label(form_frame, text="Email", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        tk.Entry(form_frame, textvariable=self.email, font=("Arial", 10), width=30).pack(pady=(0, 15))
        
        # Progress
        progress_frame = tk.LabelFrame(form_frame, text="Capture Progress", padx=10, pady=10)
        progress_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.progress_label = tk.Label(
            progress_frame,
            text=f"0 / {self.target_photos} photos",
            font=("Arial", 12, "bold"),
            fg="#2196F3"
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            length=250,
            mode='determinate',
            maximum=self.target_photos
        )
        self.progress_bar.pack(pady=10)
        
        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.pack(pady=20)
        
        self.capture_btn = tk.Button(
            btn_frame,
            text="Start Capture",
            command=self.toggle_capture,
            width=15,
            height=2,
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            cursor="hand2"
        )
        self.capture_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = tk.Button(
            btn_frame,
            text="Save Person",
            command=self.save_person,
            width=15,
            height=2,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            cursor="hand2",
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
    
    def create_webcam_panel(self, parent):
        """Create webcam preview panel"""
        webcam_frame = tk.LabelFrame(
            parent,
            text="Camera Preview",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        webcam_frame.pack(expand=True, fill=tk.BOTH)
        
        self.webcam_label = tk.Label(webcam_frame, bg="black")
        self.webcam_label.pack(expand=True, fill=tk.BOTH)
        
        # Instructions
        instructions = tk.Label(
            parent,
            text="💡 Look at the camera and keep your face visible\n"
                 "📸 Click 'Start Capture' to begin automatic photo capture",
            font=("Arial", 9),
            fg="#666666",
            justify=tk.LEFT
        )
        instructions.pack(pady=10)
    
    def start_webcam(self):
        """Start webcam"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Webcam Error", "Cannot open webcam")
                return
            
            self.webcam_running = True
            threading.Thread(target=self.update_webcam, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Webcam Error", f"Failed to start webcam: {str(e)}")
    
    def update_webcam(self):
        """Update webcam feed"""
        frame_count = 0
        last_capture = time.time()
        
        while self.webcam_running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Detect faces
                faces = []
                if self.main_window.recognition_service:
                    faces = self.main_window.recognition_service.detector.detect_faces(frame)
                
                # Auto capture if enabled
                if self.is_capturing and faces and len(self.captured_photos) < self.target_photos:
                    current_time = time.time()
                    if current_time - last_capture > 0.5:  # Capture every 0.5s
                        # Save photo
                        self.captured_photos.append(frame.copy())
                        self.update_progress()
                        last_capture = current_time
                        
                        # Check if done
                        if len(self.captured_photos) >= self.target_photos:
                            self.is_capturing = False
                            self.capture_btn.config(text="Start Capture")
                            self.save_btn.config(state=tk.NORMAL)
                            self.window.after(0, lambda: messagebox.showinfo(
                                "Complete",
                                f"Captured {self.target_photos} photos!\nClick 'Save Person' to register."
                            ))
                
                # Draw face boxes
                for face in faces:
                    x, y, w, h = face  # face is tuple (x, y, w, h)
                    color = (0, 255, 0) if self.is_capturing else (255, 255, 0)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    
                    if self.is_capturing:
                        cv2.putText(
                            frame,
                            "CAPTURING",
                            (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 0),
                            2
                        )
                
                # Convert to PhotoImage
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (480, 360))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update label
                self.webcam_label.imgtk = imgtk
                self.webcam_label.configure(image=imgtk)
                
                time.sleep(0.03)
            except Exception as e:
                print(f"Webcam error: {e}")
                break
    
    def toggle_capture(self):
        """Toggle photo capture"""
        if not self.person_name.get().strip():
            messagebox.showwarning("Validation", "Please enter person name first")
            return
        
        if not self.is_capturing:
            # Start capture
            self.captured_photos = []
            self.is_capturing = True
            self.capture_btn.config(text="Stop Capture", bg="#f44336")
            self.save_btn.config(state=tk.DISABLED)
            self.update_progress()
        else:
            # Stop capture
            self.is_capturing = False
            self.capture_btn.config(text="Start Capture", bg="#2196F3")
            if len(self.captured_photos) >= 10:
                self.save_btn.config(state=tk.NORMAL)
    
    def update_progress(self):
        """Update progress bar"""
        count = len(self.captured_photos)
        self.progress_label.config(text=f"{count} / {self.target_photos} photos")
        self.progress_bar['value'] = count
    
    def save_person(self):
        """Save person to dataset"""
        name = self.person_name.get().strip()
        if not name:
            messagebox.showwarning("Validation", "Please enter person name")
            return
        
        if len(self.captured_photos) < 10:
            messagebox.showwarning("Validation", "Need at least 10 photos")
            return
        
        try:
            # Create person folder
            dataset_path = Path("dataset") / name
            dataset_path.mkdir(parents=True, exist_ok=True)
            
            # Save photos
            for idx, photo in enumerate(self.captured_photos):
                photo_path = dataset_path / f"{name}_{idx+1:02d}.jpg"
                cv2.imwrite(str(photo_path), photo)
            
            # Save metadata
            metadata = {
                'name': name,
                'id': self.person_id.get().strip(),
                'department': self.department.get().strip(),
                'email': self.email.get().strip(),
                'photo_count': len(self.captured_photos),
                'registered_date': time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            import json
            metadata_path = dataset_path / "metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Generate encodings (using dataset manager)
            from dataset_manager import DatasetManager
            dm = DatasetManager(dataset_path="dataset")
            success = dm.generate_encodings()
            
            if success:
                messagebox.showinfo(
                    "Success",
                    f"Person '{name}' registered successfully!\n"
                    f"Photos saved: {len(self.captured_photos)}"
                )
                
                # Refresh main window stats
                self.main_window.refresh_stats()
                self.main_window.log_message(f"New person registered: {name}")
                
                # Close window
                self.on_closing()
            else:
                messagebox.showerror("Error", "Failed to generate face encodings")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save person: {str(e)}")
    
    def on_closing(self):
        """Handle window closing"""
        self.webcam_running = False
        if self.cap:
            self.cap.release()
        self.window.destroy()
