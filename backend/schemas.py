from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import date, time, datetime

class PrioritySection(str, Enum):
    immediate_urgent = "immediate_urgent"
    immediate_not_urgent = "immediate_not_urgent"
    not_immediate_urgent = "not_immediate_urgent"
    not_immediate_not_urgent = "not_immediate_not_urgent"


class TaskCreate(BaseModel):
    description: str
    task_type: str
    priority_section: PrioritySection
    due_date: date
    due_time: time

class TaskUpdate(BaseModel):
    description: str
    task_type: str
    priority_section: PrioritySection
    due_date: date
    due_time: time


class TaskResponse(BaseModel):
    id: int
    description: str
    task_type: str
    priority_section: PrioritySection
    input_date: date
    due_date: date
    due_time: time
    completed: int
    completed_at: Optional[datetime] = None