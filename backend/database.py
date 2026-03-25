from pathlib import Path
import os
import sqlite3

APP_DATA_DIR = Path(os.environ.get("FLET_APP_STORAGE_DATA", Path(__file__).resolve().parent))
DB_PATH = APP_DATA_DIR / "tasks.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS tasks (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              description TEXT,
              task_type TEXT,
              priority_section TEXT CHECK (
               priority_section IN (
               'immediate_urgent',
               'immediate_not_urgent',
               'not_immediate_urgent',
               'not_immediate_not_urgent'
                )
              ),
              input_date DATE DEFAULT CURRENT_DATE,
              due_date DATE,
              due_time TIME,

              completed INTEGER DEFAULT 0,
              completed_at DATETIME
              )""")
    print("Database initialized")
    conn.commit()
    conn.close()

def insert_task(description, task_type, priority_section, due_date, due_time):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (description, task_type, priority_section, due_date, due_time) VALUES (?, ?, ?, ?, ?)",
    (description, task_type, priority_section, str(due_date), str(due_time))
    )
    print("Task added")
    conn.commit()
    conn.close()
    return c.lastrowid

def fetch_tasks():
    conn = get_connection()
    c = conn.cursor()
    rows = c.execute("SELECT rowid, * FROM tasks ORDER BY completed ASC, due_date ASC, due_time ASC").fetchall()
    tasks = []
    for row in rows:
        tasks.append(dict(row))
    print(tasks)
    conn.close()
    return tasks

def drop_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS tasks")
    print("Table dropped or table doesn't exist")
    conn.commit()
    conn.close()

def get_task_by_id(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    row = cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)


def update_task(task_id, description, task_type, priority_section, due_date, due_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET description = ?,
            task_type = ?,
            priority_section = ?,
            due_date = ?,
            due_time = ?
        WHERE id = ?
    """, (
        description,
        task_type,
        priority_section,
        str(due_date),
        str(due_time),
        task_id
    ))

    conn.commit()
    updated_count = cursor.rowcount
    conn.close()

    return updated_count

def complete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = 1,
            completed_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    updated_count = cursor.rowcount
    conn.close()

    return updated_count

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()
    return deleted_count