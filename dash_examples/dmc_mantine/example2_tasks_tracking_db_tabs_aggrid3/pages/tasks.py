import dash
from dash import callback, Input, Output, dcc, State
import dash_mantine_components as dmc
import dash_ag_grid as dag
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.task import Task, TaskCreate
from utils.crud import get_tasks, create_task, update_task_status, delete_task
from typing import List, Dict
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path="/tasks")


def load_tasks() -> List[Task]:
    db: Session = SessionLocal()
    tasks = get_tasks(db)
    db.close()
    return tasks


def generate_table_data(tasks: List[Task], status_filter: str) -> List[Dict]:
    return [
        {
            "id": str(task.id),  # Ensure each task has a unique ID as a string
            "task_name": task.task_name,
            "description": task.description,
            "due_date": task.due_date,
            "status": task.status,
        }
        for task in tasks
        if task.status == status_filter
    ]


task_columns = [
    {
        "headerName": "Select",
        "checkboxSelection": True,
        "headerCheckboxSelection": True,
        # "sortable": True,
    },
    {"headerName": "Task Name", "field": "task_name", "sortable": True, "filter": True},
    {
        "headerName": "Description",
        "field": "description",
        "sortable": False,
        "filter": False,
    },
    {"headerName": "Due Date", "field": "due_date", "sortable": True, "filter": True},
    {"headerName": "Status", "field": "status", "sortable": True, "filter": True},
]

gridOptions = {
    "animateRows": True,
    "pagination": True,
    "paginationPageSize": 10,
    "rowSelection": "multiple",
    # "getRowId": {"function": "params => params.data.id"},  # Correctly define getRowId, this is not necessary 
}

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
        dmc.Group(
            [
                dmc.Button(
                    "Complete Selected",
                    id="complete-selected-button",
                    style={"marginRight": "10px"},
                ),
                dmc.Button("Delete Selected", id="delete-selected-button"),
            ]
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
                        dag.AgGrid(
                            id="pending-tasks-table",
                            columnDefs=task_columns,
                            rowData=[],
                            dashGridOptions=gridOptions,
                            # defaultColDef={"filter": True},
                            # className="ag-theme-alpine-dark",
                            # columnSize="sizeToFit",
                        )
                    ],
                ),
                dmc.TabsPanel(
                    value="completed",
                    children=[
                        dag.AgGrid(
                            id="completed-tasks-table",
                            columnDefs=task_columns,
                            rowData=[],
                            dashGridOptions=gridOptions,
                        )
                    ],
                ),
            ],
            id="tasks-tabs",
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
    Output("pending-tasks-table", "rowData"),
    Output("completed-tasks-table", "rowData"),
    Input("tasks-page-load", "data"),
    Input("modal-submitted", "data"),
    prevent_initial_call=True,
)
def display_tasks(_, modal_submitted):
    tasks = load_tasks()
    pending_rows = generate_table_data(tasks, "Pending")
    completed_rows = generate_table_data(tasks, "Completed")
    return pending_rows, completed_rows


@callback(
    Output("pending-tasks-table", "rowData", allow_duplicate=True),
    Output("completed-tasks-table", "rowData", allow_duplicate=True),
    [
        Input("complete-selected-button", "n_clicks"),
        Input("delete-selected-button", "n_clicks"),
    ],
    [
        State("pending-tasks-table", "selectedRows"),
        State("completed-tasks-table", "selectedRows"),
        State("tasks-page-load", "data"),
    ],
    prevent_initial_call=True,
)
def handle_action(
    complete_clicks, delete_clicks, pending_selected, completed_selected, page_load_data
):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    button_id = ctx.triggered_id
    if button_id is None:
        return dash.no_update

    selected_rows = (
        pending_selected if page_load_data["value"] == "pending" else completed_selected
    )
    if not selected_rows:
        raise PreventUpdate

    db: Session = SessionLocal()
    if button_id == "complete-selected-button":
        for row in selected_rows:
            update_task_status(db, row["id"], "Completed")
    elif button_id == "delete-selected-button":
        for row in selected_rows:
            delete_task(db, row["id"])
    db.close()
    tasks = load_tasks()
    pending_rows = generate_table_data(tasks, "Pending")
    completed_rows = generate_table_data(tasks, "Completed")
    return pending_rows, completed_rows


# Ensure active tab state is stored
@callback(
    Output("tasks-page-load", "data"),
    Input("tasks-tabs", "value"),
)
def store_tab_value(tab_value):
    return {"value": tab_value}
