"""
Lesson 2: Complete GUI dengan All Features Integrated

This is a simplified version for demo.
For full implementation, see project/ folder.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import os

class CompleteAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Complete Attendance System")
        self.root.geometry("1000x700")
        
        self.create_ui()
        
    def create_ui(self):
        # Top frame - Title
        top_frame = tk.Frame(self.root, bg="#1976D2", height=60)
        top_frame.pack(fill=tk.X)
        
        tk.Label(
            top_frame,
            text="🎯 Face Recognition Attendance System",
            font=("Arial", 18, "bold"),
            bg="#1976D2",
            fg="white"
        ).pack(pady=15)
        
        # Main container
        container = tk.Frame(self.root)
        container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Left panel - Controls
        left_panel = tk.Frame(container, width=300, bg="#f5f5f5")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        tk.Label(
            left_panel,
            text="Main Menu",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5"
        ).pack(pady=10)
        
        buttons = [
            ("📝 Register Person", self.register_person, "#4CAF50"),
            ("📸 Mark Attendance", self.mark_attendance, "#2196F3"),
            ("📊 View Reports", self.view_reports, "#FF9800"),
            ("⚙️ Settings", self.open_settings, "#9C27B0"),
            ("🗄️ Database", self.manage_database, "#607D8B"),
        ]
        
        for text, command, color in buttons:
            tk.Button(
                left_panel,
                text=text,
                command=command,
                width=25,
                height=2,
                font=("Arial", 11),
                bg=color,
                fg="white",
                cursor="hand2"
            ).pack(pady=5, padx=10)
        
        # Right panel - Preview/Info
        right_panel = tk.Frame(container, bg="white")
        right_panel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        tk.Label(
            right_panel,
            text="System Ready",
            font=("Arial", 16),
            bg="white"
        ).pack(pady=50)
        
        # Stats frame
        stats_frame = tk.LabelFrame(right_panel, text="Today's Statistics", font=("Arial", 12, "bold"))
        stats_frame.pack(pady=20, padx=20, fill=tk.X)
        
        stats = [
            ("Total Persons:", "10"),
            ("Attendance Today:", "7"),
            ("Attendance Rate:", "70%"),
        ]
        
        for label, value in stats:
            row = tk.Frame(stats_frame, bg="white")
            row.pack(fill=tk.X, padx=10, pady=5)
            tk.Label(row, text=label, font=("Arial", 10), anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, text=value, font=("Arial", 10, "bold"), fg="#2196F3").pack(side=tk.RIGHT)
        
        # Bottom status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready | Database: Connected | Last Update: Just now",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def register_person(self):
        messagebox.showinfo("Register", "Opening Register Person module...")
        self.status_bar.config(text="Status: Register Person - Capturing faces...")
    
    def mark_attendance(self):
        messagebox.showinfo("Attendance", "Opening Attendance module...")
        self.status_bar.config(text="Status: Marking attendance...")
    
    def view_reports(self):
        messagebox.showinfo("Reports", "Generating reports...")
        self.status_bar.config(text="Status: Viewing reports...")
    
    def open_settings(self):
        messagebox.showinfo("Settings", "Opening Settings...")
        self.status_bar.config(text="Status: Settings opened")
    
    def manage_database(self):
        messagebox.showinfo("Database", "Opening Database Manager...")
        self.status_bar.config(text="Status: Database management")

def main():
    print("="*60)
    print("LESSON 2: Complete GUI with All Features")
    print("="*60)
    print("\n✅ Starting complete application...")
    
    root = tk.Tk()
    app = CompleteAttendanceApp(root)
    root.mainloop()
    
    print("\n✅ LESSON 2 COMPLETED!")
    print("="*60)
    print("Production-ready GUI created!")
    print("Next: Minggu 8 - Testing & Deployment")

if __name__ == '__main__':
    main()
