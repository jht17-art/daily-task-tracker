import flet as ft
from ui.task_card import build_task_card

def build_task_list(tasks, on_complete, on_edit, on_delete):
    if not tasks:
        return ft.Text("No tasks yet.")
    task_cards = [build_task_card(task, on_complete, on_edit, on_delete) for task in tasks]
    return ft.Column([
        ft.Text("Tasks", size=22, weight=ft.FontWeight.BOLD),
        *task_cards
    ])