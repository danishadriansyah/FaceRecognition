"""Lesson 1: Build Tkinter GUI Basic"""
import tkinter as tk
from tkinter import ttk, messagebox

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("800x600")
        
        self.create_menu()
        self.create_widgets()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="Face Recognition Attendance System",
            font=("Arial", 20, "bold"),
            bg="#2196F3",
            fg="white",
            pady=20
        )
        title.pack(fill=tk.X)
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Buttons
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Register Person",
            command=self.register_person,
            width=20,
            height=2,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="Mark Attendance",
            command=self.mark_attendance,
            width=20,
            height=2,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white"
        ).pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="View Reports",
            command=self.view_reports,
            width=20,
            height=2,
            font=("Arial", 12),
            bg="#FF9800",
            fg="white"
        ).pack(pady=10)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def register_person(self):
        messagebox.showinfo("Register", "Register Person module")
        self.status_bar.config(text="Status: Register Person clicked")
    
    def mark_attendance(self):
        messagebox.showinfo("Attendance", "Mark Attendance module")
        self.status_bar.config(text="Status: Mark Attendance clicked")
    
    def view_reports(self):
        messagebox.showinfo("Reports", "View Reports module")
        self.status_bar.config(text="Status: View Reports clicked")
    
    def show_about(self):
        messagebox.showinfo(
            "About",
            "Face Recognition Attendance System\nVersion 1.0\nLesson 1: Tkinter GUI Basics"
        )

def main():
    print("="*60)
    print("LESSON 1: Tkinter GUI Basics")
    print("="*60)
    print("\nStarting GUI application...")
    
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
    
    print("\n✅ LESSON 1 COMPLETED!")

if __name__ == '__main__':
    main()
