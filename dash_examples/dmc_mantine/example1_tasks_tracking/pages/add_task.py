import dash
from dash import callback, Input, Output, State
import dash_mantine_components as dmc
import pandas as pd

dash.register_page(__name__, path="/add_task")

layout = dmc.MantineProvider(
    [
        dmc.Title("Add Task", order=1),
        dmc.TextInput(id="task-name", label="Task Name", placeholder="Enter task name"),
        dmc.Textarea(
            id="task-desc", label="Description", placeholder="Enter task description"
        ),
        dmc.DatePicker(id="task-due-date", label="Due Date"),
        dmc.Button("Submit", id="submit-task-button"),
        dmc.Text(id="add-task-output"),
    ]
)


@callback(
    Output("add-task-output", "children"),
    [Input("submit-task-button", "n_clicks")],
    [
        State("task-name", "value"),
        State("task-desc", "value"),
        State("task-due-date", "value"),
    ],
)
def add_task(n_clicks, name, desc, due_date):
    if n_clicks is None:
        return ""
    new_task = pd.DataFrame(
        [
            {
                "id": pd.Timestamp.now().value,
                "task_name": name,
                "description": desc,
                "due_date": due_date,
                "status": "Pending",
            }
        ]
    )
    tasks = pd.read_csv("data/tasks.csv")
    tasks = pd.concat([tasks, new_task], ignore_index=True)
    tasks.to_csv("data/tasks.csv", index=False)
    return f'Task "{name}" has been added.'
