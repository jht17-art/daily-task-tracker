import flet as ft
import datetime
from ui.form_view import build_task_form
from ui.task_list_view import build_task_list
from services.task_service import fetch_tasks_from_api, create_task_in_api, complete_task_in_api, update_task_in_api, delete_task_in_api
from ui.daily_task_view import build_daily_task_view

def main(page: ft.Page):
    page.title = "Daily Task Tracker App"
    page.padding = 20
    page.scroll = "auto"
    message_text = ft.Text("")
    task_list_container = ft.Column()
    form_parts = {}
    selected_date = datetime.date.today()
    daily_task_container = ft.Column()
    def get_task_for_selected_date(tasks, selected_date):
        selected_date_str = selected_date.isoformat()
        filtered_tasks = [task for task in tasks if task["due_date"] == selected_date_str and task["completed"] == 0]
        filtered_tasks.sort(key=lambda task: task["due_time"])
        return filtered_tasks
    def show_previous_day(e):
       nonlocal selected_date
       selected_date = selected_date - datetime.timedelta(days=1)
       load_tasks() 
    def show_next_day(e):
       nonlocal selected_date
       selected_date = selected_date + datetime.timedelta(days=1)
       load_tasks() 
    def handle_complete_task(task_id):
        try:
            complete_task_in_api(task_id)
            message_text.value = "Task marked as completed"
            message_text.color = ft.Colors.GREEN
            load_tasks()
        except Exception as e:
            message_text.value = f"Could not complete task: {e}"
            message_text.color = ft.Colors.RED
            page.update()
    def handle_delete_task(task_id):
        try:
            delete_task_in_api(task_id)
            message_text.value = "Task deleted successfully"
            message_text.color = ft.Colors.GREEN
            load_tasks()
        except Exception as e:
            message_text.value = f"Could not delete task: {e}"
            message_text.color = ft.Colors.RED
            page.update()
    editing_task_id  = None
    def handle_edit_task(task):
        nonlocal editing_task_id
        editing_task_id = task["id"]
        form_parts["description_field"].value = task["description"]
        form_parts["task_type_field"].value = task["task_type"]
        form_parts["priority_dropdown"].value = task["priority_section"]
        form_parts["due_date_text"].value = task["due_date"]
        form_parts["due_time_text"].value = task["due_time"]
        form_parts["add_button"].content = "Update Task"
        form_parts["add_button"].bgcolor = ft.Colors.ORANGE
        message_text.value = f"Editing task #{task['id']}"
        message_text.color = ft.Colors.BLUE
        page.update()
    def load_tasks():
        try:
            tasks = fetch_tasks_from_api()
            task_list_container.controls.clear()
            task_list_container.controls.append(build_task_list(tasks, handle_complete_task, handle_edit_task, handle_delete_task))
            daily_tasks = get_task_for_selected_date(tasks, selected_date)
            daily_task_container.controls.clear()
            daily_task_container.controls.append(
                build_daily_task_view(
                    selected_date, daily_tasks, handle_complete_task, handle_edit_task, handle_delete_task, show_previous_day, show_next_day
                )
            )
        except Exception as e:
            task_list_container.controls.clear()
            task_list_container.controls.append(ft.Text("Failed to load tasks"))
            message_text.value = f"Error: {e}"
            message_text.color = ft.Colors.RED
        page.update()
    def clear_message(e):
        message_text.value=""
        page.update()
    def handle_add_task(e):
        nonlocal editing_task_id
        try:
            description= form_parts["description_field"].value.strip()
            task_type = form_parts["task_type_field"].value.strip()
            priority_section = form_parts["priority_dropdown"].value
            due_date = form_parts["due_date_text"].value
            due_time = form_parts["due_time_text"].value
            if not description:
                message_text.value = "Description is required"
                message_text.color = ft.Colors.RED
                page.update()
                return

            if not task_type:
                message_text.value = "Task type is required"
                message_text.color = ft.Colors.RED
                page.update()
                return

            if not priority_section:
                message_text.value = "Please select a priority"
                message_text.color = ft.Colors.RED
                page.update()
                return

            if due_date == "No date selected":
                message_text.value = "Please select a due date"
                message_text.color = ft.Colors.RED
                page.update()
                return

            if due_time == "No time selected":
                message_text.value = "Please select a due time"
                message_text.color = ft.Colors.RED
                page.update()
                return
            
            task_data = {
                "description" : description,
                "task_type" : task_type,
                "priority_section": priority_section,
                "due_date": due_date,
                "due_time": due_time
            } 
            if editing_task_id is None:
                create_task_in_api(task_data)
                message_text.value = "Task added successfully"
            else:
                update_task_in_api(editing_task_id, task_data)
                message_text.value = "Task updated successfully"

            message_text.color = ft.Colors.GREEN
            editing_task_id = None
            form_parts["add_button"].content = "Add Task"
            form_parts["add_button"].bgcolor = ft.Colors.GREY
            form_parts["description_field"].value = ""
            form_parts["task_type_field"].value = ""
            form_parts["priority_dropdown"].value = None
            form_parts["due_date_text"].value = "No date selected"
            form_parts["due_time_text"].value = "No time selected"
            load_tasks()
        except Exception as e:
            if editing_task_id is None:
                message_text.value = f"Task couldn't be added: {e}"
            else:
                message_text.value = f"Task couldn't be updated: {e}"
            message_text.color = ft.Colors.RED
            page.update()
    form_parts = build_task_form(handle_add_task,clear_message,page)
    form_section = form_parts["form"]
    page.add(
        ft.Text("Daily Task Tracker", size=28, weight=ft.FontWeight.BOLD),
        form_section,
        message_text,
        ft.Divider(),
        daily_task_container,
        ft.Divider(),
        task_list_container
    )
    load_tasks()
ft.run(main)