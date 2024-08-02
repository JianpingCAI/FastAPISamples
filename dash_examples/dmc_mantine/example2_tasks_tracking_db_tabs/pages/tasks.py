import dash
from dash import callback, Input, Output, html, dcc, State
import dash_mantine_components as dmc
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.task import Task, TaskCreate
from utils.crud import get_tasks, create_task, update_task_status, delete_task
from typing import List

dash.register_page(__name__, path="/tasks")


def load_tasks() -> List[Task]:
    db: Session = SessionLocal()
    tasks = get_tasks(db)
    db.close()
    return tasks


def generate_table_rows(tasks: List[Task], status_filter: str) -> List[html.Tr]:
    rows = []
    for task in tasks:
        if task.status == status_filter:
            rows.append(
                html.Tr(
                    [
                        html.Td(task.task_name),
                        html.Td(task.description),
                        html.Td(task.due_date),
                        html.Td(task.status),
                        html.Td(
                            [
                                dmc.Button(
                                    "Complete",
                                    id={
                                        "type": "complete-button",
                                        "index": str(task.id),
                                    },
                                ),
                                dmc.Button(
                                    "Delete",
                                    id={"type": "delete-button", "index": str(task.id)},
                                ),
                            ]
                        ),
                    ]
                )
            )
    return rows


layout = dmc.MantineProvider(
    [
        dcc.Store(id="tasks-page-load", data={"load": True}),
        dcc.Store(id="modal-submitted", data=False),
        dmc.Title("Tasks", order=1),
        dmc.Button("Add Task", id="open-modal-button"),
        dmc.Modal(
            id="task-modal",
            title="Add Task",
            children=[
                dmc.TextInput(
                    id="task-name", label="Task Name", placeholder="Enter task name"
                ),
                dmc.Textarea(
                    id="task-desc",
                    label="Description",
                    placeholder="Enter task description",
                ),
                dmc.DatePicker(id="task-due-date", label="Due Date"),
                dmc.Button("Submit", id="submit-task-button", n_clicks=0),
            ],
            opened=False,
        ),
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.TabsTab("Pending", value="pending"),
                        dmc.TabsTab("Completed", value="completed"),
                    ]
                ),
                dmc.TabsPanel(
                    value="pending",
                    children=[
                        dmc.Table(
                            [
                                html.Thead(
                                    html.Tr(
                                        [
                                            html.Th(col)
                                            for col in [
                                                "Task Name",
                                                "Description",
                                                "Due Date",
                                                "Status",
                                                "Actions",
                                            ]
                                        ]
                                    )
                                ),
                                html.Tbody(id="pending-tasks-table"),
                            ]
                        )
                    ],
                ),
                dmc.TabsPanel(
                    value="completed",
                    children=[
                        dmc.Table(
                            [
                                html.Thead(
                                    html.Tr(
                                        [
                                            html.Th(col)
                                            for col in [
                                                "Task Name",
                                                "Description",
                                                "Due Date",
                                                "Status",
                                                "Actions",
                                            ]
                                        ]
                                    )
                                ),
                                html.Tbody(id="completed-tasks-table"),
                            ]
                        )
                    ],
                ),
            ],
            value="pending",
        ),
    ]
)


@callback(
    Output("task-modal", "opened"),
    Input("open-modal-button", "n_clicks"),
    Input("modal-submitted", "data"),
    State("task-modal", "opened"),
)
def toggle_modal(n_clicks, modal_submitted, is_open):
    if modal_submitted:
        return False
    if n_clicks:
        return not is_open
    return is_open


@callback(
    Output("modal-submitted", "data"),
    Input("submit-task-button", "n_clicks"),
    State("task-name", "value"),
    State("task-desc", "value"),
    State("task-due-date", "value"),
)
def submit_task(n_clicks, name, desc, due_date):
    if n_clicks:
        db: Session = SessionLocal()
        new_task = TaskCreate(task_name=name, description=desc, due_date=due_date)
        create_task(db, new_task)
        db.close()
        return True
    return False


@callback(
    Output("pending-tasks-table", "children"),
    Output("completed-tasks-table", "children"),
    Input("tasks-page-load", "data"),
    Input("modal-submitted", "data"),
)
def display_tasks(_, modal_submitted):
    tasks = load_tasks()
    pending_rows = generate_table_rows(tasks, "Pending")
    completed_rows = generate_table_rows(tasks, "Completed")
    return pending_rows, completed_rows


@callback(
    Output("pending-tasks-table", "children", allow_duplicate=True),
    Output("completed-tasks-table", "children", allow_duplicate=True),
    Input({"type": "complete-button", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def complete_task(n_clicks):
    if n_clicks is None or all(click is None for click in n_clicks):
        return dash.no_update, dash.no_update
    triggered_id = dash.callback_context.triggered_id
    if triggered_id is None:
        return dash.no_update, dash.no_update
    task_id = int(triggered_id["index"])
    db: Session = SessionLocal()
    update_task_status(db, task_id, "Completed")
    db.close()
    tasks = load_tasks()
    pending_rows = generate_table_rows(tasks, "Pending")
    completed_rows = generate_table_rows(tasks, "Completed")
    return pending_rows, completed_rows


@callback(
    Output("pending-tasks-table", "children", allow_duplicate=True),
    Output("completed-tasks-table", "children", allow_duplicate=True),
    Input({"type": "delete-button", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def delete_task_callback(n_clicks):
    if n_clicks is None or all(click is None for click in n_clicks):
        return dash.no_update, dash.no_update
    triggered_id = dash.callback_context.triggered_id
    if triggered_id is None:
        return dash.no_update, dash.no_update
    task_id = int(triggered_id["index"])
    db: Session = SessionLocal()
    delete_task(db, task_id)
    db.close()
    tasks = load_tasks()
    pending_rows = generate_table_rows(tasks, "Pending")
    completed_rows = generate_table_rows(tasks, "Completed")
    return pending_rows, completed_rows
