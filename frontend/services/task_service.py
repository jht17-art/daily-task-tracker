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

