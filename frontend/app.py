import flet as ft
from ui.form_view import build_task_form
from ui.task_list_view import build_task_list
from services.task_service import fetch_tasks_from_api, create_task_in_api

def main(page: ft.Page):
    page.title = "Daily Task Tracker App"
    page.padding = 20
    page.scroll = "auto"
    message_text = ft.Text("")
    task_list_container = ft.Column()
    def load_tasks():
        try:
            tasks = fetch_tasks_from_api()
            task_list_container.controls.clear()
            task_list_container.controls.append(build_task_list(tasks))
        except Exception as e:
            task_list_container.controls.clear()
            task_list_container.controls.append(ft.Text("Failed to load tasks"))
            message_text.value = f"Error: {e}"
            message_text.color = ft.Colors.RED
        page.update()
        
    form_parts = {}
    def clear_message(e):
        message_text.value=""
        page.update()
    def handle_add_task(e):
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
            create_task_in_api(task_data)
            
            form_parts["description_field"].value = ""
            form_parts["task_type_field"].value = ""
            form_parts["priority_dropdown"].value = None
            form_parts["due_date_text"].value = "No date selected"
            form_parts["due_time_text"].value = "No time selected"
            message_text.value = "Task added successfully"
            message_text.color = ft.Colors.GREEN
            load_tasks()
        except Exception as e:
            message_text.value = f"Task couldn't be added: {e}"
            message_text.color = ft.Colors.RED
            page.update()
    form_parts = build_task_form(handle_add_task,clear_message,page)
    form_section = form_parts["form"]
    page.add(
        ft.Text("Daily Task Tracker", size=28, weight=ft.FontWeight.BOLD),
        form_section,
        message_text,
        ft.Divider(),
        task_list_container
    )
    load_tasks()
ft.run(main)