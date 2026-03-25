import flet as ft
import datetime

def build_task_form(on_add_click,on_input_change,page):
    description_field = ft.TextField(label="Description", width=400, on_change=on_input_change)
    task_type_field = ft.TextField(label="Task Type", width=400, on_change=on_input_change)
    due_date_text = ft.Text("No date selected", size=16)
    due_time_text = ft.Text("No time selected", size=16)
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
    def handle_date_change(e):
        if e.control.value:
            due_date_text.value = e.control.value.astimezone().date().isoformat()
            page.update()

    def handle_time_change(e):
        if e.control.value:
            due_time_text.value = e.control.value.strftime("%H:%M:%S")
            page.update()

    today = datetime.datetime.now()

    date_picker = ft.DatePicker(
        first_date=datetime.date(today.year - 1, 1, 1),
        last_date=datetime.date(today.year + 1, 12, 31),
        on_change=handle_date_change,
    )
    time_picker = ft.TimePicker(
        on_change=handle_time_change,
    )

    def open_date_picker(e):
        page.show_dialog(date_picker)

    def open_time_picker(e):
        page.show_dialog(time_picker)
        
    add_button = ft.Button("Add Task", on_click=on_add_click, bgcolor=ft.Colors.GREY)
    pick_date_button = ft.Button("Pick Due Date", on_click=open_date_picker)
    pick_time_button = ft.Button("Pick Due Time", on_click=open_time_picker)
    return {
        "form" : ft.Column([
        ft.Text("Add Task", size=22, weight= ft.FontWeight.BOLD),
        description_field,
        task_type_field,
        priority_dropdown,
        ft.Row(
            [
                ft.Container(
                    content=due_date_text,
                    width=380,
                    padding=10,
                    border=ft.Border.all(1),
                    border_radius=8,
                ),
                pick_date_button,
            ],
            spacing=10,
        ),

        ft.Row(
            [
                ft.Container(
                    content=due_time_text,
                    width=380,
                    padding=10,
                    border=ft.Border.all(1),
                    border_radius=8,
                ),
                pick_time_button,
            ],
            spacing=10,
        ),
        add_button
    ]),
        "description_field" : description_field,
        "task_type_field" : task_type_field,
        "priority_dropdown" : priority_dropdown,
        "due_date_text" : due_date_text,
        "due_time_text" : due_time_text,
        "add_button": add_button
    }