from fastapi import FastAPI
from datetime import date
from database import init_db, fetch_tasks, insert_task
from schemas import TaskCreate

app = FastAPI()

init_db()

@app.get("/")
def home():
    return {"message": "Welcome to Daily Task Tracker App"}

@app.post("/tasks")
def create_task(task:TaskCreate):
    insert_task(
        description = task.description,
        task_type = task.task_type,
        priority_section = task.priority_section,
        due_date = task.due_date,
        due_time = task.due_time
    )

    return {"message": "Task created successfully"}

@app.get("/tasks")
def get_tasks():
    tasks = fetch_tasks()
    return {"tasks": tasks}
   