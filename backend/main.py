from fastapi import FastAPI, HTTPException, status
from datetime import date, time, datetime
from database import init_db, fetch_tasks, insert_task,  update_task, complete_task,delete_task,get_task_by_id
from schemas import TaskCreate, TaskUpdate, TaskResponse

app = FastAPI()

init_db()

@app.get("/")
def home():
    return {"message": "Welcome to Daily Task Tracker App"}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task:TaskCreate):
    task_id = insert_task(
        description = task.description,
        task_type = task.task_type,
        priority_section = task.priority_section.value,
        due_date=task.due_date,
        due_time=task.due_time
    )

    return {
        "message": "Task created successfully",
        "task_id": task_id
        }

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    tasks = fetch_tasks()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_single_task(task_id: int):
    task = get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@app.put("/tasks/{task_id}")
def edit_task(task_id: int, task: TaskUpdate):
    updated_count = update_task(
        task_id=task_id,
        description=task.description,
        task_type=task.task_type,
        priority_section=task.priority_section.value,
        due_date=task.due_date,
        due_time=task.due_time
    )

    if updated_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task updated successfully"}

@app.put("/tasks/{task_id}/complete")
def mark_task_complete(task_id: int):
    updated_count = complete_task(task_id)

    if updated_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task marked as completed"}

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    deleted_count = delete_task(task_id)

    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}