"""
📝 TUGAS MINGGU 7 - Desktop GUI (Fill in the Blanks)
Total: 8 soal - Tkinter GUI for attendance
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
sys.path.append('../project')
from attendance_system import AttendanceSystem

# SOAL 1: Create main window
# Hint: tk.Tk()
root = ____()
root.title("Face Recognition Attendance System")
root.geometry("800x600")

attendance = AttendanceSystem()


def check_in_gui():
    """Check-in button handler"""
    name = name_entry.get()
    
    if not name:
        # SOAL 2: Show error message
        # Hint: messagebox.showerror(title, message)
        messagebox.________("Error", "Nama tidak boleh kosong!")
        return
    
    success = attendance.check_in(name)
    
    if success:
        # SOAL 3: Show success message
        # Hint: messagebox.showinfo()
        messagebox.________("Success", f"{name} checked in!")
        name_entry.delete(0, tk.END)
        refresh_table()


def refresh_table():
    """Refresh attendance table"""
    # SOAL 4: Clear treeview
    # Hint: table.delete(*table.get_children())
    table.delete(*table._____________())
    
    records = attendance.get_today_records()
    
    # SOAL 5: Insert records ke table
    # Hint: table.insert('', 'end', values=(...))
    for r in records:
        table.______('', 'end', values=(r['name'], r['check_in'], r['check_out']))


# SOAL 6: Create Label widget
# Hint: tk.Label(parent, text=...)
title_label = ______(root, text="Attendance System", font=("Arial", 20))
title_label.pack(pady=20)

# Frame untuk input
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# SOAL 7: Create Entry widget
# Hint: tk.Entry(parent)
tk.Label(input_frame, text="Nama:").pack(side=tk.LEFT)
name_entry = ______(input_frame, width=30)
name_entry.pack(side=tk.LEFT, padx=10)

# SOAL 8: Create Button widget
# Hint: tk.Button(parent, text=..., command=...)
check_in_btn = _______(input_frame, text="Check In", command=check_in_gui)
check_in_btn.pack(side=tk.LEFT)

# Table untuk records
table_frame = tk.Frame(root)
table_frame.pack(pady=20, fill=tk.BOTH, expand=True)

table = ttk.Treeview(table_frame, columns=('Name', 'Check In', 'Check Out'), show='headings')
table.heading('Name', text='Name')
table.heading('Check In', text='Check In')
table.heading('Check Out', text='Check Out')
table.pack(fill=tk.BOTH, expand=True)

# Initial refresh
refresh_table()

# Start GUI
root.mainloop()
