import flet as ft
from ui.form_view import build_task_form
from ui.task_list_view import build_task_list
from ui.task_card import build_task_card
from services.placeholder_data import get_sample_tasks

def main(page: ft.Page):
    page.title = "Daily Task Tracker App"
    # page.add(ft.Text("Hello, World!"))
    page.padding = 20
    page.scroll = "auto"
    tasks = get_sample_tasks()
    form_section = build_task_form()
    task_list_section = build_task_list(tasks)
    page.add(
        ft.Text("Daily Task Tracker", size=28, weight=ft.FontWeight.BOLD),
        form_section,
        ft.Divider(),
        task_list_section
    )

ft.run(main)