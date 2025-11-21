# Lesson 1: Build Tkinter GUI Basic

## Tujuan
- Belajar Tkinter basics
- Create main window
- Add buttons, labels, frames
- Handle events
- Build simple interface

## GUI Components
1. Main window
2. Menu bar
3. Buttons (Register, Attendance, Reports)
4. Labels & Status bar
5. Frames untuk layout

## Langkah
1. Run: `python main.py`
2. Window GUI akan muncul
3. Explore buttons & menus
4. Check layout & design

## Tkinter Basics
```python
import tkinter as tk

root = tk.Tk()
root.title("Attendance System")

button = tk.Button(root, text="Click Me", command=on_click)
button.pack()

root.mainloop()
```

## Next: Lesson 2 - Integrate All Features
