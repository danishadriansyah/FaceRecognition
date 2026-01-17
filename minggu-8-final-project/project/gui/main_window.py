"""
Main Window - Desktop GUI
Week 7 Project Module

Main application window with webcam preview and navigation
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
import threading
import time
from pathlib import Path
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import backend modules
from core.recognition_service import RecognitionService
from core.attendance_system import AttendanceSystem
from core.model_manager import ModelManager

# Import configuration
try:
    from config import Config
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    print("⚠️  Config module not available, using default settings")


class MainWindow:
    """Main application window"""
    
    def __init__(self, root):
        """Initialize main window"""
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1200x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Backend services
        self.recognition_service = None
        self.attendance_system = None
        self.initialize_services()
        
        # Webcam
        self.cap = None
        self.webcam_running = False
        self.current_frame = None
        
        # UI Components
        self.create_menu()
        self.create_ui()
        
        # Start webcam
        self.start_webcam()
    
    def initialize_services(self):
        """Initialize backend services"""
        try:
            dataset_path = Path("dataset")
            dataset_path.mkdir(exist_ok=True)
            
            # Initialize model manager (ensure correct path)
            models_path = Path(__file__).parent.parent / "models"
            self.model_manager = ModelManager(str(models_path))
            
            # Debug: list available models
            available_models = self.model_manager.list_models()
            print(f"📦 Found {len(available_models)} Teachable Machine model(s)")
            for model in available_models:
                print(f"   - {model['name']}: {', '.join(model.get('classes', []))}")
            
            # Load configuration
            use_teachable = True
            teachable_conf = 0.7
            
            if CONFIG_AVAILABLE:
                config = Config()
                use_teachable = config.recognition.use_teachable_machine
                teachable_conf = config.recognition.teachable_confidence
            
            # Get active model from model manager
            if use_teachable:
                active_model = self.model_manager.get_active_model()
                
                if active_model:
                    model_paths = self.model_manager.get_model_path(active_model['id'])
                    if model_paths:
                        print(f"🎓 Using Teachable Machine model: {active_model['name']}")
                        self.recognition_service = RecognitionService(
                            dataset_path=str(dataset_path),
                            use_teachable_machine=True,
                            teachable_model_path=model_paths[0],
                            teachable_labels_path=model_paths[1],
                            teachable_confidence=teachable_conf
                        )
                    else:
                        print("⚠️  Model files not found, using MediaPipe")
                        self.recognition_service = RecognitionService(dataset_path=str(dataset_path))
                else:
                    print("⚠️  No Teachable Machine models found, using MediaPipe")
                    self.recognition_service = RecognitionService(dataset_path=str(dataset_path))
            else:
                # Use MediaPipe mode
                self.recognition_service = RecognitionService(dataset_path=str(dataset_path))
            
            self.attendance_system = AttendanceSystem(dataset_path=str(dataset_path), log_dir="logs")
            
            print("✅ Services initialized")
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize: {str(e)}")
            print(f"Error details: {e}")
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Model menu
        model_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Models", menu=model_menu)
        model_menu.add_command(label="Manage Models", command=self.open_model_manager)
        model_menu.add_command(label="Import Model", command=self.import_model)
        model_menu.add_command(label="Train New Model", command=self.train_new_model)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh", command=self.refresh_stats)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_ui(self):
        """Create main UI"""
        # Top bar
        top_frame = tk.Frame(self.root, bg="#1976D2", height=60)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        tk.Label(
            top_frame,
            text="🎯 Face Recognition Attendance System",
            font=("Arial", 18, "bold"),
            bg="#1976D2",
            fg="white"
        ).pack(pady=15)
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Left panel - Webcam preview
        left_panel = tk.Frame(main_container, width=700, bg="black")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Webcam label
        self.webcam_label = tk.Label(left_panel, bg="black")
        self.webcam_label.pack(expand=True, fill=tk.BOTH)
        
        # Right panel - Controls & Info
        right_panel = tk.Frame(main_container, width=480, bg="#f5f5f5")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # Title
        tk.Label(
            right_panel,
            text="Dashboard",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5"
        ).pack(pady=10)
        
        # Stats frame
        self.create_stats_frame(right_panel)
        
        # Action buttons
        self.create_action_buttons(right_panel)
        
        # Status frame
        self.create_status_frame(right_panel)
        
        # Bottom status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready | Webcam: Active | Dataset: Loaded",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_stats_frame(self, parent):
        """Create statistics frame"""
        stats_frame = tk.LabelFrame(
            parent,
            text="Today's Statistics",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        stats_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Get today's stats
        stats = self.get_today_stats()
        
        self.stats_labels = {}
        for label, value in stats.items():
            row = tk.Frame(stats_frame, bg="white")
            row.pack(fill=tk.X, pady=5)
            
            tk.Label(
                row,
                text=label + ":",
                font=("Arial", 10),
                bg="white",
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            value_label = tk.Label(
                row,
                text=str(value),
                font=("Arial", 10, "bold"),
                fg="#2196F3",
                bg="white"
            )
            value_label.pack(side=tk.RIGHT)
            self.stats_labels[label] = value_label
    
    def create_action_buttons(self, parent):
        """Create action buttons"""
        btn_frame = tk.Frame(parent, bg="#f5f5f5")
        btn_frame.pack(pady=20, padx=10, fill=tk.X)
        
        buttons = [
            ("📝 Register Person", self.open_register, "#4CAF50"),
            ("📸 Mark Attendance", self.open_attendance, "#2196F3"),
            ("📊 View Reports", self.open_reports, "#FF9800"),
            ("⚙️ Settings", self.open_settings, "#9C27B0"),
        ]
        
        for text, command, color in buttons:
            tk.Button(
                btn_frame,
                text=text,
                command=command,
                width=25,
                height=2,
                font=("Arial", 11),
                bg=color,
                fg="white",
                cursor="hand2",
                relief=tk.RAISED,
                bd=2
            ).pack(pady=5)
    
    def create_status_frame(self, parent):
        """Create status info frame"""
        status_frame = tk.LabelFrame(
            parent,
            text="System Status",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        status_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Status text
        self.status_text = tk.Text(
            status_frame,
            height=10,
            font=("Consolas", 9),
            bg="#f9f9f9",
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        self.log_message("System initialized successfully")
        self.log_message("Webcam started")
        self.log_message("Ready for operations")
    
    def start_webcam(self):
        """Start webcam preview"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Webcam Error", "Cannot open webcam")
                return
            
            self.webcam_running = True
            threading.Thread(target=self.update_webcam, daemon=True).start()
            self.log_message("Webcam started successfully")
        except Exception as e:
            messagebox.showerror("Webcam Error", f"Failed to start webcam: {str(e)}")
    
    def update_webcam(self):
        """Update webcam feed"""
        print("DEBUG: Webcam update thread started")
        while self.webcam_running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    print("DEBUG: Cannot read frame from camera")
                    break
                
                print(f"DEBUG: Frame read successfully, shape: {frame.shape}")
                
                # Detect faces using recognition service
                if self.recognition_service:
                    try:
                        print("DEBUG: Calling recognize_faces...")
                        results = self.recognition_service.recognize_faces(frame)
                        print(f"DEBUG: Got {len(results) if results else 0} results")
                        
                        # Draw bounding boxes
                        for result in results:
                            bbox = result.get('bbox')
                            if bbox:
                                x, y, w, h = bbox
                                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                cv2.putText(
                                    frame,
                                    "Face",
                                    (x, y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5,
                                    (0, 255, 0),
                                    2
                                )
                    except Exception as e:
                        print(f"DEBUG: Recognition error: {e}")
                        import traceback
                        traceback.print_exc()
                
                # Convert to PhotoImage
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (700, 500))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update label
                self.webcam_label.imgtk = imgtk
                self.webcam_label.configure(image=imgtk)
                
                self.current_frame = frame
                
                time.sleep(0.03)  # ~30 FPS
            except Exception as e:
                print(f"DEBUG: Webcam loop error: {e}")
                import traceback
                traceback.print_exc()
                break
    
    def get_today_stats(self):
        """Get today's statistics"""
        if not self.attendance_system:
            return {
                "Total Persons": 0,
                "Check-ins Today": 0,
                "Check-outs Today": 0,
                "Attendance Rate": "0%"
            }
        
        try:
            # Get today's records from CSV
            records = self.attendance_system.get_records(date_filter=datetime.now().strftime('%Y-%m-%d'))
            check_ins = len([r for r in records if r['type'] == 'check_in'])
            check_outs = len([r for r in records if r['type'] == 'check_out'])
            
            # Get total persons from dataset
            encodings_file = Path("dataset/encodings.pkl")
            total_persons = 0
            if encodings_file.exists():
                import pickle
                with open(encodings_file, 'rb') as f:
                    data = pickle.load(f)
                    total_persons = len(set(data.get('names', [])))
            
            rate = int((check_ins / total_persons * 100)) if total_persons > 0 else 0
            
            return {
                "Total Persons": total_persons,
                "Check-ins Today": check_ins,
                "Check-outs Today": check_outs,
                "Attendance Rate": f"{rate}%"
            }
        except Exception as e:
            print(f"Stats error: {e}")
            return {
                "Total Persons": 0,
                "Check-ins Today": 0,
                "Check-outs Today": 0,
                "Attendance Rate": "0%"
            }
    
    def refresh_stats(self):
        """Refresh statistics"""
        stats = self.get_today_stats()
        for label, value in stats.items():
            if label in self.stats_labels:
                self.stats_labels[label].config(text=str(value))
        self.log_message("Statistics refreshed")
    
    def log_message(self, message):
        """Log message to status text"""
        self.status_text.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
    
    def open_register(self):
        """Open register window"""
        from .register_window import RegisterWindow
        RegisterWindow(self.root, self)
    
    def open_attendance(self):
        """Open attendance window"""
        from .attendance_window import AttendanceWindow
        AttendanceWindow(self.root, self)
    
    def open_reports(self):
        """Open reports window"""
        from .reports_window import ReportsWindow
        ReportsWindow(self.root, self)
    
    def open_settings(self):
        """Open settings dialog"""
        messagebox.showinfo("Settings", "Settings window - Coming soon!")
    
    def open_model_manager(self):
        """Open model manager window"""
        from .model_manager_window import ModelManagerWindow
        ModelManagerWindow(self.root, self)
    
    def import_model(self):
        """Import external model"""
        from tkinter import filedialog
        
        model_file = filedialog.askopenfilename(
            title="Select Keras Model",
            filetypes=[("Keras Model", "*.h5"), ("All Files", "*.*")]
        )
        
        if not model_file:
            return
        
        labels_file = filedialog.askopenfilename(
            title="Select Labels File",
            filetypes=[("Text File", "*.txt"), ("All Files", "*.*")]
        )
        
        if not labels_file:
            return
        
        # Ask for model name
        name = tk.simpledialog.askstring("Model Name", "Enter model name:")
        
        try:
            model_id = self.model_manager.import_model(model_file, labels_file, name)
            messagebox.showinfo("Success", f"Model imported: {model_id}")
            
            # Ask to set as active
            if messagebox.askyesno("Set Active", "Set this model as active?"):
                self.model_manager.set_active_model(model_id)
                messagebox.showinfo("Success", "Model set as active. Please restart the application.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import model: {e}")
    
    def train_new_model(self):
        """Open Teachable Machine website"""
        import webbrowser
        messagebox.showinfo(
            "Train New Model",
            "You will be redirected to Teachable Machine.\n\n"
            "Steps:\n"
            "1. Train your model at teachablemachine.withgoogle.com\n"
            "2. Export as Tensorflow → Keras\n"
            "3. Download the files\n"
            "4. Import via Models → Import Model"
        )
        webbrowser.open("https://teachablemachine.withgoogle.com/train/image")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            "Face Recognition Attendance System\n\n"
            "Version: 1.0\n"
            "Week 7 - Desktop GUI\n\n"
            "Developed with Python + Tkinter"
        )
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.webcam_running = False
            if self.cap:
                self.cap.release()
            self.root.destroy()
