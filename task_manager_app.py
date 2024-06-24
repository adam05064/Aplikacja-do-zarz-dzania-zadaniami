import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
from task import Task
from ui import TaskManagerUI


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.tasks = []

        # MariaDB connection
        try:
            self.conn = mysql.connector.connect(
                database="BazaZZ",
                user="adam",
                password="adam",
                host="172.29.37.125",
                port="3306"
            )
            print("Połączono z bazą danych MariaDB!")
        except mysql.connector.Error as e:
            print("Wystąpił błąd podczas łączenia z bazą danych MariaDB:", e)
            self.conn = None

        self.ui = TaskManagerUI(self.root, self)
        self.load_tasks()

    def load_tasks(self):
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute("SELECT id, title, description, due_date, priority, completed FROM tasks WHERE completed = 0")
                self.tasks = [Task(*row) for row in rows]
                self.ui.update_task_listbox(self.tasks)
            except mysql.connector.Error as e:
                print("Wystąpił błąd podczas ładowania zadań:", e)

    def add_task(self):
        title = simpledialog.askstring("Task Title", "Enter task title:")
        if title:
            description = simpledialog.askstring("Task Description", "Enter task description:")
            due_date = simpledialog.askstring("Task Due Date", "Enter task due date (YYYY-MM-DD):")
            priority = simpledialog.askstring("Task Priority", "Enter task priority (Low, Medium, High):")
            if self.conn is not None:
                try:
                    cur = self.conn.cursor()
                    cur.execute(
                        "INSERT INTO tasks (title, description, due_date, priority) VALUES (%s, %s, %s, %s)",
                        (title, description, due_date, priority)
                    )
                    self.conn.commit()
                    task_id = cur.lastrowid
                    new_task = Task(task_id, title, description, due_date, priority, False)
                    self.tasks.append(new_task)
                    self.ui.update_task_listbox(self.tasks)
                except mysql.connector.Error as e:
                    print("Wystąpił błąd podczas dodawania zadania:", e)

    def edit_task(self):
        selected_task_index = self.ui.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            task.title = simpledialog.askstring("Task Title", "Edit task title:", initialvalue=task.title)
            task.description = simpledialog.askstring("Task Description", "Edit task description:", initialvalue=task.description)
            task.due_date = simpledialog.askstring("Task Due Date", "Edit task due date (YYYY-MM-DD):", initialvalue=task.due_date)
            task.priority = simpledialog.askstring("Task Priority", "Edit task priority (Low, Medium, High):", initialvalue=task.priority)
            if self.conn is not None:
                try:
                    cur = self.conn.cursor()
                    cur.execute(
                        "UPDATE tasks SET title = %s, description = %s, due_date = %s, priority = %s WHERE id = %s",
                        (task.title, task.description, task.due_date, task.priority, task.id)
                    )
                    self.conn.commit()
                    self.ui.update_task_listbox(self.tasks)
                except mysql.connector.Error as e:
                    print("Wystąpił błąd podczas edytowania zadania:", e)

    def delete_task(self):
        selected_task_index = self.ui.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            if self.conn is not None:
                try:
                    cur = self.conn.cursor()
                    cur.execute("UPDATE tasks SET completed = 1 WHERE id = %s", (task.id,))
                    self.conn.commit()
                    self.tasks = [t for t in self.tasks if t.id != task.id]
                    self.ui.update_task_listbox(self.tasks)
                except mysql.connector.Error as e:
                    print("Wystąpił błąd podczas oznaczania zadania jako zakończone:", e)

    def complete_task(self):
        selected_task_index = self.ui.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            task.completed = True
            if self.conn is not None:
                try:
                    cur = self.conn.cursor()
                    cur.execute("UPDATE tasks SET completed = 1 WHERE id = %s", (task.id,))
                    self.conn.commit()
                    self.tasks = [t for t in self.tasks if t.id != task.id]
                    self.ui.update_task_listbox(self.tasks)
                except mysql.connector.Error as e:
                    print("Wystąpił błąd podczas oznaczania zadania jako zakończone:", e)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
