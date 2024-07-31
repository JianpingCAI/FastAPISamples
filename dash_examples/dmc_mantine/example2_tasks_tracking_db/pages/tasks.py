import dash
from dash import callback, Input, Output, html
import dash_mantine_components as dmc
from sqlalchemy.orm import Session
from models.database import SessionLocal
from utils.crud import get_tasks, update_task_status, delete_task
import json
from typing import List
from models.task import Task

dash.register_page(__name__, path="/tasks")


def load_tasks() -> List[Task]:
    db: Session = SessionLocal()
    tasks = get_tasks(db)
    db.close()
    return tasks


layout = dmc.MantineProvider(
    [
        dmc.Title("Tasks", order=1),
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
                html.Tbody(id="task-table-body"),
            ]
        ),
    ]
)


@callback(Output("task-table-body", "children"), Input("task-table-body", "id"))
def display_tasks(_):
    tasks = load_tasks()
    rows = []
    for task in tasks:
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
                                id={"type": "complete-button", "index": str(task.id)},
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


@callback(
    Output("task-table-body", "children", allow_duplicate=True),
    Input({"type": "complete-button", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def complete_task(n_clicks):
    if n_clicks is None or all(click is None for click in n_clicks):
        return dash.no_update
    triggered_id = dash.callback_context.triggered_id
    if triggered_id is None:
        return dash.no_update
    task_id = int(triggered_id["index"])
    db: Session = SessionLocal()
    update_task_status(db, task_id, "Completed")
    db.close()
    return display_tasks(None)


@callback(
    Output("task-table-body", "children", allow_duplicate=True),
    Input({"type": "delete-button", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def delete_task(n_clicks):
    if n_clicks is None or all(click is None for click in n_clicks):
        return dash.no_update
    triggered_id = dash.callback_context.triggered_id
    if triggered_id is None:
        return dash.no_update
    task_id = int(triggered_id["index"])
    db: Session = SessionLocal()
    delete_task(db, task_id)
    db.close()
    return display_tasks(None)
