import tkinter as tk


class TaskManagerUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.task_listbox = tk.Listbox(root, width=50, height=20)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        self.task_listbox.bind('<Double-Button-1>', self.view_task_details)

        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        add_task_button = tk.Button(button_frame, text="Add Task", command=controller.add_task)
        add_task_button.pack(fill=tk.X)

        edit_task_button = tk.Button(button_frame, text="Edit Task", command=controller.edit_task)
        edit_task_button.pack(fill=tk.X)

        delete_task_button = tk.Button(button_frame, text="Delete Task", command=controller.delete_task)
        delete_task_button.pack(fill=tk.X)

        complete_task_button = tk.Button(button_frame, text="Complete Task", command=controller.complete_task)
        complete_task_button.pack(fill=tk.X)

    def update_task_listbox(self, tasks):
        self.task_listbox.delete(0, tk.END)
        for task in tasks:
            self.task_listbox.insert(tk.END, task.title)

    def view_task_details(self, event):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.controller.tasks[selected_task_index[0]]
            task_details = f"Title: {task.title}\nDescription: {task.description}\nDue Date: {task.due_date}\nPriority: {task.priority}\nCompleted: {'Yes' if task.completed else 'No'}"
            tk.messagebox.showinfo("Task Details", task_details)
