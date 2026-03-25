import flet as ft
import datetime
import threading
import time
from frontend.ui.form_view import build_task_form
from frontend.ui.task_list_view import build_task_list
from frontend.services.task_service import fetch_tasks_from_api, create_task_in_api, complete_task_in_api, update_task_in_api, delete_task_in_api
from frontend.ui.daily_task_view import build_daily_task_view
from frontend.backend_launcher import ensure_backend_running

def main(page: ft.Page):
    page.title = "Daily Task Tracker App"
    page.padding = 20
    page.scroll = "auto"
    page.window.width = 1100
    page.window.height = 800
    page.window.min_width = 900
    page.window.min_height = 650
    try:
        ensure_backend_running()
    except Exception as e:
        page.add(
            ft.Text("Failed to start backend", color=ft.Colors.RED),
            ft.Text(str(e), color=ft.Colors.RED),
        )
        return
    message_text = ft.Text("")
    task_list_container = ft.Column()
    form_parts = {}
    selected_date = datetime.date.today()
    daily_task_container = ft.Column()
    def show_temporary_message(text, color):
        message_text.value= text
        message_text.color = color
        page.update()
    #     def worker():
    #         time.sleep(2)
    #         if close_edit_dialog:
    #             page.pop_dialog()
    #         load_tasks()
    #         message_text.value=""
    #         page.update()
        # threading.Thread(target=worker, daemon=True).start()
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
            show_temporary_message("Task completed successfully", ft.Colors.GREEN)
            load_tasks()
        except Exception as e:
            message_text.value = f"Could not complete task: {e}"
            message_text.color = ft.Colors.RED
            page.update()
    def handle_delete_task(task_id):
        try:
            delete_task_in_api(task_id)
            show_temporary_message("Task deleted successfully", ft.Colors.GREEN)
            load_tasks()
        except Exception as e:
            message_text.value = f"Could not delete task: {e}"
            message_text.color = ft.Colors.RED
            page.update()
    
    def open_edit_dialog(task):
        if task["completed"] == 1:
            message_text.value = "Completed tasks cannot be edited"
            message_text.color = ft.Colors.RED
            page.update()
            return

        edit_description = ft.TextField(label="Description", value=task["description"], width=400)
        edit_task_type = ft.TextField(label="Task Type", value=task["task_type"], width=400)

        edit_priority = ft.Dropdown(
            label="Priority Section",
            width=400,
            value=task["priority_section"],
            options=[
                ft.dropdown.Option("immediate_urgent"),
                ft.dropdown.Option("immediate_not_urgent"),
                ft.dropdown.Option("not_immediate_urgent"),
                ft.dropdown.Option("not_immediate_not_urgent"),
            ]
        )

        edit_due_date = ft.Text(task["due_date"], size=16)
        edit_due_time = ft.Text(task["due_time"], size=16)
        def handle_edit_date_change(e):
            if e.control.value:
                edit_due_date.value = e.control.value.astimezone().date().isoformat()
                page.update()
        def handle_edit_time_change(e):
            if e.control.value:
                edit_due_time.value = e.control.value.strftime("%H:%M:%S")
                page.update()
        edit_date_picker = ft.DatePicker(
            on_change=handle_edit_date_change
        )

        edit_time_picker = ft.TimePicker(
            on_change=handle_edit_time_change
        )
        def open_edit_date_picker(e):
            page.show_dialog(edit_date_picker)

        def open_edit_time_picker(e):
            page.show_dialog(edit_time_picker)
        pick_edit_date_button = ft.Button("Pick Due Date", on_click=open_edit_date_picker)
        pick_edit_time_button = ft.Button("Pick Due Time", on_click=open_edit_time_picker)
        
        def close_dialog(e):
            page.pop_dialog()
        def submit_edit(e):
            nonlocal message_text
            try:
                updated_task_data = {
                    "description": edit_description.value.strip(),
                    "task_type": edit_task_type.value.strip(),
                    "priority_section": edit_priority.value,
                    "due_date": edit_due_date.value,
                    "due_time": edit_due_time.value,
                }

                if not updated_task_data["description"]:
                    message_text.value = "Description is required"
                    message_text.color = ft.Colors.RED
                    edit_dialog.update()
                    return

                if not updated_task_data["task_type"]:
                    message_text.value = "Task type is required"
                    message_text.color = ft.Colors.RED
                    edit_dialog.update()
                    return

                if not updated_task_data["priority_section"]:
                    message_text.value = "Please select a priority"
                    message_text.color = ft.Colors.RED
                    edit_dialog.update()
                    return

                if not edit_due_date.value:
                    message_text.value = "Please select a due date"
                    message_text.color = ft.Colors.RED
                    edit_dialog.update()
                    return

                if not edit_due_time.value:
                    message_text.value = "Please select a due time"
                    message_text.color = ft.Colors.RED
                    edit_dialog.update()
                    return
                
                
                update_task_in_api(task["id"], updated_task_data)
                page.pop_dialog()
                show_temporary_message("Task updated successfully", ft.Colors.GREEN)
                load_tasks()

            except Exception as e:
                message_text.value = f"Task couldn't be updated: {e}"
                message_text.color = ft.Colors.RED
                edit_dialog.update()
        edit_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Edit Task"),
                content=ft.Column(
                    [
                        edit_description,
                        edit_task_type,
                        edit_priority,
                        ft.Row([
                            ft.Container(
                                content=edit_due_date,
                                width=300,
                                padding=10,
                                border=ft.Border.all(1),
                                border_radius=8,
                            ),
                            pick_edit_date_button
                        ], spacing=10),
                        ft.Row([
                            ft.Container(
                                content=edit_due_time,
                                width=300,
                                padding=10,
                                border=ft.Border.all(1),
                                border_radius=8,
                            ),
                            pick_edit_time_button
                        ], spacing=10),
                        message_text,
                    ],
                    tight=True,
                    spacing=10,
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=close_dialog),
                    ft.Button("Update Task", on_click=submit_edit),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

        page.show_dialog(edit_dialog)
    def handle_edit_task(task):
       message_text.value=""
       open_edit_dialog(task)
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
            form_parts["add_button"].content = "Add Task"
            form_parts["add_button"].bgcolor = ft.Colors.GREY
            form_parts["description_field"].value = ""
            form_parts["task_type_field"].value = ""
            form_parts["priority_dropdown"].value = None
            form_parts["due_date_text"].value = "No date selected"
            form_parts["due_time_text"].value = "No time selected"
            show_temporary_message("Task added successfully", ft.Colors.GREEN)
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
        daily_task_container,
        ft.Divider(),
        task_list_container
    )
    load_tasks()
ft.run(main)