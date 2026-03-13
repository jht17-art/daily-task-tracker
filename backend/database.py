import sqlite3

def get_connection():
    conn = sqlite3.connect('database/tasks.db')
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE tasks (
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
              input_date TEXT,
              due_date TEXT,
              due_time TEXT,
              completed INTEGER,
              completed_at TEXT
              )""")
    print("Database initialized")
    conn.commit()
    conn.close()

def insert_task(description, task_type, priority_section, input_date, due_date, due_time, completed, completed_at):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (description, task_type, priority_section, input_date, due_date, due_time, completed, completed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    (description, task_type, priority_section, input_date, due_date, due_time, completed, completed_at)
    )
    print("Task added")
    conn.commit()
    conn.close()

def fetch_tasks():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    print(c.fetchall())
    conn.close()

if __name__ == "__main__":
   # init_db()
    insert_task("Submit report", "office", "immediate_urgent", "2026-03-13", "2026-03-14", "14:00", 0, None)
    fetch_tasks()

