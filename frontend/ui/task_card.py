import flet as ft

def build_task_card(task):
    return ft.Container(
        content = ft.Column([
            ft.Text(task["description"], weight=ft.FontWeight.BOLD,size=18),
            ft.Text(f'Type: {task["task_type"]}'),
            ft.Text(f'Priority: {task["priority_section"]}'),
            ft.Text(f'Due: {task["due_date"]} {task["due_time"]}')
        ],
        spacing = 6                    
        ),
        padding=12,
        border=ft.border.all(1),
        border_radius=10,
        margin=ft.margin.only(bottom=10)
    )