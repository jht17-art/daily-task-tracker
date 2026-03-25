import flet as ft
from ui.task_card import build_task_card

def build_daily_task_view(selected_date, tasks, on_complete, on_edit, on_delete, on_previous_day, on_next_day):
    header = ft.Row(
        [ft.Button("Previous Day", on_click=on_previous_day),
         ft.Text(f"Daily Tasks - {selected_date.isoformat()}",size=22, weight=ft.FontWeight.BOLD),
         ft.Button("Next Day", on_click=on_next_day)  
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    
    if not tasks:
        return ft.Column([
            header,
            ft.Text("No tasks for this day.")
        ])
    task_cards = [
        build_task_card(task, on_complete, on_edit, on_delete)
        for task in tasks
    ]
    return ft.Column([
        header,
        *task_cards
    ])