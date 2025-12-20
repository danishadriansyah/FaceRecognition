# Lesson 1: Build Tkinter GUI Basic

## Tujuan
- Belajar Tkinter basics
- Create main window dengan menu bar
- Add buttons, labels, frames
- Handle button events
- Build simple dashboard interface

## Prerequisites
- ✅ Python installed
- ✅ Tkinter (built-in dengan Python)

## GUI Components
1. Main window (Tk)
2. Menu bar (Menu)
3. Title bar (Frame + Label)
4. Action buttons (Button) - Register, Attendance, Reports
5. Status bar (Label)

## Tkinter Basics

### Create Window
```python
import tkinter as tk

root = tk.Tk()
root.title("Attendance System")
root.geometry("800x600")

root.mainloop()
```

### Add Widgets
```python
# Label
label = tk.Label(root, text="Hello", font=("Arial", 16))
label.pack()

# Button
button = tk.Button(root, text="Click Me", command=on_click)
button.pack()

# Entry
entry = tk.Entry(root, width=30)
entry.pack()
```

### Event Handling
```python
def on_click():
    messagebox.showinfo("Info", "Button clicked!")

button = tk.Button(root, text="Click", command=on_click)
```

## Langkah-Langkah

1. **Run main.py:**
   ```bash
   python main.py
   ```

2. **Explore GUI:**
   - Window muncul dengan title bar
   - 3 buttons (Register, Attendance, Reports)
   - Menu bar (File, Help)
   - Click buttons untuk lihat messagebox

3. **Modifikasi (optional):**
   - Ganti warna buttons
   - Tambah button baru
   - Ubah font & size

## Key Concepts

- `tk.Tk()` - Create main window
- `tk.Label()` - Display text
- `tk.Button()` - Clickable button
- `tk.Frame()` - Container for widgets
- `pack()` - Simple layout manager
- `messagebox` - Show dialogs

## Next: Lesson 2

Di Lesson 2, kita akan integrate semua backend modules dan add webcam preview!
