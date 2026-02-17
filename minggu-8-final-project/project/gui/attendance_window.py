"""
Attendance Window - Desktop GUI
Week 7 Project Module

Real-time attendance marking with face recognition
"""
import tkinter as tk
from tkinter import messagebox
import cv2
import time
from PIL import Image, ImageTk
from datetime import datetime
import threading
import numpy as np



class AttendanceWindow:
    """Attendance marking window"""
    
    def __init__(self, parent, main_window):
        """Initialize attendance window"""
        self.parent = parent
        self.main_window = main_window
        
        # Create top-level window
        self.window = tk.Toplevel(parent)
        self.window.title("Mark Attendance")
        self.window.geometry("1000x600")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Variables
        self.current_person = None
        self.last_recognition = None
        self.recognition_cooldown = 5  # seconds
        
        # Webcam
        self.cap = None
        self.webcam_running = False
        
        # Create UI
        self.create_ui()
        self.start_webcam()
    
    def create_ui(self):
        """Create UI components"""
        # Title
        title_frame = tk.Frame(self.window, bg="#2196F3", height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="📸 Mark Attendance",
            font=("Arial", 16, "bold"),
            bg="#2196F3",
            fg="white"
        ).pack(pady=12)
        
        # Main container
        container = tk.Frame(self.window)
        container.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)
        
        # Left panel - Webcam
        left_panel = tk.Frame(container)
        left_panel.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 10))
        
        self.create_webcam_panel(left_panel)
        
        # Right panel - Info & Controls
        right_panel = tk.Frame(container, width=350)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        right_panel.pack_propagate(False)
        
        self.create_info_panel(right_panel)
    
    def create_webcam_panel(self, parent):
        """Create webcam preview panel"""
        webcam_frame = tk.LabelFrame(
            parent,
            text="Live Camera",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        webcam_frame.pack(expand=True, fill=tk.BOTH)
        
        self.webcam_label = tk.Label(webcam_frame, bg="black")
        self.webcam_label.pack(expand=True, fill=tk.BOTH)
        
        # Status label
        self.status_label = tk.Label(
            parent,
            text="👤 Looking for faces...",
            font=("Arial", 10),
            fg="#666666"
        )
        self.status_label.pack(pady=5)
    
    def create_info_panel(self, parent):
        """Create information panel"""
        # Recognition result
        result_frame = tk.LabelFrame(
            parent,
            text="Recognition Result",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        result_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.result_name = tk.Label(
            result_frame,
            text="Unknown",
            font=("Arial", 16, "bold"),
            fg="#666666"
        )
        self.result_name.pack(pady=5)
        
        self.result_confidence = tk.Label(
            result_frame,
            text="Confidence: --",
            font=("Arial", 10),
            fg="#666666"
        )
        self.result_confidence.pack()
        
        self.result_time = tk.Label(
            result_frame,
            text="",
            font=("Arial", 9),
            fg="#999999"
        )
        self.result_time.pack(pady=5)
        
        # Attendance type
        type_frame = tk.LabelFrame(
            parent,
            text="Attendance Type",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.attendance_type = tk.StringVar(value="check_in")
        
        tk.Radiobutton(
            type_frame,
            text="✅ Check In",
            variable=self.attendance_type,
            value="check_in",
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=5)
        
        tk.Radiobutton(
            type_frame,
            text="🚪 Check Out",
            variable=self.attendance_type,
            value="check_out",
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=5)
        
        # Mark Attendance Button
        tk.Button(
            type_frame,
            text="📝 Mark Attendance",
            command=self.mark_recognized_person,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            cursor="hand2",
            height=2
        ).pack(fill=tk.X, pady=(10, 0))
        
        # Manual entry
        manual_frame = tk.LabelFrame(
            parent,
            text="Manual Entry",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        manual_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(manual_frame, text="Name:", font=("Arial", 9)).pack(anchor=tk.W)
        self.manual_name = tk.Entry(manual_frame, font=("Arial", 10))
        self.manual_name.pack(fill=tk.X, pady=(5, 10))
        
        tk.Button(
            manual_frame,
            text="Manual Check-In",
            command=self.manual_checkin,
            font=("Arial", 9),
            bg="#FF9800",
            fg="white",
            cursor="hand2"
        ).pack(fill=tk.X)
        
        # Today's records
        records_frame = tk.LabelFrame(
            parent,
            text="Today's Records",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        records_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.records_text = tk.Text(
            records_frame,
            height=10,
            font=("Consolas", 8),
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.records_text.pack(fill=tk.BOTH, expand=True)
        
        # Refresh button
        tk.Button(
            parent,
            text="🔄 Refresh Records",
            command=self.refresh_records,
            font=("Arial", 10),
            bg="#9C27B0",
            fg="white",
            cursor="hand2"
        ).pack(fill=tk.X)
        
        # Initial load
        self.refresh_records()
    
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
        """Update webcam with recognition"""
        while self.webcam_running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Face recognition
                if self.main_window.recognition_service:
                    results = self.main_window.recognition_service.recognize_faces(frame)
                    
                    if results and len(results) > 0:
                        # Get first recognized person
                        result = results[0]
                        name = result.get('name', 'Unknown')
                        confidence = result.get('confidence', 0.0)
                        bbox = result.get('bbox')
                        
                        if name != 'Unknown':
                            # Store current person for manual marking
                            self.current_person = name
                            self.current_confidence = confidence
                            self.current_frame = frame
                            
                            # Update cooldown tracker (but don't auto-mark)
                            # Auto-attendance disabled - use button instead
                            
                            # Update UI
                            self.window.after(0, lambda: self.update_recognition_ui(result))
                            
                            # Draw on frame
                            if bbox:
                                x, y, w, h = bbox
                                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                cv2.putText(
                                    frame,
                                    f"{name} ({confidence:.2f})",
                                    (x, y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.6,
                                    (0, 255, 0),
                                    2
                                )
                        else:
                            # Unknown face
                            if bbox:
                                x, y, w, h = bbox
                                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                                cv2.putText(
                                    frame,
                                    "Unknown",
                                    (x, y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.6,
                                    (0, 0, 255),
                                    2
                                )
                
                # Convert to PhotoImage
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (600, 450))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update label
                self.webcam_label.imgtk = imgtk
                self.webcam_label.configure(image=imgtk)
                
                time.sleep(0.03)
            except Exception as e:
                print(f"Webcam error: {e}")
                break
    
    def update_recognition_ui(self, result):
        """Update recognition UI"""
        name = result.get('name', 'Unknown')
        confidence = result.get('confidence', 0.0)
        
        if name != 'Unknown':
            self.result_name.config(text=name, fg="#4CAF50")
            self.result_confidence.config(
                text=f"Confidence: {confidence:.2%}",
                fg="#4CAF50"
            )
            self.result_time.config(text=time.strftime("%H:%M:%S"))
            self.status_label.config(text=f"✅ Recognized: {name}")
        else:
            self.result_name.config(text="Unknown", fg="#f44336")
            self.result_confidence.config(text="Confidence: --", fg="#666666")
            self.status_label.config(text="❌ Face not recognized")
    
    def mark_attendance(self, name, confidence, frame):
        """Mark attendance"""
        try:
            attendance_type = self.attendance_type.get()
            
            if attendance_type == 'check_in':
                result = self.main_window.attendance_system.check_in(
                    name=name,
                    confidence=confidence,
                    photo=frame
                )
                
                # Already checked in
                if isinstance(result, dict) and result.get('already_checked_in'):
                    existing_time = result['time']
                    msg = f"⚠️ {name} sudah absen pukul {existing_time}"
                    self.window.after(0, lambda: self.show_notification(msg, "warning"))
                    return
                
                record = result
            else:
                record = self.main_window.attendance_system.record_attendance(
                    name=name,
                    attendance_type=attendance_type,
                    confidence=confidence,
                    photo=frame
                )
            
            # If record is returned (not None/error), it's successful
            if record:
                # Show notification
                msg = f"✅ {name} - {attendance_type.replace('_', ' ').title()}"
                self.window.after(0, lambda: self.show_notification(msg, "success"))
                
                # Refresh records
                self.window.after(0, self.refresh_records)
                
                # Update main window
                self.main_window.refresh_stats()
                self.main_window.log_message(f"Attendance: {name} ({attendance_type})")
        
        except Exception as e:
            print(f"Attendance error: {e}")
            import traceback
            traceback.print_exc()
    
    def manual_checkin(self):
        """Manual check-in"""
        name = self.manual_name.get().strip()
        if not name:
            messagebox.showwarning("Validation", "Please enter name")
            return
        
        try:
            attendance_type = self.attendance_type.get()
            
            # record_attendance returns record dict, not {'success': True}
            record = self.main_window.attendance_system.record_attendance(
                name=name,
                attendance_type=attendance_type,
                confidence=1.0,
                notes="Manual entry"
            )
            
            # If record exists, it was successful
            if record:
                # Use showinfo instead of showerror for success message
                messagebox.showinfo("✅ Success", f"✅ {name} - {attendance_type.replace('_', ' ').title()} recorded successfully!")
                self.manual_name.delete(0, tk.END)
                self.refresh_records()
                self.main_window.refresh_stats()
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to record attendance: {str(e)}")
    
    def mark_recognized_person(self):
        """Mark attendance for currently recognized person"""
        if not hasattr(self, 'current_person') or not self.current_person:
            messagebox.showwarning("⚠️ Warning", "No person recognized!\n\nPlease face the camera and wait for recognition.")
            return
        
        try:
            attendance_type = self.attendance_type.get()
            
            if attendance_type == 'check_in':
                result = self.main_window.attendance_system.check_in(
                    name=self.current_person,
                    confidence=self.current_confidence,
                    photo=self.current_frame if hasattr(self, 'current_frame') else None
                )
                
                # Already checked in
                if isinstance(result, dict) and result.get('already_checked_in'):
                    existing_time = result['time']
                    messagebox.showinfo(
                        "ℹ️ Info",
                        f"{self.current_person} sudah absen pukul {existing_time}"
                    )
                    return
                
                record = result
            else:
                record = self.main_window.attendance_system.record_attendance(
                    name=self.current_person,
                    attendance_type=attendance_type,
                    confidence=self.current_confidence,
                    photo=self.current_frame if hasattr(self, 'current_frame') else None
                )
            
            # If record exists, it was successful
            if record:
                msg = f"✅ {self.current_person} - {attendance_type.replace('_', ' ').title()}"
                messagebox.showinfo("✅ Success", f"{msg} recorded successfully!")
                
                # Refresh records
                self.refresh_records()
                self.main_window.refresh_stats()
                self.main_window.log_message(f"Attendance: {self.current_person} ({attendance_type})")
                
                # Update last recognition time
                self.last_recognition = time.time()
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to mark attendance: {str(e)}")
    
    
    def refresh_records(self):
        """Refresh today's records"""
        try:
            # Use get_records with today's date filter
            today = datetime.now().strftime('%Y-%m-%d')
            records = self.main_window.attendance_system.get_records(date_filter=today)
            
            self.records_text.config(state=tk.NORMAL)
            self.records_text.delete(1.0, tk.END)
            
            if not records:
                self.records_text.insert(tk.END, "No records today")
            else:
                for record in records[-10:]:  # Show last 10
                    time_str = record['time']
                    name = record['person_name']
                    type_str = record['type'].replace('_', ' ').title()
                    self.records_text.insert(tk.END, f"{time_str} | {name}\n  → {type_str}\n\n")
            
            self.records_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Refresh error: {e}")
            import traceback
            traceback.print_exc()
    
    def show_notification(self, message, msg_type="info"):
        """Show notification toast"""
        # Simple messagebox for now
        # TODO: Implement toast notification
        if msg_type == "success":
            messagebox.showinfo("Attendance", message)
        elif msg_type == "warning":
            messagebox.showwarning("Attendance", message)
    
    def on_closing(self):
        """Handle window closing"""
        self.webcam_running = False
        if self.cap:
            self.cap.release()
        self.window.destroy()
