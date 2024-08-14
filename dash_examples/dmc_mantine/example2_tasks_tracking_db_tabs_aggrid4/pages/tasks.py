import json
import logging
import dash
from dash import callback, Input, Output, dcc, State, html
import dash_mantine_components as dmc
import dash_iconify as dash_iconify
from dash_iconify import DashIconify
import dash_ag_grid as dag
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.task import Task, TaskCreate
from utils.crud import (
    get_tasks,
    create_task,
    update_task_status,
    delete_task,
    update_task,
)
from typing import List, Dict
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path="/tasks")

# Set up logging to output debug messages
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


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
            "edit_mode": False,
        }
        for task in tasks
        if task.status == status_filter
    ]


task_columnDefs_base = [
    {
        "headerName": "Select",
        "checkboxSelection": True,
        "headerCheckboxSelection": True,
        # "sortable": True,
    },
    {
        "headerName": "Task Name",
        "field": "task_name",
        "sortable": True,
        "filter": True,
        # conditionally enables editing
        "editable": {"function": "params.data.edit_mode == true"},
    },
    {
        "headerName": "Description",
        "field": "description",
        "sortable": False,
        "filter": False,
        # conditionally enables editing
        "editable": {"function": "params.data.edit_mode == true"},
    },
    {
        "headerName": "Due Date",
        "field": "due_date",
        "sortable": True,
        "filter": True,
        "editable": False,
    },
    {"headerName": "Status", "field": "status", "sortable": True, "filter": True},
]


task_columnDefs_pending = []
task_columnDefs_pending.extend(task_columnDefs_base)
task_columnDefs_pending.extend(
    [
        {
            "headerName": "Set Completed",
            "cellRenderer": "DMC_Action_Button",
            "cellRendererParams": {"rightIcon": "raphael:edit", "action": "complete"},
        },
        {
            "headerName": "Edit",
            "cellRenderer": "DMC_EditSave_Button",
            "cellRendererParams": {
                "rightIcon": "raphael:edit",
                "action": "edit_or_save",
            },
        },
    ]
)

task_columnDefs_completed = []
task_columnDefs_completed.extend(task_columnDefs_base)
task_columnDefs_completed.extend(
    [
        {
            "headerName": "Watch",
            "cellRenderer": "DMC_Action_Button",
            "cellRendererParams": {
                "rightIcon": "raphael:edit",
                "action": "edit_or_save",
            },
        },
        {
            "headerName": "Set Completed",
            "cellRenderer": "DMC_EditSave_Button",
            "cellRendererParams": {"action": "delete"},
        },
    ]
)

task_dashGridOptions = {
    "rowHeight": 48,
    "animateRows": True,
    "pagination": True,
    "paginationPageSize": 10,
    "rowSelection": "multiple",
    # "getRowId": {"function": "params => params.data.id"},  # This ensures each row has a unique ID. Correctly define getRowId, this is not necessary
}

cellStyle = {
    "styleConditions": [
        {
            "condition": "params.data.edit_mode == true",
            "style": {"backgroundColor": "red"},
        },
    ]
}


layout = dmc.MantineProvider(
    [
        dcc.Store(
            id="tasks-page-load", data={"value": "pending"}
        ),  # Initial value for the active tab
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
                            columnDefs=task_columnDefs_pending,
                            rowData=[],
                            dashGridOptions=task_dashGridOptions,
                            # defaultColDef={"filter": True},
                            # className="ag-theme-alpine-dark",
                            columnSize="sizeToFit",
                            getRowId="params.data.id",
                        )
                    ],
                ),
                dmc.TabsPanel(
                    value="completed",
                    children=[
                        dag.AgGrid(
                            id="completed-tasks-table",
                            columnDefs=task_columnDefs_completed,
                            rowData=[],
                            dashGridOptions=task_dashGridOptions,
                            columnSize="sizeToFit",
                            getRowId="params.data.id",
                        )
                    ],
                ),
            ],
            id="tasks-tabs",
            value="pending",
        ),
        html.Div(id="custom-component-btn-value-changed"),
    ]
)


@callback(
    Output("task-modal", "opened"),
    [Input("open-modal-button", "n_clicks"), Input("submit-task-button", "n_clicks")],
    [State("task-modal", "opened")],
)
def toggle_modal(open_clicks, submit_clicks, is_open):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate

    triggered_id = ctx.triggered_id

    if triggered_id == "open-modal-button":
        return not is_open  # Toggle modal state when open button is clicked
    elif triggered_id == "submit-task-button":
        return False  # Close modal when submit button is clicked

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
    tasks: List[Task] = load_tasks()
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
    complete_clicks, delete_clicks, pending_selected, completed_selected, active_tab
):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    button_id = ctx.triggered_id
    if button_id is None:
        return dash.no_update

    selected_rows = (
        pending_selected if active_tab["value"] == "pending" else completed_selected
    )
    if not selected_rows or len(selected_rows) == 0:
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


