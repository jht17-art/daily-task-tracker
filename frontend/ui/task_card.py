import flet as ft

def build_task_card(task, on_complete, on_edit, on_delete):
    is_completed = task["completed"] == 1
    return ft.Container(
        bgcolor = ft.Colors.GREY_200 if is_completed else ft.Colors.WHITE,
        content = ft.Column([
            ft.Text(
                task["description"],
                style=ft.TextStyle(
                    decoration=ft.TextDecoration.LINE_THROUGH
                ) if is_completed else None,
                color=ft.Colors.GREY if is_completed else ft.Colors.BLACK,
                weight=ft.FontWeight.BOLD,
                size=18
            ),
            ft.Text(f'Type: {task["task_type"]}', color=ft.Colors.GREY if is_completed else ft.Colors.BLACK),
            ft.Text(f'Priority: {task["priority_section"]}', color=ft.Colors.GREY if is_completed else ft.Colors.BLACK),
            ft.Text(f'Due: {task["due_date"]} {task["due_time"]}', color=ft.Colors.GREY if is_completed else ft.Colors.BLACK),
            ft.Row([
            ft.ElevatedButton("Done", disabled=is_completed, on_click=lambda e: on_complete(task["id"])),
            ft.ElevatedButton("Edit", on_click=lambda e: on_edit(task)),
            ft.ElevatedButton("Delete", on_click=lambda e: on_delete(task["id"])), 
        ]),
        ],
        spacing = 6                    
        ),
        padding=12,
        border=ft.border.all(1),
        border_radius=10,
        margin=ft.margin.only(bottom=10)
    )