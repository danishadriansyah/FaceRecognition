"""
Lesson 2: Complete GUI dengan Webcam & Face Detection Integration

Tutorial: Integrate webcam preview dan face detection ke Tkinter GUI
"""
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
import sys
import os
from pathlib import Path

# Add project path untuk import modules
project_path = Path(__file__).parent.parent.parent / "project"
sys.path.insert(0, str(project_path))

try:
    from face_detector import FaceDetector
    DETECTOR_AVAILABLE = True
except ImportError:
    DETECTOR_AVAILABLE = False
    print("⚠️  FaceDetector not available - will show webcam only")


class CompleteAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Complete Attendance System - Lesson 2")
        self.root.geometry("1200x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Webcam variables
        self.cap = None
        self.webcam_running = False
        self.current_frame = None
        
        # Face detector
        self.detector = None
        if DETECTOR_AVAILABLE:
            try:
                self.detector = FaceDetector()
                print("✅ Face detector initialized")
            except Exception as e:
                print(f"⚠️  Could not init detector: {e}")
        
        self.create_ui()
        self.start_webcam()
        
    def create_ui(self):
        """Create GUI layout"""
        # Top frame - Title
        top_frame = tk.Frame(self.root, bg="#1976D2", height=60)
        top_frame.pack(fill=tk.X)
        
        tk.Label(
            top_frame,
            text="🎯 Face Recognition Attendance System - Lesson 2",
            font=("Arial", 18, "bold"),
            bg="#1976D2",
            fg="white"
        ).pack(pady=15)
        
        # Main container
        container = tk.Frame(self.root)
        container.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)
        
        # Left panel - WEBCAM PREVIEW (NEW!)
        left_panel = tk.Frame(container, width=700, bg="black")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Webcam label
        webcam_frame = tk.LabelFrame(
            left_panel, 
            text="📹 Live Webcam with Face Detection",
            font=("Arial", 11, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        webcam_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        self.webcam_label = tk.Label(webcam_frame, bg="black")
        self.webcam_label.pack(expand=True, fill=tk.BOTH)
        
        # Right panel - CONTROLS
        right_panel = tk.Frame(container, width=400, bg="white")
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        buttons = [
            ("📝 Register Person", self.register_person, "#4CAF50"),
            ("📸 Mark Attendance", self.mark_attendance, "#2196F3"),
            ("📊 View Reports", self.view_reports, "#FF9800"),
            ("⚙️ Settings", self.open_settings, "#9C27B0"),
        ]
        
        for text, command, color in buttons:
            tk.Button(
                right_panel,
                text=text,
                command=command,
                width=28,
                height=2,
                font=("Arial", 10),
                bg=color,
                fg="white",
                cursor="hand2"
            ).pack(pady=5, padx=10)
        
        # Detection info frame
        info_frame = tk.LabelFrame(
            right_panel, 
            text="Detection Info",
            font=("Arial", 11, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        info_frame.pack(pady=20, padx=10, fill=tk.X)
        
        self.faces_label = tk.Label(
            info_frame,
            text="Faces Detected: 0",
            font=("Arial", 12, "bold"),
            fg="#2196F3",
            bg="white"
        )
        self.faces_label.pack(pady=5)
        
        self.fps_label = tk.Label(
            info_frame,
            text="FPS: 0",
            font=("Arial", 10),
            fg="#666",
            bg="white"
        )
        self.fps_label.pack(pady=5)
        
        # Stats frame
        stats_frame = tk.LabelFrame(
            right_panel, 
            text="System Status",
            font=("Arial", 11, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        stats_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.status_text = tk.Text(
            stats_frame,
            height=12,
            font=("Consolas", 9),
            bg="#f9f9f9",
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        self.log_message("✅ System initialized")
        self.log_message("Webcam: Starting... | Detector: Initializing...")
        
        # Bottom status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready | Webcam: Initializing | Detector: Loading",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def start_webcam(self):
        """Start webcam in background thread"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.log_message("❌ Cannot open webcam")
                messagebox.showerror("Webcam Error", "Cannot open webcam")
                return
            
            self.webcam_running = True
            self.log_message("✅ Webcam started")
            self.status_bar.config(text="Ready | Webcam: Active | Detector: Ready")
            
            # Start webcam thread
            threading.Thread(target=self.update_webcam, daemon=True).start()
            
        except Exception as e:
            self.log_message(f"❌ Webcam error: {e}")
            messagebox.showerror("Webcam Error", f"Failed to start: {str(e)}")
    
    def update_webcam(self):
        """Update webcam display with face detection (runs in background thread)"""
        frame_count = 0
        start_time = time.time()
        face_count = 0
        
        while self.webcam_running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                
                # Face detection (NEW!)
                if self.detector:
                    faces = self.detector.detect_faces(frame)
                    face_count = len(faces)
                    
                    # Draw bounding boxes
                    for face in faces:
                        x, y, w, h = face  # face is a tuple (x, y, w, h)
                        
                        # Draw rectangle
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        
                        # Draw label
                        cv2.putText(
                            frame,
                            "Face",
                            (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 0),
                            2
                        )
                
                # Calculate FPS
                frame_count += 1
                if frame_count % 30 == 0:
                    elapsed = time.time() - start_time
                    fps = 30 / elapsed
                    start_time = time.time()
                    
                    # Update UI (thread-safe)
                    self.root.after(0, self.update_info_labels, face_count, fps)
                
                # Convert BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Resize for display
                frame = cv2.resize(frame, (680, 480))
                
                # Convert to PIL Image
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update label (thread-safe)
                self.webcam_label.imgtk = imgtk
                self.webcam_label.configure(image=imgtk)
                
                # Control frame rate (~30 FPS)
                time.sleep(0.03)
                
            except Exception as e:
                print(f"Webcam error: {e}")
                break
    
    def update_info_labels(self, face_count, fps):
        """Update detection info labels"""
        self.faces_label.config(text=f"Faces Detected: {face_count}")
        self.fps_label.config(text=f"FPS: {fps:.1f}")
    
    def log_message(self, message):
        """Add message to status log"""
        self.status_text.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
    
    def register_person(self):
        messagebox.showinfo("Register", "In full project, this opens Register Window")
        self.log_message("📝 Register Person clicked")
        self.status_bar.config(text="Status: Register Person module")
    
    def mark_attendance(self):
        messagebox.showinfo("Attendance", "In full project, this opens Attendance Window")
        self.log_message("📸 Mark Attendance clicked")
        self.status_bar.config(text="Status: Mark Attendance module")
    
    def view_reports(self):
        messagebox.showinfo("Reports", "In full project, this opens Reports Window")
        self.log_message("📊 View Reports clicked")
        self.status_bar.config(text="Status: View Reports module")
    
    def open_settings(self):
        messagebox.showinfo("Settings", "Settings configuration")
        self.log_message("⚙️ Settings clicked")
        self.status_bar.config(text="Status: Settings opened")
    
    def on_closing(self):
        """Handle window close"""
        self.webcam_running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()


def main():
    print("="*70)
    print("  LESSON 2: Complete GUI with Webcam & Face Detection")
    print("="*70)
    print()
    print("What you'll learn:")
    print("  ✅ Webcam integration in Tkinter")
    print("  ✅ Real-time face detection display")
    print("  ✅ Threading for non-blocking UI")
    print("  ✅ PIL/ImageTk for image display")
    print("  ✅ Multi-panel layout design")
    print()
    print("Starting application...")
    print("-"*70)
    
    root = tk.Tk()
    app = CompleteAttendanceApp(root)
    
    print("✅ GUI window created!")
    print("💡 Try clicking the buttons to see interactions")
    print("📹 Webcam should show live preview with face detection")
    print()
    
    root.mainloop()
    
    print()
    print("="*70)
    print("  ✅ LESSON 2 COMPLETED!")
    print("="*70)
    print()
    print("You learned:")
    print("  ✅ How to integrate webcam into GUI")
    print("  ✅ Real-time face detection visualization")
    print("  ✅ Thread-safe UI updates")
    print("  ✅ Professional multi-panel layout")
    print()
    print("Next: Lesson 3 - Testing & Deployment")
    print("="*70)


if __name__ == '__main__':
    main()
