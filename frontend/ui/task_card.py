import flet as ft
import datetime

def build_task_card(task, on_complete, on_edit, on_delete):
    is_completed = task["completed"] == 1
    due_datetime = datetime.datetime.strptime(
        f"{task['due_date']} {task['due_time']}",
        "%Y-%m-%d %H:%M:%S"
    )

    is_overdue = (not is_completed) and (datetime.datetime.now() > due_datetime)
    if is_completed:
        status_text = "Completed"
        status_color = ft.Colors.GREEN
    elif is_overdue:
        status_text = "Overdue"
        status_color = ft.Colors.RED
    else:
        status_text = "Pending"
        status_color = ft.Colors.BLUE
    
    if is_completed:
        card_bgcolor = ft.Colors.GREY_200
    elif is_overdue:
        card_bgcolor = ft.Colors.RED_50
    else:
        card_bgcolor = ft.Colors.WHITE
    return ft.Container(
        bgcolor = card_bgcolor,
        content = ft.Column([
            ft.Text(
                f"Status: {status_text}",
                color=status_color,
                weight=ft.FontWeight.BOLD
            ),
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
            ft.Button("Done", disabled=is_completed, on_click=lambda e: on_complete(task["id"])),
            ft.Button("Edit",  disabled=is_completed,on_click=lambda e: on_edit(task)),
            ft.Button("Delete", on_click=lambda e: on_delete(task["id"])), 
        ]),
        ],
        spacing = 6                    
        ),
        padding=12,
        border=ft.Border.all(1),
        border_radius=10,
        margin=ft.margin.only(bottom=10)
    )