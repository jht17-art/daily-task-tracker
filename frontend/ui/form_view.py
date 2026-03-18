import flet as ft

def build_task_form():
    description_field = ft.TextField(label="Description", width=400)
    task_type_field = ft.TextField(label="Task Type", width=400)
    due_date_field = ft.TextField(label="Due Date (YYYY-MM-DD)", width=400)
    due_time_field = ft.TextField(label="Due Time (HH:MM:SS)", width=400)
    priority_dropdown = ft.Dropdown(
        label="Priority Section",
        width=400,
        options=[
            ft.dropdown.Option("immediate_urgent"),
            ft.dropdown.Option("immediate_not_urgent"),
            ft.dropdown.Option("not_immediate_urgent"),
            ft.dropdown.Option("not_immediate_not_urgent"),
        ]
    )
    def handle_add(e):
        print(description_field.value)
        print(task_type_field.value)
        print(priority_dropdown.value)
    add_button = ft.ElevatedButton("Add Task", on_click=handle_add)
    return ft.Column([
        ft.Text("Add Task", size=22, weight= ft.FontWeight.BOLD),
        description_field,
        task_type_field,
        priority_dropdown,
        due_date_field,
        due_time_field,
        add_button
    ])