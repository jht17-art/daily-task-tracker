import sqlite3

def get_connection():
    conn = sqlite3.connect('D:\daily-task-tracker\database/tasks.db')
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
    (description, task_type, priority_section, due_date, due_time)
    )
    print("Task added")
    conn.commit()
    conn.close()

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

if __name__ == "__main__":
   init_db()
   insert_task("Submit report", "office", "immediate_urgent","2026-03-14", "14:00")
   fetch_tasks()
    # drop_table()

