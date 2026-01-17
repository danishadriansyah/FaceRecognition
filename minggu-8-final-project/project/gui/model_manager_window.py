"""
Model Manager Window - Desktop GUI
Week 8 Final Project

Window for managing Teachable Machine models:
- List all models
- Switch active model  
- Delete models
- Rename models
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path


class ModelManagerWindow:
    """Model manager window"""
    
    def __init__(self, parent, main_window):
        """Initialize model manager window"""
        self.main_window = main_window
        self.model_manager = main_window.model_manager
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Model Manager")
        self.window.geometry("800x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"+{x}+{y}")
        
        self.create_ui()
        self.load_models()
    
    def create_ui(self):
        """Create UI"""
        # Title
        title_frame = tk.Frame(self.window, bg="#1976D2", height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="🎓 Teachable Machine Models",
            font=("Arial", 14, "bold"),
            bg="#1976D2",
            fg="white"
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        # Main content
        content_frame = tk.Frame(self.window)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Models list
        list_frame = tk.LabelFrame(content_frame, text="Available Models", font=("Arial", 10, "bold"))
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        columns = ("Name", "Created", "Classes")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=15)
        
        self.tree.heading("#0", text="Status")
        self.tree.heading("Name", text="Model Name")
        self.tree.heading("Created", text="Created At")
        self.tree.heading("Classes", text="Classes")
        
        self.tree.column("#0", width=80)
        self.tree.column("Name", width=250)
        self.tree.column("Created", width=180)
        self.tree.column("Classes", width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tk.Button(
            button_frame,
            text="Set as Active",
            command=self.set_active,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Rename",
            command=self.rename_model,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Delete",
            command=self.delete_model,
            bg="#f44336",
            fg="white",
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_models,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            command=self.window.destroy,
            font=("Arial", 10),
            width=15
        ).pack(side=tk.RIGHT, padx=5)
    
    def load_models(self):
        """Load models list"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get active model
        active_model = self.model_manager.get_active_model()
        active_id = active_model['id'] if active_model else None
        
        # Load models
        models = self.model_manager.list_models()
        
        if not models:
            self.tree.insert("", "end", text="", values=("No models found", "", ""))
            return
        
        for model in models:
            is_active = model['id'] == active_id
            status = "✓ Active" if is_active else ""
            
            classes_str = ", ".join(model.get('classes', [])[:3])
            if len(model.get('classes', [])) > 3:
                classes_str += f" (+{len(model['classes']) - 3} more)"
            
            created = model.get('created_at', 'Unknown')
            if 'T' in created:
                created = created.split('T')[0] + " " + created.split('T')[1][:8]
            
            self.tree.insert(
                "",
                "end",
                text=status,
                values=(model['name'], created, classes_str),
                tags=(model['id'],)
            )
    
    def set_active(self):
        """Set selected model as active"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a model")
            return
        
        item = self.tree.item(selection[0])
        model_id = item['tags'][0] if item['tags'] else None
        
        if not model_id:
            return
        
        if self.model_manager.set_active_model(model_id):
            messagebox.showinfo(
                "Success",
                "Model set as active!\n\nPlease restart the application to use this model."
            )
            self.load_models()
        else:
            messagebox.showerror("Error", "Failed to set active model")
    
    def rename_model(self):
        """Rename selected model"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a model")
            return
        
        item = self.tree.item(selection[0])
        model_id = item['tags'][0] if item['tags'] else None
        current_name = item['values'][0]
        
        if not model_id:
            return
        
        # Ask for new name
        new_name = tk.simpledialog.askstring(
            "Rename Model",
            "Enter new name:",
            initialvalue=current_name
        )
        
        if new_name and new_name != current_name:
            if self.model_manager.rename_model(model_id, new_name):
                messagebox.showinfo("Success", "Model renamed successfully")
                self.load_models()
            else:
                messagebox.showerror("Error", "Failed to rename model")
    
    def delete_model(self):
        """Delete selected model"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a model")
            return
        
        item = self.tree.item(selection[0])
        model_id = item['tags'][0] if item['tags'] else None
        model_name = item['values'][0]
        
        if not model_id:
            return
        
        # Confirm deletion
        if not messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{model_name}'?\n\nThis action cannot be undone."
        ):
            return
        
        if self.model_manager.delete_model(model_id):
            messagebox.showinfo("Success", "Model deleted successfully")
            self.load_models()
        else:
            messagebox.showerror("Error", "Failed to delete model")
