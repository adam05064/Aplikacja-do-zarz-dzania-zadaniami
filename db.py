import mysql.connector
from mysql.connector import Error
from task import Task

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                database="nazwa bazy",
                user="login",
                password="hasło",
                host="Adres IP bazy",
                port="3306"
            )
            print("Połączono z bazą danych MariaDB!")
        except Error as e:
            print("Wystąpił błąd podczas łączenia z bazą danych MariaDB:", e)
            self.conn = None

    def get_all_tasks(self):
        tasks = []
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute("SELECT id, title, description, due_date, priority, completed FROM tasks")
                rows = cur.fetchall()
                tasks = [Task(*row) for row in rows]
            except Error as e:
                print("Wystąpił błąd podczas ładowania zadań:", e)
        return tasks

    def add_task(self, title, description, due_date, priority):
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute(
                    "INSERT INTO tasks (title, description, due_date, priority) VALUES (%s, %s, %s, %s)",
                    (title, description, due_date, priority)
                )
                self.conn.commit()
                return cur.lastrowid
            except Error as e:
                print("Wystąpił błąd podczas dodawania zadania:", e)
        return None

    def update_task(self, task_id, title, description, due_date, priority):
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute(
                    "UPDATE tasks SET title = %s, description = %s, due_date = %s, priority = %s WHERE id = %s",
                    (title, description, due_date, priority, task_id)
                )
                self.conn.commit()
                return True
            except Error as e:
                print("Wystąpił błąd podczas edytowania zadania:", e)
        return False

    def delete_task(self, task_id):
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                self.conn.commit()
                return True
            except Error as e:
                print("Wystąpił błąd podczas usuwania zadania:", e)
        return False

    def complete_task(self, task_id):
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute("UPDATE tasks SET completed = %s WHERE id = %s", (True, task_id))
                self.conn.commit()
                return True
            except Error as e:
                print("Wystąpił błąd podczas oznaczania zadania jako ukończone:", e)
        return False

    def __del__(self):
        if self.conn:
            self.conn.close()
            print("Połączenie z bazą danych zostało zamknięte.")
