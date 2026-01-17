"""
Reports Window - Desktop GUI
Week 7 Project Module

View and export attendance reports
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import csv
from pathlib import Path


class ReportsWindow:
    """Reports viewing window"""
    
    def __init__(self, parent, main_window):
        """Initialize reports window"""
        self.parent = parent
        self.main_window = main_window
        
        # Create top-level window
        self.window = tk.Toplevel(parent)
        self.window.title("Attendance Reports")
        self.window.geometry("1000x650")
        
        # Create UI
        self.create_ui()
        self.load_records()
    
    def create_ui(self):
        """Create UI components"""
        # Title
        title_frame = tk.Frame(self.window, bg="#FF9800", height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="📊 Attendance Reports",
            font=("Arial", 16, "bold"),
            bg="#FF9800",
            fg="white"
        ).pack(pady=12)
        
        # Top control panel
        control_frame = tk.Frame(self.window, bg="#f5f5f5", height=80)
        control_frame.pack(fill=tk.X, padx=15, pady=(15, 0))
        control_frame.pack_propagate(False)
        
        # Date filter
        date_frame = tk.Frame(control_frame, bg="#f5f5f5")
        date_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(date_frame, text="Date Range:", font=("Arial", 10), bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        
        self.date_filter = tk.StringVar(value="today")
        filters = [
            ("Today", "today"),
            ("This Week", "week"),
            ("This Month", "month"),
            ("All Time", "all")
        ]
        
        for text, value in filters:
            tk.Radiobutton(
                date_frame,
                text=text,
                variable=self.date_filter,
                value=value,
                font=("Arial", 9),
                bg="#f5f5f5",
                command=self.load_records
            ).pack(side=tk.LEFT, padx=5)
        
        # Search
        search_frame = tk.Frame(control_frame, bg="#f5f5f5")
        search_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        tk.Label(search_frame, text="Search:", font=("Arial", 10), bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_records())
        
        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 10),
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        # Statistics panel
        stats_frame = tk.Frame(self.window, bg="white", height=100)
        stats_frame.pack(fill=tk.X, padx=15, pady=(10, 0))
        stats_frame.pack_propagate(False)
        
        self.create_stats_panel(stats_frame)
        
        # Table
        table_frame = tk.Frame(self.window)
        table_frame.pack(expand=True, fill=tk.BOTH, padx=15, pady=10)
        
        self.create_table(table_frame)
        
        # Bottom buttons
        btn_frame = tk.Frame(self.window, bg="#f5f5f5", height=60)
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        btn_frame.pack_propagate(False)
        
        buttons = [
            ("🔄 Refresh", self.load_records, "#2196F3"),
            ("📥 Export CSV", self.export_csv, "#4CAF50"),
            ("📊 Generate Report", self.generate_report, "#FF9800"),
        ]
        
        for text, command, color in buttons:
            tk.Button(
                btn_frame,
                text=text,
                command=command,
                width=18,
                height=2,
                font=("Arial", 10),
                bg=color,
                fg="white",
                cursor="hand2"
            ).pack(side=tk.LEFT, padx=5, pady=10)
    
    def create_stats_panel(self, parent):
        """Create statistics panel"""
        # Title
        tk.Label(
            parent,
            text="Summary Statistics",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(pady=(10, 5))
        
        # Stats row
        stats_row = tk.Frame(parent, bg="white")
        stats_row.pack(pady=5)
        
        self.stats_labels = {}
        stats = [
            ("Total Records", "0"),
            ("Unique Persons", "0"),
            ("Check-ins", "0"),
            ("Check-outs", "0")
        ]
        
        for label, value in stats:
            stat_frame = tk.Frame(stats_row, bg="white", padx=20)
            stat_frame.pack(side=tk.LEFT)
            
            value_label = tk.Label(
                stat_frame,
                text=value,
                font=("Arial", 18, "bold"),
                fg="#2196F3",
                bg="white"
            )
            value_label.pack()
            
            tk.Label(
                stat_frame,
                text=label,
                font=("Arial", 9),
                fg="#666666",
                bg="white"
            ).pack()
            
            self.stats_labels[label] = value_label
    
    def create_table(self, parent):
        """Create records table"""
        # Scrollbars
        vsb = ttk.Scrollbar(parent, orient="vertical")
        hsb = ttk.Scrollbar(parent, orient="horizontal")
        
        # Treeview
        columns = ("Date", "Time", "Name", "Type", "Confidence", "Notes")
        self.table = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        vsb.config(command=self.table.yview)
        hsb.config(command=self.table.xview)
        
        # Column headings
        widths = [100, 80, 150, 100, 100, 150]
        for col, width in zip(columns, widths):
            self.table.heading(col, text=col, anchor=tk.W)
            self.table.column(col, width=width, anchor=tk.W)
        
        # Pack
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Store all records
        self.all_records = []
    
    def load_records(self):
        """Load attendance records"""
        try:
            # Clear table
            for item in self.table.get_children():
                self.table.delete(item)
            
            # Load from CSV
            attendance_file = Path("logs/attendance.csv")
            if not attendance_file.exists():
                self.update_stats([], [])
                return
            
            records = []
            with open(attendance_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(row)
            
            # Filter by date
            filtered = self.filter_by_date(records)
            self.all_records = filtered
            
            # Display records
            for record in filtered:
                values = (
                    record['date'],
                    record['time'],
                    record['person_name'],
                    record['type'].replace('_', ' ').title(),
                    f"{float(record['confidence']):.2%}" if record['confidence'] else "N/A",
                    record.get('notes', '')
                )
                self.table.insert('', 'end', values=values)
            
            # Update stats
            self.update_stats(filtered, records)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load records: {str(e)}")
    
    def filter_by_date(self, records):
        """Filter records by date range"""
        date_filter = self.date_filter.get()
        
        if date_filter == "all":
            return records
        
        today = datetime.now().date()
        
        filtered = []
        for record in records:
            try:
                record_date = datetime.fromisoformat(record['date']).date()
                
                if date_filter == "today":
                    if record_date == today:
                        filtered.append(record)
                elif date_filter == "week":
                    week_start = today - timedelta(days=today.weekday())
                    if record_date >= week_start:
                        filtered.append(record)
                elif date_filter == "month":
                    if record_date.year == today.year and record_date.month == today.month:
                        filtered.append(record)
            except:
                continue
        
        return filtered
    
    def filter_records(self):
        """Filter records by search"""
        search_text = self.search_var.get().lower()
        
        # Clear table
        for item in self.table.get_children():
            self.table.delete(item)
        
        # Filter and display
        for record in self.all_records:
            if (search_text in record['person_name'].lower() or
                search_text in record['type'].lower() or
                search_text in record['date'].lower()):
                
                values = (
                    record['date'],
                    record['time'],
                    record['person_name'],
                    record['type'].replace('_', ' ').title(),
                    f"{float(record['confidence']):.2%}" if record['confidence'] else "N/A",
                    record.get('notes', '')
                )
                self.table.insert('', 'end', values=values)
    
    def update_stats(self, filtered_records, all_records):
        """Update statistics"""
        total = len(filtered_records)
        unique = len(set(r['person_name'] for r in filtered_records))
        check_ins = len([r for r in filtered_records if r['type'] == 'check_in'])
        check_outs = len([r for r in filtered_records if r['type'] == 'check_out'])
        
        self.stats_labels["Total Records"].config(text=str(total))
        self.stats_labels["Unique Persons"].config(text=str(unique))
        self.stats_labels["Check-ins"].config(text=str(check_ins))
        self.stats_labels["Check-outs"].config(text=str(check_outs))
    
    def export_csv(self):
        """Export to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"attendance_{datetime.now().strftime('%Y%m%d')}.csv"
            )
            
            if not filename:
                return
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Time", "Name", "Type", "Confidence", "Notes"])
                
                for record in self.all_records:
                    writer.writerow([
                        record['date'],
                        record['time'],
                        record['person_name'],
                        record['type'],
                        record['confidence'],
                        record.get('notes', '')
                    ])
            
            messagebox.showinfo("Success", f"Exported {len(self.all_records)} records to CSV")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def generate_report(self):
        """Generate detailed report"""
        try:
            if not self.all_records:
                messagebox.showwarning("No Data", "No records to generate report")
                return
            
            # Generate report
            report_dir = Path("reports")
            report_dir.mkdir(exist_ok=True)
            
            date_str = datetime.now().strftime('%Y-%m-%d')
            report_file = report_dir / f"report_{date_str}_{self.date_filter.get()}.txt"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write(f"ATTENDANCE REPORT - {self.date_filter.get().upper()}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 70 + "\n\n")
                
                # Summary
                f.write("SUMMARY:\n")
                f.write("-" * 70 + "\n")
                for label, value_widget in self.stats_labels.items():
                    f.write(f"{label}: {value_widget.cget('text')}\n")
                f.write("\n")
                
                # Detailed records
                f.write("DETAILED RECORDS:\n")
                f.write("-" * 70 + "\n")
                
                for record in self.all_records:
                    f.write(f"\nDate: {record['date']}\n")
                    f.write(f"Time: {record['time']}\n")
                    f.write(f"Name: {record['person_name']}\n")
                    f.write(f"Type: {record['type'].replace('_', ' ').title()}\n")
                    f.write(f"Confidence: {record['confidence']}\n")
                    if record.get('notes'):
                        f.write(f"Notes: {record['notes']}\n")
                    f.write("-" * 70 + "\n")
            
            messagebox.showinfo("Success", f"Report generated:\n{report_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
