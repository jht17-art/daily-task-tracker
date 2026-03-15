from pydantic import BaseModel
from enum import Enum
from datetime import date, time

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