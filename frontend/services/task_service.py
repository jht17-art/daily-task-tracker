import requests
from services.api import TASKS_URL

def fetch_tasks_from_api():
    try:    
        response = requests.get(TASKS_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Could not fetch tasks: {e}")

def create_task_in_api(task_data):
    try:    
        response = requests.post(TASKS_URL, json=task_data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Could not add task: {e}")

def complete_task_in_api(task_id):
    try:
        response = requests.put(f"{TASKS_URL}/{task_id}/complete")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Could not mark task completed: {e}")

def delete_task_in_api(task_id):
    try: 
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Could not delete task: {e}")

def update_task_in_api(task_id, task_data):
    try: 
        response = requests.put(f"{TASKS_URL}/{task_id}",json=task_data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Could not update task: {e}")

        