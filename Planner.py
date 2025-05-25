import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry 
import os
import json
import time
APP_NAME = "Student Assignment Planner"
DATA_FILE = os.path.join(os.path.expanduser("~"), "Documents", "student_assignments.json")
STATUS_OPTIONS = ["To Do", "In Progress", "Completed", "Deferred"]
DEFAULT_STATUS = STATUS_OPTIONS[0]
COMPLETED_STATUS = STATUS_OPTIONS[2]
PRIORITY_OPTIONS = ["High", "Medium", "Low"]
DEFAULT_PRIORITY = PRIORITY_OPTIONS[1]
SUBJECT_OPTIONS = ["Mathematics", "Science", "History", "English", "Geography", "Physics", "Chemistry", "Biology", "Computer Science", "Art", "Music", "Other"]
DEFAULT_SUBJECT = SUBJECT_OPTIONS[0]
class TaskDialog(ttk.Toplevel):
    def __init__(self, parent, title="Task Details", task_data=None, subjects=SUBJECT_OPTIONS):
        super().__init__(master=parent, title=title) 
        self.transient(parent) 
        self.grab_set() 
        self.parent = parent
        self.result = None
        self.subjects = subjects
        self.geometry("600x600") 
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=BOTH, expand=YES)
        ttk.Label(frame, text="Assignment/Task Description:").grid(row=0, column=0, sticky=W, pady=5)
        self.desc_entry = ttk.Entry(frame, width=50)
        self.desc_entry.grid(row=0, column=1, columnspan=2, sticky=EW, pady=5)
        ttk.Label(frame, text="Subject:").grid(row=1, column=0, sticky=W, pady=5)
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(frame, textvariable=self.subject_var, values=self.subjects, state="readonly")
        self.subject_combo.grid(row=1, column=1, columnspan=2, sticky=EW, pady=5)
        self.subject_combo.set(DEFAULT_SUBJECT if not task_data else task_data.get('subject', DEFAULT_SUBJECT))
        ttk.Label(frame, text="Due Date:").grid(row=2, column=0, sticky=W, pady=5)
        self.due_date_entry = DateEntry(frame, bootstyle=INFO, dateformat="%Y-%m-%d") 
        self.due_date_entry.grid(row=2, column=1, columnspan=2, sticky=EW, pady=5)
        if task_data and task_data.get('due_date'):
            try:
                self.due_date_entry.entry.delete(0, END) 
                self.due_date_entry.entry.insert(0, task_data['due_date']) 
            except ValueError:
                pass 
        ttk.Label(frame, text="Priority:").grid(row=3, column=0, sticky=W, pady=5)
        self.priority_var = tk.StringVar()
        self.priority_combo = ttk.Combobox(frame, textvariable=self.priority_var, values=PRIORITY_OPTIONS, state="readonly")
        self.priority_combo.grid(row=3, column=1, columnspan=2, sticky=EW, pady=5)
        self.priority_combo.set(DEFAULT_PRIORITY if not task_data else task_data.get('priority', DEFAULT_PRIORITY))
        ttk.Label(frame, text="Status:").grid(row=4, column=0, sticky=W, pady=5)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(frame, textvariable=self.status_var, values=STATUS_OPTIONS, state="readonly")
        self.status_combo.grid(row=4, column=1, columnspan=2, sticky=EW, pady=5)
        self.status_combo.set(DEFAULT_STATUS if not task_data else task_data.get('status', DEFAULT_STATUS))
        ttk.Label(frame, text="Notes:").grid(row=5, column=0, sticky=(W,N), pady=5)
        self.notes_text = tk.Text(frame, height=5, width=40, wrap=tk.WORD, font=("Helvetica", 10))
        self.notes_text.grid(row=5, column=1, columnspan=2, sticky=EW, pady=5)
        notes_scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=self.notes_text.yview)
        notes_scrollbar.grid(row=5, column=3, sticky="ns")
        self.notes_text.configure(yscrollcommand=notes_scrollbar.set)
        if task_data:
            self.desc_entry.insert(0, task_data.get('description', ''))
            self.notes_text.insert(END, task_data.get('notes', ''))
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=6, column=0, columnspan=3, pady=10, sticky=E)
        save_button = ttk.Button(btn_frame, text="Save", command=self.on_save, bootstyle=SUCCESS)
        save_button.pack(side=LEFT, padx=5)
        cancel_button = ttk.Button(btn_frame, text="Cancel", command=self.on_cancel, bootstyle=SECONDARY)
        cancel_button.pack(side=LEFT, padx=5)
        self.desc_entry.bind("<Return>", lambda event: self.on_save())
        self.desc_entry.focus_set() 
        self.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    def on_save(self):
        description = self.desc_entry.get().strip()
        if not description:
            messagebox.showerror("Input Error", "Assignment description cannot be empty.", parent=self)
            return
        due_date_str = self.due_date_entry.entry.get() 
        if due_date_str:
            try:
                # Validate date format
                time.strptime(due_date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Input Error", "Invalid date format. Please use YYYY-MM-DD.", parent=self)
                return
        self.result = {
            "description": description,
            "subject": self.subject_var.get(),
            "due_date": due_date_str if due_date_str else None,
            "priority": self.priority_var.get(),
            "status": self.status_var.get(),
            "notes": self.notes_text.get("1.0", END).strip()
        }
        self.destroy()
    def on_cancel(self):
        self.result = None
        self.destroy()
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("950x700") 
        self.style = ttk.Style(theme='darkly') 
        self.tasks = []
        self.style.configure("Overstrike.TLabel", font=("Helvetica", 10, "overstrike"))
        self.style.configure("Normal.TLabel", font=("Helvetica", 10))
        self.style.configure("Timestamp.TLabel", font=("Helvetica", 9), foreground="gray")
        self.style.configure("Subject.TLabel", font=("Helvetica", 10, "bold"))
        self.style.configure("HighPriority.TLabel", foreground="red", font=("Helvetica", 10, "bold"))
        self.style.configure("MediumPriority.TLabel", foreground="orange", font=("Helvetica", 10))
        self.style.configure("LowPriority.TLabel", foreground="green", font=("Helvetica", 10))
        self.style.configure("Overdue.TLabel", foreground="lightcoral", font=("Helvetica", 9))
        self.create_widgets()
        self.load_tasks_from_file() 
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=BOTH, expand=YES)
        add_task_button = ttk.Button(main_frame, text="Add New Assignment", command=self.open_add_task_dialog, bootstyle=(PRIMARY, OUTLINE))
        add_task_button.pack(pady=(0,10), fill=X)
        tasks_list_frame = ttk.Labelframe(main_frame, text="Assignments", padding=10)
        tasks_list_frame.pack(fill=BOTH, expand=YES, pady=10)
        self.tasks_canvas = ttk.Canvas(tasks_list_frame, borderwidth=0)
        self.tasks_frame = ttk.Frame(self.tasks_canvas)
        self.scrollbar = ttk.Scrollbar(tasks_list_frame, orient=VERTICAL, command=self.tasks_canvas.yview)      
        self.tasks_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.tasks_canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        self.canvas_window = self.tasks_canvas.create_window((0, 0), window=self.tasks_frame, anchor=NW, tags="self.tasks_frame")
        self.tasks_frame.bind("<Configure>", self.on_frame_configure)
        self.tasks_canvas.bind("<Configure>", self.on_canvas_configure)
        self.root.bind("<MouseWheel>", self._on_mousewheel) # For Windows/Linux scrolling
        self.root.bind("<Button-4>", self._on_mousewheel) # For Linux scrolling up
        self.root.bind("<Button-5>", self._on_mousewheel) # For Linux scrolling down
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling for the canvas."""
        if event.num == 5 or event.delta < 0: # Scroll down
            self.tasks_canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0: # Scroll up
            self.tasks_canvas.yview_scroll(-1, "units")
    def on_frame_configure(self, event=None):
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
    def on_canvas_configure(self, event=None):
        self.tasks_canvas.itemconfig(self.canvas_window, width=event.width)
    def open_add_task_dialog(self):
        dialog = TaskDialog(self.root, title="Add New Assignment", subjects=SUBJECT_OPTIONS)
        self.root.wait_window(dialog) 
        if dialog.result:
            new_task_data = dialog.result
            if any(t['description'] == new_task_data['description'] and t['subject'] == new_task_data['subject'] for t in self.tasks):
                messagebox.showwarning("Duplicate Task", "An assignment with this description and subject already exists.", parent=self.root)
                return
            new_task_data['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S")
            new_task_data['id'] = time.time()
            self.tasks.append(new_task_data)
            self.sort_tasks()
            self.save_tasks_to_file()
            self.load_tasks_ui()
    def open_edit_task_dialog(self, task_to_edit):
        dialog = TaskDialog(self.root, title="Edit Assignment", task_data=task_to_edit, subjects=SUBJECT_OPTIONS)
        self.root.wait_window(dialog)
        if dialog.result:
            updated_data = dialog.result
            task_to_edit.update(updated_data) 
            self.sort_tasks()
            self.save_tasks_to_file()
            self.load_tasks_ui()
    def sort_tasks(self):
        def sort_key(task):
            due_date = float('inf')
            if task.get('due_date'):
                try:
                    due_date = time.mktime(time.strptime(task['due_date'], "%Y-%m-%d"))
                except (ValueError, TypeError):
                    pass 
            priority_order = {PRIORITY_OPTIONS[0]: 0, PRIORITY_OPTIONS[1]: 1, PRIORITY_OPTIONS[2]: 2} 
            priority_val = priority_order.get(task.get('priority'), 3)           
            return (task.get('status') == COMPLETED_STATUS, 
                    due_date,
                    priority_val,
                    task.get('created_at', ''))        
        self.tasks.sort(key=sort_key)
    def load_tasks_ui(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        
        if not self.tasks:
            ttk.Label(self.tasks_frame, text="No assignments yet. Click 'Add New Assignment' to start!",
                      font=("Helvetica", 12, "italic"), style="secondary.TLabel").pack(pady=20)
            self.tasks_frame.update_idletasks()
            self.on_frame_configure()
            return
        header_frame = ttk.Frame(self.tasks_frame)
        header_frame.pack(fill=X, pady=(0,5))
        header_labels = ["Description", "Subject", "Due Date", "Priority", "Status", "Actions"]
        col_weights = [4, 2, 2, 1, 2, 2] 
        for i, (label_text, weight) in enumerate(zip(header_labels, col_weights)):
            header_frame.columnconfigure(i, weight=weight)
            ttk.Label(header_frame, text=label_text, font=("Helvetica", 10, "bold")).grid(row=0, column=i, sticky=EW, padx=5)
        for task_data in self.tasks:
            task_item_frame = ttk.Frame(self.tasks_frame, padding=(8,10), relief=SOLID, borderwidth=1) 
            task_item_frame.pack(fill=X, expand=YES, pady=5)         
            for i, weight in enumerate(col_weights):
                task_item_frame.columnconfigure(i, weight=weight)
            current_status = task_data.get('status', DEFAULT_STATUS)
            is_completed = (current_status == COMPLETED_STATUS)
            label_style = "Overstrike.TLabel" if is_completed else "Normal.TLabel"
            desc_label = ttk.Label(task_item_frame, text=task_data.get('description', 'N/A'), style=label_style, anchor="w", wraplength=250)
            desc_label.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0,5))
            subj_label = ttk.Label(task_item_frame, text=task_data.get('subject', 'N/A'), style="Subject.TLabel", anchor="w")
            subj_label.grid(row=0, column=1, sticky="ew", padx=5)
            due_date_str = task_data.get('due_date', 'No Due Date')
            due_date_label_style = "Timestamp.TLabel"
            if task_data.get('due_date') and not is_completed:
                try:
                    due_timestamp = time.mktime(time.strptime(task_data['due_date'], "%Y-%m-%d"))
                    current_timestamp = time.time()
                    if due_timestamp < current_timestamp:
                        due_date_str += " (OVERDUE)"
                        due_date_label_style = "Overdue.TLabel"
                except ValueError:
                    pass 
            due_label = ttk.Label(task_item_frame, text=due_date_str, style=due_date_label_style, anchor="w")
            due_label.grid(row=0, column=2, sticky="ew", padx=5)
            priority_text = task_data.get('priority', DEFAULT_PRIORITY)
            priority_style = f"{priority_text}Priority.TLabel" if priority_text in PRIORITY_OPTIONS else "Normal.TLabel"
            prio_label = ttk.Label(task_item_frame, text=priority_text, style=priority_style, anchor="w")
            prio_label.grid(row=0, column=3, sticky="ew", padx=5)
            status_var = tk.StringVar(value=current_status)
            status_combo = ttk.Combobox(
                task_item_frame,
                textvariable=status_var,
                values=STATUS_OPTIONS,
                state="readonly",
                width=12
            )
            status_combo.grid(row=0, column=4, sticky="ew", padx=5)
            status_combo.bind("<<ComboboxSelected>>", 
                              lambda event, t_data=task_data, s_var=status_var, d_lbl=desc_label, due_lbl=due_label: \
                                 self.handle_status_change(event, t_data, s_var, d_lbl, due_lbl))
            notes_preview = task_data.get('notes', '')
            if notes_preview:
                notes_preview = (notes_preview[:30] + '...') if len(notes_preview) > 30 else notes_preview
                notes_label = ttk.Label(task_item_frame, text=f"Notes: {notes_preview}", style="Timestamp.TLabel", anchor="w", wraplength=250)
                notes_label.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5)
            actions_frame = ttk.Frame(task_item_frame)
            actions_frame.grid(row=0, column=5, rowspan=2, sticky="nse", padx=(5,0))
            edit_btn = ttk.Button(
                actions_frame,
                text="Edit",
                bootstyle=(INFO, OUTLINE),
                width=6,
                command=lambda t_data=task_data: self.open_edit_task_dialog(t_data)
            )
            edit_btn.pack(pady=2, fill=X)
            remove_btn = ttk.Button(
                actions_frame,
                text="Remove",
                bootstyle=(DANGER, OUTLINE),
                width=6,
                command=lambda t_data=task_data: self.remove_task(t_data)
            )
            remove_btn.pack(pady=2, fill=X)
        self.tasks_frame.update_idletasks()
        self.on_frame_configure()
    def handle_status_change(self, event, task_data, status_var, desc_label_widget, due_label_widget):
        new_status = status_var.get()
        task_data['status'] = new_status
        self.update_task_label_style(desc_label_widget, due_label_widget, task_data) 
        self.sort_tasks()
        self.save_tasks_to_file()
        self.load_tasks_ui()
    def update_task_label_style(self, desc_label_widget, due_label_widget, task_data):
        is_completed = (task_data.get('status') == COMPLETED_STATUS)
        label_style = "Overstrike.TLabel" if is_completed else "Normal.TLabel"
        desc_label_widget.configure(style=label_style)
        due_date_str = task_data.get('due_date', 'No Due Date')
        due_date_label_style = "Timestamp.TLabel"
        if task_data.get('due_date') and not is_completed:
            try:
                due_timestamp = time.mktime(time.strptime(task_data['due_date'], "%Y-%m-%d"))
                current_timestamp = time.time()
                if due_timestamp < current_timestamp:
                    due_date_str += " (OVERDUE)"
                    due_date_label_style = "Overdue.TLabel"
            except ValueError:
                pass
        due_label_widget.configure(text=due_date_str, style=due_date_label_style)
    def remove_task(self, task_to_remove):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove assignment: '{task_to_remove['description']}'?", parent=self.root):
            self.tasks.remove(task_to_remove)
            self.save_tasks_to_file()
            self.load_tasks_ui()
    def save_tasks_to_file(self):
        try:
            doc_dir = os.path.join(os.path.expanduser("~"), "Documents")
            if not os.path.exists(doc_dir):
                os.makedirs(doc_dir)

            with open(DATA_FILE, 'w') as f:
                json.dump(self.tasks, f, indent=4)
        except IOError as e:
            messagebox.showerror("Save Error", f"Could not save tasks to file: {e}", parent=self.root)   
    def load_tasks_from_file(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    loaded_data = json.load(f)
                    if isinstance(loaded_data, list) and all(isinstance(item, dict) for item in loaded_data):
                        self.tasks = loaded_data
                    else:
                        messagebox.showwarning("Load Warning", f"Task data file '{DATA_FILE}' seems corrupted or in an old format. Starting with an empty list.", parent=self.root)
                        self.tasks = []
            else:
                self.tasks = []
        except (IOError, json.JSONDecodeError) as e:
            messagebox.showerror("Load Error", f"Could not load tasks from file: {e}. Starting with an empty list.", parent=self.root)
            self.tasks = []
        self.sort_tasks() 
        self.load_tasks_ui() 
if __name__ == "__main__":
    root = ttk.Window(themename="darkly") 
    app = TaskManagerApp(root)
    root.mainloop()