# Toggle delete button
@callback(
    Output("delete-selected-button", "disabled"),
    Input("pending-tasks-table", "selectedRows"),
    Input("completed-tasks-table", "selectedRows"),
)
def toggle_delete_button(pending_selected, completed_selected):
    return not (pending_selected or completed_selected)


# Toggle complete button
@callback(
    Output("complete-selected-button", "disabled"),
    Input("pending-tasks-table", "selectedRows"),
)
def toggle_complete_button(
    pending_selected,
):
    return not pending_selected


# callback for cellRenderedData of a Button
@callback(
    Output("custom-component-btn-value-changed", "children"),
    Output("pending-tasks-table", "rowTransaction"),
    Output("completed-tasks-table", "rowData", allow_duplicate=True),
    Input("pending-tasks-table", "cellRendererData"),
    State("pending-tasks-table", "rowData"),
    prevent_initial_call=True,
)
def handle_task_row_complete(data, rows_data):
    if data is None:
        raise PreventUpdate

    print(f"input_data: {json.dumps(data)}")

    # get task id
    task_id = data.get("value", {}).get("data", {}).get("id")
    if task_id is None:
        raise PreventUpdate

    print(f"task_id: {task_id}")

    row_data = data.get("value", {}).get("data", {})

    # get action type
    action = data.get("value", {}).get("action")
    if action is None:
        raise PreventUpdate

    if action == "complete":
        db: Session = SessionLocal()
        update_task_status(db, task_id, "Completed")
        db.close()

        tasks = load_tasks()
        # pending_rows = generate_table_data(tasks, "Pending")
        completed_rows = generate_table_data(tasks, "Completed")
        return json.dumps(row_data), {"remove": row_data}, completed_rows

    elif action == "edit_or_save":
        prev_edit_mode = data["value"]["data"]["edit_mode"]
        new_edit_mode = not prev_edit_mode

        print(f"action: {action}")
        row_data["editable"] = True  # Make the row editable

        # Save the changes
        if new_edit_mode:
            # Make cells edit_mode
            for row in rows_data:
                if row["id"] == task_id:
                    logging.debug("row-1: %s", row)
                    row["edit_mode"] = True
                    logging.debug("row-2: %s", row)
                    logging.debug("rows_data: %s", rows_data)
                    return json.dumps(row), {"update": [row]}, dash.no_update
        else:
            # Save the changes
            for row in rows_data:
                if row["id"] == task_id:
                    logging.debug("row-3: %s", row)
                    row["edit_mode"] = False
                    db: Session = SessionLocal()
                    update_task(db, task_id, TaskCreate(**row_data))
                    db.close()
                    logging.debug("row-4: %s", row)
                    logging.debug("rows_data: %s", rows_data)
                    return json.dumps(row), {"update": rows_data}, dash.no_update

        raise PreventUpdate

    # elif action == "save":
    #     print(f"action: {action}")
    #     row_data["editable"] = False  # Make the row non-editable
    #     # Save the changes
    #     db: Session = SessionLocal()
    #     task = db.query(Task).filter(Task.id == task_id).first()
    #     task.task_name = data["value"]["data"]["task_name"]
    #     task.description = data["value"]["data"]["description"]
    #     task.due_date = data["value"]["data"]["due_date"]
    #     db.commit()
    #     db.close()

    #     tasks = load_tasks()
    #     pending_rows = generate_table_data(tasks, "Pending")
    #     completed_rows = generate_table_data(tasks, "Completed")

    #     return json.dumps(data), pending_rows, completed_rows
    else:
        raise PreventUpdate

    tasks = load_tasks()
    pending_rows = generate_table_data(tasks, "Pending")
    completed_rows = generate_table_data(tasks, "Completed")
    return json.dumps(data), pending_rows, completed_rows


# callback for cellRenderedData of a Button
@callback(
    Output("custom-component-btn-value-changed", "children", allow_duplicate=True),
    Output("completed-tasks-table", "rowData", allow_duplicate=True),
    Input("completed-tasks-table", "cellRendererData"),
    prevent_initial_call=True,
)
def handle_task_row_delete(data):
    if data is None:
        raise PreventUpdate

    print(f"{json.dumps(data)}")

    # get task id
    task_id = data.get("value", {}).get("data", {}).get("id")
    print(f"task_id: {task_id}")
    if task_id is None:
        raise PreventUpdate

    # get action type
    action = data.get("value", {}).get("action")
    if action is None:
        raise PreventUpdate

    if action == "delete":
        db: Session = SessionLocal()
        delete_task(db, task_id)
        db.close()

        tasks = load_tasks()
        completed_rows = generate_table_data(tasks, "Completed")
        return json.dumps(data), completed_rows
    elif action == "edit_or_save":
        raise PreventUpdate
